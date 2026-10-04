#!/usr/bin/env python3
"""Analyze, ground, plan, and verify bounded local simplification work."""

import argparse
from pathlib import Path
import sys

sys.dont_write_bytecode = True
from local_simplification import workflow
from local_simplification.storage import Invalid, encoded, safe_path


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    audit = commands.add_parser("audit", help="Capture local snapshots and discover structural candidates")
    audit.add_argument("--repo", required=True)
    audit.add_argument("--output", required=True)
    audit.add_argument("--scope", action="append")
    audit.add_argument("--symbol")
    audit.add_argument("--responsibility")
    audit.add_argument("--policy")
    mode = audit.add_mutually_exclusive_group()
    mode.add_argument("--base")
    mode.add_argument("--commit")
    mode.add_argument("--working-tree", action="store_true")
    mode.add_argument("--staged", action="store_true")
    audit.add_argument("--head")
    audit.add_argument("--parent", type=int)
    audit.add_argument("--offline", action="store_true", help="Backward-compatible no-op; does not restrict configured services or semantic reviewers")
    ev = commands.add_parser("evidence", help="Record exact source coordinates from a pinned snapshot")
    ev.add_argument("--run", required=True)
    ev.add_argument("--side", choices=["base", "head"], default="head")
    ev.add_argument("--path", required=True)
    ev.add_argument("--start", type=int, required=True)
    ev.add_argument("--end", type=int)
    ev.add_argument("--relation", choices=["selected", "consumer", "dependency", "test", "contract", "history", "configuration", "parallel"], required=True)
    ev.add_argument("--reason", required=True)
    candidate = commands.add_parser("candidate", help="Record an analyst-proposed candidate inside the selected responsibility")
    candidate.add_argument("--run", required=True)
    candidate.add_argument("--path", action="append", required=True)
    candidate.add_argument("--owner", action="append")
    candidate.add_argument("--classification", choices=["DUPLICATE_RESPONSIBILITY", "PARALLEL_IMPLEMENTATION", "REDUNDANT_STATE", "OBSOLETE_COMPATIBILITY_PATH", "TEMPORARY_WORKAROUND", "PASS_THROUGH_LAYER", "SPECULATIVE_ABSTRACTION", "REPEATED_TRANSFORMATION", "DEAD_MECHANISM", "DEPENDENCY_BLOAT", "CONFIGURATION_SPRAWL", "TEST_DUPLICATION", "FRAGMENTED_COHESION"], required=True)
    candidate.add_argument("--statement", required=True)
    ground = commands.add_parser("ground", help="Gather candidate-specific local history without inferring its rationale")
    ground.add_argument("--run", required=True)
    ground.add_argument("--candidate", required=True)
    ground.add_argument("--pickaxe")
    ground.add_argument("--limit", type=int, default=50)
    plan = commands.add_parser("plan", help="Validate an assessment and compile proposed local PR partitions")
    plan.add_argument("--run", required=True)
    plan.add_argument("--assessment")
    graph = commands.add_parser("import-graph", help="Bind an existing normalized local code graph to source bytes")
    graph.add_argument("--run", required=True)
    graph.add_argument("--side", choices=["base", "head"], default="head")
    graph.add_argument("--file", required=True)
    structure = commands.add_parser("structure", help="Execute a locally installed ast-grep/Tree-sitter outline against pinned source")
    structure.add_argument("--run", required=True)
    structure.add_argument("--side", choices=["base", "head"], default="head")
    structure.add_argument("--path", action="append")
    structure.add_argument("--lang", help="Optional installed ast-grep language name; otherwise inferred from extension")
    verify = commands.add_parser("verify", help="Run the same declared checks against plan baseline and local implementation")
    verify.add_argument("--run", required=True)
    verify.add_argument("--plan", help="Relative plan artifact in the original run; defaults to latest plan")
    verify.add_argument("--output", required=True)
    target = verify.add_mutually_exclusive_group()
    target.add_argument("--head")
    target.add_argument("--working-tree", action="store_true")
    verify.add_argument("--harness", help="Existing local behavioral harness, identical for both snapshots")
    verify.add_argument("--offline", action="store_true", help="Backward-compatible no-op; does not restrict configured services or semantic reviewers")
    finalize = commands.add_parser("finalize", help="Bind a local target review to the executed verification and compute the final verdict")
    finalize.add_argument("--run", required=True)
    finalize.add_argument("--review")
    report = commands.add_parser("report", help="Check artifact freshness and render local reports")
    report.add_argument("--run", required=True)
    commands.add_parser("doctor", help="Detect local capabilities and exercise isolation")
    args = parser.parse_args()
    if args.command == "audit" and (args.head and (args.commit or args.staged or args.working_tree) or args.parent is not None and not args.commit):
        parser.error("--head applies to a range; --parent applies only to --commit")
    if args.command == "ground" and args.limit < 1:
        parser.error("--limit must be positive")
    try:
        result = getattr(workflow, args.command.replace("-", "_"))(args)
        sys.stdout.buffer.write(encoded(result))
        return 0 if result.get("verdict") not in ("FAIL", "INCOMPLETE", "STALE") or args.command in ("audit", "plan", "report") else 3
    except (Invalid, OSError, UnicodeError, KeyError, TypeError, ValueError) as exc:
        value = {"status": "STALE" if str(exc).startswith("STALE:") else "INVALID", "error": str(exc)}
        if args.command in ("report", "finalize"):
            try:
                workflow.invalidate(args.run, value["status"], str(exc))
            except (Invalid, OSError, KeyError, TypeError, ValueError):
                pass
        sys.stdout.buffer.write(encoded(value))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
