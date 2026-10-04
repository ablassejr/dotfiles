"""Language adapters, code-mass accounting, and candidate discovery."""

import ast
from collections import Counter, defaultdict
import copy
import difflib
import fnmatch
import io
import json
from pathlib import Path
import re
import tokenize

from .storage import Invalid, content, digest, encoded, relative


DIMENSIONS = ("authoritative_owners", "state_representations", "runtime_paths",
              "public_contracts", "internal_abstractions", "configuration_switches",
              "runtime_dependencies")
OBLIGATIONS = ("consumers", "dynamic_use", "contracts", "behavior", "replacement",
               "failure_paths", "state_ownership", "history", "test_preservation")
DEFAULT_POLICY = {
    "schema_version": 1, "minimum_ratio": 1.2, "ratio_applies_to": "completed_transition",
    "success_requires": ["behavior_preserved", "net_code_reduction", "conceptual_reduction"],
    "exclude": ["**/node_modules/**", "node_modules/**", "**/vendor/**", "vendor/**",
                "**/generated/**", "generated/**", "**/__pycache__/**", "**/.venv/**",
                ".venv/**", "dist/**", "build/**", "**/*.min.js", "**/*.lock", "*.lock",
                "package-lock.json", "pnpm-lock.yaml", "yarn.lock", "**/package-lock.json"],
    "test_paths": ["tests/**", "test/**", "**/tests/**", "**/test/**", "test_*.py",
                   "**/test_*.py", "**/*_test.py", "**/*.test.*", "**/*.spec.*"],
    "infrastructure_paths": ["infra/**", "infrastructure/**", "**/*.tf"],
    "build_paths": [".github/**", "scripts/**", "build.py", "setup.py", "package.json"],
}
DOCUMENT_EXTENSIONS = {".md", ".rst", ".txt", ".adoc", ".svg", ".png", ".jpg", ".pdf",
                       ".jpeg", ".gif", ".ico", ".woff", ".woff2"}


def matches(path, patterns):
    return any(fnmatch.fnmatchcase(path, pattern) for pattern in patterns)


def category(path, policy):
    if matches(path, policy["exclude"]):
        return "excluded"
    if Path(path).suffix.lower() in DOCUMENT_EXTENSIONS or Path(path).name.upper().startswith(("LICENSE", "NOTICE", "COPYING")):
        return "documentation_or_asset"
    for key, name in (("test_paths", "tests"), ("infrastructure_paths", "infrastructure"),
                      ("build_paths", "build")):
        if matches(path, policy[key]):
            return name
    if Path(path).suffix.lower() in (".json", ".toml", ".yaml", ".yml", ".ini", ".cfg") or Path(path).name.startswith("."):
        return "configuration"
    return "production"


def policy_from(value=None):
    result = copy.deepcopy(DEFAULT_POLICY)
    if value:
        if set(value) - set(result):
            raise Invalid("Unknown maintained-code policy keys")
        result.update(value)
    for name in ("exclude", "test_paths", "infrastructure_paths", "build_paths"):
        if not isinstance(result[name], list) or any(not isinstance(x, str) or not x for x in result[name]):
            raise Invalid(f"Policy {name} must be a list of nonempty glob strings")
    if type(result["minimum_ratio"]) not in (int, float) or result["minimum_ratio"] <= 1:
        raise Invalid("The removal/addition target must be a finite number greater than one")
    if result["ratio_applies_to"] != "completed_transition" or result["success_requires"] != DEFAULT_POLICY["success_requires"]:
        raise Invalid("This version evaluates complete behavior-preserving transitions with both reduction dimensions")
    return result


