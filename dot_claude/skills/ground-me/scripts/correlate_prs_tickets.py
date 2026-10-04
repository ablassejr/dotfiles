#!/usr/bin/env python3
"""Extract pull-request and ticket identifiers from Git lineage records."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import sys
from typing import Any, Sequence


PR_PATTERN = re.compile(r"(?<![A-Za-z0-9])#([1-9][0-9]*)")
TICKET_PATTERN = re.compile(r"\b([A-Z][A-Z0-9]+-[1-9][0-9]*)\b")


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Correlate PR and ticket references in lineage JSON.")
    parser.add_argument("lineage", type=Path)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    try:
        with arguments.lineage.open("r", encoding="utf-8") as stream:
            payload: Any = json.load(stream)
    except FileNotFoundError:
        error = {"code": "file_not_found", "message": "The lineage file does not exist."}
        payload = None
    except json.JSONDecodeError as exception:
        error = {
            "code": "invalid_json",
            "message": f"JSON parsing failed at line {exception.lineno}, column {exception.colno}.",
        }
        payload = None
    except OSError as exception:
        error = {"code": "read_failed", "message": str(exception)}
        payload = None
    else:
        error = None

    correlations: list[dict[str, object]] = []
    if isinstance(payload, dict) and isinstance(payload.get("commits"), list):
        for commit in payload["commits"]:
            if not isinstance(commit, dict):
                continue
            subject = commit.get("subject")
            commit_id = commit.get("commit")
            if not isinstance(subject, str) or not isinstance(commit_id, str):
                continue
            correlations.append(
                {
                    "commit": commit_id,
                    "pull_requests": sorted({int(value) for value in PR_PATTERN.findall(subject)}),
                    "tickets": sorted(set(TICKET_PATTERN.findall(subject))),
                }
            )
    elif error is None:
        error = {"code": "invalid_lineage", "message": "Expected a commits array."}

    result = {
        "status": "ok" if error is None else "error",
        "lineage": str(arguments.lineage),
        "correlations": correlations,
        "errors": [] if error is None else [error],
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif error is not None:
        print(f"{error['code']}: {error['message']}", file=sys.stderr)
    else:
        for correlation in correlations:
            print(json.dumps(correlation, sort_keys=True))
    return 0 if error is None else 2


if __name__ == "__main__":
    sys.exit(main())

