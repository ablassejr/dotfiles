#!/usr/bin/env python3
"""Local evidence preparation and report finalization; no model or check execution."""

import argparse
import ast
import difflib
import hashlib
import html
import json
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import sys
import tempfile
import uuid


class ReviewError(Exception):
    pass


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return (json.dumps(value, ensure_ascii=True, sort_keys=True, indent=2) + "\n").encode()


def load_json(path):
    def invalid(value):
        raise ReviewError(f"Non-finite JSON number: {value}")
    try:
        value = json.loads(Path(path).read_text(), parse_constant=invalid)
        if not isinstance(value, dict):
            raise ReviewError(f"Expected a JSON object: {path}")
        return value
    except (ValueError, OSError) as exc:
        raise ReviewError(f"Cannot read JSON: {path}: {exc}") from exc


def no_symlinks(path):
    path = Path(os.path.abspath(path))
    for part in [path, *path.parents]:
        if part.is_symlink():
            raise ReviewError(f"Symlink is not permitted for this path: {part}")
    return path


def within(path, parent):
    return path == parent or parent in path.parents


def local_file(root, relative):
    relative = Path(relative)
    if relative.is_absolute() or ".." in relative.parts:
        raise ReviewError(f"Expected a relative local artifact path: {relative}")
    result = no_symlinks(root / relative)
    if not within(result, root):
        raise ReviewError("Artifact path escapes output")
    return result


def write_bytes(root, relative, data):
    dest = local_file(root, relative)
    dest.parent.mkdir(parents=True, exist_ok=True)
    handle, name = tempfile.mkstemp(prefix=".review-", dir=dest.parent)
    try:
        with os.fdopen(handle, "wb") as stream:
            stream.write(data)
        os.replace(name, dest)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def write_json(root, relative, value):
    write_bytes(root, relative, encoded(value))


def git(repo, *args, ok=(0,)):
    executable = shutil.which("git")
    if not executable:
        raise ReviewError("Local Git is unavailable; no installation was attempted")
    env = {"PATH": os.environ.get("PATH", os.defpath), "LC_ALL": "C",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": os.devnull,
           "GIT_CONFIG_GLOBAL": os.devnull, "GIT_OPTIONAL_LOCKS": "0",
           "GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1",
           "GIT_ALLOW_PROTOCOL": "", "GIT_TERMINAL_PROMPT": "0",
           "GIT_LITERAL_PATHSPECS": "1"}
    command = [executable, "--no-pager", "-C", str(repo),
               "-c", "core.fsmonitor=false", "-c", f"core.hooksPath={os.devnull}",
               "-c", "credential.helper=", "-c", "gc.auto=0",
               "-c", "maintenance.auto=false", *args]
    try:
        result = subprocess.run(command, env=env, stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE, timeout=120, check=False)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise ReviewError(f"Local Git command unavailable: {args[0]}: {exc}") from exc
    if result.returncode not in ok:
        detail = result.stderr.decode("utf-8", "replace").strip()
        raise ReviewError(f"Local Git {args[0]} failed: {detail}; no fetch was attempted")
    return result.stdout


def resolve(repo, ref, optional=False):
    raw = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}",
              ok=(0, 128, 1) if optional else (0,)).strip().decode()
    if optional and not raw:
        return None
    if not re.fullmatch(r"[0-9a-f]{40}|[0-9a-f]{64}", raw):
        raise ReviewError(f"Not a local commit: {ref}")
    return raw


def git_path(repo, option):
    value = os.fsdecode(git(repo, "rev-parse", option).strip())
    return (repo / value).resolve() if not Path(value).is_absolute() else Path(value).resolve()


def hash_file(path):
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while block := stream.read(1024 * 1024):
            h.update(block)
    return h.hexdigest()


def fingerprint(repo, output):
    roots = [("repository", repo)]
    for option in ("--absolute-git-dir", "--git-common-dir"):
        candidate = git_path(repo, option)
        if not any(within(candidate, root) for _, root in roots):
            roots.append((f"git-{len(roots)}", candidate))
    entries = {}

    def visit(path, key):
        if within(path, output):
            return
        info = path.lstat()
        mode = stat.S_IMODE(info.st_mode)
        if stat.S_ISLNK(info.st_mode):
            item = {"kind": "symlink", "mode": mode,
                    "sha256": digest(os.fsencode(os.readlink(path)))}
        elif stat.S_ISREG(info.st_mode):
            item = {"kind": "file", "mode": mode, "sha256": hash_file(path)}
        elif stat.S_ISDIR(info.st_mode):
            item = {"kind": "directory", "mode": mode}
        else:
            item = {"kind": "special", "mode": info.st_mode}
        entries[key] = item
        if path.name == ".git" and item["kind"] in ("file", "symlink"):
            for option in ("--absolute-git-dir", "--git-common-dir"):
                candidate = git_path(path.parent, option)
                if not any(within(candidate, existing) for _, existing in roots):
                    roots.append((f"git-{len(roots)}", candidate))
        if item["kind"] == "directory":
            for child in sorted(path.iterdir()):
                visit(child, key + "/" + child.name)

    try:
        for label, root in roots:
            visit(root, label)
    except OSError as exc:
        raise ReviewError(f"Cannot fingerprint all repository inputs: {exc}") from exc
    return {"sha256": digest(encoded(entries)), "entries": entries,
            "roots": [str(root) for _, root in roots],
            "method": "sha256-bytes-kind-mode-no-symlink-following"}


def object_tree(repo, commit):
    if commit is None:
        return {}
    result = {}
    for record in git(repo, "ls-tree", "-r", "-z", "--full-tree", commit).split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            mode, kind, oid = metadata.decode().split()
            result[os.fsdecode(name)] = {"mode": mode, "oid": oid, "kind": kind}
    return result


