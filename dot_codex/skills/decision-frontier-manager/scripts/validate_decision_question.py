#!/usr/bin/env python3
"""Validate one basis-traced, currently unblocked decision question."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys
from typing import Any, Sequence


KIND = "epic-spec.decision-question"
CONFIDENCE = {"low", "medium", "high"}
RECOMMENDATION_CRITERIA = (
    "first_principles_alignment",
    "behavioral_correctness",
    "code_mass_effect",
    "conceptual_complexity",
    "reversibility",
    "operational_risk",
    "migration_cost",
)


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, str]], int]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError:
        return None, [_error("file_not_found", str(path), "The decision file does not exist.")], 2
    except json.JSONDecodeError as exception:
        return (
            None,
            [_error("invalid_json", str(path), f"JSON parsing failed at line {exception.lineno}, column {exception.colno}.")],
            2,
        )
    except OSError as exception:
        return None, [_error("read_failed", str(path), str(exception))], 2
    if not isinstance(payload, dict):
        return None, [_error("invalid_document", "$", "Expected a JSON object.")], 1
    return payload, [], 0


def _strings(value: object, path: str, errors: list[dict[str, str]], *, minimum: int = 0) -> list[str]:
    if not isinstance(value, list):
        errors.append(_error("string_list", path, "Expected an array of non-empty strings."))
        return []
    if len(value) < minimum:
        errors.append(_error("minimum_items", path, f"Expected at least {minimum} item(s)."))
    result: list[str] = []
    for index, item in enumerate(value):
        if not _nonempty(item):
            errors.append(_error("string_item", f"{path}[{index}]", "Expected a non-empty string."))
        else:
            result.append(str(item))
    return result


def _record(value: object, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(_error("object", path, "Expected an object."))
    return {}


def _validate(payload: dict[str, Any]) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    version = payload.get("schema_version")
    if version not in (2, 3):
        errors.append(_error("schema_version", "$.schema_version", "Expected schema version 2 or 3."))
    if payload.get("kind") != KIND:
        errors.append(_error("document_kind", "$.kind", f"Expected {KIND}."))
    revision = payload.get("frontier_revision")
    if type(revision) is not int or revision < 1:
        errors.append(_error("frontier_revision", "$.frontier_revision", "Expected a positive integer."))
    if "decisions" in payload:
        errors.append(_error("batched_questions", "$.decisions", "Present exactly one selected decision."))

    decision = _record(payload.get("decision"), "$.decision", errors)
    for field in ("decision_id", "question", "why_this_is_needed", "current_state"):
        if not _nonempty(decision.get(field)):
            errors.append(_error("required_string", f"$.decision.{field}", "Expected a non-empty string."))
    if decision.get("status") != "unresolved":
        errors.append(_error("decision_status", "$.decision.status", "A presented question must be unresolved."))

    links = _strings(decision.get("first_principles_links"), "$.decision.first_principles_links", errors, minimum=1)
    if links and not any(link.startswith("FPB-") for link in links):
        errors.append(_error("basis_trace", "$.decision.first_principles_links", "Include the approved FPB identifier."))

    prerequisites = decision.get("prerequisites")
    if not isinstance(prerequisites, list):
        errors.append(_error("prerequisites", "$.decision.prerequisites", "Expected an array."))
    else:
        for index, prerequisite in enumerate(prerequisites):
            path = f"$.decision.prerequisites[{index}]"
            if not isinstance(prerequisite, dict):
                errors.append(_error("prerequisite", path, "Expected an object."))
                continue
            if not _nonempty(prerequisite.get("decision_id")):
                errors.append(_error("prerequisite_id", f"{path}.decision_id", "Expected a decision ID."))
            if prerequisite.get("status") != "resolved":
                errors.append(_error("blocked_question", f"{path}.status", "Every prerequisite must be resolved."))

    options = decision.get("options", [] if version == 3 else None)
    option_ids: list[str] = []
    if not isinstance(options, list):
        errors.append(_error("options", "$.decision.options", "Expected an array of options."))
    else:
        if version == 2 and len(options) < 2:
            errors.append(_error("option_count", "$.decision.options", "Expected at least two material options."))
        for index, option in enumerate(options):
            path = f"$.decision.options[{index}]"
            if not isinstance(option, dict):
                errors.append(_error("option", path, "Expected an object."))
                continue
            option_id = option.get("id")
            if not _nonempty(option_id):
                errors.append(_error("option_id", f"{path}.id", "Expected a non-empty option ID."))
            elif str(option_id) in option_ids:
                errors.append(_error("duplicate_option", f"{path}.id", "Option IDs must be unique."))
            else:
                option_ids.append(str(option_id))
            if not _nonempty(option.get("title")):
                errors.append(_error("option_title", f"{path}.title", "Expected a non-empty title."))
            code_mass = option.get("code_mass_effect")
            if code_mass == "UNKNOWN":
                pass
            elif not isinstance(code_mass, dict):
                errors.append(
                    _error(
                        "code_mass_effect",
                        f"{path}.code_mass_effect",
                        "Each option needs an expected maintained-code effect.",
                    )
                )
            else:
                for field in ("added", "removed"):
                    value = code_mass.get(field)
                    if type(value) is not int or value < 0:
                        errors.append(
                            _error(
                                "code_mass_effect",
                                f"{path}.code_mass_effect.{field}",
                                "Expected a non-negative integer SLOC estimate.",
                            )
                        )
                added = code_mass.get("added")
                removed = code_mass.get("removed")
                expected_net = code_mass.get("expected_net")
                if (
                    type(added) is int
                    and type(removed) is int
                    and expected_net != added - removed
                ):
                    errors.append(
                        _error(
                            "code_mass_effect",
                            f"{path}.code_mass_effect.expected_net",
                            "Expected net must equal added minus removed maintained SLOC.",
                        )
                    )
                ratio = code_mass.get("expected_ratio")
                if type(added) is int and type(removed) is int:
                    if added == 0 and ratio is not None:
                        errors.append(
                            _error(
                                "code_mass_effect",
                                f"{path}.code_mass_effect.expected_ratio",
                                "Expected ratio is null when no maintained SLOC is added.",
                            )
                        )
                    elif added > 0 and (
                        not isinstance(ratio, (int, float))
                        or isinstance(ratio, bool)
                        or abs(float(ratio) - removed / added) > 0.001
                    ):
                        errors.append(
                            _error(
                                "code_mass_effect",
                                f"{path}.code_mass_effect.expected_ratio",
                                "Expected ratio must describe removed divided by added maintained SLOC.",
                            )
                        )
            _strings(option.get("consequences"), f"{path}.consequences", errors, minimum=1)

    recommendation = _record(decision.get("recommendation"), "$.decision.recommendation", errors) if version == 2 or "recommendation" in decision else None
    if recommendation is not None:
        _validate_recommendation(recommendation, option_ids, errors)

    grounding = _record(decision.get("grounding_status"), "$.decision.grounding_status", errors)
    for field in ("explicit_rationale_found", "grounding_recommended"):
        if type(grounding.get(field)) is not bool:
            errors.append(_error("boolean", f"$.decision.grounding_status.{field}", "Expected a boolean."))
    if not _nonempty(grounding.get("target")):
        errors.append(_error("grounding_target", "$.decision.grounding_status.target", "Expected a grounding target."))

    actions = _strings(decision.get("actions"), "$.decision.actions", errors, minimum=2 if version == 3 else 4)
    expected_actions = {"answer", "ground_me"} if version == 3 else set(option_ids) | {"custom_answer", "ground_me"}
    if set(actions) != expected_actions:
        errors.append(_error("decision_actions", "$.decision.actions", "Offer an open answer and Ground Me." if version == 3 else "Actions must be every option plus custom_answer and ground_me."))
    return errors


def _validate_recommendation(recommendation, option_ids, errors):
    if recommendation.get("option") not in option_ids:
        errors.append(_error("recommendation_option", "$.decision.recommendation.option", "Recommend one declared option."))
    if recommendation.get("confidence") not in CONFIDENCE:
        errors.append(_error("recommendation_confidence", "$.decision.recommendation.confidence", "Expected low, medium, or high."))
    criteria = recommendation.get("criteria")
    if not isinstance(criteria, dict):
        errors.append(
            _error(
                "recommendation_criterion",
                "$.decision.recommendation.criteria",
                "The recommendation must account for every required tradeoff.",
            )
        )
    else:
        for criterion in RECOMMENDATION_CRITERIA:
            if not _nonempty(criteria.get(criterion)):
                errors.append(
                    _error(
                        "recommendation_criterion",
                        f"$.decision.recommendation.criteria.{criterion}",
                        "Expected a concise consequence-based assessment.",
                    )
                )

def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate one decision-frontier question.")
    parser.add_argument("question", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    payload, errors, read_code = _load(arguments.question)
    if payload is not None:
        errors.extend(_validate(payload))
    exit_code = read_code if read_code == 2 else (1 if errors else 0)
    result = {
        "status": "ok" if not errors else ("error" if exit_code == 2 else "invalid"),
        "question": str(arguments.question),
        "errors": errors,
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        for item in errors:
            print(f"{item['code']}: {item['path']}: {item['message']}", file=sys.stderr)
    else:
        print(f"valid: {arguments.question}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
