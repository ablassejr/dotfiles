"""Render local Markdown with current evidence status and measured changes."""
import argparse
from pathlib import Path

from contracts import Verification
from snapshot import digest, entrypoint, load_run, read, require, unchanged
from verify import finalize, validate_current


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run")
    args = p.parse_args()
    directory = Path(args.run).resolve()
    run = load_run(directory)
    unchanged(run)
    lines = ["# Local consolidation report", "", f"Baseline: `{run['baseline_hash']}`", "",
             "This report describes local evidence. Verification does not authorize applying or publishing a patch.", ""]
    if (directory / "verification.json").exists():
        result = read(directory / "verification.json", Verification)
        try:
            validate_current(directory, result)
            if result["status"] in {"VERIFIED", "VERIFIED_WITH_EXCEPTIONS"}:
                review = read(directory / "review.json")
                require(digest(review) == result["review_hash"], "Review changed")
                exception = directory / "exception.json" if result["exception_hash"] else None
                if exception:
                    require(digest(read(exception)) == result["exception_hash"], "Exception changed")
                recomputed = finalize(directory, dict(result), directory / "review.json", exception)
                require(recomputed["status"] == result["status"], "Saved verification status is inconsistent")
            lines += [f"Status: **{result['status']}**", "", f"Patch: `{result['patch_hash']}`", ""]
        except (ValueError, OSError, KeyError, TypeError) as error:
            lines += ["Status: **INCOMPLETE**", "", f"Current validation: {error}", ""]
            result["status"] = "INCOMPLETE"
        m = result["measurement"]
        if m:
            lines += ["| Measure | Value |", "|---|---:|", f"| Maintained source before | {m['before']} |",
                      f"| Maintained source after | {m['after']} |", f"| Added source | {m['added']} |",
                      f"| Removed source | {m['removed']} |", f"| Net change | {m['net']} |",
                      f"| 6:5 directional target | {'Met' if m['ratio_met'] else 'Not met'} |", "",
                      "Tests, tooling, and executable configuration count as maintained source. Generated and supplied files are listed separately.", ""]
        for title, entries in [("Failures", result["failures"]), ("Evidence gaps", result["gaps"]), ("Numerical waivers", result["waivers"])]:
            if entries:
                lines += [f"## {title}", ""] + [f"- {entry}" for entry in entries] + [""]
        lines += ["The receipts record the commands that ran and their declared exercised scope. The reviewer assesses whether those cases cover the required roots and variants; execution alone does not establish that coverage.", ""]
    else:
        lines += ["Status: **AUDIT ONLY**", "", "No patch verification has run.", ""]
    if (directory / "plan.json").exists():
        plan = read(directory / "plan.json")
        require(plan["baseline_hash"] == run["baseline_hash"], "Plan is stale")
        lines += ["## Responsibility candidates", ""]
        for candidate in plan["candidates"]:
            state = "blocked" if candidate["id"] in plan["blocked"] else "eligible for validation"
            lines += [f"- {candidate['id']}: {candidate['responsibility']} ({state}). {candidate['target']}"]
        lines += ["", f"Unique proposed removal paths: {len(plan['unique_removal_paths'])}. Estimated source reduction: UNKNOWN.", ""]
    lines += ["## Preservation boundary", ""] + [f"- {p['id']}: {p['behavior']}" for p in run["basis"]["preserve"]]
    lines += ["", "## Locality", "", "The helper executes preinstalled tools in containers with no host mounts and no network. Model inference is outside this helper; using a hosted assistant is not an offline workflow.", ""]
    output = directory / "report.md"
    output.write_text("\n".join(lines))
    print(output)


if __name__ == "__main__":
    entrypoint(main)
