#!/usr/bin/env python3
"""Correlate offline Git, GitHub, and Linear records through explicit identifiers."""

from __future__ import annotations

import argparse
import sys
from collections import defaultdict
from typing import Any, Iterable

from research_compiler_lib import emit_failure, read_json, stable_id, unique_strings, write_json


def values(record: dict[str, Any], keys: Iterable[str]) -> list[Any]:
    collected: list[Any] = []
    for key in keys:
        value = record.get(key)
        if value is None:
            continue
        if isinstance(value, list):
            collected.extend(value)
        else:
            collected.append(value)
    return collected


def identifiers(record: dict[str, Any]) -> list[str]:
    commits = [f"commit:{str(value).strip().lower()}" for value in values(record, ("commit", "commit_sha", "sha", "commits", "commit_shas")) if str(value).strip()]
    pull_requests = [f"pr:{str(value).strip().upper().removeprefix('PR-').removeprefix('#')}" for value in values(record, ("pr", "pr_number", "pr_numbers", "pull_request", "pull_requests")) if str(value).strip()]
    issues = [f"issue:{str(value).strip().upper()}" for value in values(record, ("issue", "issue_id", "issue_ids", "linear_issue", "linear_ids")) if str(value).strip()]
    return unique_strings(commits + pull_requests + issues)


def correlate(document: Any) -> dict[str, Any]:
    if not isinstance(document, dict):
        raise ValueError("Input must be an object with git, github, and linear arrays")
    records: dict[str, dict[str, Any]] = {}
    for system in ("git", "github", "linear"):
        system_records = document.get(system, [])
        if not isinstance(system_records, list) or not all(isinstance(item, dict) for item in system_records):
            raise ValueError(f"{system} must be an array of objects")
        for index, raw in enumerate(system_records):
            explicit_id = raw.get("record_id") or raw.get("id") or raw.get("sha") or raw.get("commit_sha") or raw.get("pr_number") or raw.get("issue_id")
            record_id = f"{system}:{explicit_id}" if explicit_id is not None else stable_id(system.upper(), index, raw)
            if record_id in records:
                raise ValueError(f"Duplicate record identity: {record_id}")
            records[record_id] = {"record_id": record_id, "system": system, "identifiers": identifiers(raw), "record": raw}

    parent = {record_id: record_id for record_id in records}

    def find(record_id: str) -> str:
        while parent[record_id] != record_id:
            parent[record_id] = parent[parent[record_id]]
            record_id = parent[record_id]
        return record_id

    def union(left: str, right: str) -> None:
        left_root, right_root = find(left), find(right)
        if left_root != right_root:
            parent[max(left_root, right_root)] = min(left_root, right_root)

    identifier_owners: dict[str, list[str]] = defaultdict(list)
    for record_id, record in records.items():
        for identifier in record["identifiers"]:
            identifier_owners[identifier].append(record_id)
    for owners in identifier_owners.values():
        for owner in owners[1:]:
            union(owners[0], owner)

    components: dict[str, list[str]] = defaultdict(list)
    for record_id in records:
        components[find(record_id)].append(record_id)

    correlations: list[dict[str, Any]] = []
    uncorrelated: list[dict[str, Any]] = []
    for record_ids in components.values():
        ordered_ids = sorted(record_ids)
        component_records = [records[record_id] for record_id in ordered_ids]
        shared_identifiers = unique_strings(identifier for record in component_records for identifier in record["identifiers"])
        systems = {record["system"] for record in component_records}
        if len(component_records) > 1 and len(systems) > 1:
            correlations.append(
                {
                    "correlation_id": stable_id("COR", ordered_ids, shared_identifiers),
                    "identifiers": shared_identifiers,
                    "records": component_records,
                    "systems": sorted(systems),
                }
            )
        else:
            uncorrelated.extend(component_records)

    return {
        "correlation_result": {
            "correlations": sorted(correlations, key=lambda item: item["correlation_id"]),
            "uncorrelated": sorted(uncorrelated, key=lambda item: item["record_id"]),
            "record_count": len(records),
        }
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Correlate offline Git, GitHub, and Linear records by explicit commit, pull-request, and issue identifiers.")
    parser.add_argument("input", help="Input JSON path")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        write_json(correlate(read_json(args.input)), args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
