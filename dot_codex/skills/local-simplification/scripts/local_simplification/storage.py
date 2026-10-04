"""Content-addressed local artifacts and read-only Git snapshots."""

import hashlib
import json
import math
import os
from pathlib import Path
import re
import shutil
import stat
import subprocess
import tempfile


class Invalid(Exception):
    """A request or its evidence cannot satisfy the declared contract."""


def encoded(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       allow_nan=False) + "\n").encode()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    def reject(value):
        raise Invalid(f"Non-finite JSON value: {value}")
    def pairs(items):
        result = {}
        for key, value in items:
            if key in result:
                raise Invalid(f"Duplicate JSON key: {key}")
            result[key] = value
        return result
    def finite(value):
        number = float(value)
        if not math.isfinite(number):
            raise Invalid(f"Non-finite JSON number: {value}")
        return number
    try:
        value = json.loads(Path(path).read_bytes(), parse_constant=reject,
                           parse_float=finite,
                           object_pairs_hook=pairs)
        if not isinstance(value, dict):
            raise Invalid("Expected a JSON object")
        return value
    except (ValueError, OSError) as exc:
        raise Invalid(f"Cannot read JSON {path}: {exc}") from exc


def inside(path, parent):
    return path == parent or parent in path.parents


def safe_path(path):
    path = Path(os.path.abspath(path))
    for item in (path, *path.parents):
        if item.is_symlink():
            raise Invalid(f"Artifact path traverses a symlink: {item}")
    return path


def relative(name):
    p = Path(name)
    if not name or p.is_absolute() or ".." in p.parts or ".git" in p.parts:
        raise Invalid(f"Expected a relative source path: {name!r}")
    return p.as_posix()


def write(root, name, value, raw=False):
    dest = safe_path(Path(root) / relative(name))
    dest.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".simplify-", dir=dest.parent)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(value if raw else encoded(value))
        os.replace(temp, dest)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def clean_env():
    return {"PATH": os.environ.get("PATH", os.defpath), "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_SYSTEM": os.devnull,
            "GIT_CONFIG_GLOBAL": os.devnull, "GIT_OPTIONAL_LOCKS": "0",
            "GIT_NO_LAZY_FETCH": "1", "GIT_NO_REPLACE_OBJECTS": "1",
            "GIT_ALLOW_PROTOCOL": "", "GIT_TERMINAL_PROMPT": "0",
            "GIT_LITERAL_PATHSPECS": "1"}


def git(repo, *args, data=None, ok=(0,)):
    executable = shutil.which("git")
    if not executable:
        raise Invalid("Local Git is unavailable; nothing was installed")
    command = [executable, "--no-pager", "-C", str(repo),
               "-c", "core.fsmonitor=false", "-c", f"core.hooksPath={os.devnull}",
               "-c", "credential.helper=", "-c", "gc.auto=0",
               "-c", "maintenance.auto=false", *args]
    try:
        result = subprocess.run(command, input=data, capture_output=True,
                                env=clean_env(), timeout=120)
    except (OSError, subprocess.TimeoutExpired) as exc:
        raise Invalid(f"Git {args[0]} unavailable: {exc}") from exc
    if result.returncode not in ok:
        raise Invalid(f"Git {args[0]} failed; no fetch attempted: " +
                      result.stderr.decode("utf-8", "replace").strip())
    return result.stdout


def git_path(repo, option):
    value = Path(os.fsdecode(git(repo, "rev-parse", option).strip()))
    return (repo / value).resolve() if not value.is_absolute() else value.resolve()


def resolve(repo, ref, optional=False):
    oid = git(repo, "rev-parse", "--verify", "--end-of-options", ref + "^{commit}",
              ok=(0, 1, 128) if optional else (0,)).decode().strip()
    if optional and not oid:
        return None
    if not re.fullmatch(r"[a-f0-9]{40}|[a-f0-9]{64}", oid):
        raise Invalid(f"Not an available local commit: {ref}")
    return oid


def fingerprint(repo, output):
    roots = [repo]
    for option in ("--absolute-git-dir", "--git-common-dir"):
        path = git_path(repo, option)
        if not any(inside(path, root) for root in roots):
            roots.append(path)
    entries = {}
    def visit(path, key):
        if inside(path, output):
            return
        info = path.lstat()
        if stat.S_ISREG(info.st_mode):
            h = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    h.update(block)
            value = ["file", stat.S_IMODE(info.st_mode), h.hexdigest()]
        elif stat.S_ISLNK(info.st_mode):
            value = ["symlink", stat.S_IMODE(info.st_mode), os.readlink(path)]
        elif stat.S_ISDIR(info.st_mode):
            value = ["directory", stat.S_IMODE(info.st_mode)]
        else:
            value = ["special", info.st_mode]
        entries[key] = value
        if path.name == ".git" and value[0] in ("file", "symlink"):
            for option in ("--absolute-git-dir", "--git-common-dir"):
                target = git_path(path.parent, option)
                if not any(inside(target, root) for root in roots):
                    roots.append(target)
        if value[0] == "directory":
            for child in sorted(path.iterdir()):
                visit(child, key + "/" + child.name)
    for i, root in enumerate(roots):
        visit(root, str(i))
    return {"sha256": digest(encoded(entries)), "roots": list(map(str, roots)),
            "method": "file-bytes-kind-mode-and-symlink-text", "entries": entries}