def index_tree(repo, allow_unmerged=False):
    result = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if record:
            metadata, name = record.split(b"\t", 1)
            mode, oid, stage = metadata.decode().split()
            if stage != "0":
                if allow_unmerged:
                    return None
                raise ReviewError("The index contains unresolved merge stages")
            result[os.fsdecode(name)] = {"mode": mode, "oid": oid,
                                        "kind": "commit" if mode == "160000" else "blob"}
    return result


def same_tree(repo, first, second):
    return set(first) == set(second) and all(first[n]["mode"] == second[n]["mode"] and source_bytes(repo, first, n) == source_bytes(repo, second, n) for n in first)


def working_tree(repo, index, output, visited=None):
    visited = set(visited or ()) | {repo.resolve()}
    names = set(index)
    names.update(os.fsdecode(p) for p in git(repo, "ls-files", "--others",
                                           "--exclude-standard", "-z").split(b"\0") if p)
    result = {}
    for name in sorted(names):
        path = repo / name
        if within(Path(os.path.abspath(path)), output):
            continue
        if index.get(name, {}).get("mode") == "160000":
            entry = dict(index[name])
            no_symlinks(path)
            if path.is_dir() and (path / ".git").exists() and path.resolve() not in visited:
                entry["oid"] = resolve(path, "HEAD")
                subindex = index_tree(path, allow_unmerged=True)
                subwork = working_tree(path, subindex, output, visited) if subindex is not None else None
                entry["dirty"] = subindex is None or not same_tree(path, object_tree(path, entry["oid"]), subindex) or not same_tree(path, subindex, subwork)
            else:
                entry["unavailable"] = True
            result[name] = entry
            continue
        if not path.exists() and not path.is_symlink():
            continue
        for parent in path.parents:
            if parent == repo:
                break
            if parent.is_symlink():
                raise ReviewError(f"Source path traverses a symlink: {name}")
        info = path.lstat()
        if path.is_symlink():
            data, mode = os.fsencode(os.readlink(path)), "120000"
        elif path.is_file():
            data = path.read_bytes()
            mode = "100755" if info.st_mode & stat.S_IXUSR else "100644"
        else:
            raise ReviewError(f"Unsupported working-tree file kind: {name}")
        result[name] = {"mode": mode, "kind": "working", "sha256": digest(data)}
    return result


def source_bytes(repo, tree, name):
    if name is None or name not in tree:
        return b""
    entry = tree[name]
    if entry["mode"] == "160000":
        suffix = "-dirty" if entry.get("dirty") else " (local contents unavailable)" if entry.get("unavailable") else ""
        return ("Subproject commit " + entry["oid"] + suffix + "\n").encode()
    if entry["kind"] != "working":
        return git(repo, "cat-file", "blob", entry["oid"])
    path = repo / name
    if path.is_symlink():
        data = os.fsencode(os.readlink(path))
    else:
        no_symlinks(path)
        data = path.read_bytes()
    if digest(data) != entry["sha256"]:
        raise ReviewError(f"Captured working-tree content changed: {name}")
    return data


def exact_pairs(repo, left, right):
    removed = sorted(set(left) - set(right))
    added = sorted(set(right) - set(left))
    pairs = []
    by_hash = {}
    for name in removed:
        key = (left[name]["mode"], digest(source_bytes(repo, left, name)))
        by_hash.setdefault(key, []).append(name)
    for name in added:
        key = (right[name]["mode"], digest(source_bytes(repo, right, name)))
        if by_hash.get(key):
            old = by_hash[key].pop(0)
            pairs.append(("R100", old, name))
            removed.remove(old)
        else:
            pairs.append(("A", None, name))
    pairs.extend(("D", name, None) for name in removed)
    for name in sorted(set(left) & set(right)):
        if left[name]["mode"] != right[name]["mode"] or source_bytes(repo, left, name) != source_bytes(repo, right, name):
            pairs.append(("M", name, name))
    return sorted(pairs, key=lambda item: item[2] or item[1])


def git_pairs(repo, revisions):
    data = git(repo, "diff", "--no-ext-diff", "--no-textconv", "--name-status",
               "--find-renames", "--ignore-submodules=none", "-z", *revisions, "--")
    parts = iter(data.split(b"\0")[:-1])
    result = []
    for status_bytes in parts:
        status = status_bytes.decode()
        name = os.fsdecode(next(parts))
        if status.startswith(("R", "C")):
            result.append((status, name, os.fsdecode(next(parts))))
        elif status == "A":
            result.append((status, None, name))
        elif status == "D":
            result.append((status, name, None))
        else:
            result.append((status, name, name))
    return result


def text_lines(data):
    if b"\0" in data:
        return None
    try:
        return data.decode("utf-8").splitlines(keepends=True)
    except UnicodeDecodeError:
        return None


def python_symbols(data, intervals):
    try:
        root = ast.parse(data)
    except (SyntaxError, ValueError) as exc:
        return {"status": "UNAVAILABLE", "reason": str(exc), "symbols": []}
    symbols = []
    for node in ast.walk(root):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            start = min([node.lineno, *[d.lineno for d in node.decorator_list]])
            if any(start <= end and node.end_lineno >= begin for begin, end in intervals):
                symbols.append({"name": node.name, "start_line": start,
                                "end_line": node.end_lineno, "kind": type(node).__name__})
    return {"status": "AVAILABLE", "symbols": symbols,
            "limitation": "Syntactic overlap only; module-level changes and call relationships require source review"}


