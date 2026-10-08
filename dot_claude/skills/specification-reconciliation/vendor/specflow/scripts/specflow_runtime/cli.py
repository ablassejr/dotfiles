"""Public specflow Camunda commands; no independent workflow state machine."""

import json
import os
from pathlib import Path
import time

from .client import (
    Client,
    RuntimeFailure,
    canonical,
    digest,
    read_json,
    validate_references,
)
from .operations import OperationStore, apply_operation, normalized_request
from .worker import finish, work_once
from .proposal import CONTRACT, validate_proposal
from .visuals import validate_visuals, validate_embedded_visuals
from .approvals import effective_variables, human_variables
from .progress import stage_progress, render_progress
from .project_resources import inventory_artifacts
from .issue_content import validate_content

COMMANDS = {
    "deploy",
    "start",
    "status",
    "inspect",
    "resume",
    "validate",
    "activate",
    "complete-job",
    "fail-job",
    "complete-task",
    "correlate",
    "resolve-incident",
    "worker",
    "apply-operation",
    "hash-operation",
    "validate-visuals",
    "validate-issue-content",
    "validate-pr-content",
    "prepare-response",
    "inventory-project-artifacts",
}
DEFINITIONS = {
    "epic": "epic-spec-workflow",
    "grounding": "ground-me-workflow",
    "research": "multimodal-research-workflow",
    "program": "implementation-program-workflow",
    "ticket": "implementation-ticket-workflow",
}


def add_commands(commands):
    for command in sorted(COMMANDS):
        parser = commands.add_parser(command, help=f"Camunda integration: {command}.")
        parser.add_argument("--json", action="store_true", dest="json_output")
        parser.add_argument(
            "--url", default=os.getenv("SPECFLOW_CAMUNDA_URL", "http://localhost:8097")
        )
        parser.add_argument(
            "--tenant", default=os.getenv("SPECFLOW_CAMUNDA_TENANT", "<default>")
        )
        parser.add_argument("--config", type=Path)
        if command in {"start", "status", "inspect", "resume", "validate"}:
            parser.add_argument("business_id")
            parser.add_argument("--definition")
            parser.add_argument("--version-tag", default="v1")
            parser.add_argument("--key")
        if command == "deploy":
            parser.add_argument(
                "--resources", type=Path, default=Path(__file__).parent / "bpmn"
            )
        if command == "start":
            parser.add_argument("--variables", type=Path)
        if command == "activate":
            parser.add_argument("job_type")
            parser.add_argument("--timeout-ms", type=int, default=60000)
            parser.add_argument("--worker-name", default="specflow-agent")
        if command in {"complete-job", "fail-job"}:
            parser.add_argument(
                "job",
                type=Path,
                help="Activated job JSON, including jobKey and retries.",
            )
            parser.add_argument("result", type=Path)
        if command == "complete-task":
            parser.add_argument("response", type=Path)
        if command == "prepare-response":
            parser.add_argument("task_key")
            parser.add_argument("--actor", required=True)
            parser.add_argument("--action", required=True)
            parser.add_argument("--answer")
        if command == "correlate":
            parser.add_argument("name")
            parser.add_argument("correlation_key")
            parser.add_argument("--message-id", required=True)
            parser.add_argument("--ttl-ms", type=int, default=0)
            parser.add_argument("--variables", type=Path)
        if command == "resolve-incident":
            parser.add_argument("incident_key")
            parser.add_argument("--retries", type=int, default=1)
        if command == "worker":
            parser.add_argument("--once", action="store_true")
            parser.add_argument("--poll-seconds", type=float, default=2)
            parser.add_argument("--worker-name", default="specflow-worker")
        if command in {
            "apply-operation",
            "hash-operation",
            "validate-visuals",
            "validate-issue-content",
            "validate-pr-content",
        }:
            parser.add_argument("request", type=Path)
        if command == "inventory-project-artifacts":
            parser.add_argument("directory", type=Path)
            parser.add_argument("--source", type=Path, required=True)
        if command == "apply-operation":
            parser.add_argument("token", type=Path)
            parser.add_argument("--store", required=True, type=Path)


