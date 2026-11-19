"""Camunda REST v2 transport. Engine state is never persisted locally."""

import hashlib
import json
import os
from pathlib import Path
import subprocess
import urllib.error
import urllib.parse
import urllib.request
import uuid


class RuntimeFailure(Exception):
    def __init__(self, code, message, details=None):
        super().__init__(message)
        self.code, self.details = code, details


def digest(data):
    return "sha256:" + hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(
        value, sort_keys=True, separators=(",", ":"), allow_nan=False
    ).encode()


def read_json(path):
    return json.loads(Path(path).read_text())


class Client:
    def __init__(self, url, tenant="<default>", timeout=30):
        parsed = urllib.parse.urlparse(url)
        if (
            parsed.scheme not in {"http", "https"}
            or not parsed.netloc
            or parsed.username
        ):
            raise RuntimeFailure(
                "invalid_url",
                "Use an HTTP(S) Camunda URL without embedded credentials.",
            )
        self.url = url.rstrip("/").removesuffix("/v2") + "/v2"
        self.tenant, self.timeout = tenant, timeout

    def request(self, method, path, payload=None, content_type="application/json"):
        body = (
            payload
            if isinstance(payload, bytes)
            else canonical(payload) if payload is not None else None
        )
        headers = {"Accept": "application/json", "Content-Type": content_type}
        if os.getenv("SPECFLOW_CAMUNDA_TOKEN"):
            headers["Authorization"] = "Bearer " + os.environ["SPECFLOW_CAMUNDA_TOKEN"]
        request = urllib.request.Request(
            self.url + path, data=body, headers=headers, method=method
        )
        try:
            with urllib.request.urlopen(request, timeout=self.timeout) as response:
                data = response.read()
                return json.loads(data) if data else {}
        except urllib.error.HTTPError as error:
            try:
                details = json.loads(error.read())
            except (ValueError, OSError):
                details = {"status": error.code}
            finally:
                error.close()
            raise RuntimeFailure(
                "camunda_http_error",
                f"Camunda returned HTTP {error.code} for {method} {path}.",
                details,
            ) from error
        except (urllib.error.URLError, TimeoutError, OSError) as error:
            raise RuntimeFailure(
                "camunda_unavailable",
                "Camunda request failed; a mutation may have been accepted. Inspect engine state before retrying.",
                str(error),
            ) from error

    def search(self, resource, filters=None):
        result, after = [], None
        while True:
            page = {"limit": 100}
            if after:
                page["after"] = after
            data = self.request(
                "POST",
                "/" + resource + "/search",
                {"filter": filters or {}, "page": page},
            )
            items = data.get("items", [])
            result.extend(items)
            cursor = data.get("page", {}).get("endCursor")
            if len(items) < 100 or not cursor or cursor == after:
                return result
            after = cursor

    def deploy(self, directory):
        topology = self.request("GET", "/topology")
        if not topology.get("gatewayVersion", "").startswith("8.9."):
            raise RuntimeFailure(
                "unsupported_engine", "This integration targets Camunda 8.9.", topology
            )
        boundary = "specflow-" + uuid.uuid4().hex
        chunks = []
        for path in sorted(Path(directory).iterdir()):
            if path.suffix not in {".bpmn", ".form", ".dmn"}:
                continue
            chunks.append(
                (
                    f'--{boundary}\r\nContent-Disposition: form-data; name="resources"; filename="{path.name}"\r\nContent-Type: application/octet-stream\r\n\r\n'
                ).encode()
                + path.read_bytes()
                + b"\r\n"
            )
        if not chunks:
            raise RuntimeFailure(
                "missing_resources",
                "No BPMN, form, or DMN deployment resources were found.",
            )
        chunks.append(
            (
                f'--{boundary}\r\nContent-Disposition: form-data; name="tenantId"\r\n\r\n{self.tenant}\r\n--{boundary}--\r\n'
            ).encode()
        )
        return self.request(
            "POST",
            "/deployments",
            b"".join(chunks),
            "multipart/form-data; boundary=" + boundary,
        )

    def roots(self, business_id, definition):
        return [
            item
            for item in self.search(
                "process-instances",
                {
                    "businessId": business_id,
                    "processDefinitionId": definition,
                    "tenantId": self.tenant,
                },
            )
            if not item.get("parentProcessInstanceKey")
        ]

    def resolve(self, business_id, definition, key=None):
        if key:
            root = self.request("GET", "/process-instances/" + str(key))
            if (
                root.get("businessId") != business_id
                or root.get("processDefinitionId") != definition
                or root.get("tenantId") != self.tenant
            ):
                raise RuntimeFailure(
                    "identity_mismatch",
                    "The process key does not match the requested business ID, definition, and tenant.",
                )
            return root
        roots = self.roots(business_id, definition)
        active = [item for item in roots if item["state"] == "ACTIVE"]
        if len(active) > 1:
            raise RuntimeFailure(
                "ambiguous_root",
                "Several active roots exist. Select a process key and reconcile the duplicate roots.",
                active,
            )
        if active:
            return active[0]
        if not roots:
            raise RuntimeFailure(
                "process_not_found",
                "No matching indexed root exists. Camunda search is eventually consistent; retry after indexing or supply its key.",
            )
        return max(roots, key=lambda item: int(item["processInstanceKey"]))

    def start(self, business_id, definition, variables, version_tag="v1"):
        active = [
            item
            for item in self.roots(business_id, definition)
            if item["state"] == "ACTIVE"
        ]
        if len(active) > 1:
            raise RuntimeFailure(
                "ambiguous_root", "Multiple active roots exist.", active
            )
        if active:
            if active[0].get("processDefinitionVersionTag") != version_tag:
                raise RuntimeFailure(
                    "definition_version_mismatch",
                    "The existing root is pinned to a different version tag.",
                    active[0],
                )
            return {"disposition": "existing", "process": active[0]}
        definitions = self.search(
            "process-definitions",
            {
                "processDefinitionId": definition,
                "tenantId": self.tenant,
                "versionTag": version_tag,
            },
        )
        if not definitions:
            raise RuntimeFailure(
                "definition_not_found",
                "Deploy the selected version tag before starting a workflow.",
            )
        selected = max(definitions, key=lambda item: item["version"])
        variables = dict(variables, workflowBusinessId=business_id)
        response = self.request(
            "POST",
            "/process-instances",
            {
                "processDefinitionKey": selected["processDefinitionKey"],
                "businessId": business_id,
                "tenantId": self.tenant,
                "variables": variables,
            },
        )
        return {"disposition": "created", "process": response, "definition": selected}

    def variables(self, key):
        values = {}
        for item in self.search(
            "variables",
            {
                "processInstanceKey": str(key),
                "scopeKey": str(key),
                "tenantId": self.tenant,
            },
        ):
            if item.get("isTruncated"):
                item = self.request("GET", "/variables/" + str(item["variableKey"]))
            values[item["name"]] = json.loads(item["value"])
        return values

    def inspect(self, root):
        instances, pending = [], [root]
        seen = set()
        while pending:
            instance = pending.pop(0)
            key = str(instance["processInstanceKey"])
            if key in seen:
                continue
            seen.add(key)
            filters = {"processInstanceKey": key, "tenantId": self.tenant}
            state = {"process": instance, "variables": self.variables(key)}
            for resource in (
                "user-tasks",
                "jobs",
                "incidents",
                "element-instances",
                "message-subscriptions",
            ):
                state[resource] = self.search(resource, filters)
            state["activeUserTasks"] = [
                item
                for item in state["user-tasks"]
                if item["state"] not in {"COMPLETED", "CANCELED"}
            ]
            state["activeJobs"] = [
                item
                for item in state["jobs"]
                if item["state"] not in {"COMPLETED", "CANCELED", "ERROR_THROWN"}
            ]
            state["activeIncidents"] = [
                item for item in state["incidents"] if item["state"] != "RESOLVED"
            ]
            state["activeElements"] = [
                item for item in state["element-instances"] if item["state"] == "ACTIVE"
            ]
            state["waitingMessages"] = [
                item
                for item in state["message-subscriptions"]
                if item.get("messageSubscriptionState") != "CORRELATED"
            ]
            instances.append(state)
            pending.extend(
                self.search(
                    "process-instances",
                    {"parentProcessInstanceKey": key, "tenantId": self.tenant},
                )
            )
        return {
            "root": root,
            "instances": instances,
            "consistency": "eventually_consistent",
            "exclusiveOwnership": False,
        }