def changes(repo, left, right, pairs, output):
    records = []
    for number, (status, old, new) in enumerate(pairs, 1):
        before, after = source_bytes(repo, left, old), source_bytes(repo, right, new)
        a, b = text_lines(before), text_lines(after)
        binary = a is None or b is None
        item = {"path": new or old, "old_path": old, "new_path": new, "status": status,
                "base_sha256": digest(before), "head_sha256": digest(after),
                "base_mode": left.get(old, {}).get("mode"), "head_mode": right.get(new, {}).get("mode"),
                "binary": binary, "added_lines": None, "removed_lines": None, "hunks": []}
        if item["base_mode"] == "160000" or item["head_mode"] == "160000":
            item["limitation"] = "Gitlink pointer and local dirty state only; nested contents need a separate pinned review"
        if not binary:
            added = removed = 0
            for tag, i, j, k, m in difflib.SequenceMatcher(a=a, b=b, autojunk=False).get_opcodes():
                if tag != "equal":
                    added += m - k
                    removed += j - i
                    item["hunks"].append({"base_start": i + 1, "base_count": j - i,
                                          "head_start": k + 1, "head_count": m - k})
            item.update(added_lines=added, removed_lines=removed)
            patch = "".join(difflib.unified_diff(a, b, fromfile=old or "/dev/null",
                                                tofile=new or "/dev/null"))
            item["patch"] = f"patches/{number:05d}.diff"
            write_bytes(output, item["patch"], patch.encode())
        if (new or old).endswith(".py") and not binary:
            item["base_symbols"] = python_symbols(before, [(h["base_start"], h["base_start"] + max(0, h["base_count"] - 1)) for h in item["hunks"]])
            item["head_symbols"] = python_symbols(after, [(h["head_start"], h["head_start"] + max(0, h["head_count"] - 1)) for h in item["hunks"]])
        else:
            item["head_symbols"] = {"status": "UNAVAILABLE", "reason": "Use an installed local parser or source inspection", "symbols": []}
        records.append(item)
    return records


def pin(repo, args):
    head_now = resolve(repo, "HEAD", optional=True)
    identity = {"repository": str(repo), "mode": "range", "base_ref": args.base,
                "head_ref": args.head or "HEAD", "base_commit": None, "head_commit": None,
                "merge_bases": [], "comparison_base": None, "parent": args.parent,
                "checkout_head": head_now}
    if args.staged or args.working_tree:
        identity.update(mode="staged" if args.staged else "working-tree",
                        base_ref="HEAD", head_ref="INDEX" if args.staged else "WORKING_TREE",
                        base_commit=head_now, head_commit=head_now, comparison_base=head_now)
    elif args.commit:
        commit = resolve(repo, args.commit)
        parents = [s.split()[1] for s in git(repo, "cat-file", "commit", commit).decode("utf-8", "replace").split("\n\n", 1)[0].splitlines() if s.startswith("parent ")]
        if len(parents) > 1 and args.parent is None:
            raise ReviewError("A merge commit requires an explicit --parent number")
        parent = args.parent or 1
        if args.parent is not None and not 1 <= parent <= len(parents):
            raise ReviewError("--parent is outside this commit's parent list")
        baseline = parents[parent - 1] if parents else None
        identity.update(mode="commit", base_ref=None, head_ref=args.commit,
                        base_commit=baseline, head_commit=commit, comparison_base=baseline)
    else:
        if not args.base:
            raise ReviewError("Supply --base, --commit, --staged, or --working-tree")
        base, head = resolve(repo, args.base), resolve(repo, args.head or "HEAD")
        bases = git(repo, "merge-base", "--all", base, head, ok=(0, 1)).decode().splitlines()
        if args.comparison == "merge-base" and len(bases) != 1:
            raise ReviewError("No unique local merge base; supply available history or explicitly choose --comparison direct")
        identity.update(base_commit=base, head_commit=head, merge_bases=bases,
                        comparison_base=bases[0] if args.comparison == "merge-base" else base)
    identity["comparison"] = args.comparison if identity["mode"] == "range" else "snapshot"
    return identity


def assessment_template(analysis_id, records):
    return {"schema_version": "1", "analysis_id": analysis_id,
            "host": {"model": "unverified", "isolation_evidence_id": None},
            "intent": {"status": "unavailable", "explanation": "No authoritative local intent supplied", "evidence_ids": []},
            "behavior_summary": "Review not performed yet.",
            "coverage": [{"path": f["path"], "status": "pending", "evidence_ids": [],
                          "explanation": "Inspect changed behavior and its relevant responsibility domain"} for f in records],
            "lenses": [{"name": name, "status": "pending", "explanation": "Review not performed"} for name in
                       ["correctness", "contracts", "tests", "architecture", "security-reliability", "infrastructure", "debt"]],
            "checks": [], "checks_explanation": "Repository-native checks have not been selected or executed",
            "findings": [], "challenge": {"status": "unavailable", "evidence_id": None,
                                          "reviewer": "", "covered_finding_ids": []},
            "code_mass": {"added": None, "removed": None, "evidence_id": None,
                          "method": "Unknown maintained SLOC", "ratio_removed": None,
                          "ratio_added": None, "ratio_basis": "6:5 direction not supplied"},
            "unresolved_questions": ["Complete context expansion, review passes, native-check selection, and counterevidence challenge"],
            "limitations": []}


