"""Collect current execution evidence, then finalize it against an independent review."""
import argparse
import fnmatch
import json
from pathlib import Path
import shutil
import tempfile

from collect import Sandbox, engine_hash, run_checks
from contracts import Authorization, Checks, ExceptionApproval, MAINTAINED, Measurement, Review, Runtime, Verification
from snapshot import current, digest, entrypoint, load_run, patch_hash, read, require, scan, unchanged, unexpired, write


def integer(value):
    require(type(value) is int and value >= 0, "Counter returned a missing, negative, or non-integer count")
    return value


def check_logs(executions):
    for execution in executions:
        require(digest(Path(execution["log"]).read_bytes()) == execution["log_hash"], "Execution log is missing or changed")


def evidence_hash(result):
    keys = ["patch_hash", "baseline_hash", "candidate_hash", "inventory_hash", "basis_hash", "checks_hash",
            "engine_hash", "runtime_hash", "measurement", "receipts", "measurement_receipts"]
    return digest({key: result[key] for key in keys})


def measure(directory, run, sandbox):
    receipts = []
    with tempfile.TemporaryDirectory(prefix="measurement-", dir=directory) as temp:
        staging = Path(temp)
        files = {side: scan(Path(directory) / side, run["inventory"]) for side in ["baseline", "candidate"]}
        included = {side: {p: f for p, f in entries.items() if f["category"] in MAINTAINED} for side, entries in files.items()}
        for side in files:
            (staging / side).mkdir()
            for path in included[side]:
                target = staging / side / path
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(Path(directory) / side / path, target)
        def execute(arguments, label):
            receipt = sandbox.execute(staging, ["perl", "/tmp/cloc.pl", "--config", "/dev/null"] + arguments, label)
            receipts.append(receipt)
            require(receipt["exit_code"] == 0, f"Counter did not complete: {receipt['log']}")
            return Path(receipt["log"]).read_text()
        version = execute(["--version"], "counter-version").strip()
        require(version, "Counter version is missing")
        counts = {}
        for side in files:
            if not included[side]:
                counts[side] = {}
                continue
            data = json.loads(execute(["--json", "--by-file", "--skip-uniqueness", "--quiet", side], "count-" + side))
            rows = {p.removeprefix(side + "/"): integer(row.get("code")) for p, row in data.items() if p not in {"header", "SUM"}}
            require(set(rows) == set(included[side]), f"Counter coverage incomplete for {side}: {sorted(set(included[side]) ^ set(rows))}")
            require(sum(rows.values()) == integer(data.get("SUM", {}).get("code")), "Counter total disagrees with file counts")
            counts[side] = rows
        moved = []
        baseline_only = set(included["baseline"]) - set(included["candidate"])
        candidate_only = set(included["candidate"]) - set(included["baseline"])
        for before in sorted(baseline_only):
            matches = sorted(after for after in candidate_only
                             if included["baseline"][before]["sha256"] == included["candidate"][after]["sha256"])
            if matches:
                after = matches[0]
                candidate_only.remove(after)
                moved.append([before, after])
                (staging / "baseline" / before).unlink()
                (staging / "candidate" / after).unlink()
        has_diff = any(p.is_file() for side in files for p in (staging / side).rglob("*"))
        if has_diff:
            data = json.loads(execute(["--json", "--by-file", "--skip-uniqueness", "--quiet", "--diff",
                                       "baseline", "candidate"], "counter-diff"))
            summary = data.get("SUM", {})
            modified = integer(summary.get("modified", {}).get("code"))
            added = integer(summary.get("added", {}).get("code")) + modified
            removed = integer(summary.get("removed", {}).get("code")) + modified
        else:
            added = removed = 0
        before, after = sum(counts["baseline"].values()), sum(counts["candidate"].values())
        measurement = {"before": before, "after": after, "added": added, "removed": removed,
                       "net": after - before, "ratio_met": 5 * removed >= 6 * added,
                       "by_category": {cat: {side: sum(n for p, n in counts[side].items() if included[side][p]["category"] == cat)
                                              for side in files} for cat in sorted(MAINTAINED)},
                       "file_counts": counts, "excluded_files": {side: sorted(set(files[side]) - set(included[side])) for side in files},
                       "moved_files": moved, "counter_version": version, "counter_hash": sandbox.counter_hash}
        validate_measurement(measurement)
        return measurement, receipts


