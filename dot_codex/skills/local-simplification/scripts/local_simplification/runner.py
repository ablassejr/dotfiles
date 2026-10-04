"""Native checks run only under a tested, deny-by-default macOS sandbox."""

import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time

from .storage import Invalid, content, digest, encoded, relative


def materialize(run, snapshot, dest):
    if snapshot["gaps"]:
        raise Invalid("Snapshot has unavailable nested or LFS content")
    for name, entry in snapshot["files"].items():
        path = dest / relative(name)
        path.parent.mkdir(parents=True, exist_ok=True)
        if entry["mode"] == "120000":
            target = os.fsdecode(content(run, snapshot, name))
            resolved = (path.parent / target).resolve()
            if Path(target).is_absolute() or not resolved.is_relative_to(dest):
                raise Invalid(f"Snapshot symlink escapes the disposable tree: {name}")
            os.symlink(target, path)
        elif entry["mode"] in ("100644", "100755"):
            path.write_bytes(content(run, snapshot, name))
            path.chmod(0o755 if entry["mode"] == "100755" else 0o644)
        else:
            raise Invalid(f"Unsupported snapshot entry: {name}")


def sandbox_profile(work):
    if any(c in str(work) for c in ('"', "\\", "\n")):
        raise Invalid("Cannot encode sandbox workspace path")
    return f'''(version 1)
(deny default)
(allow process-exec process-fork)
(allow signal (target self))
(allow sysctl-read)
(allow file-read*)
(allow file-write* (subpath "{work}") (literal "/dev/null"))
(deny network*)
'''


def execute(argv, cwd, work, timeout):
    executable = Path("/usr/bin/sandbox-exec")
    if sys.platform != "darwin" or not executable.is_file():
        return {"status": "UNAVAILABLE", "reason": "A supported macOS sandbox-exec host is unavailable", "exit_code": None}, b""
    if not argv or not all(isinstance(x, str) and x for x in argv):
        raise Invalid("Check argv must contain nonempty strings")
    profile = work / "sandbox.sb"
    profile.write_text(sandbox_profile(work))
    home, tmp = work / "home", work / "tmp"
    home.mkdir(exist_ok=True); tmp.mkdir(exist_ok=True)
    env = {"PATH": os.environ.get("PATH", os.defpath), "HOME": str(home), "TMPDIR": str(tmp),
           "XDG_CACHE_HOME": str(home / ".cache"), "LC_ALL": "C", "PYTHONDONTWRITEBYTECODE": "1",
           "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
           "GIT_TERMINAL_PROMPT": "0", "GIT_ALLOW_PROTOCOL": "", "GIT_NO_LAZY_FETCH": "1"}
    command = [str(executable), "-f", str(profile), *argv]
    start = time.monotonic()
    log = work / "command.log"
    with log.open("wb") as stream:
        try:
            process = subprocess.Popen(command, cwd=cwd, env=env, stdin=subprocess.DEVNULL,
                                       stdout=stream, stderr=subprocess.STDOUT, start_new_session=True)
            try:
                code = process.wait(timeout=timeout)
                status = "PASS" if code == 0 else "FAIL"
            except subprocess.TimeoutExpired:
                status, code = "TIMEOUT", None
            finally:
                try:
                    os.killpg(process.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
                process.wait()
        except OSError as exc:
            return {"status": "UNAVAILABLE", "reason": str(exc), "exit_code": None}, b""
    output = log.read_bytes()
    if b"sandbox_apply:" in output or b"sandbox-exec: " in output and code != 0:
        status = "UNAVAILABLE"
    return {"status": status, "exit_code": code, "duration_seconds": round(time.monotonic() - start, 3),
            "isolation": "macos-seatbelt-deny-default", "profile_sha256": digest(profile.read_bytes()),
            "argv": argv}, output


def probe():
    with tempfile.TemporaryDirectory(prefix="simplify-probe-", dir=Path(tempfile.gettempdir()).resolve()) as temporary:
        outer = Path(temporary)
        work = outer / "allowed"
        work.mkdir()
        forbidden = outer / "forbidden"
        forbidden.write_text("unchanged")
        code = """import pathlib, socket, sys
p = pathlib.Path(sys.argv[1])
pathlib.Path('inside').write_text('allowed')
try:
    p.write_text('escaped')
except PermissionError:
    pass
else:
    raise SystemExit('outside write permitted')
try:
    s = socket.socket()
    s.bind(('127.0.0.1', 0))
except PermissionError:
    pass
else:
    raise SystemExit('network permitted')
print('filesystem and network restrictions enforced')
"""
        record, log = execute([sys.executable, "-I", "-B", "-c", code, str(forbidden)], work, work, 10)
        record["probe_log"] = log.decode("utf-8", "replace")
        record["outside_file_unchanged"] = forbidden.read_text() == "unchanged"
        if record["status"] != "PASS" or not record["outside_file_unchanged"]:
            record["status"] = "UNAVAILABLE"
        return record


def run_checks(run, snapshots, checks, harness=None):
    capability = probe()
    receipts = []
    for check in checks:
        for side in ("base", "head"):
            record = {"check_id": check["id"], "kind": check["kind"], "side": side,
                      "snapshot_digest": snapshots[side]["digest"], "contract_ids": check["contract_ids"]}
            if capability["status"] != "PASS":
                receipts.append({**record, "status": "UNAVAILABLE", "reason": capability.get("probe_log", capability.get("reason", "Isolation unavailable"))})
                continue
            with tempfile.TemporaryDirectory(prefix="simplify-check-", dir=Path(tempfile.gettempdir()).resolve()) as name:
                work = Path(name)
                source = work / "source"
                source.mkdir()
                try:
                    materialize(run, snapshots[side], source)
                    if harness:
                        harness_dir = work / "harness"
                        harness_dir.mkdir()
                        for path, data in harness.items():
                            target = harness_dir / relative(path)
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(data)
                    argv = [arg.replace("{python}", sys.executable).replace("{source}", str(source)).replace("{harness}", str(work / "harness")) for arg in check["argv"]]
                    result, log = execute(argv, source, work, check["timeout_seconds"])
                except Invalid as exc:
                    result, log = {"status": "UNAVAILABLE", "reason": str(exc)}, b""
                record.update(result)
                record["log_sha256"] = digest(log)
                record["log"] = log.decode("utf-8", "replace")
                receipts.append(record)
    return capability, receipts
