"""Three-person ownership and dependency contracts for Linear program plans."""

from itertools import product

POLICY = "three-person-workstreams-v1"


def analyze_workstreams(plan):
    errors = []

    def reject(code, path, message):
        errors.append({"code": code, "path": path, "message": message})

    def text(value):
        return isinstance(value, str) and bool(value.strip())

    milestones = plan.get("milestones")
    if not isinstance(milestones, list) or len(milestones) != 3:
        reject(
            "workstream_count",
            "$.milestones",
            "Assign exactly three milestone workstreams to the three-person team.",
        )
        return errors, None
    if not all(
        isinstance(m, dict) and text(m.get("key")) and text(m.get("owner"))
        for m in milestones
    ):
        reject(
            "workstream_owner",
            "$.milestones",
            "Each workstream needs its key and named person.",
        )
        return errors, None
    owners = {m["owner"].strip().casefold() for m in milestones}
    if len(owners) != 3:
        reject(
            "workstream_owner",
            "$.milestones",
            "Assign each workstream to a different person using consistent owner identities.",
        )
    lanes = {
        m["key"]: {
            "milestone": m["key"],
            "owner": m["owner"],
            "issues": [],
            "ready_issues": [],
        }
        for m in milestones
    }
    issues = plan.get("issues")
    if not isinstance(issues, list):
        reject(
            "workstream_issues",
            "$.issues",
            "Supply the bite-sized issues for all three workstreams.",
        )
        return errors, None
    for index, issue in enumerate(issues):
        path = f"$.issues[{index}]"
        if (
            not isinstance(issue, dict)
            or not text(issue.get("key"))
            or not text(issue.get("milestone"))
        ):
            reject(
                "workstream_issues",
                path,
                "Each work unit needs an issue key and one milestone.",
            )
            continue
        lane = lanes.get(issue["milestone"])
        if lane is None:
            reject(
                "workstream_issues",
                path + ".milestone",
                "Assign the issue to one of the three workstreams.",
            )
            continue
        lane["issues"].append(issue["key"])
        if issue.get("owner") != lane["owner"]:
            reject(
                "workstream_owner",
                path + ".owner",
                "The issue owner must be the person assigned to its workstream.",
            )
        unit = issue.get("work_unit")
        if not isinstance(unit, dict) or not all(
            text(unit.get(k)) for k in ("outcome", "verification")
        ):
            reject(
                "work_unit",
                path + ".work_unit",
                "Describe one independently reviewable outcome and how to verify it at an observable boundary.",
            )
            continue
        size = unit.get("size")
        if (
            not isinstance(size, dict)
            or not text(size.get("rationale"))
            or size.get("assessment") != "bite_sized"
        ):
            reject(
                "work_unit_size",
                path + ".work_unit.size",
                "Split oversized work and resolve uncertain sizing before publication; explain why this outcome fits one reviewable PR.",
            )
    for lane in lanes.values():
        if not lane["issues"]:
            reject(
                "empty_workstream",
                "$.milestones",
                f"Workstream {lane['milestone']} needs independently useful work.",
            )
    if errors:
        return errors, None

    planned = {key for lane in lanes.values() for key in lane["issues"]}
    external = (
        {
            r["key"]
            for r in plan.get("existing_issue_refs", [])
            if isinstance(r, dict) and text(r.get("key"))
        }
        if isinstance(plan.get("existing_issue_refs", []), list)
        else set()
    )
    nodes = planned | external
    predecessors = {key: set() for key in nodes}
    relations = plan.get("relations", [])
    for relation in relations if isinstance(relations, list) else []:
        if not isinstance(relation, dict) or relation.get("type") != "blocks":
            continue
        source, target = relation.get("source"), relation.get("target")
        if text(source) and text(target) and source in nodes and target in nodes:
            predecessors[target].add(source)
    remaining = set(nodes)
    ancestors = {}
    while remaining:
        ready = sorted(key for key in remaining if not predecessors[key] & remaining)
        if not ready:
            reject(
                "dependency_cycle",
                "$.relations",
                "Native blocks relations contain a cycle. Resolve it before scheduling the workstreams.",
            )
            return errors, None
        for key in ready:
            ancestors[key] = set(predecessors[key])
            for parent in predecessors[key]:
                ancestors[key].update(ancestors[parent])
        remaining.difference_update(ready)
    frontier = next(
        (
            list(group)
            for group in product(*(sorted(lane["issues"]) for lane in lanes.values()))
            if all(
                a not in ancestors[b] and b not in ancestors[a]
                for i, a in enumerate(group)
                for b in group[i + 1 :]
            )
        ),
        None,
    )
    if frontier is None:
        reject(
            "parallel_workstreams",
            "$.relations",
            "The dependency graph cannot make one issue per person ready together. Split or regroup the work; surface any unavoidable constraint for an open-ended human decision.",
        )
        return errors, None
    prerequisites = set().union(*(ancestors[key] for key in frontier))
    for lane in lanes.values():
        lane["ready_issues"] = sorted(
            key for key in lane["issues"] if not predecessors[key]
        )
    return errors, {
        "policy": POLICY,
        "lanes": list(lanes.values()),
        "parallel_frontier": frontier,
        "prerequisites": sorted(prerequisites & planned),
        "external_blockers": sorted(prerequisites & external),
    }
