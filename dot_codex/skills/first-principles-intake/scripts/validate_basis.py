#!/usr/bin/env python3
"""Validate a First-Principles Basis and optional version lineage."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Sequence


KIND = "epic-spec.first-principles-basis"
BASIS_ID = re.compile(r"^FPB-.+-[0-9]{3}$")
ALLOWED_SOURCE_TYPES = {
    "user_request",
    "task_or_ticket_statement",
    "approved_product_goal",
    "explicit_constraint",
}
REQUIRED_QUESTIONS = {
    "desired_state",
    "underlying_problem",
    "irreducible_new_behavior",
    "expected_simplification",
    "invariants",
}
CONDITIONAL_QUESTIONS = {"minimum_sufficient_change", "success_evidence"}


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, str]], int]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError:
        return None, [_error("file_not_found", str(path), "The basis file does not exist.")], 2
    except json.JSONDecodeError as exception:
        return (
            None,
            [
                _error(
                    "invalid_json",
                    str(path),
                    f"JSON parsing failed at line {exception.lineno}, column {exception.colno}.",
                )
            ],
            2,
        )
    except OSError as exception:
        return None, [_error("read_failed", str(path), str(exception))], 2
    if not isinstance(payload, dict):
        return None, [_error("invalid_document", "$", "Expected a JSON object.")], 1
    return payload, [], 0


def _statement_record(
    value: object, path: str, errors: list[dict[str, str]], *, list_field: str | None = None
) -> None:
    if not isinstance(value, dict):
        errors.append(_error("statement_record", path, "Expected an object."))
        return
    if not _nonempty(value.get("statement")):
        errors.append(_error("statement", f"{path}.statement", "Expected a non-empty statement."))
    if list_field is not None:
        _string_list(value.get(list_field), f"{path}.{list_field}", errors)


def _string_list(
    value: object,
    path: str,
    errors: list[dict[str, str]],
    *,
    minimum: int = 0,
) -> None:
    if not isinstance(value, list):
        errors.append(_error("string_list", path, "Expected an array of non-empty strings."))
        return
    if len(value) < minimum:
        errors.append(_error("minimum_items", path, f"Expected at least {minimum} item(s)."))
    for index, item in enumerate(value):
        if not _nonempty(item):
            errors.append(
                _error("string_item", f"{path}[{index}]", "Expected a non-empty string.")
            )


def _identified_statements(
    value: object,
    path: str,
    errors: list[dict[str, str]],
    *,
    minimum: int = 0,
    require_source: bool = False,
) -> None:
    if not isinstance(value, list):
        errors.append(_error("record_list", path, "Expected an array of records."))
        return
    if len(value) < minimum:
        errors.append(_error("minimum_items", path, f"Expected at least {minimum} item(s)."))
    identifiers: set[str] = set()
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(_error("record", item_path, "Expected an object."))
            continue
        identifier = item.get("id")
        if not _nonempty(identifier):
            errors.append(_error("record_id", f"{item_path}.id", "Expected a non-empty ID."))
        elif identifier in identifiers:
            errors.append(_error("duplicate_id", f"{item_path}.id", "The ID is repeated."))
        else:
            identifiers.add(str(identifier))
        if not _nonempty(item.get("statement")):
            errors.append(
                _error("statement", f"{item_path}.statement", "Expected a non-empty statement.")
            )
        if require_source and not _nonempty(item.get("source")):
            errors.append(
                _error("constraint_source", f"{item_path}.source", "Expected a named source.")
            )


def _expected_simplification(
    value: object, path: str, errors: list[dict[str, str]]
) -> None:
    if not isinstance(value, list) or not value:
        errors.append(
            _error(
                "expected_simplification",
                path,
                "Expected at least one conceptual responsibility that becomes unnecessary or simpler.",
            )
        )
        return
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(_error("expected_simplification", item_path, "Expected an object."))
            continue
        if not _nonempty(item.get("responsibility")):
            errors.append(
                _error(
                    "expected_simplification",
                    f"{item_path}.responsibility",
                    "Expected a conceptual responsibility, process, behavior, or concept.",
                )
            )
        if type(item.get("expected_to_disappear")) is not bool:
            errors.append(
                _error(
                    "expected_simplification",
                    f"{item_path}.expected_to_disappear",
                    "Expected a boolean simplification outcome.",
                )
            )


def _validate(payload: dict[str, Any], *, require_approved: bool) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if payload.get("schema_version") != 2:
        errors.append(_error("schema_version", "$.schema_version", "Expected schema version 2."))
    if payload.get("kind") != KIND:
        errors.append(_error("document_kind", "$.kind", f"Expected {KIND}."))
    basis_id = payload.get("basis_id")
    if not _nonempty(basis_id) or BASIS_ID.fullmatch(str(basis_id)) is None:
        errors.append(
            _error("basis_id", "$.basis_id", "Expected an FPB identifier ending in three digits.")
        )
    if not _nonempty(payload.get("task_ref")):
        errors.append(_error("task_ref", "$.task_ref", "Expected a non-empty task reference."))
    version = payload.get("version")
    if type(version) is not int or version < 1:
        errors.append(_error("version", "$.version", "Expected a positive integer version."))
    supersedes = payload.get("supersedes_basis_id")
    if supersedes is not None and not _nonempty(supersedes):
        errors.append(
            _error(
                "supersedes_basis_id",
                "$.supersedes_basis_id",
                "Expected null or a non-empty prior basis ID.",
            )
        )
    if version == 1 and supersedes is not None:
        errors.append(
            _error(
                "initial_supersedes",
                "$.supersedes_basis_id",
                "The initial basis does not supersede another version.",
            )
        )

    provenance = payload.get("intake_provenance")
    if not isinstance(provenance, dict):
        errors.append(_error("intake_provenance", "$.intake_provenance", "Expected an object."))
    else:
        if provenance.get("context_isolation") not in {"fresh", "restricted"}:
            errors.append(_error("context_isolation", "$.intake_provenance.context_isolation", "Expected fresh or restricted."))
        if provenance.get("implementation_context_exposed") is not False:
            errors.append(_error("implementation_context_exposed", "$.intake_provenance.implementation_context_exposed", "Implementation context must not be exposed during intake."))
        sources = provenance.get("sources")
        if not isinstance(sources, list) or not sources:
            errors.append(_error("intake_sources", "$.intake_provenance.sources", "Expected at least one allowed source."))
        else:
            for index, source in enumerate(sources):
                path = f"$.intake_provenance.sources[{index}]"
                if not isinstance(source, dict):
                    errors.append(_error("intake_source", path, "Expected an object."))
                    continue
                if source.get("type") not in ALLOWED_SOURCE_TYPES:
                    errors.append(_error("prohibited_intake_source", f"{path}.type", "The source is not allowed before basis approval."))
                if not _nonempty(source.get("ref")):
                    errors.append(_error("intake_source_ref", f"{path}.ref", "Expected a non-empty source reference."))
        question_resolution = provenance.get("question_resolution")
        if not isinstance(question_resolution, dict):
            errors.append(_error("question_resolution", "$.intake_provenance.question_resolution", "Expected an object."))
        else:
            for question in REQUIRED_QUESTIONS:
                if question_resolution.get(question) not in {"inferred_from_allowed_input", "asked_and_answered"}:
                    errors.append(_error("required_question_resolution", f"$.intake_provenance.question_resolution.{question}", "Expected inferred_from_allowed_input or asked_and_answered."))
            for question in CONDITIONAL_QUESTIONS:
                if question_resolution.get(question) not in {"inferred_from_allowed_input", "asked_and_answered", "not_needed"}:
                    errors.append(_error("conditional_question_resolution", f"$.intake_provenance.question_resolution.{question}", "Expected inferred_from_allowed_input, asked_and_answered, or not_needed."))
        for field in ("agent_solution_proposals", "agent_introduced_implementation_terms"):
            if provenance.get(field) != []:
                errors.append(_error("anchored_intake", f"$.intake_provenance.{field}", "The intake must not introduce solutions or implementation terminology."))

    _statement_record(
        payload.get("desired_state"),
        "$.desired_state",
        errors,
        list_field="observable_effects",
    )
    _statement_record(
        payload.get("underlying_problem"),
        "$.underlying_problem",
        errors,
        list_field="consequences",
    )
    _string_list(
        payload.get("irreducible_new_behavior"),
        "$.irreducible_new_behavior",
        errors,
        minimum=1,
    )
    _expected_simplification(
        payload.get("expected_simplification"),
        "$.expected_simplification",
        errors,
    )
    _statement_record(payload.get("minimum_sufficient_change"), "$.minimum_sufficient_change", errors)
    _identified_statements(payload.get("invariants"), "$.invariants", errors, minimum=1)
    _identified_statements(
        payload.get("hard_constraints"),
        "$.hard_constraints",
        errors,
        require_source=True,
    )
    _string_list(payload.get("non_goals"), "$.non_goals", errors)
    _string_list(payload.get("forbidden_tradeoffs"), "$.forbidden_tradeoffs", errors)
    _string_list(payload.get("success_evidence"), "$.success_evidence", errors, minimum=1)
    _string_list(payload.get("assumptions"), "$.assumptions", errors)
    _string_list(payload.get("unresolved"), "$.unresolved", errors)

    approved_by = payload.get("approved_by")
    approved_at = payload.get("approved_at")
    if (approved_by is None) != (approved_at is None):
        errors.append(
            _error(
                "partial_approval",
                "$.approved_by",
                "Approval identity and timestamp must be present together.",
            )
        )
    for field, value in (("approved_by", approved_by), ("approved_at", approved_at)):
        if value is not None and not _nonempty(value):
            errors.append(_error("approval", f"$.{field}", "Expected null or a non-empty string."))
    if require_approved and not (_nonempty(approved_by) and _nonempty(approved_at)):
        errors.append(
            _error(
                "approval_required",
                "$.approved_by",
                "Explicit human approval is required before context loading.",
            )
        )
    return errors


def _validate_lineage(
    current: dict[str, Any], previous: dict[str, Any]
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if current.get("task_ref") != previous.get("task_ref"):
        errors.append(
            _error("task_ref_changed", "$.task_ref", "A successor must keep the same task reference.")
        )
    current_version = current.get("version")
    previous_version = previous.get("version")
    if type(current_version) is int and type(previous_version) is int:
        if current_version != previous_version + 1:
            errors.append(
                _error(
                    "version_sequence",
                    "$.version",
                    "A successor version must increment the prior version by one.",
                )
            )
    if current.get("basis_id") == previous.get("basis_id"):
        errors.append(
            _error("basis_id_reused", "$.basis_id", "A successor must use a new basis ID.")
        )
    if current.get("supersedes_basis_id") != previous.get("basis_id"):
        errors.append(
            _error(
                "supersedes_mismatch",
                "$.supersedes_basis_id",
                "A successor must point to the prior basis ID.",
            )
        )
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a First-Principles Basis.")
    parser.add_argument("basis", type=Path)
    parser.add_argument("--previous", type=Path)
    parser.add_argument("--require-approved", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    payload, errors, read_code = _load(arguments.basis)
    if payload is not None:
        errors.extend(_validate(payload, require_approved=arguments.require_approved))
    if arguments.previous is not None:
        previous, previous_errors, previous_code = _load(arguments.previous)
        read_code = max(read_code, previous_code)
        errors.extend({**item, "path": f"previous:{item['path']}"} for item in previous_errors)
        if payload is not None and previous is not None:
            errors.extend(_validate(previous, require_approved=True))
            errors.extend(_validate_lineage(payload, previous))
    exit_code = read_code if read_code == 2 else (1 if errors else 0)
    result = {
        "status": "ok" if not errors else ("error" if exit_code == 2 else "invalid"),
        "basis": str(arguments.basis),
        "approved": bool(
            payload
            and _nonempty(payload.get("approved_by"))
            and _nonempty(payload.get("approved_at"))
        ),
        "previous": str(arguments.previous) if arguments.previous else None,
        "errors": errors,
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        for item in errors:
            print(f"{item['code']}: {item['path']}: {item['message']}", file=sys.stderr)
    else:
        print(f"valid: {arguments.basis}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
