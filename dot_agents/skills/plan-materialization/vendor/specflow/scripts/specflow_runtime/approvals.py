"""Evidence-bound approval reuse, review routing, and combined human responses."""

import json

from .client import RuntimeFailure
from .visuals import validate_embedded_visuals

POLICY = "approval-economy-v1"
BASIS_TASKS = {"approve_basis", "approve_program_basis", "approve_ticket_basis"}


def require(condition, message):
    if not condition:
        raise RuntimeFailure("invalid_approval_evidence", message)


def effective_variables(client, task_key):
    values = {}
    for item in client.search("user-tasks/" + str(task_key) + "/effective-variables"):
        require(
            not item.get("isTruncated"),
            "Refresh truncated task evidence before responding.",
        )
        values[item["name"]] = json.loads(item["value"])
    return values


def inherited_basis(client, reuse, binding):
    if not reuse:
        return {"mode": "HUMAN_REQUIRED", "reason": "No source approval supplied."}
    require(
        isinstance(reuse, dict) and str(reuse.get("approvalTaskKey", "")).isdigit(),
        "Supply the source basis approval task key.",
    )
    task = client.request("GET", "/user-tasks/" + str(reuse["approvalTaskKey"]))
    require(
        task.get("tenantId") == client.tenant and task.get("elementId") in BASIS_TASKS,
        "Reuse a basis approval in this tenant.",
    )
    require(task.get("state") == "COMPLETED", "The source basis task is not completed.")
    headers = task["customHeaders"]
    source = client.variables(task["processInstanceKey"])
    response = source.get(headers["responseVariable"], {})
    require(
        isinstance(response, dict)
        and str(response.get("user_task_key")) == str(task["userTaskKey"])
        and response.get("action") == "approved"
        and response.get("actor"),
        "The source task has no matching human approval record.",
    )
    approved = response.get("binding")
    require(
        approved and source.get(headers["bindingVariable"]) == approved,
        "The source basis has changed since that approval.",
    )
    if binding != approved:
        return {
            "mode": "HUMAN_REQUIRED",
            "reason": "The child basis differs from the approved source.",
        }
    validate_embedded_visuals(approved)
    return {
        "mode": "INHERITED",
        "approvalTaskKey": str(task["userTaskKey"]),
        "sourceProcessInstanceKey": str(task["processInstanceKey"]),
        "actor": response["actor"],
        "binding": approved,
    }


def check_revision(variables, output=None):
    guard = variables.get("revisionGuard")
    if not guard:
        return
    require(
        isinstance(guard, dict) and isinstance(guard.get("sources"), dict),
        "The presentation revision needs its source snapshot.",
    )
    for key, value in guard["sources"].items():
        require(
            variables.get(key) == value
            and (output is None or output.get(key, value) == value),
            "Presentation-only revision changed "
            + key
            + ". Request a semantic revision.",
        )
    if output is not None:
        require(
            output.get("revisionGuard", guard) == guard,
            "A worker cannot clear the presentation revision scope.",
        )


def check_combined_visuals(headers, variables, proposal):
    if headers.get("combinedVisualReview") != "true":
        return
    compiled = variables.get("visualBinding", {}).get("visuals")
    presented = proposal.get("visuals") if isinstance(proposal, dict) else None
    require(
        isinstance(compiled, list)
        and isinstance(presented, list)
        and all(visual in presented for visual in compiled),
        "The final proposal must include the current compiled visuals.",
    )


