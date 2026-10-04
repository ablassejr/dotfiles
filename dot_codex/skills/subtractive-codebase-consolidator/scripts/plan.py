"""Normalize responsibility candidates and deduplicate their proposed removal closures."""
import argparse
from pathlib import Path

from contracts import CandidateSet
from snapshot import entrypoint, load_run, read, relative, require, unchanged, write


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run")
    p.add_argument("candidates")
    args = p.parse_args()
    run = load_run(args.run)
    unchanged(run)
    source = read(args.candidates, CandidateSet)
    require(source["baseline_hash"] == run["baseline_hash"], "Candidate evidence is stale")
    candidates = {c["id"]: c for c in source["candidates"]}
    require(len(candidates) == len(source["candidates"]), "Duplicate candidate IDs")
    obligations = {b["id"] for b in run["basis"]["preserve"]}
    closures, blocked = {}, {}
    for name, candidate in candidates.items():
        reasons = list(run["gaps"])
        require(set(candidate["preserve"]) <= obligations, f"Unknown preservation obligation: {name}")
        require(set(candidate["depends_on"]) <= candidates.keys(), f"Unknown candidate dependency: {name}")
        if candidate["unknown_consumers"] or run["basis"]["unknown_consumers"]:
            reasons.append("Unresolved consumers or roots")
        if candidate["rationale"] in {"unknown", "still-required"}:
            reasons.append("Removal rationale has not established replaceability")
        if not set(candidate["retired_behavior"]) <= set(run["basis"]["approved_retirements"]):
            reasons.append("Behavior retirement lacks authorization")
        if candidate["change"] != "retirement" and candidate["retired_behavior"]:
            reasons.append("A preservation change declares retired behavior")
        for path in candidate["removal_paths"]:
            relative(path)
            require(path in run["files"], f"Removal path is absent from inventory: {path}")
            closures.setdefault(path, []).append(name)
        if reasons:
            blocked[name] = reasons
    ordered, visiting, visited = [], set(), set()
    def visit(name):
        require(name not in visiting, "Candidate dependency cycle")
        if name in visited:
            return
        visiting.add(name)
        for dependency in candidates[name]["depends_on"]:
            visit(dependency)
            if dependency in blocked:
                blocked.setdefault(name, []).append(f"Dependency blocked: {dependency}")
        visiting.remove(name)
        visited.add(name)
        ordered.append(name)
    for name in candidates:
        visit(name)
    output = {"format_version": 1, "baseline_hash": run["baseline_hash"], "candidates": source["candidates"],
              "order": ordered, "blocked": blocked, "unique_removal_paths": sorted(closures),
              "overlaps": {p: sorted(set(ids)) for p, ids in closures.items() if len(set(ids)) > 1},
              "estimated_source_reduction": "UNKNOWN", "permission": "analysis-only"}
    unchanged(run)
    write(Path(args.run) / "plan.json", output)
    print(f"Recorded {len(candidates)} candidates; {len(blocked)} blocked; {len(closures)} unique removal paths")


if __name__ == "__main__":
    entrypoint(main)
