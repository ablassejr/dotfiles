"""Local guarded artifact publication and explicit external adapter boundaries."""

from datetime import datetime, timezone
import json
from pathlib import Path
import shutil
import sqlite3
import subprocess
import uuid

from .client import RuntimeFailure, canonical, digest
from .visuals import validate_embedded_visuals

ADAPTERS = {
    "notion": "NotionCanonicalSpecAdapter",
    "linear": "LinearProgramAdapter",
    "github": "GitHubChangeAdapter",
    "figma": "FigmaProjectionAdapter",
    "likec4": "LikeC4ArtifactAdapter",
    "archify": "ArchifyArtifactAdapter",
    "artifact-storage": "ArtifactStorageAdapter",
}
GUARANTEES = {
    "IDEMPOTENT",
    "GUARDED_PUBLISH",
    "CONDITIONAL_WRITE",
    "RECONCILED",
    "BEST_EFFORT",
}


def normalized_request(request):
    normalized = dict(request)
    if "files" in request:
        normalized["files"] = {
            name: digest(Path(path).read_bytes())
            for name, path in request["files"].items()
        }
    return normalized


def operation_token(job, intent, request, adapter):
    token = dict(intent)
    token.update(
        workflow_business_id=job["variables"]["workflowBusinessId"],
        process_instance_key=str(job["processInstanceKey"]),
        bpmn_element_id=job["elementId"],
        adapter=adapter,
        attempt_id="ATT-" + uuid.uuid4().hex,
        issued_at=datetime.now(timezone.utc).isoformat(),
    )
    token.setdefault("input_hash", digest(canonical(normalized_request(request))))
    return token


def validate_token(token, request):
    required = {
        "workflow_business_id",
        "process_instance_key",
        "bpmn_element_id",
        "adapter",
        "target_id",
        "operation_id",
        "operation_generation",
        "semantic_revision",
        "input_hash",
        "expected_target_revision",
        "attempt_id",
        "issued_at",
    }
    if required - token.keys():
        raise RuntimeFailure(
            "invalid_operation_token",
            "Missing operation token fields.",
            sorted(required - token.keys()),
        )
    if (
        token["adapter"] not in ADAPTERS
        or type(token["operation_generation"]) is not int
        or token["operation_generation"] < 1
    ):
        raise RuntimeFailure(
            "invalid_operation_token",
            "Use a registered adapter and a positive generation.",
        )
    if any(
        not isinstance(token[name], str) or not token[name]
        for name in required - {"operation_generation", "expected_target_revision"}
    ):
        raise RuntimeFailure(
            "invalid_operation_token",
            "Operation identity fields must be nonempty strings.",
        )
    revision = token["expected_target_revision"]
    if revision is not None and not (
        isinstance(revision, str) or type(revision) is int and revision >= 0
    ):
        raise RuntimeFailure(
            "invalid_operation_token",
            "Use a target revision string, nonnegative generation, or null.",
        )
    if digest(canonical(normalized_request(request))) != token["input_hash"]:
        raise RuntimeFailure(
            "input_hash_mismatch",
            "The token does not identify the normalized input and source bytes.",
        )