def validate_measurement(value):
    m = Measurement.model_validate(value).model_dump()
    require(m["net"] == m["after"] - m["before"] == m["added"] - m["removed"], "Measurement arithmetic does not reconcile")
    require(m["ratio_met"] == (5 * m["removed"] >= 6 * m["added"]), "Supplied ratio result disagrees with counts")
    require(set(m["by_category"]) == MAINTAINED, "Measurement categories are incomplete")
    require(set(m["file_counts"]) == {"baseline", "candidate"}, "Measurement file coverage is absent")
    for side, total in [("baseline", m["before"]), ("candidate", m["after"])]:
        require(sum(m["file_counts"][side].values()) == total, "File counts disagree with total")
        require(sum(v[side] for v in m["by_category"].values()) == total, "Category counts disagree with total")
    return m


def bind_measurement(directory, run, result):
    m = result["measurement"]
    executions = result["measurement_receipts"]
    require(all(r["exit_code"] == 0 and not r["timed_out"] for r in executions), "Measurement execution failed")
    indexed = {tuple(r["argv"]): r for r in executions}
    require(len(indexed) == len(executions), "Duplicate measurement executions")
    prefix = ["perl", "/tmp/cloc.pl", "--config", "/dev/null"]
    used = set()
    def output(args):
        key = tuple(prefix + args)
        require(key in indexed, "Required measurement command was not executed")
        used.add(key)
        return Path(indexed[key]["log"]).read_text()
    require(output(["--version"]).strip() == m["counter_version"], "Counter version does not match its log")
    inventories = {side: scan(Path(directory) / side, run["inventory"]) for side in ["baseline", "candidate"]}
    for side, files in inventories.items():
        included = {p for p, f in files.items() if f["category"] in MAINTAINED}
        rows = {}
        if included:
            data = json.loads(output(["--json", "--by-file", "--skip-uniqueness", "--quiet", side]))
            rows = {p.removeprefix(side + "/"): integer(r.get("code")) for p, r in data.items() if p not in {"header", "SUM"}}
            require(sum(rows.values()) == integer(data.get("SUM", {}).get("code")), "Raw counter total is inconsistent")
        require(set(rows) == included and rows == m["file_counts"][side], "Measurement differs from the executed counter or inventory")
        require(m["excluded_files"][side] == sorted(set(files) - included), "Excluded measurement files changed")
        for cat in MAINTAINED:
            require(m["by_category"][cat][side] == sum(n for p, n in rows.items() if files[p]["category"] == cat), "Source classification disagrees with file counts")
    before_names, after_names = set(m["file_counts"]["baseline"]), set(m["file_counts"]["candidate"])
    available = after_names - before_names
    moves = []
    for before in sorted(before_names - after_names):
        matches = sorted(after for after in available if inventories["baseline"][before]["sha256"] == inventories["candidate"][after]["sha256"])
        if matches:
            moves.append([before, matches[0]])
            available.remove(matches[0])
    require(moves == m["moved_files"], "Move accounting differs from snapshot contents")
    if len(before_names) + len(after_names) > 2 * len(moves):
        data = json.loads(output(["--json", "--by-file", "--skip-uniqueness", "--quiet", "--diff", "baseline", "candidate"]))
        summary = data.get("SUM", {})
        modified = integer(summary.get("modified", {}).get("code"))
        require(m["added"] == integer(summary.get("added", {}).get("code")) + modified and
                m["removed"] == integer(summary.get("removed", {}).get("code")) + modified,
                "Churn measurement disagrees with executed counter")
    else:
        require(m["added"] == m["removed"] == 0, "Pure moves receive no reduction credit")
    require(set(indexed) == used, "Unexpected measurement execution")


