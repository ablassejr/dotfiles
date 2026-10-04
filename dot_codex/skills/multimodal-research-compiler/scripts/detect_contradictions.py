#!/usr/bin/env python3
"""Detect declared and normalized-value contradictions between claims."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from typing import Any

from research_compiler_lib import canonical_json, emit_failure, extract_list, read_json, stable_id, validation_issue, write_json

MATERIALITY_RANK = {"nonblocking": 0, "material": 1, "blocking": 2}


def pair_key(left: str, right: str) -> tuple[str, str]:
    return tuple(sorted((left, right)))


def detect(document: Any) -> dict[str, Any]:
    claims = extract_list(document, "claims")
    claim_map = {str(claim.get("claim_id", "")).strip(): claim for claim in claims if str(claim.get("claim_id", "")).strip()}
    errors: list[dict[str, Any]] = []
    pairs: dict[tuple[str, str], dict[str, Any]] = {}

    for claim_id, claim in claim_map.items():
        for other_id in claim.get("contradicts", []):
            if other_id not in claim_map:
                errors.append(validation_issue("UNKNOWN_CONTRADICTED_CLAIM", "Declared contradiction references an unknown claim", claim_id=claim_id, contradicted_claim=other_id))
                continue
            key = pair_key(claim_id, other_id)
            pairs[key] = {"claims": list(key), "detection": "DECLARED"}

    value_groups: dict[tuple[str, str], list[dict[str, Any]]] = defaultdict(list)
    for claim in claims:
        claim_key = str(claim.get("claim_key", "")).strip()
        if claim_key and "normalized_value" in claim:
            value_groups[(claim_key, canonical_json(claim.get("scope", {})))].append(claim)
    for (claim_key, _scope), group in value_groups.items():
        by_value: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for claim in group:
            by_value[canonical_json(claim["normalized_value"])].append(claim)
        values = sorted(by_value)
        for left_index, left_value in enumerate(values):
            for right_value in values[left_index + 1 :]:
                for left_claim in by_value[left_value]:
                    for right_claim in by_value[right_value]:
                        left_id = str(left_claim.get("claim_id", "")).strip()
                        right_id = str(right_claim.get("claim_id", "")).strip()
                        if not left_id or not right_id:
                            continue
                        key = pair_key(left_id, right_id)
                        pairs.setdefault(
                            key,
                            {
                                "claims": list(key),
                                "detection": "VALUE_CONFLICT",
                                "claim_key": claim_key,
                                "values": [left_claim["normalized_value"], right_claim["normalized_value"]],
                            },
                        )

    contradictions: list[dict[str, Any]] = []
    for key, contradiction in pairs.items():
        materiality = max(
            (claim_map[claim_id].get("materiality", "material") for claim_id in key),
            key=lambda value: MATERIALITY_RANK.get(value, 1),
        )
        contradiction["contradiction_id"] = stable_id("CON", key)
        contradiction["materiality"] = materiality
        contradiction["status"] = "OPEN"
        contradictions.append(contradiction)

    return {
        "contradiction_result": {
            "contradictions": sorted(contradictions, key=lambda item: item["contradiction_id"]),
            "errors": sorted(errors, key=lambda item: (item["code"], str(item.get("claim_id", "")))),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Detect declared and same-scope normalized-value contradictions in claim JSON.")
    parser.add_argument("claims", help="JSON document containing claims")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        result = detect(read_json(args.claims))
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 1 if result["contradiction_result"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
