#!/usr/bin/env python3
"""Validate a Grounding Packet and its decision-return invariant."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Sequence

from specflow_runtime.visuals import validate_visuals
from specflow_runtime.client import RuntimeFailure


KIND = "epic-spec.grounding-packet"
GROUNDING_ID = re.compile(r"^GRD-.+-[0-9]{3}$")
CLASSIFICATIONS = {
    "INTENTIONAL_AND_CURRENT",
    "INTENTIONAL_BUT_POSSIBLY_OBSOLETE",
    "INTENTIONAL_BUT_OBSOLETE",
    "TEMPORARY_WORKAROUND",
    "CONSTRAINT_DERIVED",
    "EMERGENT_OR_INCREMENTAL",
    "ACCIDENTAL",
    "POST_HOC_DOCUMENTED",
    "CONFLICTED",
    "UNKNOWN",
}
CONFIDENCE = {"EXPLICIT", "CORROBORATED", "INFERRED", "CONFLICTED", "UNKNOWN"}
DELETION_RECOMMENDATIONS = {
    "SAFE",
    "SAFE_WITH_REPLACEMENT",
    "REQUIRES_GROUNDING",
    "BLOCKED_BY_CURRENT_CONSTRAINT",
    "BEHAVIOR_STILL_REQUIRED",
    "UNKNOWN",
}


def _error(code: str, path: str, message: str) -> dict[str, str]:
    return {"code": code, "path": path, "message": message}


def _nonempty(value: object) -> bool:
    return isinstance(value, str) and bool(value.strip())


def _load(path: Path) -> tuple[dict[str, Any] | None, list[dict[str, str]], int]:
    try:
        with path.open("r", encoding="utf-8") as stream:
            payload = json.load(stream)
    except FileNotFoundError:
        return None, [_error("file_not_found", str(path), "The packet file does not exist.")], 2
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
            errors.append(_error("string_item", f"{path}[{index}]", "Expected a non-empty string."))


def _object(value: object, path: str, errors: list[dict[str, str]]) -> dict[str, Any]:
    if isinstance(value, dict):
        return value
    errors.append(_error("object", path, "Expected an object."))
    return {}


def _required_strings(
    value: dict[str, Any], path: str, fields: tuple[str, ...], errors: list[dict[str, str]]
) -> None:
    for field in fields:
        if not _nonempty(value.get(field)):
            errors.append(_error("required_string", f"{path}.{field}", "Expected a non-empty string."))


def _record_list(
    value: object,
    path: str,
    fields: tuple[str, ...],
    errors: list[dict[str, str]],
    *,
    minimum: int = 0,
) -> list[dict[str, Any]]:
    if not isinstance(value, list):
        errors.append(_error("record_list", path, "Expected an array of objects."))
        return []
    if len(value) < minimum:
        errors.append(_error("minimum_items", path, f"Expected at least {minimum} item(s)."))
    records: list[dict[str, Any]] = []
    for index, item in enumerate(value):
        item_path = f"{path}[{index}]"
        if not isinstance(item, dict):
            errors.append(_error("record", item_path, "Expected an object."))
            continue
        _required_strings(item, item_path, fields, errors)
        records.append(item)
    return records


def _validate(
    payload: dict[str, Any], *, require_aligned_understanding: bool
) -> list[dict[str, str]]:
    errors: list[dict[str, str]] = []
    if payload.get("schema_version") != 2:
        errors.append(_error("schema_version", "$.schema_version", "Expected schema version 2."))
    if payload.get("kind") != KIND:
        errors.append(_error("document_kind", "$.kind", f"Expected {KIND}."))
    grounding_id = payload.get("grounding_id")
    if not _nonempty(grounding_id) or GROUNDING_ID.fullmatch(str(grounding_id)) is None:
        errors.append(
            _error(
                "grounding_id",
                "$.grounding_id",
                "Expected a GRD identifier ending in three digits.",
            )
        )
    mode = payload.get("mode")
    if mode not in {"integrated", "standalone"}:
        errors.append(_error("mode", "$.mode", "Expected integrated or standalone."))
    triggering = payload.get("triggering_decision")
    basis_ref = payload.get("basis_ref")
    if mode == "integrated":
        if not _nonempty(triggering):
            errors.append(
                _error(
                    "triggering_decision",
                    "$.triggering_decision",
                    "Integrated grounding requires the unresolved decision ID.",
                )
            )
        if not _nonempty(basis_ref):
            errors.append(
                _error("basis_ref", "$.basis_ref", "Integrated grounding requires a basis reference.")
            )
    elif mode == "standalone" and triggering is not None:
        errors.append(
            _error(
                "standalone_trigger",
                "$.triggering_decision",
                "Standalone grounding does not claim a triggering decision.",
            )
        )

    target = _object(payload.get("target"), "$.target", errors)
    _required_strings(target, "$.target", ("type", "identifier"), errors)
    visual_requirement = target.get("visual_requirement")
    if visual_requirement not in {"none", "architecture", "interaction"}:
        errors.append(
            _error(
                "visual_requirement",
                "$.target.visual_requirement",
                "Expected none, architecture, or interaction.",
            )
        )

    current = _object(payload.get("current_state"), "$.current_state", errors)
    _required_strings(current, "$.current_state", ("summary",), errors)
    for field in ("symbols", "tests", "contracts", "consumers", "dependencies", "affected_surfaces"):
        _string_list(current.get(field), f"$.current_state.{field}", errors)

    coverage = _object(payload.get("source_coverage"), "$.source_coverage", errors)
    issue_fields = [field for field in ("issues", "linear") if field in coverage] or ["issues"]
    for field in ("current_state", "git", "pull_request", *issue_fields, "semantic", "external"):
        entry = _object(coverage.get(field), f"$.source_coverage.{field}", errors)
        status = entry.get("status")
        if status not in {"found", "searched_not_found", "unavailable", "not_applicable"}:
            errors.append(_error("source_coverage_status", f"$.source_coverage.{field}.status", "Expected found, searched_not_found, unavailable, or not_applicable."))
        refs = entry.get("refs")
        _string_list(refs, f"$.source_coverage.{field}.refs", errors)
        if status == "found" and (not isinstance(refs, list) or not refs):
            errors.append(_error("source_coverage_refs", f"$.source_coverage.{field}.refs", "Found coverage requires at least one source reference."))

    _record_list(
        payload.get("decision_lineage"),
        "$.decision_lineage",
        ("source_type", "source_ref", "relationship"),
        errors,
        minimum=1,
    )
    _string_list(payload.get("explicit_rationale"), "$.explicit_rationale", errors)
    _string_list(payload.get("inferred_rationale"), "$.inferred_rationale", errors)
    constraints = _object(payload.get("constraints"), "$.constraints", errors)
    for field in ("current", "expired", "uncertain"):
        _string_list(constraints.get(field), f"$.constraints.{field}", errors)
    _string_list(payload.get("contradictions"), "$.contradictions", errors)

    if payload.get("classification") not in CLASSIFICATIONS:
        errors.append(_error("classification", "$.classification", "Expected a supported classification."))
    if payload.get("confidence") not in CONFIDENCE:
        errors.append(_error("confidence", "$.confidence", "Expected a supported confidence level."))
    if payload.get("classification") == "CONFLICTED" and payload.get("confidence") != "CONFLICTED":
        errors.append(
            _error(
                "conflict_confidence",
                "$.confidence",
                "Conflicted provenance requires conflicted confidence.",
            )
        )
    if payload.get("confidence") == "UNKNOWN" and (
        payload.get("explicit_rationale") or payload.get("inferred_rationale")
    ):
        errors.append(
            _error(
                "unknown_with_rationale",
                "$.confidence",
                "Unknown confidence cannot claim an established rationale.",
            )
        )
    if payload.get("classification") == "INTENTIONAL_BUT_POSSIBLY_OBSOLETE" and not (
        constraints.get("expired") or constraints.get("uncertain")
    ):
        errors.append(
            _error(
                "obsolete_without_constraint",
                "$.constraints",
                "Possibly obsolete provenance requires an expired or uncertain force.",
            )
        )

    timeline = _record_list(
        payload.get("timeline"),
        "$.timeline",
        ("observed_at", "event"),
        errors,
        minimum=1,
    )
    for index, item in enumerate(timeline):
        _string_list(item.get("source_refs"), f"$.timeline[{index}].source_refs", errors, minimum=1)
    visuals = _record_list(payload.get("visuals"), "$.visuals", ("type", "ref"), errors)
    try:
        validate_visuals(payload.get("visuals"))
    except RuntimeFailure as error:
        errors.append(_error(error.code, "$.visuals", str(error)))
    visual_types = {
        str(item.get("type"))
        for item in visuals
        if _nonempty(item.get("type"))
    }
    if visual_requirement == "architecture" and not any(
        item.get("kind") == "graph" and item.get("renderer") in {"likec4", "figma", "archify"}
        for item in visuals
    ):
        errors.append(
            _error(
                "architecture_visual",
                "$.visuals",
                "Architecture grounding requires a Figma, LikeC4, or Archify graph.",
            )
        )
    if visual_requirement == "interaction" and not any(
        visual_type.startswith("figma") for visual_type in visual_types
    ):
        errors.append(
            _error(
                "interaction_visual",
                "$.visuals",
                "Interaction grounding requires a Figma visual.",
            )
        )
    excerpts = _record_list(
        payload.get("source_excerpts"),
        "$.source_excerpts",
        ("source_ref", "excerpt", "evidence_level"),
        errors,
        minimum=1,
    )
    for index, item in enumerate(excerpts):
        if item.get("evidence_level") not in CONFIDENCE:
            errors.append(
                _error(
                    "evidence_level",
                    f"$.source_excerpts[{index}].evidence_level",
                    "Expected a supported evidence level.",
                )
            )
    _string_list(payload.get("decision_implications"), "$.decision_implications", errors)
    _string_list(payload.get("revised_options"), "$.revised_options", errors)

    deletion_credit: dict[str, Any] = {}
    deletion_safety_value = payload.get("deletion_safety")
    if target.get("type") == "deletion_candidate":
        deletion_safety = _object(
            deletion_safety_value, "$.deletion_safety", errors
        )
        introduced_by = _object(
            deletion_safety.get("introduced_by"),
            "$.deletion_safety.introduced_by",
            errors,
        )
        introduction_refs = []
        for field in ("commit", "pull_request", "issue", "linear_issue"):
            value = introduced_by.get(field)
            if value is not None and not _nonempty(value):
                errors.append(
                    _error(
                        "deletion_introduction",
                        f"$.deletion_safety.introduced_by.{field}",
                        "Expected null or a non-empty source reference.",
                    )
                )
            elif _nonempty(value):
                introduction_refs.append(str(value))
        if not introduction_refs:
            errors.append(
                _error(
                    "deletion_introduction",
                    "$.deletion_safety.introduced_by",
                    "Deletion grounding needs at least one introduction source.",
                )
            )

        original_reason = _object(
            deletion_safety.get("original_reason"),
            "$.deletion_safety.original_reason",
            errors,
        )
        _required_strings(
            original_reason,
            "$.deletion_safety.original_reason",
            ("statement",),
            errors,
        )
        original_constraint = _object(
            deletion_safety.get("original_constraint"),
            "$.deletion_safety.original_constraint",
            errors,
        )
        if original_constraint.get("status") not in {
            "CURRENT",
            "EXPIRED",
            "UNCERTAIN",
            "UNKNOWN",
        }:
            errors.append(
                _error(
                    "original_constraint_status",
                    "$.deletion_safety.original_constraint.status",
                    "Expected CURRENT, EXPIRED, UNCERTAIN, or UNKNOWN.",
                )
            )
        _required_strings(
            original_constraint,
            "$.deletion_safety.original_constraint",
            ("statement",),
            errors,
        )

        replacement = _object(
            deletion_safety.get("current_replacement"),
            "$.deletion_safety.current_replacement",
            errors,
        )
        replacement_symbol = replacement.get("symbol")
        if replacement_symbol is not None and not _nonempty(replacement_symbol):
            errors.append(
                _error(
                    "replacement_symbol",
                    "$.deletion_safety.current_replacement.symbol",
                    "Expected null or a non-empty symbol.",
                )
            )
        _string_list(
            replacement.get("verified_by"),
            "$.deletion_safety.current_replacement.verified_by",
            errors,
        )
        recommendation = deletion_safety.get("deletion_recommendation")
        if recommendation not in DELETION_RECOMMENDATIONS:
            errors.append(
                _error(
                    "deletion_recommendation",
                    "$.deletion_safety.deletion_recommendation",
                    "Expected a supported deletion-safety state.",
                )
            )
        if recommendation == "SAFE_WITH_REPLACEMENT" and (
            not _nonempty(replacement_symbol) or not replacement.get("verified_by")
        ):
            errors.append(
                _error(
                    "replacement_verification",
                    "$.deletion_safety.current_replacement",
                    "SAFE_WITH_REPLACEMENT needs a named, behaviorally verified replacement.",
                )
            )
        _string_list(
            deletion_safety.get("required_verification"),
            "$.deletion_safety.required_verification",
            errors,
            minimum=1,
        )
        deletion_credit = _object(
            deletion_safety.get("removal_credit"),
            "$.deletion_safety.removal_credit",
            errors,
        )
        if deletion_credit.get("status") not in {
            "PROVISIONAL",
            "VALIDATED",
            "REJECTED",
        }:
            errors.append(
                _error(
                    "removal_credit_status",
                    "$.deletion_safety.removal_credit.status",
                    "Expected PROVISIONAL, VALIDATED, or REJECTED.",
                )
            )
        if deletion_credit.get("status") == "VALIDATED" and recommendation not in {
            "SAFE",
            "SAFE_WITH_REPLACEMENT",
        }:
            errors.append(
                _error(
                    "removal_credit_safety",
                    "$.deletion_safety.removal_credit.status",
                    "Only safe or verified replacement removals receive validated credit.",
                )
            )
    elif deletion_safety_value is not None:
        errors.append(
            _error(
                "unexpected_deletion_safety",
                "$.deletion_safety",
                "Deletion-safety evidence applies only to a deletion_candidate target.",
            )
        )

    understanding = _object(payload.get("understanding"), "$.understanding", errors)
    understanding_status = understanding.get("status")
    if understanding_status not in {"pending", "confirmed", "corrected", "ground_deeper"}:
        errors.append(_error("understanding_status", "$.understanding.status", "Expected a supported status."))
    confirmed_by = understanding.get("confirmed_by")
    if understanding_status in {"confirmed", "corrected"} and not _nonempty(confirmed_by):
        errors.append(
            _error(
                "understanding_confirmation",
                "$.understanding.confirmed_by",
                "Confirmed or corrected understanding requires the human identity.",
            )
        )
    if understanding_status in {"pending", "ground_deeper"} and confirmed_by is not None:
        errors.append(
            _error(
                "premature_confirmation",
                "$.understanding.confirmed_by",
                "Pending or deeper grounding cannot claim confirmation.",
            )
        )
    if require_aligned_understanding and understanding_status not in {"confirmed", "corrected"}:
        errors.append(
            _error(
                "understanding_alignment_required",
                "$.understanding.status",
                "Confirm or correct the reconstructed understanding before returning.",
            )
        )
    if deletion_credit.get("status") == "VALIDATED":
        if understanding_status not in {"confirmed", "corrected"} or not _nonempty(
            deletion_credit.get("confirmed_by")
        ):
            errors.append(
                _error(
                    "removal_credit_confirmation",
                    "$.deletion_safety.removal_credit",
                    "Validated removal credit requires confirmed or corrected human understanding.",
                )
            )

    outcome = _object(payload.get("decision_outcome"), "$.decision_outcome", errors)
    outcome_status = outcome.get("status")
    resume = outcome.get("resume_decision")
    invalidation_reason = outcome.get("invalidation_reason")
    if outcome_status == "unresolved":
        if mode == "integrated" and resume != triggering:
            errors.append(
                _error(
                    "decision_return_invariant",
                    "$.decision_outcome.resume_decision",
                    "Grounding must return to the same unresolved decision.",
                )
            )
        if mode == "standalone" and resume is not None:
            errors.append(
                _error(
                    "standalone_resume",
                    "$.decision_outcome.resume_decision",
                    "Standalone grounding does not resume a framework decision.",
                )
            )
        if invalidation_reason is not None:
            errors.append(
                _error(
                    "unexpected_invalidation_reason",
                    "$.decision_outcome.invalidation_reason",
                    "An unresolved decision has no invalidation reason.",
                )
            )
    elif outcome_status == "question_invalidated":
        if resume is not None:
            errors.append(
                _error(
                    "invalidated_resume",
                    "$.decision_outcome.resume_decision",
                    "An invalidated question returns control for frontier recomputation.",
                )
            )
        if not _nonempty(invalidation_reason):
            errors.append(
                _error(
                    "invalidation_reason",
                    "$.decision_outcome.invalidation_reason",
                    "Question invalidation requires an evidence-grounded reason.",
                )
            )
    else:
        errors.append(
            _error(
                "decision_outcome",
                "$.decision_outcome.status",
                "Expected unresolved or question_invalidated.",
            )
        )

    persistence = _object(payload.get("persistence"), "$.persistence", errors)
    if not _nonempty(persistence.get("normalized_destination")):
        errors.append(
            _error(
                "normalized_destination",
                "$.persistence.normalized_destination",
                "Expected the selected authoritative destination, including repository documentation when that is its chosen home.",
            )
        )
    if persistence.get("raw_workspace_disposition") != "ephemeral":
        errors.append(
            _error(
                "raw_workspace_disposition",
                "$.persistence.raw_workspace_disposition",
                "Raw grounding work must remain ephemeral.",
            )
        )
    repository_artifacts = persistence.get("repository_artifacts")
    if repository_artifacts != []:
        errors.append(
            _error(
                "repository_artifacts",
                "$.persistence.repository_artifacts",
                "Do not persist raw Ground Me artifacts in the implementation repository.",
            )
        )
    return errors


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Validate a Grounding Packet.")
    parser.add_argument("packet", type=Path)
    parser.add_argument("--require-aligned-understanding", action="store_true")
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    payload, errors, read_code = _load(arguments.packet)
    if payload is not None:
        errors.extend(
            _validate(
                payload,
                require_aligned_understanding=arguments.require_aligned_understanding,
            )
        )
    exit_code = read_code if read_code == 2 else (1 if errors else 0)
    result = {
        "status": "ok" if not errors else ("error" if exit_code == 2 else "invalid"),
        "packet": str(arguments.packet),
        "errors": errors,
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        for item in errors:
            print(f"{item['code']}: {item['path']}: {item['message']}", file=sys.stderr)
    else:
        print(f"valid: {arguments.packet}")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())