def prepare(args):
    requested_repo = Path(args.repo).resolve()
    repo = git_path(requested_repo, "--show-toplevel")
    output = no_symlinks(args.output or Path(tempfile.gettempdir()).resolve() / "personal-pr-review" / uuid.uuid4().hex)
    for protected in (repo, git_path(repo, "--absolute-git-dir"), git_path(repo, "--git-common-dir")):
        if within(protected, output) or (protected != repo and within(output, protected)):
            raise ReviewError("Output overlaps repository root or Git storage")
    if output.exists():
        raise ReviewError("Output must be a new directory; existing runs are never overwritten by prepare")
    output.mkdir(parents=True)
    try:
        before = fingerprint(repo, output)
        identity = pin(repo, args)
        checkout = object_tree(repo, identity["checkout_head"])
        current_index = index_tree(repo, allow_unmerged=not (args.staged or args.working_tree))
        current_work = working_tree(repo, current_index, output) if current_index is not None else None
        identity["working_tree_clean"] = current_index is not None and same_tree(repo, checkout, current_index) and same_tree(repo, current_index, current_work)
        identity["cleanliness_method"] = "raw-byte-and-mode-comparison-with-nonignored-untracked-files"
        left = object_tree(repo, identity["comparison_base"])
        if args.staged or args.working_tree:
            index = index_tree(repo)
            right = working_tree(repo, index, output) if args.working_tree else index
            revisions = ["--cached"] + ([identity["base_commit"]] if identity["base_commit"] else [])
        else:
            right = object_tree(repo, identity["head_commit"])
            revisions = [identity["comparison_base"], identity["head_commit"]]
        pairs = exact_pairs(repo, left, right) if args.working_tree or None in revisions else git_pairs(repo, revisions)
        records = changes(repo, left, right, pairs, output)
        identity["source_fingerprint"] = before["sha256"]
        identity["snapshot_digest"] = digest(encoded({"base": left, "head": right}))
        identity["base_tree"] = None if identity["comparison_base"] is None else git(repo, "rev-parse", identity["comparison_base"] + "^{tree}").decode().strip()
        identity["head_tree"] = git(repo, "rev-parse", identity["head_commit"] + "^{tree}").decode().strip() if identity["mode"] in ("range", "commit") else identity["snapshot_digest"]
        identity["analysis_id"] = "local-review:" + digest(encoded(identity))
        after = fingerprint(repo, output)
        stale = before != after
        capsule = {"schema_version": "1", "identity": identity, "depth": args.depth,
                   "output": str(output), "trees": {"base": left, "head": right}, "changes": records,
                   "rename_method": "exact-content" if args.working_tree or None in revisions else "git-similarity",
                   "limitations": ["Model analysis and repository-native checks are not executed by this helper",
                                   "Local refs do not establish current remote PR state",
                                   "Symbol/call graph completeness requires agent review"]}
        capsule["limitations"].extend(r["path"] + ": " + r["limitation"] for r in records if "limitation" in r)
        write_json(output, "context-packet.json", capsule)
        write_json(output, "integrity-before.json", before)
        write_json(output, "request.json", {"schema_version": "1", "repository": str(repo), "mode": identity["mode"],
                                           "base_ref": identity["base_ref"], "head_ref": identity["head_ref"],
                                           "comparison": identity["comparison"], "parent": args.parent,
                                           "output": str(output), "depth": args.depth})
        write_json(output, "prepared-hashes.json", {name: hash_file(output / name) for name in
                                                    ("request.json", "context-packet.json", "integrity-before.json")})
        write_json(output, "context-manifest.json", {"schema_version": "1", "analysis_id": identity["analysis_id"], "evidence": []})
        write_json(output, "assessment.json", assessment_template(identity["analysis_id"], records))
        write_json(output, "code-mass.json", {"schema_version": "1", "text_added": sum(r["added_lines"] or 0 for r in records),
                                           "text_removed": sum(r["removed_lines"] or 0 for r in records),
                                           "binary_files": sum(r["binary"] for r in records),
                                           "maintained_added": None, "maintained_removed": None,
                                           "ratio_status": "UNKNOWN", "rename_method": capsule["rename_method"]})
        write_json(output, "findings.json", {"schema_version": "1", "analysis_id": identity["analysis_id"], "findings": []})
        write_json(output, "tool-results.json", {"schema_version": "1", "analysis_id": identity["analysis_id"],
                                                 "origin": "bundled-helper", "checks": [],
                                                 "note": "Git inventory completed; native checks not run"})
        summary = {"schema_version": "1", "analysis_id": identity["analysis_id"], "verdict": "STALE" if stale else "INCOMPLETE",
                   "complete": False, "integrity": "CHANGED" if stale else "UNCHANGED",
                   "gaps": ["Preparation is complete; semantic review and native verification remain"],
                   "identity": identity}
        write_json(output, "analysis-summary.json", summary)
        write_bytes(output, "review.md", ("# Local PR review\n\n" + summary["verdict"] + "\n\nPreparation is not a completed review. See assessment.json.\n").encode())
        write_bytes(output, "technical-debt.md", b"# Technical-debt observations\n\nDebt analysis has not been performed.\n")
        print(json.dumps({"output": str(output), "analysis_id": identity["analysis_id"], "verdict": summary["verdict"], "changed_files": len(records)}))
        return 4 if stale else 0
    except ReviewError as exc:
        write_json(output, "analysis-summary.json", {"schema_version": "1", "verdict": "INCOMPLETE", "complete": False, "error": str(exc)})
        raise


def open_run(value):
    output = no_symlinks(value)
    seals = load_json(local_file(output, "prepared-hashes.json"))
    for name in ("request.json", "context-packet.json", "integrity-before.json"):
        if name not in seals or hash_file(local_file(output, name)) != seals[name]:
            raise ReviewError("Prepared input was modified: " + name)
    capsule = load_json(local_file(output, "context-packet.json"))
    identity = dict(capsule["identity"])
    analysis_id = identity.pop("analysis_id")
    if analysis_id != "local-review:" + digest(encoded(identity)):
        raise ReviewError("Prepared identity digest is invalid")
    if identity["snapshot_digest"] != digest(encoded(capsule["trees"])):
        raise ReviewError("Prepared tree digest is invalid")
    if capsule["output"] != str(output):
        raise ReviewError("Run directory identity changed; prepare a new run")
    return output, capsule, Path(capsule["identity"]["repository"])


def unchanged(output, capsule, repo):
    before = load_json(local_file(output, "integrity-before.json"))
    after = fingerprint(repo, output)
    if before != after or before["sha256"] != capsule["identity"]["source_fingerprint"]:
        return False
    identity = capsule["identity"]
    for ref, expected in [(identity["base_ref"], identity["base_commit"]),
                          (identity["head_ref"], identity["head_commit"])]:
        if ref and ref not in ("INDEX", "WORKING_TREE") and resolve(repo, ref, optional=True) != expected:
            return False
    return True