class OperationStore:
    """One shared local SQLite registry; it makes no distributed lease claim."""

    def __init__(self, directory):
        self.directory = Path(directory).resolve()
        self.directory.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(
            self.directory / "operations.sqlite3", timeout=30, isolation_level=None
        )
        self.db.row_factory = sqlite3.Row
        self.db.executescript("""
            PRAGMA journal_mode=WAL;
            CREATE TABLE IF NOT EXISTS operations (
                id TEXT PRIMARY KEY, identity TEXT NOT NULL, target TEXT NOT NULL,
                generation INTEGER NOT NULL, receipt TEXT);
            CREATE TABLE IF NOT EXISTS targets (
                id TEXT PRIMARY KEY, desired INTEGER NOT NULL, current INTEGER NOT NULL DEFAULT 0,
                operation_id TEXT NOT NULL, receipt TEXT);
        """)

    def close(self):
        self.db.close()

    def _identity(self, token):
        return canonical(
            {
                key: value
                for key, value in token.items()
                if key not in {"attempt_id", "issued_at"}
            }
        ).decode()

    def _target(self, token):
        return canonical(
            [token["workflow_business_id"], token["adapter"], token["target_id"]]
        ).decode()

    def prepare(self, token, request):
        validate_token(token, request)
        target, identity = self._target(token), self._identity(token)
        self.db.execute("BEGIN IMMEDIATE")
        try:
            existing = self.db.execute(
                "SELECT * FROM operations WHERE id=?", (token["operation_id"],)
            ).fetchone()
            if existing and existing["identity"] != identity:
                raise RuntimeFailure(
                    "operation_identity_conflict",
                    "An operation ID cannot identify different content, generation, or target.",
                )
            if existing and existing["receipt"]:
                self.db.execute("COMMIT")
                return json.loads(existing["receipt"])
            current = self.db.execute(
                "SELECT * FROM targets WHERE id=?", (target,)
            ).fetchone()
            if current and (
                current["desired"] > token["operation_generation"]
                or (
                    current["desired"] == token["operation_generation"]
                    and current["operation_id"] != token["operation_id"]
                )
            ):
                if current["desired"] == token["operation_generation"]:
                    raise RuntimeFailure(
                        "generation_conflict",
                        "A target generation is already bound to another operation.",
                    )
                self.db.execute("COMMIT")
                return {
                    "status": "SUPERSEDED",
                    "current": (
                        json.loads(current["receipt"]) if current["receipt"] else None
                    ),
                    "desiredGeneration": current["desired"],
                }
            self.db.execute(
                "INSERT OR IGNORE INTO operations(id,identity,target,generation) VALUES(?,?,?,?)",
                (
                    token["operation_id"],
                    identity,
                    target,
                    token["operation_generation"],
                ),
            )
            self.db.execute(
                "INSERT INTO targets(id,desired,operation_id) VALUES(?,?,?) ON CONFLICT(id) DO UPDATE SET desired=excluded.desired,operation_id=excluded.operation_id",
                (target, token["operation_generation"], token["operation_id"]),
            )
            self.db.execute("COMMIT")
            return None
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def stage(self, token):
        path = (
            self.directory
            / "staging"
            / digest(token["operation_id"].encode())[7:]
            / digest(token["attempt_id"].encode())[7:]
        )
        path.mkdir(parents=True, exist_ok=True)
        return path

    def publish(self, token, stage, request=None):
        files = {}
        for path in Path(stage).iterdir():
            if path.name == "manifest.json" or path.is_symlink() or not path.is_file():
                raise RuntimeFailure(
                    "invalid_artifact_set",
                    "Staged artifacts must be regular files; manifest.json is reserved.",
                )
            files[path.name] = digest(path.read_bytes())
        if not files:
            raise RuntimeFailure(
                "empty_artifact_set", "No validated artifacts were staged."
            )
        target = self._target(token)
        destination = (
            self.directory
            / "published"
            / digest(target.encode())[7:]
            / ("generation-%06d" % token["operation_generation"])
        )
        receipt = {
            "status": "COMPLETED",
            "adapter": token["adapter"],
            "guarantee": "GUARDED_PUBLISH",
            "operationId": token["operation_id"],
            "generation": token["operation_generation"],
            "inputHash": token["input_hash"],
            "workflowBusinessId": token["workflow_business_id"],
            "targetId": token["target_id"],
            "semanticRevision": token["semantic_revision"],
            "source": request.get("source", {}) if request else {},
            "rendererVersion": request.get("renderer_version") if request else None,
            "requestedExports": (
                request.get("exports", ["html"])
                if request and token["adapter"] == "archify"
                else None
            ),
            "manifest": str(destination / "manifest.json"),
            "files": files,
        }
        self.db.execute("BEGIN IMMEDIATE")
        try:
            operation = self.db.execute(
                "SELECT * FROM operations WHERE id=?", (token["operation_id"],)
            ).fetchone()
            if not operation or operation["identity"] != self._identity(token):
                raise RuntimeFailure(
                    "operation_not_prepared",
                    "Prepare this exact operation before publication.",
                )
            if operation["receipt"]:
                self.db.execute("COMMIT")
                return json.loads(operation["receipt"])
            current = self.db.execute(
                "SELECT * FROM targets WHERE id=?", (target,)
            ).fetchone()
            if (
                current["desired"] != token["operation_generation"]
                or current["operation_id"] != token["operation_id"]
            ):
                self.db.execute("COMMIT")
                return {
                    "status": "SUPERSEDED",
                    "current": (
                        json.loads(current["receipt"]) if current["receipt"] else None
                    ),
                    "desiredGeneration": current["desired"],
                }
            expected = token["expected_target_revision"]
            if expected is not None and current["current"] != expected:
                raise RuntimeFailure(
                    "target_revision_conflict",
                    "The authoritative target revision differs from the expected revision.",
                    {"expected": expected, "actual": current["current"]},
                )
            if destination.exists():
                saved = json.loads((destination / "manifest.json").read_text())
                if any(
                    saved.get(key) != receipt[key]
                    for key in {
                        "status",
                        "adapter",
                        "operationId",
                        "generation",
                        "inputHash",
                        "manifest",
                    }
                ) or any(
                    digest((destination / name).read_bytes()) != value
                    for name, value in saved["files"].items()
                ):
                    raise RuntimeFailure(
                        "immutable_generation_conflict",
                        "An existing immutable artifact set differs from this operation.",
                    )
                receipt = saved
            else:
                (Path(stage) / "manifest.json").write_bytes(canonical(receipt))
                destination.parent.mkdir(parents=True, exist_ok=True)
                Path(stage).rename(destination)
            serialized = canonical(receipt).decode()
            self.db.execute(
                "UPDATE targets SET current=?,receipt=? WHERE id=?",
                (token["operation_generation"], serialized, target),
            )
            self.db.execute(
                "UPDATE operations SET receipt=? WHERE id=?",
                (serialized, token["operation_id"]),
            )
            self.db.execute("COMMIT")
            return receipt
        except BaseException:
            if self.db.in_transaction:
                self.db.execute("ROLLBACK")
            raise

    def current(self, token):
        row = self.db.execute(
            "SELECT receipt,desired,current FROM targets WHERE id=?",
            (self._target(token),),
        ).fetchone()
        return (
            {
                "desiredGeneration": row["desired"],
                "currentGeneration": row["current"],
                "result": json.loads(row["receipt"]) if row["receipt"] else None,
            }
            if row
            else None
        )

    def remember(self, token, receipt):
        self.db.execute(
            "UPDATE operations SET receipt=? WHERE id=?",
            (canonical(receipt).decode(), token["operation_id"]),
        )


