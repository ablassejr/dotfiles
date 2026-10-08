"""Complete artifact inventories and verified Linear project resource publication."""

import mimetypes
import os
from pathlib import Path
from urllib.parse import urlparse

from .client import RuntimeFailure, canonical, digest
from .operations import (
    OperationStore,
    apply_operation,
    external_exchange,
    operation_token,
)

POLICY = "linear-project-resources-v1"


def require(condition, message):
    if not condition:
        raise RuntimeFailure("invalid_project_resources", message)


def inventory_artifacts(directory, source):
    root = Path(directory).resolve()
    require(root.is_dir(), "Use the workflow's dedicated artifact directory.")
    require(
        isinstance(source, dict) and source.get("ref") and source.get("hash"),
        "Bind the inventory to its program source.",
    )
    artifacts = []
    try:
        paths = []

        def fail_walk(error):
            raise error

        for directory, directories, files in os.walk(root, onerror=fail_walk):
            paths.extend(Path(directory) / name for name in directories + files)
        for path in sorted(paths):
            require(
                not path.is_symlink(),
                "Export linked artifacts into the artifact directory before inventorying it.",
            )
            if not path.is_file():
                continue
            content = path.read_bytes()
            artifacts.append(
                {
                    "key": path.relative_to(root).as_posix(),
                    "sha256": digest(content),
                    "size": len(content),
                    "content_type": mimetypes.guess_type(path.name)[0]
                    or "application/octet-stream",
                }
            )
    except OSError as error:
        raise RuntimeFailure(
            "invalid_project_resources",
            "Every artifact must be readable; nothing is silently omitted.",
        ) from error
    require(bool(artifacts), "The project artifact inventory cannot be empty.")
    inventory = {
        "schema_version": 1,
        "source": source,
        "root": str(root),
        "artifacts": artifacts,
    }
    return dict(inventory, inventory_hash=digest(canonical(inventory)))


def validate_inventory(inventory, source, refresh=False):
    require(
        isinstance(inventory, dict),
        "Supply projectArtifactInventory before project resource publication.",
    )
    require(
        inventory.get("source") == source,
        "The artifact inventory must belong to the current program binding.",
    )
    require(
        isinstance(inventory.get("root"), str),
        "The artifact inventory needs its dedicated directory.",
    )
    current = inventory_artifacts(inventory["root"], source)
    if not refresh:
        require(
            inventory == current,
            "The artifact set changed or is incomplete. Re-inventory it before publication.",
        )
    return current


def validate_binding(binding, inventory, carrier):
    require(isinstance(binding, dict), "Supply the read-back projectResourcesBinding.")
    require(
        binding.get("schema_version") == 1
        and binding.get("source") == inventory["source"]
        and binding.get("inventory_hash") == inventory["inventory_hash"],
        "Project resources must match this exact artifact inventory and program.",
    )
    project = binding.get("project_id")
    require(
        isinstance(project, str) and bool(project.strip()),
        "Resolve the actual Linear project before issue creation.",
    )
    if carrier.get("mode") == "existing":
        require(
            project == carrier.get("id"),
            "Resources must belong to the approved carrier project.",
        )
    require(
        binding.get("carrier") == carrier,
        "Project publication must preserve the approved carrier selection or creation record.",
    )
    resources = binding.get("resources")
    require(
        isinstance(resources, list) and len(resources) == len(inventory["artifacts"]),
        "Every artifact needs a project resource and verified uploaded bytes.",
    )
    expected = {a["key"]: a for a in inventory["artifacts"]}
    seen = set()
    ids = set()
    for resource in resources:
        require(
            isinstance(resource, dict),
            "Each project resource must have a readback record.",
        )
        key = resource.get("artifact_key")
        require(
            isinstance(key, str) and key in expected and key not in seen,
            "Project resources must cover every artifact exactly once.",
        )
        seen.add(key)
        identity = resource.get("resource_id")
        require(
            isinstance(identity, str)
            and bool(identity.strip())
            and identity not in ids,
            "Each artifact must be discoverable as its own project resource.",
        )
        ids.add(identity)
        require(
            resource.get("project_id") == project,
            "Read back each resource's project membership.",
        )
        require(
            resource.get("sha256") == expected[key]["sha256"]
            and resource.get("readback_sha256") == expected[key]["sha256"],
            "Uploaded and downloaded artifact bytes must match the inventory.",
        )
        asset = urlparse(resource.get("asset_url", ""))
        require(
            asset.scheme == "https"
            and asset.hostname == "uploads.linear.app"
            and bool(asset.path.strip("/"))
            and not asset.query
            and not asset.fragment
            and not asset.username,
            "Persist a durable Linear upload URL, not a local path or expiring signed URL.",
        )
    readback = binding.get("readback")
    require(
        isinstance(readback, dict) and readback.get("project_id") == project,
        "Fetch the project's Resources section after publication.",
    )
    listed = readback.get("resource_ids")
    require(
        isinstance(listed, list)
        and all(isinstance(i, str) for i in listed)
        and ids <= set(listed),
        "All uploaded artifacts must appear in project Resources.",
    )
    access = readback.get("access")
    require(
        isinstance(access, dict)
        and access.get("scope") == "project_members"
        and access.get("verified") is True
        and isinstance(access.get("evidence"), str)
        and bool(access["evidence"].strip()),
        "Verify project-member access to every uploaded resource; uploader-only access is insufficient.",
    )
    require(
        isinstance(readback.get("verified_at"), str)
        and bool(readback["verified_at"].strip()),
        "Record when project resources and access were read back.",
    )