def require_unchanged(output, capsule, repo):
    if not unchanged(output, capsule, repo):
        invalidate(output, "STALE", "Repository or selected refs changed; prepare a new run", capsule["identity"]["analysis_id"])
        raise ReviewError("STALE: repository or selected refs changed; prepare a new run")


def invalidate(output, verdict, reason, analysis_id=None):
    summary = {"schema_version": "1", "verdict": verdict, "complete": False, "error": reason,
               "integrity": "CHANGED" if verdict == "STALE" else "UNVERIFIED"}
    if analysis_id:
        summary["analysis_id"] = analysis_id
    write_json(output, "analysis-summary.json", summary)
    message = "# Local PR review\n\n" + verdict + "\n\n" + reason + "\n\nEarlier finding artifacts are retained for diagnosis, not a current recommendation.\n"
    write_bytes(output, "review.md", message.encode())
    write_bytes(output, "report.html", ("<!doctype html><meta charset='utf-8'><meta http-equiv='Content-Security-Policy' content=\"default-src 'none'\"><pre>" + html.escape(message) + "</pre>").encode())
    return summary


def invalidate_failed_finalization(value, reason):
    output = no_symlinks(value)
    seals = load_json(local_file(output, "prepared-hashes.json"))
    request_path = local_file(output, "request.json")
    request = load_json(request_path)
    if hash_file(request_path) != seals.get("request.json") or request["output"] != str(output):
        return
    repo = Path(request["repository"])
    if within(output, repo) and (output == repo or ".git" in output.relative_to(repo).parts):
        return
    invalidate(output, "STALE" if reason.startswith("STALE:") else "INCOMPLETE", reason)


def add_evidence(args):
    output, capsule, repo = open_run(args.output)
    require_unchanged(output, capsule, repo)
    tree = capsule["trees"][args.side]
    if args.path not in tree:
        raise ReviewError("Evidence path is absent from the selected snapshot")
    data = source_bytes(repo, tree, args.path)
    lines = text_lines(data)
    start, end = args.start, args.end
    if (start is None) != (end is None):
        raise ReviewError("Supply both --start and --end, or neither")
    if start is not None and (lines is None or not 1 <= start <= end <= len(lines)):
        raise ReviewError("Evidence coordinates are outside the selected text snapshot")
    excerpt = "".join(lines[start - 1:end]) if start is not None else None
    record = {"kind": "source", "side": args.side, "path": args.path,
              "start_line": start, "end_line": end, "sha256": digest(data),
              "excerpt": excerpt, "relation": args.relation, "reason": args.reason}
    return append_evidence(output, capsule, repo, record)


def add_receipt(args):
    output, capsule, repo = open_run(args.output)
    require_unchanged(output, capsule, repo)
    path = no_symlinks(args.file)
    data = path.read_bytes()
    artifact = "evidence-artifacts/" + digest(data) + ".bin"
    write_bytes(output, artifact, data)
    record = {"kind": args.kind, "artifact": artifact, "sha256": digest(data),
              "reason": args.reason, "origin": "supplied-local-artifact"}
    return append_evidence(output, capsule, repo, record)


def append_evidence(output, capsule, repo, record):
    manifest = load_json(local_file(output, "context-manifest.json"))
    record["analysis_id"] = capsule["identity"]["analysis_id"]
    record["id"] = "EV-" + digest(encoded(record))[:24]
    if record["id"] not in {e["id"] for e in manifest["evidence"]}:
        manifest["evidence"].append(record)
    require_unchanged(output, capsule, repo)
    write_json(output, "context-manifest.json", manifest)
    print(json.dumps(record))
    return 0


def schema_validate(value, schema, path="assessment"):
    types = {"object": lambda x: isinstance(x, dict), "array": lambda x: isinstance(x, list),
             "string": lambda x: isinstance(x, str), "integer": lambda x: type(x) is int,
             "boolean": lambda x: type(x) is bool, "null": lambda x: x is None}
    if "type" in schema:
        allowed = schema["type"] if isinstance(schema["type"], list) else [schema["type"]]
        if not any(types[t](value) for t in allowed):
            raise ReviewError(f"{path}: expected {allowed}")
    if "enum" in schema and value not in schema["enum"]:
        raise ReviewError(f"{path}: invalid value {value!r}")
    if value is None:
        return
    if isinstance(value, dict):
        missing = set(schema.get("required", [])) - value.keys()
        if missing:
            raise ReviewError(f"{path}: missing {sorted(missing)}")
        properties = schema.get("properties", {})
        if schema.get("additionalProperties") is False and value.keys() - properties.keys():
            raise ReviewError(f"{path}: unknown fields {sorted(value.keys() - properties.keys())}")
        for name, child in value.items():
            if name in properties:
                schema_validate(child, properties[name], path + "." + name)
    if isinstance(value, list):
        if len(value) < schema.get("minItems", 0):
            raise ReviewError(f"{path}: not enough entries")
        if schema.get("uniqueItems") and len({encoded(x) for x in value}) != len(value):
            raise ReviewError(f"{path}: duplicate entries")
        for i, child in enumerate(value):
            schema_validate(child, schema.get("items", {}), path + f"[{i}]")
    if isinstance(value, str) and len(value.strip()) < schema.get("minLength", 0):
        raise ReviewError(f"{path}: empty value")
    if type(value) is int and value < schema.get("minimum", value):
        raise ReviewError(f"{path}: below minimum")


