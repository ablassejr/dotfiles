#!/usr/bin/env python3
"""Collect read-only Git lineage for one path or symbol."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
from typing import Sequence


FIELD_SEPARATOR = "\x1f"
RECORD_SEPARATOR = "\x1e"
FORMAT = f"%H{FIELD_SEPARATOR}%aI{FIELD_SEPARATOR}%an{FIELD_SEPARATOR}%s{RECORD_SEPARATOR}"


def _git(repository: Path, arguments: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repository), *arguments],
        check=False,
        capture_output=True,
        text=True,
    )


def _commits(output: str) -> list[dict[str, str]]:
    records: list[dict[str, str]] = []
    for raw_record in output.split(RECORD_SEPARATOR):
        record = raw_record.strip("\n")
        if not record:
            continue
        fields = record.split(FIELD_SEPARATOR, 3)
        if len(fields) != 4:
            continue
        commit, authored_at, author, subject = fields
        records.append(
            {
                "commit": commit,
                "authored_at": authored_at,
                "author": author,
                "subject": subject,
            }
        )
    return records


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Trace read-only Git lineage for Ground Me.")
    parser.add_argument("--repository", required=True, type=Path)
    parser.add_argument("--path")
    parser.add_argument("--symbol")
    parser.add_argument("--line", type=int)
    parser.add_argument("--max-commits", type=int, default=100)
    parser.add_argument("--json", action="store_true", dest="json_output")
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    arguments = _parser().parse_args(argv)
    errors: list[dict[str, str]] = []
    if not arguments.path and not arguments.symbol:
        errors.append(
            {
                "code": "missing_target",
                "path": "--path|--symbol",
                "message": "Provide a path, a symbol, or both.",
            }
        )
    if arguments.line is not None and (not arguments.path or arguments.line < 1):
        errors.append(
            {
                "code": "invalid_line",
                "path": "--line",
                "message": "A positive line requires --path.",
            }
        )
    if arguments.max_commits < 1:
        errors.append(
            {
                "code": "invalid_limit",
                "path": "--max-commits",
                "message": "The commit limit must be positive.",
            }
        )

    root: str | None = None
    commits: list[dict[str, str]] = []
    blame: dict[str, str] | None = None
    if not errors:
        root_result = _git(arguments.repository, ["rev-parse", "--show-toplevel"])
        if root_result.returncode != 0:
            errors.append(
                {
                    "code": "not_a_repository",
                    "path": str(arguments.repository),
                    "message": root_result.stderr.strip() or "Git could not resolve the repository.",
                }
            )
        else:
            root = root_result.stdout.strip()

    if root is not None:
        log_arguments = [
            "log",
            f"--max-count={arguments.max_commits}",
            f"--format={FORMAT}",
        ]
        if arguments.symbol:
            log_arguments.extend(["-S", arguments.symbol, "--all"])
        elif arguments.path:
            log_arguments.append("--follow")
        if arguments.path:
            log_arguments.extend(["--", arguments.path])
        log_result = _git(Path(root), log_arguments)
        if log_result.returncode != 0:
            errors.append(
                {
                    "code": "git_log_failed",
                    "path": arguments.path or arguments.symbol or "target",
                    "message": log_result.stderr.strip() or "Git log failed.",
                }
            )
        else:
            commits = _commits(log_result.stdout)

        if arguments.line is not None and arguments.path:
            blame_result = _git(
                Path(root),
                [
                    "blame",
                    "--line-porcelain",
                    "-L",
                    f"{arguments.line},{arguments.line}",
                    "--",
                    arguments.path,
                ],
            )
            if blame_result.returncode != 0:
                errors.append(
                    {
                        "code": "git_blame_failed",
                        "path": arguments.path,
                        "message": blame_result.stderr.strip() or "Git blame failed.",
                    }
                )
            else:
                first_line = blame_result.stdout.splitlines()[0].split()
                blame = {
                    "commit": first_line[0] if first_line else "",
                    "line": str(arguments.line),
                }

    result = {
        "status": "ok" if not errors else "error",
        "repository": root or str(arguments.repository),
        "target": {"path": arguments.path, "symbol": arguments.symbol, "line": arguments.line},
        "commits": commits,
        "introducing_commit": commits[-1]["commit"] if commits else None,
        "blame": blame,
        "errors": errors,
    }
    if arguments.json_output:
        print(json.dumps(result, sort_keys=True))
    elif errors:
        for error in errors:
            print(f"{error['code']}: {error['message']}", file=sys.stderr)
    else:
        for commit in commits:
            print(f"{commit['commit']} {commit['authored_at']} {commit['subject']}")
    return 0 if not errors else 2


if __name__ == "__main__":
    sys.exit(main())