def validate_completion(job, result):
    headers = job.get("customHeaders", {})
    if (
        result.get("status") != "completed"
        or headers.get("projectResourcePolicy") != POLICY
    ):
        return
    current = job.get("variables", {})
    output = result.get("variables", {})
    publishing = headers.get("phase") == "publish_project_resources"
    inventory = validate_inventory(
        current.get("projectArtifactInventory"),
        current.get("programBinding"),
        refresh=publishing,
    )
    require(
        output.get("projectArtifactInventory", current.get("projectArtifactInventory"))
        == inventory,
        "Publication must return the complete current artifact inventory from the same directory.",
    )
    binding = (
        output.get("projectResourcesBinding")
        if publishing
        else current.get("projectResourcesBinding")
    )
    validate_binding(
        binding, inventory, current.get("linearPlan", {}).get("carrier_project", {})
    )
    if not publishing:
        require(
            output.get("projectResourcesBinding", binding) == binding,
            "Issue creation and dispatch must preserve the verified project resources.",
        )


def publish_resources(job, config, handler):
    variables = job["variables"]
    inventory = validate_inventory(
        variables.get("projectArtifactInventory"),
        variables.get("programBinding"),
        refresh=True,
    )
    from .program import validate_completion as validate_program

    validate_program(job, {"status": "completed", "variables": {}})
    plan = variables["linearPlan"]
    carrier = plan["carrier_project"]
    request = {
        "kind": POLICY,
        "carrier": carrier,
        "source": inventory["source"],
        "inventory_hash": inventory["inventory_hash"],
        "artifacts": inventory["artifacts"],
        "files": {
            a["key"]: str(Path(inventory["root"]) / a["key"])
            for a in inventory["artifacts"]
        },
        "audience": "project_members",
    }
    intent = {
        "target_id": "project-resources:"
        + (carrier.get("id") or variables["workflowBusinessId"])
        + ":"
        + inventory["inventory_hash"],
        "operation_id": "project-resources:"
        + str(job["processInstanceKey"])
        + ":"
        + inventory["inventory_hash"],
        "operation_generation": 1,
        "semantic_revision": str(plan["semantic_release"]["revision"]),
        "expected_target_revision": None,
    }
    token = operation_token(job, intent, request, "linear")
    store = OperationStore(config["operation_store"])
    try:
        receipt = apply_operation(store, token, request, handler)
    finally:
        store.close()
    validate_binding(receipt.get("result"), inventory, carrier)
    # Cached receipts establish operation identity; this read checks current provider state.
    live = external_exchange(
        handler.get("command"),
        {
            "phase": "verify",
            "token": token,
            "request": request,
            "result": receipt["result"],
        },
        handler.get("timeout_seconds", 60),
    )
    require(
        live.get("status") == "found",
        "Resource publication is incomplete until live verification finds the full set.",
    )
    binding = live.get("result")
    validate_binding(binding, inventory, carrier)
    require(
        {
            (r["artifact_key"], r["resource_id"], r["asset_url"])
            for r in binding["resources"]
        }
        == {
            (r["artifact_key"], r["resource_id"], r["asset_url"])
            for r in receipt["result"]["resources"]
        },
        "Live verification must identify the published artifacts.",
    )
    return {
        "status": "completed",
        "variables": {
            "projectArtifactInventory": inventory,
            "projectResourcesBinding": binding,
        },
    }