def validate_evidence(output, capsule, repo):
    manifest = load_json(local_file(output, "context-manifest.json"))
    analysis_id = capsule["identity"]["analysis_id"]
    if manifest["analysis_id"] != analysis_id:
        raise ReviewError("Context manifest belongs to another analysis")
    if not isinstance(manifest["evidence"], list):
        raise ReviewError("Manifest evidence must be an array")
    records = {}
    for item in manifest["evidence"]:
        if not isinstance(item, dict):
            raise ReviewError("Manifest evidence entries must be objects")
        if item["analysis_id"] != analysis_id or item["id"] in records:
            raise ReviewError("Evidence identity is invalid or duplicated")
        content = dict(item)
        del content["id"]
        if item["id"] != "EV-" + digest(encoded(content))[:24]:
            raise ReviewError("Evidence record was changed after capture")
        if item["kind"] == "source":
            tree = capsule["trees"][item["side"]]
            if item["path"] not in tree:
                raise ReviewError("Evidence source is absent")
            data = source_bytes(repo, tree, item["path"])
            if item["start_line"] is not None:
                lines = text_lines(data)
                if lines is None or not 1 <= item["start_line"] <= item["end_line"] <= len(lines):
                    raise ReviewError("Evidence coordinates are invalid")
                if item["excerpt"] != "".join(lines[item["start_line"] - 1:item["end_line"]]):
                    raise ReviewError("Evidence excerpt differs from pinned content")
        else:
            data = local_file(output, item["artifact"]).read_bytes()
        if digest(data) != item["sha256"]:
            raise ReviewError("Evidence content hash differs from its receipt")
        records[item["id"]] = item
    return records


def adjudicate(assessment, records, capsule):
    gaps = list(assessment["unresolved_questions"])
    blockers, kept, discarded = [], [], []
    analysis_id = capsule["identity"]["analysis_id"]

    def evidence(ids, kinds=None):
        for key in ids:
            if key not in records or (kinds and records[key]["kind"] not in kinds):
                raise ReviewError(f"Missing or wrong-kind local evidence: {key}")

    if assessment["analysis_id"] != analysis_id:
        raise ReviewError("Assessment belongs to a different pinned analysis")
    evidence(assessment["intent"]["evidence_ids"])
    if assessment["intent"]["status"] == "assessed" and not assessment["intent"]["evidence_ids"]:
        gaps.append("Specification alignment has no authoritative local evidence")
    isolation = assessment["host"]["isolation_evidence_id"]
    if isolation:
        evidence([isolation], {"isolation"})
    covered = set()
    for item in assessment["coverage"]:
        if item["path"] in covered:
            raise ReviewError("Duplicate file coverage record")
        covered.add(item["path"])
        evidence(item["evidence_ids"])
        if item["status"] == "reviewed" and not item["evidence_ids"]:
            gaps.append(f"Coverage has no evidence: {item['path']}")
        if item["status"] == "reviewed" and not any(records[e]["kind"] == "source" and records[e]["path"] == item["path"] for e in item["evidence_ids"]):
            gaps.append(f"Coverage evidence does not address its path: {item['path']}")
        if item["status"] != "reviewed":
            gaps.append(f"Unreviewed changed surface: {item['path']}")
    for item in capsule["changes"]:
        if item["path"] not in covered:
            gaps.append(f"Changed file omitted from coverage: {item['path']}")
        if item.get("base_mode") == "160000" or item.get("head_mode") == "160000":
            gaps.append("Submodule contents need a separate pinned review; this helper verifies only the gitlink surface: " + item["path"])
    names = set()
    for lens in assessment["lenses"]:
        if lens["name"] in names:
            raise ReviewError("Duplicate review lens")
        names.add(lens["name"])
        if lens["status"] == "pending":
            gaps.append(f"Review lens pending: {lens['name']}")
    expected = {"correctness", "contracts", "tests", "architecture", "security-reliability", "infrastructure", "debt"}
    if expected - names:
        gaps.append("Review lenses missing: " + ", ".join(sorted(expected - names)))
    if not assessment["checks"]:
        gaps.append("No repository-native check selection was recorded")
    for check in assessment["checks"]:
        if check["analysis_id"] != analysis_id:
            raise ReviewError("A check belongs to another analysis")
        if check["status"] in ("passed", "failed"):
            evidence([check["evidence_id"]], {"tool_log"})
            if check["isolation_evidence_id"]:
                evidence([check["isolation_evidence_id"]], {"isolation"})
            if not check["command"] or not check["provenance"]:
                raise ReviewError("Executed checks need a command and local provenance")
            if check["exit_code"] is None or (check["status"] == "passed") != (check["exit_code"] == 0):
                raise ReviewError("Check exit code conflicts with its outcome")
        if check["status"] == "failed":
            blockers.append("Deterministic check failed: " + check["name"])
        if check["status"] == "unavailable":
            gaps.append("Check unavailable: " + check["name"] + ": " + check["explanation"])
    challenge = assessment["challenge"]
    if challenge["status"] == "completed":
        evidence([challenge["evidence_id"]], {"challenge"})
        if not challenge["reviewer"].strip():
            raise ReviewError("Completed challenge needs a reviewer/context identity")
    else:
        gaps.append("Counterevidence challenge unavailable")
    seen_ids, seen_problems = set(), set()
    allowed_paths = {e["path"] for e in records.values() if e["kind"] == "source"}
    for finding in assessment["findings"]:
        if finding["id"] in seen_ids:
            raise ReviewError("Duplicate finding ID")
        seen_ids.add(finding["id"])
        evidence(finding["evidence_ids"])
        evidence(finding["counterevidence_ids"])
        if finding["relationship"] == "UNRELATED" or finding["disposition"] == "discarded":
            discarded.append({"id": finding["id"], "reason": "Out of scope or rejected after challenge"})
            continue
        key = (finding["root_cause"].strip().casefold(), finding["location"]["path"], finding["kind"])
        if key in seen_problems:
            discarded.append({"id": finding["id"], "reason": "Duplicate root problem and boundary"})
            continue
        seen_problems.add(key)
        location = finding["location"]
        if (location["start_line"] is None) != (location["end_line"] is None):
            raise ReviewError("Supply both finding line coordinates or neither")
        if location["path"] not in allowed_paths:
            raise ReviewError("Finding has no source evidence inside the responsibility domain")
        sources = [records[e] for e in finding["evidence_ids"] if records[e]["kind"] == "source"]
        if not any(e["path"] == location["path"] and e["side"] == location["side"] and
                   ((location["start_line"] is None and e["start_line"] is None) or
                    (location["start_line"] is not None and e["start_line"] is not None and
                     e["start_line"] <= location["start_line"] <= location["end_line"] <= e["end_line"])) for e in sources):
            raise ReviewError("Finding coordinates are not covered by its pinned source evidence")
        if not finding["counterevidence_ids"]:
            gaps.append("Counterevidence search lacks a local record: " + finding["id"])
        if finding["confidence"] in ("LOW", "CONFLICTED"):
            gaps.append("Unresolved candidate: " + finding["id"])
            discarded.append({"id": finding["id"], "reason": "Unresolved low-confidence or conflicted candidate"})
            continue
        if finding["deletion"] is not None:
            deletion = finding["deletion"]
            for field in ("replacement_evidence_ids", "consumer_evidence_ids", "compatibility_evidence_ids"):
                evidence(deletion[field])
                if not deletion[field]:
                    raise ReviewError("Deletion claim is missing " + field)
            if deletion["safe"] and deletion["unresolved_risks"]:
                raise ReviewError("Deletion cannot be called safe with unresolved consumers or compatibility risks")
        if finding["blocking"]:
            if finding["kind"] != "defect" or finding["relationship"] not in ("INTRODUCED", "WORSENED", "EXPOSED") or finding["confidence"] not in ("CERTAIN", "HIGH"):
                raise ReviewError("Blocking status conflicts with the finding evidence/scope contract")
            if challenge["status"] != "completed" or finding["id"] not in challenge["covered_finding_ids"]:
                gaps.append("Blocking candidate lacks independent challenge: " + finding["id"])
                finding = dict(finding, blocking=False)
            else:
                blockers.append(finding["id"] + ": " + finding["title"])
        if finding["severity"] in ("BLOCKER", "HIGH") and finding["id"] not in challenge["covered_finding_ids"]:
            gaps.append("Serious finding was not covered by the challenge: " + finding["id"])
        kept.append(finding)
    mass = assessment["code_mass"]
    if (mass["added"] is None) != (mass["removed"] is None):
        raise ReviewError("Supply both maintained added/removed counts or neither")
    if mass["added"] is not None:
        evidence([mass["evidence_id"]], {"code_mass"})
    if (mass["ratio_added"] is None) != (mass["ratio_removed"] is None):
        raise ReviewError("Supply both ratio terms or neither")
    verdict = "HOLD" if blockers else "INCOMPLETE" if gaps else "PASS_WITH_DEBT" if kept else "PASS"
    return verdict, list(dict.fromkeys(gaps)), blockers, kept, discarded


