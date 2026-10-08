"""At-least-once jobs with explicit handlers and destination-specific adapters."""

import subprocess
from .client import RuntimeFailure
from .proposal import validate_completion
from .program import validate_completion as validate_program_completion
from .project_resources import (
    publish_resources,
    validate_completion as validate_resource_completion,
)
from .approvals import prepare_completion, check_revision
from .decisions import prepare_completion as prepare_decision_completion
from .issue_reviews import (
    before_handler,
    prepare_completion as prepare_issue_completion,
)
from .visuals import validate_embedded_visuals, validate_visual_completion
from .operations import (
    OperationStore,
    apply_operation,
    command_exchange,
    operation_token,
)


def finish(client, job, result):
    result = prepare_completion(client, job, result)
    result = prepare_decision_completion(client, job, result)
    validate_program_completion(job, result)
    validate_resource_completion(job, result)
    result = prepare_issue_completion(client, job, result)
    validate_visual_completion(job, result)
    validate_completion(job, result)
    key = str(job["jobKey"])
    status = result.get("status")
    if status == "completed":
        return client.request(
            "POST",
            f"/jobs/{key}/completion",
            {"variables": result.get("variables", {})},
        )
    if status == "business_error":
        return client.request(
            "POST",
            f"/jobs/{key}/error",
            {
                "errorCode": result["errorCode"],
                "errorMessage": result.get("message", ""),
                "variables": result.get("variables", {}),
            },
        )
    if status in {"transient", "unrecoverable"}:
        retries = max(0, job["retries"] - 1) if status == "transient" else 0
        return client.request(
            "POST",
            f"/jobs/{key}/failure",
            {
                "retries": retries,
                "errorMessage": result.get("message", status),
                "retryBackOff": result.get("retryBackOff", 1000),
            },
        )
    raise RuntimeFailure(
        "invalid_worker_result",
        "Use completed, transient, business_error, or unrecoverable.",
    )


def work_once(client, config, worker_name):
    handled = []
    for job_type, handler in config.get("handlers", {}).items():
        timeout = handler.get("timeout_seconds", 60)
        activated = client.request(
            "POST",
            "/jobs/activation",
            {
                "type": job_type,
                "timeout": int((timeout + 10) * 1000),
                "maxJobsToActivate": 1,
                "worker": worker_name,
                "requestTimeout": -1,
                "tenantIds": [client.tenant],
            },
        )
        for job in activated.get("jobs", []):
            try:
                validate_embedded_visuals(job.get("variables", {}))
                check_revision(job.get("variables", {}))
                if (
                    job.get("customHeaders", {}).get("phase")
                    == "publish_linear_program"
                ):
                    validate_program_completion(
                        job, {"status": "completed", "variables": {}}
                    )
                before_handler(client, job)
                if handler.get("builtin") in {"grounded-answer", "issue-reviews"}:
                    result = {"status": "completed", "variables": {}}
                elif handler.get("builtin") == "project-resources":
                    result = publish_resources(job, config, handler)
                elif handler.get("adapter"):
                    request = job["variables"]["operationRequest"]
                    token = operation_token(
                        job,
                        job["variables"]["operationIntent"],
                        request,
                        handler["adapter"],
                    )
                    store = OperationStore(config["operation_store"])
                    try:
                        receipt = apply_operation(store, token, request, handler)
                    finally:
                        store.close()
                    if receipt["status"] == "SUPERSEDED" and not receipt.get("current"):
                        result = {
                            "status": "transient",
                            "message": "The desired successor has not published a result yet.",
                        }
                    else:
                        result = {
                            "status": "completed",
                            "variables": {
                                handler.get(
                                    "result_variable", "operationResult"
                                ): receipt,
                                "operationStatus": receipt["status"],
                            },
                        }
                        if "visuals" in request:
                            result["variables"]["visuals"] = request["visuals"]
                else:
                    result = command_exchange(
                        handler.get("command"), {"job": job}, timeout
                    )
            except subprocess.TimeoutExpired:
                result = {
                    "status": "transient",
                    "message": "Handler exceeded its configured timeout; reconcile uncertain effects on retry.",
                }
            except (RuntimeFailure, KeyError, ValueError, OSError) as error:
                retryable = getattr(error, "code", None) in {
                    "transient_external_failure",
                    "uncertain_external_result",
                }
                details = getattr(error, "details", None)
                result = {
                    "status": "transient" if retryable else "unrecoverable",
                    "message": str(error),
                    "retryBackOff": (
                        details.get("retryBackOff", 1000)
                        if isinstance(details, dict)
                        else 1000
                    ),
                }
            if result.get("status") not in {
                "completed",
                "business_error",
                "transient",
                "unrecoverable",
            } or not isinstance(result.get("variables", {}), dict):
                result = {
                    "status": "unrecoverable",
                    "message": "Handler returned an invalid completion or failure contract.",
                }
            try:
                finish(client, job, result)
                handled.append(
                    {
                        "jobKey": job["jobKey"],
                        "type": job_type,
                        "result": result["status"],
                        "accepted": True,
                    }
                )
            except RuntimeFailure as error:
                if error.code == "pending_engine_readback":
                    finish(
                        client,
                        job,
                        {
                            "status": "transient",
                            "message": str(error),
                            "retryBackOff": 1000,
                        },
                    )
                    handled.append(
                        {
                            "jobKey": job["jobKey"],
                            "type": job_type,
                            "result": "transient",
                            "accepted": True,
                            "error": error.code,
                        }
                    )
                    continue
                if error.code in {
                    "invalid_design_proposal",
                    "invalid_program_plan",
                    "invalid_project_resources",
                    "invalid_issue_review",
                    "invalid_issue_content",
                    "invalid_visual",
                    "invalid_approval_evidence",
                    "invalid_decision_analysis",
                }:
                    finish(
                        client, job, {"status": "unrecoverable", "message": str(error)}
                    )
                handled.append(
                    {
                        "jobKey": job["jobKey"],
                        "type": job_type,
                        "result": result["status"],
                        "accepted": False,
                        "error": error.code,
                    }
                )
    return {"handled": handled}