def tree(repo, revision=None, index=False):
    result = {}
    if revision is None and not index:
        return result
    output = git(repo, "ls-files", "--stage", "-z") if index else git(
        repo, "ls-tree", "-r", "-z", "--full-tree", revision)
    for raw in output.split(b"\0"):
        if not raw:
            continue
        meta, name = raw.split(b"\t", 1)
        a, b, c = meta.decode().split()
        if index:
            if c != "0":
                raise Invalid("Unmerged index stages cannot be captured")
            mode, oid = a, b
        else:
            mode, oid = a, c
        result[relative(os.fsdecode(name))] = {"mode": mode, "oid": oid}
    return result


def blob_batch(repo, oids):
    oids = sorted(set(oids))
    if not oids:
        return {}
    raw = git(repo, "cat-file", "--batch", data=("\n".join(oids) + "\n").encode())
    offset, result = 0, {}
    for oid in oids:
        end = raw.find(b"\n", offset)
        header = raw[offset:end].decode().split()
        if len(header) != 3 or header[0] != oid or header[1] != "blob":
            raise Invalid(f"Source blob unavailable: {oid}; no network fallback")
        size = int(header[2])
        content = raw[end + 1:end + 1 + size]
        if len(content) != size or raw[end + 1 + size:end + 2 + size] != b"\n":
            raise Invalid("Truncated Git object stream")
        result[oid], offset = content, end + 2 + size
    return result


def capture(repo, revision, output, working=False, staged=False):
    entries = tree(repo, revision, index=working or staged)
    if working:
        for name in git(repo, "ls-files", "--others", "--exclude-standard", "-z").split(b"\0"):
            if name:
                entries.setdefault(relative(os.fsdecode(name)), {"mode": "100644"})
    blobs = {} if working else blob_batch(repo, [x["oid"] for x in entries.values()
                                                if x["mode"] != "160000"])
    files, gaps = {}, []
    for name, item in sorted(entries.items()):
        if inside(Path(os.path.abspath(repo / name)), output):
            continue
        mode = item["mode"]
        if mode == "160000":
            gaps.append({"path": name, "reason": "Submodule needs its own pinned local analysis"})
            files[name] = {"mode": mode, "oid": item["oid"], "sha256": None}
            continue
        if working:
            path = repo / name
            for parent in path.parents:
                if parent == repo:
                    break
                if parent.is_symlink():
                    raise Invalid(f"Working source traverses a symlink: {name}")
            if not path.exists() and not path.is_symlink():
                continue
            info = path.lstat()
            if path.is_symlink():
                content, mode = os.fsencode(os.readlink(path)), "120000"
            elif stat.S_ISREG(info.st_mode):
                content = path.read_bytes()
                mode = "100755" if info.st_mode & stat.S_IXUSR else "100644"
            else:
                raise Invalid(f"Unsupported working source: {name}")
        else:
            content = blobs[item["oid"]]
        sha = digest(content)
        files[name] = {"mode": mode, "sha256": sha, "size": len(content)}
        destination = output / "blobs" / sha
        if not destination.exists():
            write(output, "blobs/" + sha, content, raw=True)
        if content.startswith(b"version https://git-lfs.github.com/spec/v1\n"):
            gaps.append({"path": name, "reason": "Git LFS pointer captured; payload is not materialized"})
    return {"commit": revision, "mode": "working-tree" if working else "staged" if staged else "commit",
            "digest": digest(encoded(files)), "files": files, "gaps": gaps}


def content(run, snapshot, name):
    item = snapshot["files"][name]
    if item["sha256"] is None:
        raise Invalid(f"Snapshot content unavailable: {name}")
    path = safe_path(run / "blobs" / item["sha256"])
    value = path.read_bytes()
    if digest(value) != item["sha256"]:
        raise Invalid(f"Snapshot content was altered: {name}")
    return value


def seal(run, names):
    write(run, "seal.json", {name: digest((run / name).read_bytes()) for name in names})


def open_run(path, current=True):
    run = safe_path(path)
    manifest = read_json(run / "manifest.json")
    sealed = read_json(run / "seal.json")
    required = {"manifest.json", "integrity-before.json", "code-mass.json"}
    required.update({"plan.json", "integrity-after.json", "execution-report.json"} if "origin_plan" in manifest
                    else {"inventory.json", "candidates.json", "responsibility-current.json"})
    if not required.issubset(sealed):
        raise Invalid("Pinned artifact seal is incomplete")
    for name, expected in sealed.items():
        source = safe_path(run / relative(name))
        if digest(source.read_bytes()) != expected:
            raise Invalid(f"Pinned artifact was altered: {name}")
    for snapshot in manifest["snapshots"].values():
        if digest(encoded(snapshot["files"])) != snapshot["digest"]:
            raise Invalid("Snapshot manifest digest mismatch")
        for name, item in snapshot["files"].items():
            relative(name)
            if item["sha256"] is not None:
                content(run, snapshot, name)
    if current and fingerprint(Path(manifest["repository"]), run)["sha256"] != manifest["source_fingerprint"]:
        raise Invalid("STALE: repository or Git storage changed since capture")
    return run, manifest
