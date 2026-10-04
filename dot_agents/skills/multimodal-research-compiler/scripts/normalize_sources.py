#!/usr/bin/env python3
"""Normalize and deduplicate research source records."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import canonical_json, emit_failure, extract_list, read_json, stable_id, unique_strings, write_json


def source_key(source: dict[str, Any]) -> tuple[str, str, str, str]:
    version = source.get("version") or source.get("revision") or ""
    return (
        str(source.get("source_type", "")).strip().lower(),
        str(source.get("locator", "")).strip(),
        str(version).strip(),
        canonical_json(source.get("scope", {})),
    )


def normalize(input_value: Any) -> dict[str, Any]:
    sources = extract_list(input_value, "sources")
    normalized: dict[tuple[str, str, str, str], dict[str, Any]] = {}
    duplicates: list[dict[str, str]] = []

    for index, raw in enumerate(sources):
        source = dict(raw)
        key = source_key(source)
        if not key[0] or not key[1]:
            raise ValueError(f"Source at index {index} requires source_type and locator")
        if not str(source.get("title", "")).strip():
            raise ValueError(f"Source at index {index} requires title")
        source_id = str(source.get("source_id", "")).strip() or stable_id("SRC", *key)
        source["source_id"] = source_id
        source["source_type"] = key[0]
        source["locator"] = key[1]
        source["authority_for"] = unique_strings(source.get("authority_for", []))
        if key in normalized:
            retained = normalized[key]
            duplicates.append({"duplicate": source_id, "retained": retained["source_id"]})
            retained["authority_for"] = unique_strings(retained.get("authority_for", []) + source.get("authority_for", []))
            retained["excerpts"] = sorted(
                {
                    canonical_json(excerpt): excerpt
                    for excerpt in retained.get("excerpts", []) + source.get("excerpts", [])
                    if isinstance(excerpt, dict)
                }.values(),
                key=lambda item: (str(item.get("excerpt_id", "")), str(item.get("locator", ""))),
            )
        else:
            normalized[key] = source

    result_sources = sorted(normalized.values(), key=lambda item: item["source_id"])
    return {
        "sources": result_sources,
        "normalization": {
            "duplicates": sorted(duplicates, key=lambda item: (item["retained"], item["duplicate"])),
            "input_count": len(sources),
            "output_count": len(result_sources),
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Normalize and deduplicate research sources as deterministic JSON.")
    parser.add_argument("input", help="Input JSON path, or - for standard input")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        write_json(normalize(read_json(args.input)), args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