def python_adapter(data):
    module = ast.parse(data)
    tokens = list(tokenize.tokenize(io.BytesIO(data).readline))
    docs = set()
    for node in ast.walk(module):
        body = getattr(node, "body", None)
        if isinstance(node, (ast.Module, ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef)) and body and isinstance(body[0], ast.Expr) and isinstance(body[0].value, ast.Constant) and isinstance(body[0].value.value, str):
            doc = body[0].value
            docs.add((doc.lineno, doc.col_offset, doc.end_lineno, doc.end_col_offset))
    lines, signatures, units = set(), defaultdict(list), []
    ignored = {tokenize.ENCODING, tokenize.ENDMARKER, tokenize.NEWLINE, tokenize.NL,
               tokenize.INDENT, tokenize.DEDENT, tokenize.COMMENT}
    for token in tokens:
        if token.type in ignored or (token.start[0], token.start[1], token.end[0], token.end[1]) in docs:
            continue
        if token.type == tokenize.ERRORTOKEN and not token.string.isspace():
            raise Invalid("Python tokenization is incomplete")
        if not token.string.strip():
            continue
        units.append({"value": repr((token.type, token.string)),
                      "lines": list(range(token.start[0], token.end[0] + 1))})
        for line in range(token.start[0], token.end[0] + 1):
            lines.add(line)
            signatures[line].append((token.type, token.string))
    symbols, references = [], []
    def visit(node, prefix="", owner=None):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            qualified = prefix + node.name
            symbols.append({"name": qualified, "short_name": node.name, "kind": type(node).__name__,
                            "start": min([node.lineno, *[x.lineno for x in node.decorator_list]]),
                            "end": node.end_lineno, "ast": ast.dump(node, include_attributes=False)})
            prefix, owner = qualified + ".", qualified
        if isinstance(node, ast.Call):
            references.append({"name": ast.unparse(node.func), "line": node.lineno,
                               "owner": owner, "kind": "CALL_SYNTAX", "confidence": "structural"})
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            references.append({"name": ast.unparse(node), "line": node.lineno,
                               "owner": owner, "kind": "IMPORT_SYNTAX", "confidence": "structural"})
        for child in ast.iter_child_nodes(node):
            visit(child, prefix, owner)
    visit(module)
    return {"adapter": "python-ast-tokenize-v1", "status": "MEASURED", "msloc": len(lines),
             "lines": sorted(lines), "signatures": {str(k): repr(v) for k, v in signatures.items()},
            "units": units,
            "structure": ast.dump(module, include_attributes=False), "symbols": symbols,
            "references": references}


def inspect_file(data, path):
    try:
        if path.endswith((".py", ".pyi")):
            return python_adapter(data)
        if path.endswith(".json"):
            value = json.loads(data)
            text = data.decode("utf-8")
            lines = text.splitlines()
            selected = [i + 1 for i, line in enumerate(lines) if line.strip()]
            units = [{"value": match.group(), "lines": [text.count("\n", 0, match.start()) + 1]}
                     for match in re.finditer(r'"(?:[^"\\]|\\.)*"|[^\s"{}\[\],:]+|[{}\[\],:]', text)]
            return {"adapter": "json-v1", "status": "MEASURED", "msloc": len(selected),
                     "lines": selected, "signatures": {str(i): lines[i - 1].strip() for i in selected},
                    "units": units,
                    "structure": json.dumps(value, sort_keys=True, ensure_ascii=True, allow_nan=False),
                    "symbols": [], "references": []}
        reason = "No exact maintained-SLOC adapter for this file type"
    except (SyntaxError, ValueError, tokenize.TokenError, UnicodeError, Invalid) as exc:
        reason = str(exc)
    return {"adapter": None, "status": "UNKNOWN", "msloc": None, "lines": [],
            "signatures": {}, "structure": None, "symbols": [], "references": [], "reason": reason}


def inventory(run, snapshot, policy):
    result = {}
    for path, item in snapshot["files"].items():
        group = category(path, policy)
        if group in ("excluded", "documentation_or_asset") or item["mode"] in ("120000", "160000"):
            result[path] = {"category": group, "status": "EXCLUDED" if item["mode"] not in ("120000", "160000") else "UNKNOWN",
                            "msloc": None, "symbols": [], "references": [], "signatures": {},
                            "structure": None, "reason": "Non-maintained path, symlink, or nested repository"}
        else:
            result[path] = {"category": group, **inspect_file(content(run, snapshot, path), path)}
        for symbol in result[path]["symbols"]:
            symbol["id"] = path + "::" + symbol["name"]
            symbol["path"] = path
    return result


