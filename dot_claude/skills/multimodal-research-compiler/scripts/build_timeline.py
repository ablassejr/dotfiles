#!/usr/bin/env python3
"""Build a deterministic evidence timeline from explicit dated records."""

from __future__ import annotations

import argparse
import sys
from datetime import datetime, timezone
from typing import Any

from research_compiler_lib import emit_failure, read_json, stable_id, validation_issue, write_json


def parse_time(value: str) -> float:
    normalized = value.strip().replace("Z", "+00:00")
    parsed = datetime.fromisoformat(normalized)
    if parsed.tzinfo is None:
        parsed = parsed.replace(tzinfo=timezone.utc)
    return parsed.timestamp()


def build(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ValueError("Timeline input must be an object")
    events: list[dict[str, Any]] = []
    errors: list[dict[str, Any]] = []

    candidates: list[tuple[str, dict[str, Any], str, str]] = []
    for event in document.get("events", []):
        if not isinstance(event, dict):
            raise ValueError("events must contain objects")
        candidates.append(("EVENT", event, str(event.get("event_at") or event.get("occurred_at") or event.get("timestamp") or event.get("date") or ""), str(event.get("label") or event.get("statement") or event.get("title") or "")))
    for source in document.get("sources", []):
        if not isinstance(source, dict):
            raise ValueError("sources must contain objects")
        at = str(source.get("event_at") or source.get("published_at") or "")
        if at:
            candidates.append(("SOURCE", source, at, str(source.get("title") or source.get("source_id") or "")))
    for claim in document.get("claims", []):
        if not isinstance(claim, dict):
            raise ValueError("claims must contain objects")
        at = str(claim.get("occurred_at") or claim.get("introduced_at") or "")
        if at:
            candidates.append(("CLAIM", claim, at, str(claim.get("statement") or claim.get("claim_id") or "")))

    for kind, raw, at, label in candidates:
        if not at or not label:
            errors.append(validation_issue("INCOMPLETE_TIMELINE_EVENT", "Timeline event requires a date and label", kind=kind))
            continue
        try:
            sort_time = parse_time(at)
        except ValueError:
            errors.append(validation_issue("INVALID_EVENT_TIME", "Timeline event has an invalid ISO date or date-time", kind=kind, at=at, label=label))
            continue
        event: dict[str, Any] = {
            "at": at,
            "kind": kind,
            "label": label,
            "sort_time": sort_time,
        }
        if raw.get("source_id"):
            event["source_ref"] = raw["source_id"]
        if raw.get("claim_id"):
            event["claim_ref"] = raw["claim_id"]
        if raw.get("confidence"):
            event["confidence"] = raw["confidence"]
        event["event_id"] = str(raw.get("event_id", "")).strip() or stable_id("EVT", kind, at, label, event.get("source_ref"), event.get("claim_ref"))
        events.append(event)

    events.sort(key=lambda event: (event["sort_time"], event["event_id"]))
    for event in events:
        event.pop("sort_time")
    return {"timeline": {"events": events, "errors": errors}}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a chronologically sorted evidence timeline from explicitly dated JSON records.")
    parser.add_argument("input", help="Input JSON path")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        result = build(read_json(args.input))
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 1 if result["timeline"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