def check_scope(run, checks):
    ids = [c["id"] for c in checks["checks"]]
    require(len(set(ids)) == len(ids), "Duplicate check IDs")
    obligations = {p["id"] for p in run["basis"]["preserve"]}
    e2e = {o for c in checks["checks"] if c["kind"] == "e2e" for o in c["obligations"]}
    integrations = {s for c in checks["checks"] if c["kind"] in {"e2e", "integration"} for s in c["seams"]}
    require(obligations <= e2e, "Preserved behavior lacks an end-to-end check")
    require(set(run["basis"]["seams"]) <= integrations, "A declared seam lacks an integration check")
    require(not any(c["skipped_scope"] for c in checks["checks"]), "Declared verification scope is skipped")
    require(not run["basis"]["unknown_consumers"], "Unknown consumers remain")
    require(not run["gaps"], "Inventory gaps remain")


def validate_current(directory, result):
    run = load_run(directory)
    unchanged(run)
    _, candidate_hash = current(directory, run)
    require(result["baseline_hash"] == run["baseline_hash"] and result["candidate_hash"] == candidate_hash,
            "Evidence belongs to another snapshot")
    require(result["patch_hash"] == patch_hash(run, candidate_hash), "Evidence belongs to another patch or preservation basis")
    require(result["engine_hash"] == engine_hash(), "Verifier implementation changed; collect fresh evidence")
    require(result["inventory_hash"] == run["inventory_hash"] and result["basis_hash"] == run["basis_hash"], "Evidence policy is stale")
    checks = read(Path(directory) / "checks.json", Checks)
    require(digest(checks) == result["checks_hash"], "Declared checks changed")
    check_scope(run, checks)
    sandbox = Sandbox(read(Path(directory) / "runtime.json", Runtime), Path(directory) / "logs")
    require(sandbox.binding == result["runtime_hash"], "Runtime or counter changed")
    require(result["evidence_hash"] == evidence_hash(result), "Evidence bundle changed")
    expected = {(side, c["id"]): c for side in ["baseline", "candidate"] for c in checks["checks"]}
    actual = {(r["subject"], r["check"]["id"]): r for r in result["receipts"]}
    require(len(actual) == len(result["receipts"]) and set(actual) == set(expected), "Execution receipts are missing or duplicated")
    for key, check in expected.items():
        receipt = actual[key]
        require(receipt["check"] == check and receipt["rules_hash"] == digest(check), "Executed check differs from declared contract")
        require(receipt["snapshot_hash"] == result[key[0] + "_hash"], "Check receipt is stale")
        require(receipt["image"] == sandbox.runtime["image"], "Check used a different runtime")
        require(receipt["execution"]["argv"] == check["argv"] and receipt["version"]["argv"] == check["version_argv"], "Executed command changed")
        check_logs([receipt["execution"], receipt["version"]])
        require(receipt["version"]["exit_code"] != 0 or Path(receipt["version"]["log"]).read_text().strip(), "Tool version output is empty")
    require(result["measurement"] is not None and result["measurement_receipts"], "Complete measurement and execution evidence are required")
    validate_measurement(result["measurement"])
    require(result["measurement"]["counter_hash"] == sandbox.counter_hash, "Measurement counter is stale")
    check_logs(result["measurement_receipts"])
    bind_measurement(directory, run, result)
    auth_path = Path(directory) / "authorization.json"
    if auth_path.exists():
        auth = read(auth_path, Authorization)
        require(auth["baseline_hash"] == run["baseline_hash"], "Experiment authorization is stale")
        baseline, candidate = scan(Path(directory) / "baseline", run["inventory"]), scan(Path(directory) / "candidate", run["inventory"])
        changed = {p for p in baseline.keys() | candidate.keys() if baseline.get(p) != candidate.get(p)}
        require(all(any(fnmatch.fnmatchcase(p, allowed) for allowed in auth["allowed_paths"]) for p in changed), "Patch exceeds authorized experiment scope")
    return run


