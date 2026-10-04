#!/usr/bin/env python3
"""Validate a Research Packet as a releasable, internally consistent artifact."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import digest, emit_failure, has_open_blockers, read_json, unwrap, validate_claim_records, validation_issue, write_json


def validate(packet_document: Any, session_document: Any | None = None) -> dict[str, Any]:
    packet = unwrap(packet_document, "research_packet")
    if not isinstance(packet, dict):
        raise ValueError("research_packet must be an object")
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []

    for field in ("packet_id", "status", "mode", "question", "direct_answer", "sources", "reviews", "model_digest", "research_model"):
        if field not in packet:
            errors.append(validation_issue("MISSING_PACKET_FIELD", "Research Packet is missing a required field", field=field))

    sources = packet.get("sources", []) if isinstance(packet.get("sources", []), list) else []
    claims = packet.get("claims", []) if isinstance(packet.get("claims", []), list) else []
    source_ids: set[str] = set()
    for index, source in enumerate(sources):
        if not isinstance(source, dict):
            errors.append(validation_issue("INVALID_SOURCE", "Packet source must be an object", index=index))
            continue
        source_id = str(source.get("source_id", "")).strip()
        if not source_id:
            errors.append(validation_issue("MISSING_SOURCE_ID", "Packet source has no source_id", index=index))
        elif source_id in source_ids:
            errors.append(validation_issue("DUPLICATE_SOURCE_ID", "Packet source_id is not unique", source_id=source_id))
        source_ids.add(source_id)
    claim_objects = [claim for claim in claims if isinstance(claim, dict)]
    if len(claim_objects) != len(claims):
        errors.append(validation_issue("INVALID_CLAIM", "Every packet claim must be an object"))
    claim_errors, claim_warnings = validate_claim_records(claim_objects, source_ids)
    errors.extend(claim_errors)
    warnings.extend(claim_warnings)

    question = packet.get("question", {}) if isinstance(packet.get("question"), dict) else {}
    if not str(question.get("id", "")).strip() or not str(question.get("statement", "")).strip():
        errors.append(validation_issue("INVALID_QUESTION", "Packet question requires id and statement"))
    direct_answer = packet.get("direct_answer", {}) if isinstance(packet.get("direct_answer"), dict) else {}
    if not str(direct_answer.get("statement", "")).strip():
        errors.append(validation_issue("MISSING_DIRECT_ANSWER", "Packet direct_answer requires a statement"))
    if direct_answer.get("confidence") not in {"single_source", "corroborated", "conflicted", "unknown"}:
        errors.append(validation_issue("INVALID_DIRECT_ANSWER_CONFIDENCE", "Packet direct_answer confidence is not recognized", confidence=direct_answer.get("confidence")))

    research_model = packet.get("research_model")
    expected_digest = digest(research_model) if isinstance(research_model, dict) else None
    if expected_digest and packet.get("model_digest") != expected_digest:
        errors.append(validation_issue("MODEL_DIGEST_MISMATCH", "Packet model_digest does not match research_model", expected=expected_digest, actual=packet.get("model_digest")))

    if packet.get("status") not in {"REVIEWED", "PUBLISHED"}:
        errors.append(validation_issue("RELEASE_STATUS_INCOMPLETE", "Packet is not in a releasable status", status=packet.get("status")))

    reviews = packet.get("reviews", {}) if isinstance(packet.get("reviews"), dict) else {}
    alignment = reviews.get("first_principles", {}) if isinstance(reviews.get("first_principles"), dict) else {}
    adversarial = reviews.get("adversarial", {}) if isinstance(reviews.get("adversarial"), dict) else {}
    if alignment.get("status") != "ALIGNED":
        errors.append(validation_issue("FIRST_PRINCIPLES_NOT_ALIGNED", "First-principles review has not passed", status=alignment.get("status")))
    if adversarial.get("status") != "PASSED" or has_open_blockers(adversarial):
        errors.append(validation_issue("ADVERSARIAL_REVIEW_NOT_PASSED", "Adversarial review is missing, failed, or has an open blocker", status=adversarial.get("status")))
    if adversarial.get("review_kind") not in {"INDEPENDENT", "SELF_REVIEWED"}:
        errors.append(validation_issue("REVIEW_KIND_MISSING", "Adversarial review must identify whether it was independent or self-reviewed"))

    synthesis = research_model.get("synthesis", {}) if isinstance(research_model, dict) and isinstance(research_model.get("synthesis"), dict) else {}
    if synthesis.get("understanding_required") and reviews.get("human_understanding") != "CONFIRMED":
        errors.append(validation_issue("UNDERSTANDING_NOT_CONFIRMED", "Material grounding requires a separate confirmed understanding checkpoint"))

    for unresolved in packet.get("unresolved", []):
        if isinstance(unresolved, dict) and unresolved.get("materiality", "material") == "blocking":
            errors.append(validation_issue("BLOCKING_UNRESOLVED_ITEM", "A blocking research item remains unresolved", item=unresolved))
    for contradiction in packet.get("contradictions", []):
        if isinstance(contradiction, dict) and contradiction.get("materiality") == "blocking" and contradiction.get("status", "OPEN") not in {"RESOLVED", "BOUNDED"}:
            errors.append(validation_issue("BLOCKING_CONTRADICTION", "A blocking contradiction remains open", contradiction_id=contradiction.get("contradiction_id")))

    views = packet.get("views", {})
    if not isinstance(views, dict):
        errors.append(validation_issue("INVALID_VIEWS", "views must be an object"))
    else:
        for name, view in views.items():
            if not isinstance(view, dict):
                errors.append(validation_issue("UNVERIFIABLE_VIEW", "Published view must include model and verification metadata", view=name))
                continue
            if view.get("model_digest") != packet.get("model_digest"):
                errors.append(validation_issue("VIEW_MODEL_MISMATCH", "View does not reference the packet model digest", view=name))
            verification = view.get("verification", {}) if isinstance(view.get("verification"), dict) else {}
            if verification.get("status") != "PASSED":
                errors.append(validation_issue("VIEW_NOT_VERIFIED", "View read-back verification has not passed", view=name, status=verification.get("status")))

    if session_document is not None:
        session = unwrap(session_document, "research_session")
        if not isinstance(session, dict):
            errors.append(validation_issue("INVALID_SESSION", "research_session must be an object"))
        else:
            if session.get("model_digest") != packet.get("model_digest"):
                errors.append(validation_issue("SESSION_MODEL_MISMATCH", "Session manifest does not reference the packet model digest"))
            if session.get("current_release") and session.get("current_release") != packet.get("packet_id"):
                errors.append(validation_issue("SESSION_RELEASE_MISMATCH", "Session manifest points to a different release", session_release=session.get("current_release"), packet_id=packet.get("packet_id")))

    return {
        "release_validation": {
            "valid": not errors,
            "packet_id": packet.get("packet_id"),
            "model_digest": packet.get("model_digest"),
            "errors": errors,
            "warnings": warnings,
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate a Research Packet and optional session manifest for release.")
    parser.add_argument("packet", help="Research Packet JSON path")
    parser.add_argument("--session", help="Optional Research Session JSON path")
    parser.add_argument("-o", "--output", default="-", help="Output report path, or - for standard output")
    args = parser.parse_args()
    try:
        result = validate(read_json(args.packet), read_json(args.session) if args.session else None)
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0 if result["release_validation"]["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