def validate_references(snapshot, validators=()):
    from .visuals import validate_embedded_visuals

    checks = []
    for state in snapshot["instances"]:
        try:
            validate_embedded_visuals(state["variables"])
        except RuntimeFailure as error:
            checks.append(
                {"reference": "visuals", "status": "unverified", "reason": str(error)}
            )
        for ref in state["variables"].get("artifactRefs", []):
            if (
                not isinstance(ref, dict)
                or not ref.get("path")
                or not ref.get("sha256")
            ):
                checks.append(
                    {
                        "reference": ref,
                        "status": "unverified",
                        "reason": "A local path and sha256 are required, or a configured validator must verify the external reference.",
                    }
                )
                continue
            try:
                actual = digest(Path(ref["path"]).read_bytes())
                checks.append(
                    {
                        "reference": ref["path"],
                        "status": "passed" if actual == ref["sha256"] else "failed",
                        "actualHash": actual,
                    }
                )
            except OSError as error:
                checks.append(
                    {"reference": ref["path"], "status": "failed", "reason": str(error)}
                )
    for validator in validators:
        try:
            result = subprocess.run(
                validator["command"],
                input=json.dumps(snapshot),
                text=True,
                capture_output=True,
                timeout=validator.get("timeout_seconds", 60),
                check=False,
            )
            checks.append(
                {
                    "validator": validator["name"],
                    "status": "passed" if result.returncode == 0 else "failed",
                    "exitCode": result.returncode,
                }
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            checks.append(
                {
                    "validator": validator["name"],
                    "status": "failed",
                    "reason": str(error),
                }
            )
    for check in checks:
        reference = check.get("reference")
        if (
            check["status"] == "unverified"
            and isinstance(reference, dict)
            and reference.get("validator")
        ):
            matching = [
                result
                for result in checks
                if result.get("validator") == reference["validator"]
            ]
            if matching and all(result["status"] == "passed" for result in matching):
                check["status"] = "passed"
                check["reason"] = (
                    "Verified by its explicitly named external-reference validator."
                )
    return {
        "status": (
            "passed"
            if all(check["status"] == "passed" for check in checks)
            else "incomplete"
        ),
        "checks": checks,
        "scope": "Referenced local artifacts and explicitly configured validators only; no orchestration or exclusivity proof.",
    }