def scope_paths(base, head, requested, symbol=None, changed_only=False):
    all_paths = set(base["files"]) | set(head["files"])
    if requested:
        scopes = [relative(s).rstrip("/") for s in requested]
        selected = {p for p in all_paths if any(s == "." or p == s or p.startswith(s + "/") for s in scopes)}
    else:
        scopes = []
        selected = {p for p in all_paths if base["files"].get(p) != head["files"].get(p)}
    if not selected and requested:
        raise Invalid("Selected scope has no captured files")
    return scopes, sorted(selected)


def measure(base, head, inventories, selected, policy):
    a, b = inventories["base"], inventories["head"]
    groups = {name: {"before": 0, "after": 0, "net": 0, "unknown": []}
              for name in ("production", "tests", "infrastructure", "build", "configuration")}
    removed, added, raw_removed, raw_added = Counter(), Counter(), 0, 0
    unknown, moves, formatting = [], [], []
    for path in selected:
        left, right = a.get(path), b.get(path)
        for side, entry in (("before", left), ("after", right)):
            if entry and entry["category"] in groups:
                if entry["status"] == "MEASURED":
                    groups[entry["category"]][side] += entry["msloc"]
                else:
                    groups[entry["category"]]["unknown"].append(path)
                    unknown.append(path)
        l = list(left["signatures"].values()) if left and left["status"] == "MEASURED" else []
        r = list(right["signatures"].values()) if right and right["status"] == "MEASURED" else []
        for tag, i, j, k, m in difflib.SequenceMatcher(a=l, b=r, autojunk=False).get_opcodes():
            if tag != "equal":
                raw_removed += j - i; raw_added += m - k
        if left and right and left["status"] == right["status"] == "MEASURED" and left["structure"] == right["structure"]:
            if base["files"][path]["sha256"] != head["files"][path]["sha256"]:
                formatting.append(path)
            continue
        lu = left.get("units", []) if left else []
        ru = right.get("units", []) if right else []
        old_lines, new_lines = set(), set()
        for tag, i, j, k, m in difflib.SequenceMatcher(a=[x["value"] for x in lu], b=[x["value"] for x in ru], autojunk=False).get_opcodes():
            if tag != "equal":
                old_lines.update(line for unit in lu[i:j] for line in unit["lines"])
                new_lines.update(line for unit in ru[k:m] for line in unit["lines"])
        removed.update(left["signatures"][str(line)] for line in old_lines)
        added.update(right["signatures"][str(line)] for line in new_lines)
    matched = removed & added
    removed.subtract(matched); added.subtract(matched)
    escape = []
    for old in selected:
        if old not in base["files"]:
            continue
        sha = base["files"][old]["sha256"]
        for new, item in head["files"].items():
            if old != new and sha is not None and item["sha256"] == sha and base["files"].get(new) != item:
                moves.append({"from": old, "to": new})
                if new not in selected or b[new]["status"] == "EXCLUDED":
                    escape.append({"from": old, "to": new})
    for group in groups.values():
        group["net"] = group["after"] - group["before"]
        group["unknown"] = sorted(set(group["unknown"]))
    before, after = sum(x["before"] for x in groups.values()), sum(x["after"] for x in groups.values())
    d, n = sum(removed.values()), sum(added.values())
    ratio = d / n if n else None
    ratio_status = "UNKNOWN" if unknown or escape else "NO_CHANGE" if not d and not n else "PASS" if not n or ratio >= policy["minimum_ratio"] else "BELOW_TARGET"
    return {"schema_version": 1, "status": "UNKNOWN" if unknown or escape else "MEASURED",
            "method": "physical classified-code totals; token-difference line credit; equal structures excluded; matching line signatures reconciled",
            "components": groups, "known_before": before, "known_after": after,
            "before": None if unknown else before, "after": None if unknown else after,
            "net": None if unknown else after - before, "added": None if unknown or escape else n,
            "removed": None if unknown or escape else d, "ratio": None if unknown or escape else ratio,
            "ratio_kind": "UNKNOWN" if unknown or escape else "INFINITE" if d and not n else "NOT_APPLICABLE" if not d and not n else "FINITE",
            "ratio_status": ratio_status, "target": policy["minimum_ratio"],
            "validated_removal_credit": None, "physical_code_churn": {"added": raw_added, "removed": raw_removed},
            "reconciled_moved_lines": sum(matched.values()), "moves": moves, "scope_escapes": escape,
            "formatting_only_paths": formatting, "unknown_paths": sorted(set(unknown))}


