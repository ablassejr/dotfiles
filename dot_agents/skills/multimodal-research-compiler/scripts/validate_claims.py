#!/usr/bin/env python3
"""Validate claim-to-evidence behavior at the JSON contract boundary."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import emit_failure, extract_list, read_json, validate_claim_records, validation_issue, write_json


def validate(claims_document: Any, sources_document: Any | None = None) -> dict[str, Any]:
    claims = extract_list(claims_document, "claims")
    source_ids: set[str] | None = None
    source_errors: list[dict[str, Any]] = []
    if sources_document is not None:
        sources = extract_list(sources_document, "sources")
        source_ids = set()
        for source in sources:
            source_id = str(source.get("source_id", "")).strip()
            if not source_id:
                source_errors.append(validation_issue("MISSING_SOURCE_ID", "Source has no source_id"))
            elif source_id in source_ids:
                source_errors.append(validation_issue("DUPLICATE_SOURCE_ID", "source_id is not unique", source_id=source_id))
            source_ids.add(source_id)
    errors, warnings = validate_claim_records(claims, source_ids)
    errors = source_errors + errors
    return {
        "claim_validation": {
            "valid": not errors,
            "claim_count": len(claims),
            "errors": errors,
            "warnings": warnings,
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate observable claim and evidence invariants.")
    parser.add_argument("claims", help="JSON document containing claims")
    parser.add_argument("--sources", help="Optional JSON document containing the referenced sources")
    parser.add_argument("-o", "--output", default="-", help="Output report path, or - for standard output")
    args = parser.parse_args()
    try:
        result = validate(read_json(args.claims), read_json(args.sources) if args.sources else None)
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0 if result["claim_validation"]["valid"] else 1


if __name__ == "__main__":
    sys.exit(main())
