"""Public analysis lifecycle; semantic judgments retain their declared provenance."""

import copy
import json
from pathlib import Path
import re
import shutil
import sys
import tempfile
import uuid

from . import VERSION
from .analysis import (DIMENSIONS, OBLIGATIONS, assessment_template, category, discover,
                       inventory, measure, policy_from, scope_paths)
from .runner import execute, probe, run_checks
from .reports import render
from .storage import (Invalid, capture, content, digest, encoded, fingerprint, git,
                      git_path, inside, open_run, read_json, relative, resolve,
                      safe_path, seal, write)


SCHEMAS = Path(__file__).resolve().parents[2] / "schemas"


def validate(value, schema, location="input"):
    types = {"object": dict, "array": list, "string": str, "integer": int,
             "number": (int, float), "boolean": bool, "null": type(None)}
    expected = schema.get("type")
    if expected:
        choices = expected if isinstance(expected, list) else [expected]
        if not any(isinstance(value, types[k]) and not (k in ("number", "integer") and isinstance(value, bool)) for k in choices):
            raise Invalid(f"{location}: expected {expected}")
    if "enum" in schema and value not in schema["enum"]:
        raise Invalid(f"{location}: unsupported value {value!r}")
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - set(value)
        if missing:
            raise Invalid(f"{location}: missing {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            raise Invalid(f"{location}: unknown fields {sorted(set(value) - set(properties))}")
        for name, child in value.items():
            child_schema = properties.get(name, schema.get("additionalProperties", {}))
            if isinstance(child_schema, dict):
                validate(child, child_schema, location + "." + name)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise Invalid(f"{location}: too few items")
        if schema.get("uniqueItems") and len({encoded(x) for x in value}) != len(value):
            raise Invalid(f"{location}: duplicate items")
        for i, child in enumerate(value):
            validate(child, schema.get("items", {}), f"{location}[{i}]")
    if isinstance(value, str) and len(value.strip()) < schema.get("minLength", 0):
        raise Invalid(f"{location}: expected nonempty text")
    if type(value) in (int, float) and value < schema.get("minimum", float("-inf")):
        raise Invalid(f"{location}: value below minimum")


def state(run):
    result = read_json(run / "state.json")
    for path, sha in result["artifacts"].items():
        if digest(safe_path(run / relative(path)).read_bytes()) != sha:
            raise Invalid(f"Evidence artifact was altered: {path}")
    manifest = read_json(run / "manifest.json")
    for binding in result["evidence"]:
        if binding["path"] not in result["artifacts"]:
            raise Invalid("Evidence artifact has no content binding")
        record = read_json(run / relative(binding["path"]))
        payload = {key: value for key, value in record.items() if key != "id"}
        if record["id"] != binding["id"] or record["id"] != "EV-" + digest(encoded(payload))[:16]:
            raise Invalid("Evidence identity does not match its content")
        if record["kind"] == "source":
            snapshot = manifest["snapshots"][record["side"]]
            path = relative(record["path"])
            if record["snapshot_digest"] != snapshot["digest"] or record["source_sha256"] != snapshot["files"][path]["sha256"]:
                raise Invalid("Source evidence belongs to different source bytes")
            lines = content(run, snapshot, path).decode("utf-8").splitlines()
            if not 1 <= record["start"] <= record["end"] <= len(lines) or record["text"] != "\n".join(lines[record["start"] - 1:record["end"]]):
                raise Invalid("Source evidence does not match its pinned coordinates")
    return result


def artifact(run, current, name, value):
    write(run, name, value)
    current["artifacts"][name] = digest((run / name).read_bytes())


def make_output(repo, requested):
    output = safe_path(requested)
    for protected in (repo, git_path(repo, "--absolute-git-dir"), git_path(repo, "--git-common-dir")):
        if inside(protected, output) or protected != repo and inside(output, protected):
            raise Invalid("Output overlaps repository root or Git storage")
    if output.exists():
        raise Invalid("Output must be a new directory")
    output.mkdir(parents=True)
    return output


def audit(args):
    repo = git_path(Path(args.repo).resolve(), "--show-toplevel")
    output = make_output(repo, args.output)
    initial = fingerprint(repo, output)
    policy = policy_from(read_json(args.policy) if args.policy else None)
    head_now = resolve(repo, "HEAD", optional=True)
    if args.commit:
        head = resolve(repo, args.commit)
        parents = [s.split()[1] for s in git(repo, "cat-file", "commit", head).decode("utf-8", "replace").split("\n\n", 1)[0].splitlines() if s.startswith("parent ")]
        if len(parents) > 1 and args.parent is None:
            raise Invalid("Merge commit analysis requires an explicit --parent")
        parent = args.parent or 1
        if parent < 1 or parent > len(parents) and parents or args.parent and not parents:
            raise Invalid("Commit parent is out of range")
        base = parents[parent - 1] if parents else None
    elif args.working_tree or args.staged:
        base, head = head_now, head_now
    else:
        head = resolve(repo, args.head or "HEAD")
        base = resolve(repo, args.base) if args.base else head
    if not args.scope and not args.symbol and not (args.base or args.commit or args.staged or args.working_tree):
        raise Invalid("Choose a bounded --scope, --symbol, or local change")
    snapshots = {"base": capture(repo, base, output),
                 "head": capture(repo, head, output, args.working_tree, args.staged)}
    inventories = {side: inventory(output, snap, policy) for side, snap in snapshots.items()}
    requested = args.scope
    if args.symbol and not requested:
        matches = [x for value in inventories["head"].values() for x in value["symbols"] if args.symbol in (x["name"], x["short_name"], x["id"])]
        if len({x["id"] for x in matches}) > 1:
            raise Invalid("Symbol is ambiguous; choose a qualified path::symbol or an explicit scope")
        requested = sorted({x["path"] for x in matches})
        if not requested:
            raise Invalid("Symbol cannot be resolved by an available adapter; select a module")
    scopes, selected = scope_paths(snapshots["base"], snapshots["head"], requested)
    candidates, graph = discover(inventories, selected, args.symbol)
    mass = measure(snapshots["base"], snapshots["head"], inventories, selected, policy)
    identity = {"repository": str(repo), "snapshots": {k: v["digest"] for k, v in snapshots.items()},
                "scope": selected, "policy": policy}
    run_id = "simplify:" + digest(encoded(identity))
    manifest = {"schema_version": 1, "framework_version": VERSION, "run_id": run_id,
                "repository": str(repo), "source_fingerprint": initial["sha256"],
                "snapshots": snapshots, "scope": {"requested": scopes, "paths": selected,
                "responsibility": args.responsibility or "User-selected local responsibility",
                "discovery_extent": "Whole captured tree inventoried; semantic candidates must intersect selected paths"},
                "policy": policy, "tool_versions": {"python": sys.version.split()[0], "git": git(repo, "--version").decode().strip()},
                "limitations": ["The helper invokes no model; semantic review is supplied by a hosted or local analyst",
                                "Python syntax references are not a complete consumer graph",
                                "Imported judgments are evidence-bound statements, not execution proof"]}
    final = fingerprint(repo, output)
    if final["sha256"] != initial["sha256"]:
        raise Invalid("STALE: repository changed during snapshot capture")
    write(output, "manifest.json", manifest)
    write(output, "integrity-before.json", initial)
    write(output, "inventory.json", inventories)
    write(output, "candidates.json", {"schema_version": 1, "run_id": run_id, "candidates": candidates})
    write(output, "responsibility-current.json", graph)
    write(output, "code-mass.json", mass)
    write(output, "assessment.json", assessment_template(run_id, candidates))
    write(output, "state.json", {"schema_version": 1, "artifacts": {}, "evidence": [], "manual_candidates": []})
    seal(output, ["manifest.json", "integrity-before.json", "inventory.json", "candidates.json", "responsibility-current.json", "code-mass.json"])
    result = {"schema_version": 1, "run_id": run_id, "verdict": "INCOMPLETE", "complete": False,
              "stage": "AUDITED", "candidate_count": len(candidates), "code_mass": mass,
              "gaps": ["Candidate discovery is complete; semantic grounding and implementation verification remain"]}
    render(output, result)
    return {"run": str(output), **result}


def evidence(args):
    run, manifest = open_run(args.run)
    current = state(run)
    path = relative(args.path)
    snapshot = manifest["snapshots"][args.side]
    if path not in snapshot["files"]:
        raise Invalid("Evidence path is absent from the pinned snapshot")
    text = content(run, snapshot, path).decode("utf-8").splitlines()
    end = args.end or args.start
    if not 1 <= args.start <= end <= len(text):
        raise Invalid("Evidence coordinates are out of range")
    item = {"kind": "source", "side": args.side, "path": path, "start": args.start, "end": end,
            "source_sha256": snapshot["files"][path]["sha256"], "snapshot_digest": snapshot["digest"],
            "relation": args.relation, "reason": args.reason, "text": "\n".join(text[args.start - 1:end])}
    return store_evidence(run, current, item)


def store_evidence(run, current, item):
    evidence_id = "EV-" + digest(encoded(item))[:16]
    path = f"evidence/{evidence_id}.json"
    artifact(run, current, path, {"id": evidence_id, **item})
    if evidence_id not in [x["id"] for x in current["evidence"]]:
        current["evidence"].append({"id": evidence_id, "path": path})
    write(run, "state.json", current)
    return {"evidence_id": evidence_id, "artifact": str(run / path)}


def all_candidates(run, current):
    return read_json(run / "candidates.json")["candidates"] + current["manual_candidates"]


def candidate(args):
    run, manifest = open_run(args.run)
    current = state(run)
    paths = [relative(p) for p in args.path]
    if not any(p in manifest["scope"]["paths"] for p in paths):
        raise Invalid("A candidate must intersect the selected responsibility")
    if any(p not in manifest["snapshots"]["head"]["files"] for p in paths):
        raise Invalid("Candidate path is absent from the pinned head")
    record = {"classification": args.classification, "statement": args.statement,
              "owners": args.owner or [], "paths": paths, "safety": "UNKNOWN", "confidence": "ANALYST_PROPOSED",
              "estimated_added": None, "estimated_removed": None,
              "unresolved": ["Complete behavioral and historical grounding"]}
    record["candidate_id"] = "CON-" + digest(encoded(record))[:12]
    if record["candidate_id"] not in [x["candidate_id"] for x in all_candidates(run, current)]:
        current["manual_candidates"].append(record)
    write(run, "state.json", current)
    draft = read_json(run / "assessment.json")
    if record["candidate_id"] not in [x["candidate_id"] for x in draft["candidates"]]:
        draft["candidates"].extend(assessment_template(manifest["run_id"], [record])["candidates"])
        write(run, "assessment.json", draft)
    return record


def ground(args):
    run, manifest = open_run(args.run)
    current = state(run)
    found = [x for x in all_candidates(run, current) if x["candidate_id"] == args.candidate]
    if len(found) != 1:
        raise Invalid("Unknown candidate ID")
    repo, histories = Path(manifest["repository"]), []
    revision = manifest["snapshots"]["head"]["commit"]
    if revision is None:
        return {"status": "UNAVAILABLE", "reason": "No committed local history", "candidate_id": args.candidate}
    for path in found[0]["paths"]:
        command = ["log", "--no-ext-diff", "--no-textconv", "--format=%H%x00%s", "-n", str(args.limit), "--follow"]
        if args.pickaxe:
            command.append("-S" + args.pickaxe)
        raw = git(repo, *command, revision, "--", path).decode("utf-8", "replace")
        histories.append({"path": path, "revision": revision, "history": raw})
    item = {"kind": "git_history", "candidate_id": args.candidate, "histories": histories,
            "limit": args.limit, "pickaxe": args.pickaxe,
            "interpretation": "Chronology supports investigation; commit messages do not establish current necessity"}
    if fingerprint(repo, run)["sha256"] != manifest["source_fingerprint"]:
        raise Invalid("STALE: repository changed while grounding")
    return store_evidence(run, current, item)


def check_assessment(run, manifest, assessment, current):
    validate(assessment, read_json(SCHEMAS / "assessment.schema.json"))
    if assessment["run_id"] != manifest["run_id"]:
        raise Invalid("Assessment belongs to a different snapshot or scope")
    known = {x["candidate_id"]: x for x in all_candidates(run, current)}
    cards = assessment["candidates"]
    ids = [x["candidate_id"] for x in cards]
    if len(set(ids)) != len(ids) or set(ids) - set(known):
        raise Invalid("Candidate IDs are duplicated or do not belong to this run")
    checks = {x["id"]: x for x in assessment["checks"]}
    if len(checks) != len(assessment["checks"]):
        raise Invalid("Check IDs must be unique")
    evidence_ids = {x["id"] for x in current["evidence"]}
    if assessment.get("ratio_exception") and set(assessment["ratio_exception"]["evidence_ids"]) - evidence_ids:
        raise Invalid("Ratio exception references unavailable evidence")
    behavior_ids = set()
    for card in cards:
        if set(card["prerequisites"]) - set(ids) or card["candidate_id"] in card["prerequisites"]:
            raise Invalid("Candidate prerequisite is missing or self-referential")
        for obligation in card["obligations"].values():
            if set(obligation["evidence_ids"]) - evidence_ids:
                raise Invalid("Obligation references unavailable evidence")
            if obligation["status"] != "UNKNOWN" and (not obligation["explanation"].strip() or not obligation["evidence_ids"]):
                raise Invalid("Supported, conflicted, and inapplicable obligations require explanations and evidence")
        for behavior in card["behaviors"]:
            if behavior["id"] in behavior_ids:
                raise Invalid("Behavior IDs must be unique across the plan")
            behavior_ids.add(behavior["id"])
            if set(behavior["check_ids"]) - set(checks):
                raise Invalid("Behavior references an unknown check")
    for check in checks.values():
        if set(check["contract_ids"]) - behavior_ids:
            raise Invalid("Check references an unknown behavior contract")
    visiting, visited = set(), set()
    by_id = {x["candidate_id"]: x for x in cards}
    def visit(key):
        if key in visiting:
            raise Invalid("Plan prerequisite graph contains a cycle")
        if key in visited:
            return
        visiting.add(key)
        for parent in by_id[key]["prerequisites"]:
            visit(parent)
        visiting.remove(key); visited.add(key)
    for key in ids:
        visit(key)
    return known


def plan(args):
    run, manifest = open_run(args.run)
    current = state(run)
    assessment = read_json(args.assessment or run / "assessment.json")
    known = check_assessment(run, manifest, assessment, current)
    scope = set(manifest["scope"]["paths"])
    for card in assessment["candidates"]:
        scope.update(known[card["candidate_id"]]["paths"])
    for item in current["evidence"]:
        record = read_json(run / item["path"])
        if record["kind"] == "source" and record["relation"] in ("consumer", "dependency", "test", "configuration", "parallel"):
            scope.add(record["path"])
    prs = []
    for card in assessment["candidates"]:
        if card["disposition"] == "REJECTED":
            continue
        prs.append({"pr_id": "PR-" + card["candidate_id"], "candidate_ids": [card["candidate_id"]],
                    "responsibility": card["responsibility"], "target_owner": card["target_owner"],
                    "paths": known[card["candidate_id"]]["paths"], "depends_on": ["PR-" + x for x in card["prerequisites"]],
                    "rollback": card["rollback"], "expected_added": card["estimated_added"],
                    "expected_removed": card["estimated_removed"], "status": "PROPOSED"})
    if not prs:
        raise Invalid("Plan contains no proposed responsibility transitions")
    assigned = {c for pr in prs for c in pr["candidate_ids"]}
    if any(set(x["prerequisites"]) - assigned for x in assessment["candidates"] if x["candidate_id"] in assigned):
        raise Invalid("A proposed candidate depends on a rejected candidate")
    missing = any(x["expected_added"] is None or x["expected_removed"] is None for x in prs)
    total = None if missing else {"added": sum(x["expected_added"] for x in prs), "removed": sum(x["expected_removed"] for x in prs)}
    if total is not None:
        total["net"] = total["added"] - total["removed"]
    value = {"schema_version": 1, "run_id": manifest["run_id"], "plan_id": "PLAN-" + digest(encoded(assessment))[:16],
             "baseline_digest": manifest["snapshots"]["head"]["digest"], "assessment": assessment,
             "scope_paths": sorted(scope),
             "prs": prs, "expected_total": total, "status": "PROPOSED", "policy": manifest["policy"],
             "evidence_artifacts": {x["path"]: current["artifacts"][x["path"]] for x in current["evidence"]}}
    name = "plans/" + value["plan_id"] + ".json"
    artifact(run, current, name, value)
    current["latest_plan"] = name
    write(run, "state.json", current)
    write(run, "responsibility-target.json", {"plan_id": value["plan_id"], "status": "PROPOSED",
                                              "responsibilities": [{"candidate_id": x["candidate_id"], "statement": x["responsibility"], "surface": x["surface"]} for x in assessment["candidates"]]})
    render(run, {"schema_version": 1, "run_id": manifest["run_id"], "stage": "PLANNED", "verdict": "INCOMPLETE",
                 "complete": False, "plan": value, "code_mass": read_json(run / "code-mass.json"),
                 "gaps": ["Plan is a proposed transition; estimates are not verified savings"]})
    return {"plan": str(run / name), "status": "PROPOSED", "expected_total": total}


def import_graph(args):
    run, manifest = open_run(args.run)
    current = state(run)
    value = read_json(args.file)
    validate(value, read_json(SCHEMAS / "graph.schema.json"))
    snapshot = manifest["snapshots"][args.side]
    if value["snapshot_digest"] != snapshot["digest"]:
        raise Invalid("Imported graph belongs to a different snapshot")
    ids = [node["id"] for node in value["nodes"]]
    if len(ids) != len(set(ids)):
        raise Invalid("Imported graph node IDs must be unique")
    for node in value["nodes"]:
        path = relative(node["path"])
        if path not in snapshot["files"] or node["source_sha256"] != snapshot["files"][path]["sha256"]:
            raise Invalid("Imported graph source identity mismatch")
        lines = content(run, snapshot, path).decode("utf-8").splitlines()
        if not 1 <= node["start"] <= node["end"] <= len(lines):
            raise Invalid("Imported graph coordinates are out of range")
    if any(e["from"] not in ids or e["to"] not in ids for e in value["edges"]):
        raise Invalid("Imported graph has an unresolved edge endpoint")
    return store_evidence(run, current, {"kind": "local_graph", "side": args.side, "graph": value,
                                        "interpretation": "Provider claims are imported; snapshot binding does not attest indexer execution or completeness"})


def structure(args):
    run, manifest = open_run(args.run)
    current = state(run)
    snapshot = manifest["snapshots"][args.side]
    paths = [relative(path) for path in (args.path or manifest["scope"]["paths"])]
    if any(path not in snapshot["files"] for path in paths):
        raise Invalid("Structural query path is absent from the pinned snapshot")
    executable = shutil.which("ast-grep")
    capability = probe() if executable else {"status": "UNAVAILABLE", "reason": "ast-grep is not installed locally"}
    records, nodes, edges = [], [], []
    for path in paths:
        record = {"path": path, "source_sha256": snapshot["files"][path]["sha256"]}
        if capability["status"] != "PASS" or snapshot["files"][path]["mode"] not in ("100644", "100755"):
            records.append({**record, "status": "UNAVAILABLE", "reason": "Local tool, containment, or regular source bytes are unavailable"})
            continue
        data = content(run, snapshot, path)
        with tempfile.TemporaryDirectory(prefix="simplify-structure-", dir=Path(tempfile.gettempdir()).resolve()) as name:
            work = Path(name)
            source = work / ("input" + Path(path).suffix)
            source.write_bytes(data)
            config = work / "sgconfig.yml"
            config.write_text("ruleDirs: []\n")
            argv = [executable, "outline", "--config", str(config), "--items", "all", "--view", "expanded", "--json=compact", str(source)]
            if args.lang:
                argv.extend(["--lang", args.lang])
            receipt, raw = execute(argv, work, work, 60)
            record.update(receipt)
            record["log_sha256"] = digest(raw)
            record["log"] = raw.decode("utf-8", "replace")
            if record["status"] == "PASS":
                try:
                    outputs = json.loads(raw)
                    if len(outputs) != 1 or outputs[0]["path"] != str(source):
                        raise Invalid("Indexer did not identify the requested source file")
                    def add(entry, parent=None):
                        offset = entry["range"]["byteOffset"]
                        start, end = offset["start"], offset["end"]
                        if not 0 <= start < end <= len(data):
                            raise Invalid("Indexer returned invalid source coordinates")
                        identity = "SYM-" + digest(encoded([path, start, end, entry["name"]]))[:16]
                        nodes.append({"id": identity, "name": entry["name"], "kind": entry["symbolType"],
                                      "path": path, "source_sha256": record["source_sha256"],
                                      "start": data[:start].count(b"\n") + 1, "end": data[:end - 1].count(b"\n") + 1,
                                      "excerpt_sha256": digest(data[start:end]), "confidence": "structural"})
                        if parent:
                            edges.append({"from": identity, "to": parent, "kind": "MEMBER_OF", "confidence": "structural"})
                        for child in entry.get("members", []):
                            add(child, identity)
                    for entry in outputs[0]["items"]:
                        add(entry)
                except (Invalid, ValueError, KeyError, TypeError) as exc:
                    record.update(status="UNAVAILABLE", reason=str(exc))
            records.append(record)
    if fingerprint(Path(manifest["repository"]), run)["sha256"] != manifest["source_fingerprint"]:
        raise Invalid("STALE: source changed during structural indexing")
    result = store_evidence(run, current, {"kind": "executed_structure", "side": args.side,
        "snapshot_digest": snapshot["digest"], "provider": "ast-grep/tree-sitter", "isolation": capability,
        "tool_sha256": digest(Path(executable).read_bytes()) if executable else None,
        "records": records, "nodes": nodes, "edges": edges,
        "coverage": "Requested files, bundled top-level outline declarations/imports/exports and direct members only; no resolved-call or absence proof"})
    return {**result, "status": "RECORDED", "coverage_status": "AVAILABLE" if records and all(x["status"] == "PASS" for x in records) else "INCOMPLETE",
            "nodes": len(nodes), "paths": paths}


def verify(args):
    old, original = open_run(args.run, current=False)
    current = state(old)
    plan_path = relative(args.plan or current.get("latest_plan", ""))
    if plan_path not in current["artifacts"]:
        raise Invalid("Plan is not bound to the source run")
    planned = read_json(old / plan_path)
    assessment = planned["assessment"]
    known = check_assessment(old, original, assessment, current)
    if planned["baseline_digest"] != original["snapshots"]["head"]["digest"]:
        raise Invalid("Plan baseline mismatch")
    repo = Path(original["repository"])
    output = make_output(repo, args.output)
    initial = fingerprint(repo, output)
    baseline = copy.deepcopy(original["snapshots"]["head"])
    for item in baseline["files"].values():
        if item["sha256"] is not None:
            write(output, "blobs/" + item["sha256"], (old / "blobs" / item["sha256"]).read_bytes(), raw=True)
    head = resolve(repo, args.head or "HEAD", optional=args.working_tree)
    target = capture(repo, head, output, working=args.working_tree)
    snapshots = {"base": baseline, "head": target}
    policy = original["policy"]
    scopes = (original["scope"]["requested"] or []) + planned["scope_paths"]
    _, selected = scope_paths(baseline, target, scopes)
    inventories = {side: inventory(output, snap, policy) for side, snap in snapshots.items()}
    mass = measure(baseline, target, inventories, selected, policy)
    changed = [p for p in set(baseline["files"]) | set(target["files"]) if baseline["files"].get(p) != target["files"].get(p)]
    outside = [p for p in changed if p not in selected and category(p, policy) not in ("excluded", "documentation_or_asset")]
    gaps, failures = [], []
    if outside:
        gaps.append("Maintained changes outside planned scope: " + ", ".join(sorted(outside)))
    active = [x for x in assessment["candidates"] if x["disposition"] != "REJECTED"]
    def owner_exists(owner, side):
        if "::" in owner:
            path, symbol = owner.split("::", 1)
            return any(x["name"] == symbol for x in inventories[side].get(path, {}).get("symbols", []))
        return owner in snapshots[side]["files"]
    surfaces = []
    for card in active:
        if card["disposition"] == "BLOCKED":
            failures.append(card["candidate_id"] + ": blocked by the local assessment")
        if not card["responsibility"].strip() or not card["target_owner"].strip() or not card["rollback"].strip() or not card["rationale"].strip():
            gaps.append(card["candidate_id"] + ": responsibility, target owner, or rollback is incomplete")
        if not owner_exists(card["target_owner"], "head"):
            failures.append(card["candidate_id"] + ": canonical target owner is absent")
        if not card["remove"]:
            gaps.append(card["candidate_id"] + ": no specific obsolete mechanism was named")
        for removed in card["remove"]:
            if not owner_exists(removed, "base"):
                gaps.append(card["candidate_id"] + ": removed mechanism was absent from baseline: " + removed)
            if owner_exists(removed, "head"):
                failures.append(card["candidate_id"] + ": obsolete mechanism remains: " + removed)
        gaps.extend(card["unresolved"])
        for name, obligation in card["obligations"].items():
            if obligation["status"] == "UNKNOWN":
                gaps.append(card["candidate_id"] + ": " + name + " is unresolved")
            elif obligation["status"] == "CONFLICTED":
                failures.append(card["candidate_id"] + ": " + name + " has contradictory evidence")
        if not card["behaviors"]:
            gaps.append(card["candidate_id"] + ": no declared observable behaviors")
        for behavior in card["behaviors"]:
            linked = [c for c in assessment["checks"] if c["id"] in behavior["check_ids"] and behavior["id"] in c["contract_ids"]]
            if not linked:
                gaps.append(behavior["id"] + ": no bidirectionally mapped executable check")
            kinds = {c["kind"] for c in linked}
            if "end_to_end" not in kinds:
                gaps.append(behavior["id"] + ": no end-to-end check")
            if behavior["crosses_seam"] and "integration" not in kinds:
                gaps.append(behavior["id"] + ": no integration check for its declared seam")
        vector = {name: {"before": len(v["before"]), "after": len(v["after"]),
                         "removed": sorted(set(v["before"]) - set(v["after"])),
                         "added": sorted(set(v["after"]) - set(v["before"]))} for name, v in card["surface"].items()}
        if not any(v["after"] < v["before"] for v in vector.values()):
            failures.append(card["candidate_id"] + ": no declared conceptual reduction")
        surfaces.append({"candidate_id": card["candidate_id"], "provenance": "analyst declaration", "vector": vector})
    harness = {}
    if args.harness:
        harness_root = safe_path(args.harness)
        for path in sorted(harness_root.rglob("*")):
            safe_path(path)
            if path.is_file():
                harness[path.relative_to(harness_root).as_posix()] = path.read_bytes()
    capability, receipts = run_checks(output, snapshots, assessment["checks"], harness)
    if not receipts:
        gaps.append("No repository-native checks were supplied")
    for receipt in receipts:
        if receipt["status"] in ("FAIL", "TIMEOUT"):
            failures.append(receipt["check_id"] + " on " + receipt["side"] + ": " + receipt["status"])
        elif receipt["status"] != "PASS":
            gaps.append(receipt["check_id"] + " on " + receipt["side"] + ": unavailable")
    if mass["status"] != "MEASURED":
        gaps.append("Maintained-code accounting is incomplete")
    elif mass["net"] >= 0 or not mass["removed"]:
        failures.append("Completed transition does not reduce eligible maintained code")
    elif mass["ratio_status"] != "PASS" and not assessment.get("ratio_exception"):
        failures.append("Removal/addition ratio is below the configured completed-transition target")
    final = fingerprint(repo, output)
    execution_verdict = "STALE" if final["sha256"] != initial["sha256"] else "FAIL" if failures else "INCOMPLETE" if gaps else "PASS"
    verdict = execution_verdict if execution_verdict != "PASS" else "INCOMPLETE"
    result = {"schema_version": 1, "run_id": "verify:" + uuid.uuid4().hex, "plan_id": planned["plan_id"],
              "verdict": verdict, "execution_verdict": execution_verdict, "complete": False, "stage": "CHECKS_EXECUTED",
              "failures": failures, "gaps": sorted(set(gaps)), "code_mass": mass, "conceptual_surface": surfaces,
               "checks": receipts, "isolation": capability, "plan_sha256": digest(encoded(planned)),
              "responsibilities": [{k: card[k] for k in ("candidate_id", "responsibility", "target_owner", "remove", "rationale", "rollback")} for card in active],
               "semantic_evidence": "Imported analyst judgments; executable checks establish only exercised behavior",
               "harness_sha256": digest(encoded({p: digest(v) for p, v in harness.items()})),
              "ratio_exception": assessment.get("ratio_exception") if mass["status"] == "MEASURED" and mass["net"] < 0 and mass["ratio_status"] == "BELOW_TARGET" else None,
              "source_integrity": "UNCHANGED" if final["sha256"] == initial["sha256"] else "CHANGED"}
    manifest = {**original, "run_id": result["run_id"], "snapshots": snapshots,
                "source_fingerprint": initial["sha256"], "origin_plan": planned["plan_id"]}
    write(output, "manifest.json", manifest)
    write(output, "plan.json", planned)
    write(output, "integrity-before.json", initial)
    write(output, "integrity-after.json", final)
    write(output, "code-mass.json", mass)
    write(output, "execution-report.json", result)
    result = copy.deepcopy(result)
    result["gaps"].append("Complete the local semantic review of this exact implementation before finalizing")
    write(output, "verification-report.json", result)
    write(output, "target-review.json", {"schema_version": 1, "run_id": result["run_id"], "plan_id": planned["plan_id"],
                                         "target_snapshot_digest": target["digest"], "reviewer": "", "candidates": [
                                         {"candidate_id": x["candidate_id"], "conclusion": "UNKNOWN", "covered_obligations": [],
                                          "statement": "Review the pinned replacement against each preservation obligation", "unresolved": [], "evidence": []} for x in active]})
    seal(output, ["manifest.json", "plan.json", "integrity-before.json", "integrity-after.json", "code-mass.json", "execution-report.json"])
    write(output, "state.json", {"schema_version": 1, "artifacts": {}, "evidence": [], "manual_candidates": []})
    render(output, result)
    return {"run": str(output), **result}


def finalize(args):
    run, manifest = open_run(args.run)
    current = state(run)
    review = read_json(args.review or run / "target-review.json")
    validate(review, read_json(SCHEMAS / "target-review.schema.json"))
    result = read_json(run / "execution-report.json")
    planned = read_json(run / "plan.json")
    if review["run_id"] != manifest["run_id"] or review["plan_id"] != planned["plan_id"] or review["target_snapshot_digest"] != manifest["snapshots"]["head"]["digest"]:
        raise Invalid("Target review is bound to a different implementation")
    expected = {x["candidate_id"] for x in planned["assessment"]["candidates"] if x["disposition"] != "REJECTED"}
    ids = [x["candidate_id"] for x in review["candidates"]]
    if set(ids) != expected or len(ids) != len(set(ids)):
        raise Invalid("Target review must cover every proposed candidate exactly once")
    for card in review["candidates"]:
        if set(card["covered_obligations"]) != set(OBLIGATIONS):
            result["gaps"].append(card["candidate_id"] + ": target review does not cover all preservation obligations")
        result["gaps"].extend(card["unresolved"])
        if card["conclusion"] == "UNKNOWN":
            result["gaps"].append(card["candidate_id"] + ": target review is inconclusive")
        if card["conclusion"] == "CONFLICTED":
            result["failures"].append(card["candidate_id"] + ": target review found contradictory evidence")
        if not any(x["side"] == "head" for x in card["evidence"]):
            result["gaps"].append(card["candidate_id"] + ": target review has no implementation evidence")
        for item in card["evidence"]:
            snap = manifest["snapshots"][item["side"]]
            path = relative(item["path"])
            if path not in snap["files"] or snap["files"][path]["sha256"] != item["source_sha256"]:
                raise Invalid("Target review evidence does not match the pinned source")
            lines = content(run, snap, path).decode("utf-8").splitlines()
            if not 1 <= item["start"] <= item["end"] <= len(lines):
                raise Invalid("Target review source coordinates are invalid")
    if fingerprint(Path(manifest["repository"]), run)["sha256"] != manifest["source_fingerprint"]:
        raise Invalid("STALE: repository changed during final review")
    result["verdict"] = "STALE" if result["execution_verdict"] == "STALE" else "FAIL" if result["failures"] else "INCOMPLETE" if result["gaps"] else "PASS"
    result["complete"] = not result["gaps"] and result["verdict"] != "STALE"
    result["stage"] = "FINALIZED"
    result["target_review_sha256"] = digest(encoded(review))
    result["deletion_safety"] = "SAFE_WITH_REPLACEMENT" if result["verdict"] == "PASS" else "UNKNOWN"
    if result["verdict"] == "PASS":
        result["code_mass"]["validated_removal_credit"] = result["code_mass"]["removed"]
    artifact(run, current, "target-review-final.json", review)
    artifact(run, current, "verification-report.json", result)
    write(run, "state.json", current)
    render(run, result)
    return {"run": str(run), **result}


def report(args):
    run, manifest = open_run(args.run)
    current = state(run)
    if "origin_plan" in manifest:
        if "verification-report.json" in current["artifacts"]:
            result = read_json(run / "verification-report.json")
        else:
            result = read_json(run / "execution-report.json")
            result["gaps"].append("Complete the local semantic review of this exact implementation before finalizing")
        write(run, "verification-report.json", result)
    else:
        result = {"schema_version": 1, "run_id": manifest["run_id"], "verdict": "INCOMPLETE", "complete": False,
                  "stage": "AUDITED", "code_mass": read_json(run / "code-mass.json"),
                  "candidate_count": len(all_candidates(run, current)),
                  "gaps": ["Semantic grounding and implementation verification remain"]}
        if current.get("latest_plan"):
            if current["latest_plan"] not in current["artifacts"]:
                raise Invalid("Latest plan has no content binding")
            result.update(stage="PLANNED", plan=read_json(run / relative(current["latest_plan"])),
                          gaps=["Plan is a proposed transition; estimates are not verified savings"])
    render(run, result)
    return {"verdict": result["verdict"], "report": str(run / "simplification-report.html")}


def invalidate(path, status, reason):
    run = safe_path(path)
    if not (run / "manifest.json").is_file():
        return
    result = {"verdict": status, "complete": False, "gaps": [reason],
              "code_mass": {"validated_removal_credit": None}}
    try:
        _, manifest = open_run(run, current=False)
        result["run_id"] = manifest["run_id"]
        if "origin_plan" in manifest:
            result = read_json(run / "execution-report.json")
        else:
            result["code_mass"] = read_json(run / "code-mass.json")
        result.update(verdict=status, complete=False, stage="EVIDENCE_CHECK", historical_only=True)
        result["gaps"] = sorted(set([*result.get("gaps", []), reason]))
        result["code_mass"]["validated_removal_credit"] = None
    except (Invalid, OSError, KeyError, TypeError, ValueError):
        pass
    render(run, result)
    if (run / "execution-report.json").is_file():
        write(run, "verification-report.json", result)
        current = read_json(run / "state.json")
        current["artifacts"]["verification-report.json"] = digest(encoded(result))
        write(run, "state.json", current)


def doctor(args):
    return {"framework_version": VERSION, "python": sys.version.split()[0], "git": shutil.which("git"),
            "native_check_isolation": probe(), "maintained_sloc_adapters": ["Python", "JSON"],
            "optional_tools": {name: shutil.which(name) for name in ("scc", "tokei", "tree-sitter", "ast-grep", "scip", "codeql")},
            "model_execution": "none", "automatic_installation": False}