def render(output, capsule, assessment, summary, findings, mass):
    identity = capsule["identity"]
    review = ["# Local PR review", "", "**" + summary["verdict"] + "**", "",
              f"Mode: {identity['mode']} · Changed files: {len(capsule['changes'])}",
              f"Base commit: {identity['base_commit'] or 'empty tree'}",
              f"Comparison baseline: {identity['comparison_base'] or 'empty tree'}",
              f"Head commit: {identity['head_commit'] or 'unborn'}",
              f"Snapshot: {identity['snapshot_digest']}", "", "## Reviewed behavior", "", assessment["behavior_summary"],
              "", "## Specification alignment", "", assessment["intent"]["explanation"], "", "## Findings", ""]
    debt = ["# Technical-debt observations", ""]
    for finding in findings:
        location = finding["location"]
        block = [f"### {finding['id']} — {finding['title']}", "",
                 f"Severity: {finding['severity']} · Confidence: {finding['confidence']} · Relationship: {finding['relationship']}",
                 f"Location: {location['side']} {location['path']}:{location['start_line'] or 'file'}", "",
                 finding["claim"], "", "Impact: " + finding["impact"], "",
                 "Suggested treatment: " + finding["recommendation"], "",
                 "Counterevidence search: " + finding["counterevidence_search"], "",
                 "Local evidence: " + ", ".join(finding["evidence_ids"]), ""]
        (debt if finding["kind"] == "debt" else review).extend(block)
    if len(debt) == 2:
        debt.append("No adjudicated debt observations." if summary["complete"] else "No adjudicated debt observations; analysis is incomplete.")
    if not findings:
        review.append("No adjudicated findings. Interpret this together with completeness and verification gaps.")
    review.extend(["", "## Verification gaps", "", *["- " + gap for gap in summary["gaps"]],
                   "", "## Commands and local evidence", ""])
    for check in assessment["checks"]:
        review.append(f"- {check['name']}: {check['status']}. {check['explanation']} Command: {json.dumps(check['command'])}. Evidence: {check['evidence_id'] or 'none'}.")
    review.extend(["", "Native check and model-host receipts are supplied local evidence; the helper validates their binding and hashes, not their execution.",
                   "", "## Code-mass assessment", "", f"Raw text lines: +{mass['text_added']} / -{mass['text_removed']}. Maintained SLOC: {mass['maintained_added']} added / {mass['maintained_removed']} removed.",
                   "Advisory ratio: " + mass["ratio_status"] + ". " + assessment["code_mass"]["ratio_basis"],
                   "", "## Limitations", "", *["- " + s for s in summary["limitations"]],
                   "", "## Repository integrity", "", summary["integrity"], "",
                   "This report is a local recommendation. It does not represent CI execution, a published review, or a merge decision."])
    review_text, debt_text = "\n".join(review) + "\n", "\n".join(debt) + "\n"
    write_bytes(output, "review.md", review_text.encode())
    write_bytes(output, "technical-debt.md", debt_text.encode())
    document = "<!doctype html><html lang='en'><meta charset='utf-8'><meta name='viewport' content='width=device-width'><meta http-equiv='Content-Security-Policy' content=\"default-src 'none'; style-src 'unsafe-inline'\"><title>Local PR review</title><style>body{font:16px system-ui;max-width:1000px;margin:40px auto;padding:0 24px;color:#182033;background:#faf9f5}pre{white-space:pre-wrap;overflow-wrap:anywhere;line-height:1.55}</style><body><pre>" + html.escape(review_text + "\n" + debt_text) + "</pre></body></html>"
    write_bytes(output, "report.html", document.encode())