def discover(inventories, selected, symbol_filter=None):
    head = inventories["head"]
    symbols = [x for info in head.values() for x in info["symbols"]]
    selected_ids = {x["id"] for x in symbols if x["path"] in selected and
                    (not symbol_filter or symbol_filter in (x["name"], x["short_name"], x["id"]))}
    if symbol_filter and not selected_ids:
        raise Invalid("Selected symbol was not found by an available syntax adapter")
    buckets = defaultdict(list)
    for item in symbols:
        if item["kind"] in ("FunctionDef", "AsyncFunctionDef"):
            # Names identify the declarations; body equivalence is only a discovery signal.
            normalized = item["ast"].replace("name=" + repr(item["short_name"]), "name='<candidate>'", 1)
            buckets[normalized].append(item)
    candidates = []
    for values in buckets.values():
        if len(values) > 1 and any(x["id"] in selected_ids for x in values):
            ids = sorted(x["id"] for x in values)
            candidates.append({"candidate_id": "CON-" + digest(encoded(ids))[:12],
                               "classification": "PARALLEL_IMPLEMENTATION", "owners": ids,
                               "paths": sorted({x["path"] for x in values}),
                               "statement": "These declarations have the same syntax after normalizing their declaration names.",
                               "safety": "UNKNOWN", "confidence": "STRUCTURALLY_DERIVED",
                               "estimated_added": None, "estimated_removed": None,
                               "unresolved": ["Establish whether these declarations own the same required behavior", "Characterize callers, dynamic uses, contracts, failures, and historical constraints"]})
    for item in symbols:
        if item["id"] not in selected_ids or item["kind"] == "ClassDef":
            continue
        text = item["ast"]
        if "body=[Return(value=Call(" in text and text.count("Return(") == 1:
            candidates.append({"candidate_id": "CON-" + digest(item["id"].encode())[:12],
                               "classification": "PASS_THROUGH_LAYER", "owners": [item["id"]],
                               "paths": [item["path"]], "statement": "A function delegates its returned value to another call; policy and boundary value need review.",
                               "safety": "UNKNOWN", "confidence": "STRUCTURALLY_DERIVED",
                               "estimated_added": None, "estimated_removed": None,
                               "unresolved": ["Determine whether the wrapper protects a public contract, isolation, error semantics, or test boundary"]})
    graph = {"schema_version": 1, "provider": "python-ast", "coverage": "structural-only",
             "nodes": [{k: v for k, v in x.items() if k != "ast"} for x in symbols if x["id"] in selected_ids],
             "edges": [{"path": path, **ref} for path, entry in head.items() for ref in entry["references"]
                       if path in selected],
             "limitations": ["Call expressions do not prove resolved callers", "No absence-of-consumer proof", "Non-Python symbol extraction requires an imported local graph"]}
    return sorted(candidates, key=lambda x: x["candidate_id"]), graph


def assessment_template(run_id, candidates):
    cards = []
    for candidate in candidates:
        cards.append({"candidate_id": candidate["candidate_id"], "responsibility": "",
                      "target_owner": "", "remove": [], "rationale": "", "disposition": "PROPOSED",
                      "obligations": {name: {"status": "UNKNOWN", "explanation": "", "evidence_ids": []} for name in OBLIGATIONS},
                      "surface": {name: {"before": [], "after": []} for name in DIMENSIONS},
                      "behaviors": [], "unresolved": candidate["unresolved"], "rollback": "",
                      "prerequisites": [], "estimated_added": None, "estimated_removed": None})
    return {"schema_version": 1, "run_id": run_id, "candidates": cards, "checks": []}
