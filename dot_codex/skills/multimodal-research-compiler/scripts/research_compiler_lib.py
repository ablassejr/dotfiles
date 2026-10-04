#!/usr/bin/env python3
"""Shared JSON and validation utilities for the research compiler scripts."""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path
from typing import Any, Iterable

EVIDENCE_TYPES = {
    "EXPLICIT",
    "CORROBORATED",
    "STRUCTURALLY_DERIVED",
    "CHRONOLOGICALLY_INFERRED",
    "BEHAVIORALLY_INFERRED",
    "CONFLICTED",
    "UNKNOWN",
}
CLAIM_STATUSES = {"supported", "inferred", "conflicted", "unresolved", "rejected"}
CONFIDENCE_LEVELS = {"single_source", "corroborated", "conflicted", "unknown"}
BLOCKING_FINDING_TYPES = {
    "EVIDENCE_BLOCKER",
    "CONTRADICTION_BLOCKER",
    "SCOPE_BLOCKER",
    "FIRST_PRINCIPLES_CONFLICT",
    "HITL_DECISION_REQUIRED",
    "OUTPUT_REVISION_REQUIRED",
}


def read_json(path: str) -> Any:
    text = sys.stdin.read() if path == "-" else Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(text)
    except json.JSONDecodeError as exc:
        raise ValueError(f"Invalid JSON in {path}: {exc.msg} at line {exc.lineno}, column {exc.colno}") from exc


def write_json(value: Any, path: str) -> None:
    rendered = json.dumps(value, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if path == "-":
        sys.stdout.write(rendered)
    else:
        Path(path).write_text(rendered, encoding="utf-8")


def canonical_json(value: Any) -> str:
    return json.dumps(value, ensure_ascii=False, separators=(",", ":"), sort_keys=True)


def digest(value: Any) -> str:
    return hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def stable_id(prefix: str, *parts: Any) -> str:
    return f"{prefix}-{digest(list(parts))[:12].upper()}"


def unwrap(value: Any, key: str) -> Any:
    if isinstance(value, dict) and key in value:
        return value[key]
    return value


def extract_list(value: Any, *keys: str) -> list[dict[str, Any]]:
    if isinstance(value, list):
        items = value
    elif isinstance(value, dict):
        items = None
        for key in keys:
            candidate = value.get(key)
            if isinstance(candidate, list):
                items = candidate
                break
        if items is None:
            raise ValueError(f"Expected a JSON array or one of these array fields: {', '.join(keys)}")
    else:
        raise ValueError("Expected a JSON array or object")
    if not all(isinstance(item, dict) for item in items):
        raise ValueError("Every array item must be a JSON object")
    return list(items)


def unique_strings(values: Iterable[Any]) -> list[str]:
    return sorted({str(value).strip() for value in values if str(value).strip()})


def validation_issue(code: str, message: str, **context: Any) -> dict[str, Any]:
    issue = {"code": code, "message": message}
    issue.update({key: value for key, value in context.items() if value is not None})
    return issue


def validate_claim_records(
    claims: list[dict[str, Any]], source_ids: set[str] | None = None
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    errors: list[dict[str, Any]] = []
    warnings: list[dict[str, Any]] = []
    seen: set[str] = set()

    for index, claim in enumerate(claims):
        claim_id = str(claim.get("claim_id", "")).strip()
        if not claim_id:
            errors.append(validation_issue("MISSING_CLAIM_ID", "Claim has no claim_id", index=index))
            continue
        if claim_id in seen:
            errors.append(validation_issue("DUPLICATE_CLAIM_ID", "claim_id is not unique", claim_id=claim_id))
        seen.add(claim_id)

        if not str(claim.get("statement", "")).strip():
            errors.append(validation_issue("MISSING_STATEMENT", "Claim has no statement", claim_id=claim_id))
        if not str(claim.get("claim_type", "")).strip():
            errors.append(validation_issue("MISSING_CLAIM_TYPE", "Claim has no claim_type", claim_id=claim_id))

        status = claim.get("status")
        if status not in CLAIM_STATUSES:
            errors.append(validation_issue("INVALID_CLAIM_STATUS", "Claim status is not recognized", claim_id=claim_id, status=status))
        confidence = claim.get("confidence")
        if confidence not in CONFIDENCE_LEVELS:
            errors.append(validation_issue("INVALID_CONFIDENCE", "Claim confidence is not recognized", claim_id=claim_id, confidence=confidence))

        support = claim.get("support", [])
        if not isinstance(support, list):
            errors.append(validation_issue("INVALID_SUPPORT", "Claim support must be an array", claim_id=claim_id))
            support = []
        if status in {"supported", "inferred"} and not support:
            errors.append(validation_issue("UNSUPPORTED_CLAIM", "Supported or inferred claim has no evidence link", claim_id=claim_id))

        distinct_sources: set[str] = set()
        usable_evidence = 0
        for support_index, link in enumerate(support):
            if not isinstance(link, dict):
                errors.append(validation_issue("INVALID_EVIDENCE_LINK", "Evidence link must be an object", claim_id=claim_id, index=support_index))
                continue
            source_ref = str(link.get("source_ref", "")).strip()
            evidence_type = link.get("evidence_type")
            if not source_ref:
                errors.append(validation_issue("MISSING_SOURCE_REF", "Evidence link has no source_ref", claim_id=claim_id, index=support_index))
            else:
                distinct_sources.add(source_ref)
                if source_ids is not None and source_ref not in source_ids:
                    errors.append(validation_issue("UNKNOWN_SOURCE_REF", "Evidence link references an unknown source", claim_id=claim_id, source_ref=source_ref))
            if evidence_type not in EVIDENCE_TYPES:
                errors.append(validation_issue("INVALID_EVIDENCE_TYPE", "Evidence classification is not recognized", claim_id=claim_id, evidence_type=evidence_type))
            elif evidence_type not in {"UNKNOWN", "CONFLICTED"}:
                usable_evidence += 1

        if status == "supported" and support and usable_evidence == 0:
            errors.append(validation_issue("NO_USABLE_SUPPORT", "Supported claim contains only unknown or conflicted evidence", claim_id=claim_id))
        if confidence == "corroborated" and len(distinct_sources) < 2:
            errors.append(validation_issue("INSUFFICIENT_CORROBORATION", "Corroborated confidence requires at least two distinct source references", claim_id=claim_id))
        if status == "conflicted" and not claim.get("contradictions") and not claim.get("contradicts") and not any(
            isinstance(link, dict) and link.get("evidence_type") == "CONFLICTED" for link in support
        ):
            warnings.append(validation_issue("UNLINKED_CONFLICT", "Conflicted claim does not reference the conflict", claim_id=claim_id))

    return errors, warnings


def open_blocking_types(review: dict[str, Any]) -> set[str]:
    findings = review.get("findings", []) if isinstance(review, dict) else []
    return {
        str(finding.get("type"))
        for finding in findings
        if isinstance(finding, dict)
        and finding.get("type") in BLOCKING_FINDING_TYPES
        and finding.get("status", "OPEN") not in {"RESOLVED", "ACCEPTED"}
    }


def has_open_blockers(review: dict[str, Any]) -> bool:
    return bool(open_blocking_types(review))


def emit_failure(exc: Exception) -> int:
    sys.stderr.write(json.dumps({"error": {"type": exc.__class__.__name__, "message": str(exc)}}, sort_keys=True) + "\n")
    return 2