def prepare_completion(client, job, result):
    if result.get("status") != "completed":
        return result
    headers = job.get("customHeaders", {})
    if headers.get("approvalPolicy") != POLICY:
        return result
    current = job.get("variables", {})
    output = dict(result.get("variables", {}))
    check_revision(current, output)
    basis_name = headers.get("inheritBasisVariable")
    if basis_name:
        require(
            isinstance(output.get(basis_name), dict)
            and output[basis_name].get("ref")
            and output[basis_name].get("hash"),
            "Return the current child basis binding.",
        )
        evidence = inherited_basis(
            client, current.get("basisReuse"), output[basis_name]
        )
        output.update(basisApprovalMode=evidence["mode"], basisInheritance=evidence)
    route = headers.get("approvalRoute")
    if route == "review":
        review = output.get("reviewResult")
        disposition = "human"
        if review is not None:
            binding = output.get("reviewBinding")
            require(
                isinstance(review, dict)
                and binding
                and review.get("binding") == binding,
                "Review evidence must bind its reviewed source.",
            )
            require(
                current.get("semanticBinding") == binding,
                "Review evidence must match the current semantic source.",
            )
            require(
                isinstance(review.get("findings"), list)
                and review.get("status") in {"PASS", "REPAIR", "HUMAN"},
                "Return a complete review result and findings inventory.",
            )
            if review["status"] == "PASS":
                require(
                    review["findings"] == [],
                    "A clean review cannot contain unresolved findings.",
                )
                disposition = "approved"
            elif review["status"] == "REPAIR":
                basis = current.get("basisBinding")
                require(
                    basis
                    and review["findings"]
                    and all(
                        isinstance(f, dict) and f.get("ref") and f.get("basis") == basis
                        for f in review["findings"]
                    ),
                    "Automatic repairs must identify their finding and existing approved basis.",
                )
                disposition = "repair"
        output.update(
            reviewDisposition=disposition,
            reviewVerification={
                "kind": "AUTOMATED_REVIEW",
                "disposition": disposition,
                "binding": output.get("reviewBinding"),
            },
        )
    elif route == "human-review":
        response = current.get("reviewResponse", {})
        require(
            response.get("binding") == current.get("reviewBinding")
            and response.get("actor")
            and response.get("action")
            in {"approved", "repair", "research", "decision", "revise_basis"},
            "Record the exact current human review disposition.",
        )
        output["reviewDisposition"] = response["action"]
    elif route == "grounded-answer":
        output.update(grounded_answer(client, current))
    check_combined_visuals(headers, current, output.get("designProposalBinding"))
    return dict(result, variables=output)


def human_variables(headers, current, response):
    variables = {}
    if headers.get("approvalPolicy") != POLICY:
        return variables
    action = response["action"]
    if headers.get("revisionSources"):
        if action == "presentation_change":
            names = headers["revisionSources"].split(",")
            sources = {name: current[name] for name in names if name in current}
            require(sources, "A presentation repair needs a planning source.")
            variables["revisionGuard"] = {"sources": sources, "response": response}
        elif action in {"approved", "changes_requested", "semantic_change"}:
            variables["revisionGuard"] = None
    if action == "aligned_and_answer":
        decision = response.get("decision")
        require(
            headers.get("combinedDecision") == "true" and isinstance(decision, dict),
            "This task does not support a combined decision response.",
        )
        binding = current.get("decisionBinding")
        require(
            binding
            and response["binding"].get("question") == binding
            and decision.get("binding") == binding,
            "The grounding explanation and answer must bind the same current question.",
        )
        require(
            isinstance(decision.get("answer"), str) and decision["answer"].strip(),
            "Supply the answer explicitly selected by the human.",
        )
    check_combined_visuals(headers, current, response["binding"])
    return variables


def grounded_answer(client, variables):
    outcome = {"combinedAnswerOutcome": "ASK", "decisionResponse": None}
    response = variables.get("groundingResponse", {})
    binding = variables.get("decisionBinding")
    decision = response.get("decision", {})
    if (
        response.get("action") != "aligned_and_answer"
        or not binding
        or response.get("binding") != variables.get("groundingBinding")
        or response.get("binding", {}).get("question") != binding
        or decision.get("binding") != binding
    ):
        return outcome
    task = client.request("GET", "/user-tasks/" + str(response.get("user_task_key")))
    require(
        task.get("tenantId") == client.tenant
        and task.get("elementId") == "confirm_understanding"
        and str(task.get("processInstanceKey"))
        == str(response.get("process_instance_key")),
        "The combined response must come from the completed grounding task.",
    )
    if task.get("state") in {"CREATED", "COMPLETING"}:
        raise RuntimeFailure(
            "pending_engine_readback",
            "Wait for the completed grounding task to appear in Camunda readback.",
        )
    require(
        task.get("state") == "COMPLETED",
        "The grounding approval task did not complete.",
    )
    source = client.variables(task["processInstanceKey"])
    if (
        source.get("groundingResponse") != response
        or source.get("groundingBinding") != response["binding"]
    ):
        return outcome
    validate_embedded_visuals(response["binding"])
    require(
        response.get("actor")
        and isinstance(decision.get("answer"), str)
        and decision["answer"].strip(),
        "The combined answer needs its human actor and selected answer.",
    )
    return {
        "combinedAnswerOutcome": "APPLIED",
        "decisionResponse": {
            "action": "select_answer",
            "actor": response["actor"],
            "binding": binding,
            "answer": decision["answer"],
            "sourceGroundingResponse": response,
        },
    }