def finalize(args):
    invalidate_failed_finalization(args.output, "Finalization in progress; no current recommendation is available")
    output, capsule, repo = open_run(args.output)
    if not unchanged(output, capsule, repo):
        summary = invalidate(output, "STALE", "Repository or selected refs changed; prepare a new run", capsule["identity"]["analysis_id"])
        print(json.dumps(summary))
        return 4
    assessment = load_json(args.assessment)
    schema = load_json(Path(__file__).resolve().parents[1] / "schemas/assessment.schema.json")
    schema_validate(assessment, schema)
    records = validate_evidence(output, capsule, repo)
    verdict, gaps, blockers, findings, discarded = adjudicate(assessment, records, capsule)
    require_unchanged(output, capsule, repo)
    mass = {"schema_version": "1", "text_added": sum(r["added_lines"] or 0 for r in capsule["changes"]),
            "text_removed": sum(r["removed_lines"] or 0 for r in capsule["changes"]),
            "binary_files": sum(r["binary"] for r in capsule["changes"]), "rename_method": capsule["rename_method"]}
    measured = assessment["code_mass"]
    mass.update(maintained_added=measured["added"], maintained_removed=measured["removed"], ratio_status="UNKNOWN")
    if measured["added"] is not None and measured["ratio_added"] is not None:
        mass["ratio_status"] = "REMOVAL_ONLY" if measured["added"] == 0 and measured["removed"] > 0 else "NO_MAINTAINED_CHANGE" if measured["added"] == measured["removed"] == 0 else "MET" if measured["removed"] * measured["ratio_added"] >= measured["added"] * measured["ratio_removed"] else "BELOW_ADVISORY_TARGET"
    summary = {"schema_version": "1", "analysis_id": assessment["analysis_id"], "verdict": verdict,
               "complete": not gaps, "integrity": "UNCHANGED", "gaps": gaps, "blocking_reasons": blockers,
               "identity": capsule["identity"], "limitations": capsule["limitations"] + assessment["limitations"],
               "evidence_origin": "Local source verified by helper; model and native-check execution supplied by host",
               "finding_count": len(findings)}
    write_json(output, "findings.json", {"schema_version": "1", "analysis_id": assessment["analysis_id"], "findings": findings, "discarded": discarded})
    write_json(output, "tool-results.json", {"schema_version": "1", "analysis_id": assessment["analysis_id"], "origin": "supplied-local-evidence", "checks": assessment["checks"]})
    write_json(output, "code-mass.json", mass)
    write_json(output, "assessment-final.json", assessment)
    render(output, capsule, assessment, summary, findings, mass)
    require_unchanged(output, capsule, repo)
    write_json(output, "analysis-summary.json", summary)
    print(json.dumps({"output": str(output), "verdict": verdict, "complete": summary["complete"], "gaps": gaps}))
    return 3 if verdict == "INCOMPLETE" else 1 if verdict == "HOLD" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    prep = commands.add_parser("prepare", help="Pin local inputs and create an unfinished local review")
    prep.add_argument("--repo", default=".")
    prep.add_argument("--output")
    mode = prep.add_mutually_exclusive_group(required=True)
    mode.add_argument("--base")
    mode.add_argument("--staged", action="store_true")
    mode.add_argument("--working-tree", action="store_true")
    mode.add_argument("--commit")
    prep.add_argument("--head")
    prep.add_argument("--parent", type=int)
    prep.add_argument("--comparison", choices=["merge-base", "direct"], default="merge-base")
    prep.add_argument("--depth", choices=["quick", "standard", "deep"], default="standard")
    ev = commands.add_parser("evidence", help="Capture exact local source evidence")
    ev.add_argument("--output", required=True)
    ev.add_argument("--side", choices=["base", "head"], required=True)
    ev.add_argument("--path", required=True)
    ev.add_argument("--start", type=int)
    ev.add_argument("--end", type=int)
    ev.add_argument("--relation", choices=["changed", "caller", "callee", "interface", "implementation", "test", "configuration", "coupled", "history"], required=True)
    ev.add_argument("--reason", required=True)
    receipt = commands.add_parser("receipt", help="Import a supplied local evidence artifact")
    receipt.add_argument("--output", required=True)
    receipt.add_argument("--file", required=True)
    receipt.add_argument("--kind", choices=["tool_log", "challenge", "isolation", "spec", "history", "graph", "code_mass"], required=True)
    receipt.add_argument("--reason", required=True)
    finish = commands.add_parser("finalize", help="Validate an assessment and render local reports")
    finish.add_argument("--output", required=True)
    finish.add_argument("--assessment", required=True)
    args = parser.parse_args()
    if args.command == "prepare":
        if args.head and not args.base:
            parser.error("--head requires --base")
        if args.parent is not None and not args.commit:
            parser.error("--parent requires --commit")
        if args.comparison != "merge-base" and not args.base:
            parser.error("--comparison applies to base/head ranges")
    try:
        return {"prepare": prepare, "evidence": add_evidence, "receipt": add_receipt, "finalize": finalize}[args.command](args)
    except (ReviewError, OSError, KeyError, StopIteration, TypeError, ValueError) as exc:
        if args.command == "finalize":
            try:
                invalidate_failed_finalization(args.output, str(exc))
            except (ReviewError, OSError, KeyError):
                pass
        print(json.dumps({"error": str(exc), "status": "INCOMPLETE"}), file=sys.stderr)
        return 2


if __name__ == "__main__":
    sys.exit(main())