def command_exchange(command, envelope, timeout=60):
    if (
        not isinstance(command, list)
        or not command
        or not all(isinstance(part, str) for part in command)
    ):
        raise RuntimeFailure(
            "invalid_handler_command", "Configure an explicit command argument array."
        )
    result = subprocess.run(
        command,
        input=json.dumps(envelope),
        text=True,
        capture_output=True,
        timeout=timeout,
        check=False,
    )
    try:
        payload = json.loads(result.stdout)
        if not isinstance(payload, dict):
            raise ValueError("Expected an object")
    except ValueError as error:
        raise RuntimeFailure(
            "invalid_handler_result", "The handler must emit one JSON object on stdout."
        ) from error
    if result.returncode and payload.get("status") != "transient":
        raise RuntimeFailure(
            "handler_failed",
            "The configured handler returned a nonzero exit code.",
            {"exitCode": result.returncode},
        )
    if payload.get("status") == "transient":
        delay = payload.get("retryBackOff", 1000)
        if type(delay) is not int or delay < 0:
            raise RuntimeFailure(
                "invalid_handler_result", "retryBackOff must be a nonnegative integer."
            )
    return payload


def external_exchange(command, envelope, timeout):
    result = command_exchange(command, envelope, timeout)
    if result.get("status") == "transient":
        raise RuntimeFailure(
            "transient_external_failure",
            result.get("message", "External service temporarily unavailable."),
            {"retryBackOff": result.get("retryBackOff", 1000)},
        )
    return result


