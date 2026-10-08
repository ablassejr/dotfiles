#!/usr/bin/env python3
"""Apply one human action to a selected decision without advancing Ground Me."""

from __future__ import annotations

import argparse
import json
import hashlib
from pathlib import Path
import sys
from typing import Any, Sequence

from validate_decision_question import _load, _nonempty, _validate

from specflow_runtime.decisions import validate_analysis, analysis_binding
from specflow_runtime.client import RuntimeFailure


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Apply one action to a decision question.")
    parser.add_argument("question", type=Path)
    parser.add_argument("action", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    question, errors, question_code = _load(arguments.question)
    if question is not None:
        errors.extend(_validate(question))
    action, action_errors, action_code = _load(arguments.action)
    errors.extend({**item, "path": f"action:{item['path']}"} for item in action_errors)
    read_code = max(question_code, action_code)

    transition: dict[str, Any] | None = None
    if question is not None and action is not None and not errors:
        decision = question["decision"]
        decision_id = decision["decision_id"]
        revision = question["frontier_revision"]
        action_type = action.get("type")
        if action_type == "ground_me":
            transition = {
                "type": "grounding_required",
                "decision_id": decision_id,
                "decision_resolved": False,
                "resume_decision": decision_id,
                "frontier_recompute_required": False,
                "next_frontier_revision": revision,
                "decision_record": None,
            }
        elif action_type in {"answer", "option", "custom_answer"}:
            answer = action.get("option_id") if action_type == "option" else action.get("answer")
            actor = action.get("actor", action.get("confirmed_by"))
            if action_type == "option" and answer not in {o["id"] for o in decision.get("options", [])}:
                errors.append(_error("unknown_option", "action:$.option_id", "The referenced option is not in this question."))
            if not _nonempty(answer) or not _nonempty(actor):
                errors.append(_error("decision_answer", "action:$", "Supply the named human and their explicit answer."))
            binding = {
                "ref": decision_id,
                "hash": "sha256:" + hashlib.sha256(json.dumps(question, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest(),
                "frontierRevision": revision,
            }
            response = {"action": "select_answer", "answer": answer, "actor": actor, "binding": binding}
            transition = {
                "type": "decision_analysis_required",
                "decision_id": decision_id,
                "decision_resolved": False,
                "resume_decision": decision_id,
                "frontier_recompute_required": False,
                "next_frontier_revision": revision,
                "decision_record": None,
                "analysis_input": {"decisionBinding": binding, "response": response},
            }
            analysis = action.get("analysis")
            if analysis is not None and not errors:
                try:
                    outcome = validate_analysis(analysis, binding, response)
                    followup = action.get("followup")
                    reviewed = (
                        isinstance(followup, dict)
                        and followup.get("binding") == analysis_binding(analysis)
                        and followup.get("action") == "keep_answer"
                        and _nonempty(followup.get("actor"))
                    )
                    if followup is not None and not reviewed:
                        raise RuntimeFailure("invalid_decision_analysis", "The follow-up must bind the current analysis and the human's explicit choice to keep the answer.")
                    if outcome == "ACCEPT" or reviewed:
                        transition.update(
                            type="decision_recorded", decision_resolved=True, resume_decision=None,
                            frontier_recompute_required=True, next_frontier_revision=revision + 1,
                            decision_record={"answer_type": action_type, "answer": answer, "confirmed_by": actor,
                                             "basis_refs": decision["first_principles_links"], "analysis": analysis,
                                             "followup": followup if outcome == "DISCUSS" else None},
                        )
                    else:
                        transition.update(type="decision_discussion_required", analysis=analysis,
                                          analysis_binding=analysis_binding(analysis))
                except RuntimeFailure as error:
                    errors.append(_error(error.code, "action:$.analysis", str(error)))
        elif action_type == "question_invalidated":
            if not _nonempty(action.get("reason")):
                errors.append(_error("invalidation_reason", "action:$.reason", "Expected an evidence-grounded reason."))
            evidence_refs = action.get("evidence_refs")
            if not isinstance(evidence_refs, list) or not evidence_refs or not all(_nonempty(item) for item in evidence_refs):
                errors.append(_error("invalidation_evidence", "action:$.evidence_refs", "Expected one or more evidence references."))
            if not errors:
                transition = {
                    "type": "question_invalidated",
                    "decision_id": decision_id,
                    "decision_resolved": False,
                    "resume_decision": None,
                    "frontier_recompute_required": True,
                    "next_frontier_revision": revision + 1,
                    "decision_record": None,
                    "reason": action["reason"],
                    "evidence_refs": action["evidence_refs"],
                }
        else:
            errors.append(_error("action_type", "action:$.type", "Expected answer, option, custom_answer, ground_me, or question_invalidated."))

    exit_code = read_code if read_code == 2 else (1 if errors else 0)
    result = {
        "status": "ok" if not errors else ("error" if exit_code == 2 else "invalid"),
        "question": str(arguments.question),
        "action": str(arguments.action),
        "transition": transition,
        "errors": errors,
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        for item in errors:
            print(f"{item['code']}: {item['path']}: {item['message']}", file=sys.stderr)
    else:
        print(json.dumps(transition, indent=2, sort_keys=True))
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
