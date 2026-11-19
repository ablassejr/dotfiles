"""Open answers, evidence-bound assessment, and human-owned reconsideration."""

import hashlib
import json

from .client import RuntimeFailure

POLICY = "open-decisions-v1"


def require(condition, message):
    if not condition:
        raise RuntimeFailure("invalid_decision_analysis", message)


def nonempty(value):
    return isinstance(value, str) and bool(value.strip())


def validate_analysis(analysis, binding, response):
    require(isinstance(analysis, dict), "Analyze the human answer before recording it.")
    require(
        analysis.get("schema_version") == 1
        and analysis.get("decisionBinding") == binding
        and analysis.get("response") == response,
        "The assessment must bind the exact current question and human response.",
    )
    require(
        binding
        and isinstance(response, dict)
        and response.get("binding") == binding
        and nonempty(response.get("actor"))
        and nonempty(response.get("answer")),
        "Preserve the named human's explicit answer and current question binding.",
    )
    require(
        nonempty(analysis.get("summary")),
        "Explain the meaning and consequences of the answer.",
    )
    findings = analysis.get("findings")
    require(isinstance(findings, list), "Supply the assessment's findings inventory.")
    ids = set()
    for finding in findings:
        require(
            isinstance(finding, dict), "Each finding must explain a material concern."
        )
        require(
            nonempty(finding.get("id")) and finding["id"] not in ids,
            "Identify each distinct concern.",
        )
        ids.add(finding["id"])
        require(
            finding.get("kind")
            in {"DISAGREEMENT", "CONFLICT", "EVIDENCE", "CLARIFICATION"}
            and nonempty(finding.get("reason"))
            and nonempty(finding.get("suggested_change")),
            "Explain the concern and suggest a concrete change or clarification.",
        )
        refs = finding.get("evidence_refs")
        require(
            isinstance(refs, list) and all(nonempty(ref) for ref in refs),
            "List the supporting references; distinguish reasoning from sourced facts.",
        )
        if finding["kind"] in {"CONFLICT", "EVIDENCE"}:
            require(
                refs, "Cite the conflicting decision, constraint, or relevant evidence."
            )
    return "DISCUSS" if findings else "ACCEPT"


def analysis_binding(analysis):
    digest = hashlib.sha256(
        json.dumps(
            analysis, sort_keys=True, separators=(",", ":"), ensure_ascii=False
        ).encode()
    ).hexdigest()
    return {
        "ref": "decision-analysis:" + digest,
        "hash": "sha256:" + digest,
        "question": analysis["decisionBinding"],
    }


def human_variables(headers, current, response):
    if headers.get("decisionPolicy") != POLICY:
        return {}
    action = response["action"]
    if action in {"select_answer", "revise_answer"}:
        require(
            nonempty(response.get("answer")),
            "Supply the human's answer in their own words.",
        )
    if headers.get("bindingVariable") != "decisionAnalysisBinding":
        return {}
    analysis = current.get("decisionAnalysis")
    validate_analysis(
        analysis, current.get("decisionBinding"), current.get("decisionResponse")
    )
    require(
        response["binding"] == analysis_binding(analysis),
        "Respond to the current assessment and its exact evidence.",
    )
    if action == "revise_answer":
        return {
            "decisionResponse": dict(
                response,
                action="select_answer",
                binding=current["decisionBinding"],
                sourceDecisionReviewResponse=response,
            )
        }
    return {}


def prepare_completion(client, job, result):
    headers = job.get("customHeaders", {})
    if result.get("status") != "completed" or headers.get("decisionPolicy") != POLICY:
        return result
    current = job.get("variables", {})
    output = dict(result.get("variables", {}))
    phase = headers.get("phase")
    if phase not in {"analyze_decision", "record_decision"}:
        return result
    for key in ("decisionBinding", "decisionResponse", "decisionReviewResponse"):
        require(
            output.get(key, current.get(key)) == current.get(key),
            "Assessment cannot replace " + key + ".",
        )
    binding, response = current.get("decisionBinding"), current.get("decisionResponse")
    analysis = (
        output.get("decisionAnalysis")
        if phase == "analyze_decision"
        else current.get("decisionAnalysis")
    )
    outcome = validate_analysis(analysis, binding, response)
    if phase == "analyze_decision":
        output.update(
            decisionAnalysisOutcome=outcome,
            decisionAnalysisBinding=analysis_binding(analysis),
            decisionReviewResponse=None,
        )
    else:
        require(
            output.get("decisionAnalysis", analysis) == analysis,
            "Record the assessment that was actually performed.",
        )
        review = current.get("decisionReviewResponse")
        if outcome == "DISCUSS":
            require(
                isinstance(review, dict)
                and review.get("binding") == analysis_binding(analysis)
                and review.get("action") == "keep_answer"
                and nonempty(review.get("actor")),
                "Surface the concerns and obtain the human's disposition before recording.",
            )
            task = client.request(
                "GET", "/user-tasks/" + str(review.get("user_task_key"))
            )
            require(
                task.get("state") == "COMPLETED"
                and task.get("tenantId") == client.tenant
                and task.get("elementId") == "consider_decision"
                and str(task.get("processInstanceKey"))
                == str(job["processInstanceKey"])
                and client.variables(task["processInstanceKey"]).get(
                    "decisionReviewResponse"
                )
                == review,
                "Keeping the answer requires the completed, matching human assessment task.",
            )
        output["recordedDecision"] = {
            "binding": binding,
            "answer": response["answer"],
            "actor": response["actor"],
            "response": response,
            "analysis": analysis,
            "followup": review if outcome == "DISCUSS" else None,
        }
    return dict(result, variables=output)
