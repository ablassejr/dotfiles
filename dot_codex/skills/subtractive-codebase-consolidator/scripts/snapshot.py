"""Inventory and pin local files without invoking repository code or Git hooks."""
import argparse
import fnmatch
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from datetime import datetime, timezone

from contracts import Authorization, Basis, Inventory, Run


def digest(value):
    data = value if isinstance(value, bytes) else json.dumps(value, sort_keys=True, separators=(",", ":")).encode()
    return hashlib.sha256(data).hexdigest()


def read(path, model=None):
    value = json.loads(Path(path).read_text())
    return model.model_validate(value).model_dump() if model else value


def write(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_name(path.name + ".tmp")
    temp.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")
    temp.replace(path)


def require(condition, message):
    if not condition:
        raise ValueError(message)


def relative(path):
    require(isinstance(path, str) and path and not any(c in path for c in "\n\r\x00"), "Invalid relative path")
    p = Path(path)
    require(not p.is_absolute() and ".." not in p.parts and str(p) != ".", f"Unsafe path: {path}")
    return p


def category(path, policy):
    for rule in policy["rules"]:
        if fnmatch.fnmatchcase(path, rule["pattern"]):
            return rule["category"]
    return "unclassified"


def scan(root, policy=None, skip_git=True):
    root = Path(root).resolve()
    require(root.is_dir(), f"Directory missing: {root}")
    files = {}
    def visit(directory):
        for path in sorted(directory.iterdir()):
            rel = path.relative_to(root).as_posix()
            relative(rel)
            if skip_git and rel == ".git":
                continue
            info = path.lstat()
            if stat.S_ISDIR(info.st_mode):
                visit(path)
                continue
            if stat.S_ISLNK(info.st_mode):
                kind, data = "symlink", os.readlink(path).encode()
            elif stat.S_ISREG(info.st_mode):
                kind, data = "file", path.read_bytes()
            else:
                kind, data = "special", str(stat.S_IFMT(info.st_mode)).encode()
            files[rel] = {"kind": kind, "sha256": digest(data), "mode": stat.S_IMODE(info.st_mode),
                          "size": len(data), "category": category(rel, policy) if policy else "unclassified"}
    visit(root)
    return files


def metadata(root):
    dotgit = Path(root) / ".git"
    if dotgit.is_dir():
        return digest(scan(dotgit, skip_git=False))
    if dotgit.is_file():
        marker = dotgit.read_text().strip()
        require(marker.startswith("gitdir: "), "Unrecognized .git pointer")
        gitdir = (Path(root) / marker[8:]).resolve()
        parts = {"pointer": marker, "worktree": scan(gitdir, skip_git=False)}
        common = gitdir / "commondir"
        if common.is_file():
            common_dir = (gitdir / common.read_text().strip()).resolve()
            parts["common"] = scan(common_dir, skip_git=False)
        return digest(parts)
    return digest({})


def outside(output, original):
    output, original = Path(output).resolve(), Path(original).resolve()
    require(output != original and original not in output.parents and output not in original.parents,
            "Output must be separate from the original directory")
    return output


def copy_files(source, target, files):
    target = Path(target)
    require(not target.exists(), f"Refusing to overwrite: {target}")
    target.mkdir(parents=True)
    for name, entry in files.items():
        if entry["category"] in {"excluded", "unclassified"}:
            continue
        require(entry["kind"] == "file", f"Executable copy cannot include {entry['kind']}: {name}")
        source_path = Path(source) / relative(name)
        require(not source_path.is_symlink() and source_path.is_file(), f"Source changed: {name}")
        destination = target / relative(name)
        destination.parent.mkdir(parents=True, exist_ok=True)
        data = source_path.read_bytes()
        require(digest(data) == entry["sha256"], f"Source changed during copying: {name}")
        destination.write_bytes(data)
        destination.chmod(entry["mode"])


def load_run(directory):
    run = read(Path(directory) / "run.json", Run)
    require(digest(run["inventory"]) == run["inventory_hash"], "Inventory changed")
    require(digest(run["basis"]) == run["basis_hash"], "Preservation basis changed")
    require(digest(scan(Path(directory) / "baseline", run["inventory"])) == run["baseline_hash"], "Baseline snapshot changed")
    return run


def unchanged(run):
    require(digest(scan(run["original"], run["inventory"])) == run["original_hash"], "Original worktree changed")
    require(metadata(run["original"]) == run["metadata_hash"], "Original Git metadata changed")


def current(directory, run):
    files = scan(Path(directory) / "candidate", run["inventory"])
    require(all(v["kind"] == "file" and v["category"] not in {"excluded", "unclassified"} for v in files.values()),
            "Candidate contains unsupported, excluded, or unclassified files")
    return files, digest(files)


def patch_hash(run, candidate_hash):
    return digest({"baseline": run["baseline_hash"], "candidate": candidate_hash,
                   "inventory": run["inventory_hash"], "basis": run["basis_hash"]})


def unexpired(value):
    expiry = datetime.fromisoformat(value.replace("Z", "+00:00"))
    require(expiry.tzinfo is not None and expiry > datetime.now(timezone.utc), "Authorization expired or has no timezone")


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    inv = sub.add_parser("inventory")
    inv.add_argument("source")
    inv.add_argument("output")
    init = sub.add_parser("init")
    init.add_argument("source")
    init.add_argument("output")
    init.add_argument("--inventory", required=True)
    init.add_argument("--basis", required=True)
    exp = sub.add_parser("experiment")
    exp.add_argument("run")
    exp.add_argument("--authorization", required=True)
    cand = sub.add_parser("candidate")
    cand.add_argument("run")
    cand.add_argument("source")
    args = p.parse_args()
    if args.action == "inventory":
        outside(args.output, args.source)
        write(args.output, {"files": scan(args.source), "git_metadata_hash": metadata(args.source)})
    elif args.action == "init":
        target = outside(args.output, args.source)
        require(not target.exists(), "Run directory already exists")
        policy, basis = read(args.inventory, Inventory), read(args.basis, Basis)
        require(len({x["id"] for x in basis["preserve"]}) == len(basis["preserve"]), "Duplicate obligation IDs")
        files, meta = scan(args.source, policy), metadata(args.source)
        gaps = [f"{v['category']} or unsupported entry: {k}" for k, v in files.items()
                if v["category"] == "unclassified" or (v["kind"] != "file" and v["category"] != "excluded")]
        require(not any(v["kind"] != "file" and v["category"] not in {"excluded", "unclassified"} for v in files.values()),
                "Classify symlinks and special files as excluded before creating a runnable copy")
        copy_files(args.source, target / "baseline", files)
        result = {"format_version": 1, "original": str(Path(args.source).resolve()), "original_hash": digest(files),
                  "metadata_hash": meta, "baseline_hash": digest(scan(target / "baseline", policy)),
                  "inventory_hash": digest(policy), "basis_hash": digest(basis), "inventory": policy,
                  "basis": basis, "files": files, "gaps": gaps}
        Run.model_validate(result)
        unchanged(result)
        write(target / "run.json", result)
    else:
        target = Path(args.run).resolve()
        run = load_run(target)
        unchanged(run)
        require(not run["gaps"], "Resolve the recorded inventory gaps before copying a candidate")
        if args.action == "experiment":
            auth = read(args.authorization, Authorization)
            require(auth["baseline_hash"] == run["baseline_hash"], "Authorization is stale")
            unexpired(auth["expires"])
            for name in auth["allowed_paths"]:
                relative(name)
            copy_files(target / "baseline", target / "candidate", scan(target / "baseline", run["inventory"]))
            write(target / "authorization.json", auth)
        else:
            require(Path(args.source).resolve() != Path(run["original"]), "Candidate must be separate from the original")
            files = scan(args.source, run["inventory"])
            require(all(v["category"] != "unclassified" for v in files.values()), "Unclassified candidate files")
            copy_files(args.source, target / "candidate", files)
        unchanged(run)
    print(json.dumps({"status": "RECORDED", "action": args.action}))


def entrypoint(function):
    try:
        function()
    except KeyboardInterrupt:
        print(json.dumps({"status": "INCOMPLETE", "reason": "Interrupted"}))
        sys.exit(130)
    except (ValueError, OSError, KeyError, TypeError, subprocess.SubprocessError) as error:
        print(json.dumps({"status": "INCOMPLETE", "reason": str(error)}))
        sys.exit(2)


if __name__ == "__main__":
    entrypoint(main)