def complete_task(client, response):
    key = str(response["user_task_key"])
    task = client.request("GET", "/user-tasks/" + key)
    if (
        task["tenantId"] != client.tenant
        or str(task["processInstanceKey"]) != str(response["process_instance_key"])
        or task["elementId"] != response["element_id"]
    ):
        raise RuntimeFailure(
            "response_binding_mismatch",
            "The response does not match this task, process, element, and tenant.",
        )
    headers = task.get("customHeaders", {})
    action = response["action"]
    if action not in headers.get("actions", "").split(",") or not response.get("actor"):
        raise RuntimeFailure(
            "invalid_human_response",
            "Supply a named actor and one of the task's declared actions.",
        )
    binding_name = headers["bindingVariable"]
    data = client.request(
        "POST",
        f"/user-tasks/{key}/effective-variables/search",
        {"filter": {"name": binding_name}, "page": {"from": 0, "limit": 10}},
    )
    values = {item["name"]: json.loads(item["value"]) for item in data.get("items", [])}
    binding = values.get(binding_name)
    if not binding or binding != response.get("binding"):
        raise RuntimeFailure(
            "stale_human_response",
            "The response must contain the task's exact current reviewed-content binding.",
            {"requiredBinding": binding},
        )
    if headers.get("resultContract") == CONTRACT:
        source_name = headers["sourceBindingVariable"]
        source_data = client.request(
            "POST",
            f"/user-tasks/{key}/effective-variables/search",
            {"filter": {"name": source_name}, "page": {"from": 0, "limit": 10}},
        )
        sources = {
            item["name"]: json.loads(item["value"])
            for item in source_data.get("items", [])
        }
        validate_proposal(binding, headers["planningScope"], sources.get(source_name))
    variables = {headers["responseVariable"]: response}
    current = effective_variables(client, key)
    variables.update(human_variables(headers, current, response))
    from .decisions import human_variables as decision_variables

    variables.update(decision_variables(headers, current, response))
    if headers.get("visualBindingVariable"):
        validate_visuals(binding.get("visuals"))
    validate_embedded_visuals(binding)
    return client.request(
        "POST",
        f"/user-tasks/{key}/completion",
        {"variables": variables, "action": action},
    )