def finalize(directory, result, review_path, exception_path):
    validate_current(directory, result)
    result["failures"] = [f"{r['subject']}: {r['check']['id']} failed" for r in result["receipts"]
                          if r["execution"]["exit_code"] or r["version"]["exit_code"]]
    result["gaps"], result["waivers"] = [], []
    review = read(review_path, Review)
    require(review["patch_hash"] == result["patch_hash"] and review["evidence_hash"] == result["evidence_hash"], "Independent review is stale")
    result["failures"] += review["counterexamples"]
    result["gaps"] += review["unresolved"]
    result["review_hash"] = digest(review)
    write(Path(directory) / "review.json", review)
    if exception_path:
        exception = read(exception_path, ExceptionApproval)
        require(exception["patch_hash"] == result["patch_hash"], "Numerical exception is stale")
        unexpired(exception["expires"])
        result["waivers"] = sorted(set(exception["waived"]))
        result["exception_hash"] = digest(exception)
        write(Path(directory) / "exception.json", exception)
    else:
        result["exception_hash"] = None
    m = result["measurement"]
    if not m["ratio_met"] and "ratio" not in result["waivers"]:
        result["failures"].append("6:5 directional target is not met")
    if m["net"] > 0 and "net_growth" not in result["waivers"]:
        result["failures"].append("Net source growth needs its own scoped exception")
    result["status"] = "FAILED" if result["failures"] else "INCOMPLETE" if result["gaps"] else "VERIFIED_WITH_EXCEPTIONS" if result["waivers"] else "VERIFIED"
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run")
    p.add_argument("--checks")
    p.add_argument("--runtime")
    p.add_argument("--finalize", action="store_true")
    p.add_argument("--review")
    p.add_argument("--exception")
    args = p.parse_args()
    directory = Path(args.run).resolve()
    output = directory / "verification.json"
    if args.finalize:
        require(args.review and not args.checks and not args.runtime, "Finalize requires review; collection uses checks and runtime")
        result = finalize(directory, read(output, Verification), args.review, args.exception)
    else:
        require(args.checks and args.runtime and not args.review and not args.exception, "Collect evidence first, then review the actual results")
        run = load_run(directory)
        unchanged(run)
        _, candidate_hash = current(directory, run)
        checks, runtime = read(args.checks, Checks), read(args.runtime, Runtime)
        check_scope(run, checks)
        sandbox = Sandbox(runtime, directory / "logs")
        write(directory / "checks.json", checks)
        write(directory / "runtime.json", runtime)
        receipts = run_checks(directory, run, sandbox, checks, "baseline")
        receipts += run_checks(directory, run, sandbox, checks, "candidate")
        measurement, measurement_receipts = measure(directory, run, sandbox)
        unchanged(run)
        require(current(directory, run)[1] == candidate_hash, "Candidate changed during verification")
        failures = [f"{r['subject']}: {r['check']['id']} failed" for r in receipts if r["execution"]["exit_code"] or r["version"]["exit_code"]]
        result = {"format_version": 1, "status": "FAILED" if failures else "INCOMPLETE", "patch_hash": patch_hash(run, candidate_hash),
                  "baseline_hash": run["baseline_hash"], "candidate_hash": candidate_hash, "inventory_hash": run["inventory_hash"],
                  "basis_hash": run["basis_hash"], "checks_hash": digest(checks), "engine_hash": engine_hash(),
                  "runtime_hash": sandbox.binding, "measurement": measurement, "receipts": receipts,
                  "measurement_receipts": measurement_receipts, "failures": failures,
                  "gaps": ["Independent review of the collected evidence is required"], "waivers": [],
                  "evidence_hash": "0" * 64, "review_hash": None, "exception_hash": None}
        result["evidence_hash"] = evidence_hash(result)
    Verification.model_validate(result)
    write(output, result)
    print(json.dumps({"status": result["status"], "patch_hash": result["patch_hash"], "evidence_hash": result["evidence_hash"],
                      "measurement": result["measurement"], "failures": result["failures"], "gaps": result["gaps"]}))
    if result["status"] not in {"VERIFIED", "VERIFIED_WITH_EXCEPTIONS"}:
        raise SystemExit(1 if result["failures"] else 2)


if __name__ == "__main__":
    entrypoint(main)