def apply_operation(store, token, request, config=None):
    config = config or {}
    validate_embedded_visuals(request)
    existing = store.prepare(token, request)
    if existing:
        if existing.get("guarantee") == "GUARDED_PUBLISH":
            current = store.current(token)
            if current and current["desiredGeneration"] > token["operation_generation"]:
                return {
                    "status": "SUPERSEDED",
                    "original": existing,
                    "current": (
                        current["result"]
                        if current["currentGeneration"] == current["desiredGeneration"]
                        else None
                    ),
                    "desiredGeneration": current["desiredGeneration"],
                }
        return existing
    adapter = token["adapter"]
    if adapter in {"artifact-storage", "archify", "likec4"}:
        stage = store.stage(token)
        if adapter == "archify":
            exports = request.get("exports", ["html"])
            if (
                not isinstance(exports, list)
                or not exports
                or any(
                    kind not in {"html", "svg", "png", "jpeg", "webp"}
                    for kind in exports
                )
            ):
                raise RuntimeFailure(
                    "unsupported_export",
                    "Request html, svg, png, jpeg, or webp exports.",
                )
            if any(kind != "html" for kind in exports) and not config.get(
                "export_command"
            ):
                raise RuntimeFailure(
                    "exporter_not_configured",
                    "Configure the renderer's static-export boundary for requested non-HTML formats.",
                )
            archify = config.get("command")
            if not archify:
                raise RuntimeFailure(
                    "adapter_not_configured",
                    "Configure the installed Archify CLI command array.",
                )
            model = stage / "model.json"
            model.write_bytes(canonical(request["model"]))
            for arguments in (
                [
                    "validate",
                    request["view_type"],
                    str(model),
                    "--quality",
                    "showcase",
                    "--json",
                ],
                [
                    "deliver",
                    request["view_type"],
                    str(model),
                    str(stage / "view.html"),
                    "--quality",
                    "showcase",
                    "--json",
                ],
            ):
                result = subprocess.run(
                    archify + arguments,
                    capture_output=True,
                    text=True,
                    timeout=config.get("timeout_seconds", 120),
                    check=False,
                )
                if result.returncode:
                    raise RuntimeFailure(
                        "archify_validation_failed",
                        "Archify validation or delivery failed; the generation remains unpublished.",
                        {"exitCode": result.returncode},
                    )
                (stage / ("archify-" + arguments[0] + ".json")).write_bytes(
                    canonical(json.loads(result.stdout))
                )
            if not (stage / "view.html").is_file():
                raise RuntimeFailure(
                    "archify_delivery_missing",
                    "Archify did not produce the requested HTML artifact.",
                )
            if config.get("export_command") and any(kind != "html" for kind in exports):
                command_exchange(
                    config["export_command"],
                    {
                        "stage": str(stage),
                        "formats": exports,
                        "inputHash": token["input_hash"],
                    },
                    config.get("timeout_seconds", 120),
                )
            if any(not (stage / ("view." + kind)).is_file() for kind in exports):
                raise RuntimeFailure(
                    "incomplete_exports",
                    "Every requested export must exist before publication.",
                )
        else:
            source_hashes = normalized_request(request)["files"]
            for name, source in request["files"].items():
                if Path(name).name != name or name in {"", ".", "..", "manifest.json"}:
                    raise RuntimeFailure(
                        "invalid_artifact_name",
                        "Use plain filenames, excluding manifest.json.",
                    )
                shutil.copyfile(source, stage / name)
                if digest((stage / name).read_bytes()) != source_hashes[name]:
                    raise RuntimeFailure(
                        "input_changed_during_staging",
                        "Source bytes changed during staging; the artifact set remains unpublished.",
                    )
            if adapter == "likec4":
                if not config.get("validate_command"):
                    raise RuntimeFailure(
                        "adapter_not_configured",
                        "Configure the LikeC4 validation command.",
                    )
                command_exchange(
                    config["validate_command"],
                    {"request": request, "stage": str(stage)},
                    config.get("timeout_seconds", 60),
                )
        validate_token(token, request)
        return store.publish(token, stage, request)
    guarantee = config.get("guarantee")
    if guarantee not in GUARANTEES or guarantee == "GUARDED_PUBLISH":
        raise RuntimeFailure(
            "adapter_not_configured",
            "External destinations must declare their verified guarantee; local publication guards do not fence remote writes.",
        )
    if (
        guarantee == "BEST_EFFORT"
        and config.get("materially_harmful", True)
        and not config.get("risk_record")
    ):
        raise RuntimeFailure(
            "risk_record_required",
            "A materially harmful BEST_EFFORT write needs its accepted risk record.",
        )
    envelope = {"phase": "reconcile", "token": token, "request": request}
    result = external_exchange(
        config.get("command"), envelope, config.get("timeout_seconds", 60)
    )
    if result.get("status") != "found":
        if result.get("status") != "absent":
            raise RuntimeFailure(
                "uncertain_external_result",
                "Reconciliation must establish found or absent before applying an effect.",
            )
        result = external_exchange(
            config.get("command"),
            dict(envelope, phase="apply"),
            config.get("timeout_seconds", 60),
        )
        if result.get("status") != "completed":
            raise RuntimeFailure(
                "uncertain_external_result",
                "The adapter has not confirmed durable completion.",
            )
    receipt = {
        "status": "COMPLETED",
        "adapter": adapter,
        "guarantee": guarantee,
        "operationId": token["operation_id"],
        "inputHash": token["input_hash"],
        "result": result["result"],
    }
    if request.get("kind") == "linear-project-resources-v1":
        from .project_resources import validate_binding

        validate_binding(result["result"], request, request["carrier"])
    store.remember(token, receipt)
    return receipt