def execute(args):
    config = read_json(args.config) if args.config else {}
    client = Client(args.url, args.tenant)
    command = args.command
    if command in {"validate-issue-content", "validate-pr-content"}:
        return validate_content(
            read_json(args.request), pull_request=command == "validate-pr-content"
        )
    if command == "validate-visuals":
        manifest = read_json(args.request)
        validate_visuals(
            manifest.get("visuals") if isinstance(manifest, dict) else None
        )
        return {"validated": len(manifest["visuals"]), "policy": "graph-renderers-v1"}
    if command == "deploy":
        return client.deploy(args.resources)
    if command in {"start", "status", "inspect", "resume", "validate"}:
        definition = args.definition or DEFINITIONS.get(
            args.business_id.split(":", 1)[0]
        )
        if not definition:
            raise RuntimeFailure(
                "definition_required",
                "Use an epic:, grounding:, research:, program:, or ticket: ID, or supply --definition.",
            )
        if command == "start":
            return client.start(
                args.business_id,
                definition,
                read_json(args.variables) if args.variables else {},
                args.version_tag,
            )
        root = client.resolve(args.business_id, definition, args.key)
        if root.get("processDefinitionVersionTag") != args.version_tag:
            raise RuntimeFailure(
                "definition_version_mismatch",
                "The root is pinned to another version tag.",
                root,
            )
        snapshot = client.inspect(root)
        if command in {"resume", "validate"}:
            snapshot["validation"] = validate_references(
                snapshot, config.get("validators", [])
            )
            snapshot["permittedActions"] = []
            for state in snapshot["instances"]:
                if state["process"]["state"] != "ACTIVE":
                    continue
                for collection, action in (
                    ("activeUserTasks", "present_human_task"),
                    ("activeJobs", "activate_job"),
                    ("activeIncidents", "repair_incident"),
                    ("waitingMessages", "await_message"),
                ):
                    for item in state[collection]:
                        passed = snapshot["validation"]["status"] == "passed"
                        incident_blocked = collection == "activeJobs" and any(
                            str(incident.get("elementInstanceKey"))
                            == str(item.get("elementInstanceKey"))
                            for incident in state["activeIncidents"]
                        )
                        snapshot["permittedActions"].append(
                            {
                                "action": (
                                    "repair_references"
                                    if not passed
                                    else (
                                        "repair_incident"
                                        if incident_blocked
                                        else action
                                    )
                                ),
                                "processInstanceKey": state["process"][
                                    "processInstanceKey"
                                ],
                                "workItem": item,
                                "referenceChecksPassed": passed,
                            }
                        )
            snapshot["engineCompleted"] = root["state"] == "COMPLETED"
        snapshot["progress"] = stage_progress(snapshot)
        if command == "status":
            return dict(root, progress=snapshot["progress"])
        return snapshot
    if command == "activate":
        return client.request(
            "POST",
            "/jobs/activation",
            {
                "type": args.job_type,
                "timeout": args.timeout_ms,
                "maxJobsToActivate": 1,
                "worker": args.worker_name,
                "requestTimeout": -1,
                "tenantIds": [client.tenant],
            },
        )
    if command in {"complete-job", "fail-job"}:
        result = read_json(args.result)
        if (command == "complete-job") != (result.get("status") == "completed"):
            raise RuntimeFailure(
                "invalid_worker_result",
                "Use complete-job for completed results and fail-job for failure classifications.",
            )
        return finish(client, read_json(args.job), result)
    if command == "complete-task":
        return complete_task(client, read_json(args.response))
    if command == "prepare-response":
        task = client.request("GET", "/user-tasks/" + args.task_key)
        if task.get("tenantId") != client.tenant or task.get("state") != "CREATED":
            raise RuntimeFailure(
                "invalid_human_response",
                "Prepare a response for an active task in this tenant.",
            )
        headers = task["customHeaders"]
        if (
            args.action not in headers.get("actions", "").split(",")
            or not args.actor.strip()
        ):
            raise RuntimeFailure(
                "invalid_human_response",
                "Choose a declared action and named human actor.",
            )
        current = effective_variables(client, args.task_key)
        response = {
            "user_task_key": args.task_key,
            "process_instance_key": str(task["processInstanceKey"]),
            "element_id": task["elementId"],
            "actor": args.actor,
            "action": args.action,
            "binding": current[headers["bindingVariable"]],
        }
        if args.action == "aligned_and_answer":
            response["decision"] = {
                "binding": current.get("decisionBinding"),
                "answer": args.answer,
            }
        elif args.answer is not None:
            response["answer"] = args.answer
        human_variables(headers, current, response)
        from .decisions import human_variables as decision_variables

        decision_variables(headers, current, response)
        validate_embedded_visuals(response["binding"])
        return {"response": response, "submitted": False}
    if command == "correlate":
        result = client.request(
            "POST",
            "/messages/publication",
            {
                "name": args.name,
                "correlationKey": args.correlation_key,
                "messageId": args.message_id,
                "timeToLive": args.ttl_ms,
                "variables": read_json(args.variables) if args.variables else {},
                "tenantId": client.tenant,
            },
        )
        return {
            "publication": result,
            "disposition": "accepted",
            "note": "Read engine state to confirm correlation; TTL controls buffering and deduplication lifetime.",
        }
    if command == "resolve-incident":
        incident = client.request("GET", "/incidents/" + args.incident_key)
        if incident["tenantId"] != client.tenant:
            raise RuntimeFailure(
                "identity_mismatch", "The incident belongs to a different tenant."
            )
        if incident.get("jobKey"):
            client.request(
                "PATCH",
                "/jobs/" + str(incident["jobKey"]),
                {"changeset": {"retries": args.retries}},
            )
        return client.request(
            "POST", "/incidents/" + args.incident_key + "/resolution", {}
        )
    if command == "worker":
        config = dict(
            config,
            handlers={
                "specflow.resume-grounded-decision": {"builtin": "grounded-answer"},
                **config.get("handlers", {}),
            },
        )
        if not config.get("handlers"):
            raise RuntimeFailure(
                "handlers_required",
                "Configure job handlers; no semantic or approval results are fabricated by the runtime.",
            )
        while True:
            result = work_once(client, config, args.worker_name)
            if args.once:
                return result
            if result["handled"]:
                print(json.dumps(result), flush=True)
            time.sleep(args.poll_seconds)
    if command == "inventory-project-artifacts":
        return inventory_artifacts(args.directory, read_json(args.source))
    if command == "hash-operation":
        return {
            "input_hash": digest(canonical(normalized_request(read_json(args.request))))
        }
    if command == "apply-operation":
        token = read_json(args.token)
        store = OperationStore(args.store)
        try:
            return apply_operation(
                store,
                token,
                read_json(args.request),
                config.get("adapters", {}).get(token["adapter"], {}),
            )
        finally:
            store.close()


def run(args):
    try:
        result = execute(args)
        failed = (
            isinstance(result, dict)
            and result.get("validation", {}).get("status") == "incomplete"
        )
        if args.command in {"status", "resume"} and not args.json_output:
            print(render_progress(result))
            return 1 if failed else 0
        print(
            json.dumps(
                {
                    "status": "incomplete" if failed else "ok",
                    "command": args.command,
                    "result": result,
                },
                sort_keys=True,
                indent=None if args.json_output else 2,
            )
        )
        return 1 if failed else 0
    except (RuntimeFailure, OSError, ValueError, KeyError) as error:
        print(
            json.dumps(
                {
                    "status": "error",
                    "command": args.command,
                    "error": {
                        "code": getattr(error, "code", "invalid_input"),
                        "message": str(error),
                        "details": getattr(error, "details", None),
                    },
                }
            )
        )
        return 2
