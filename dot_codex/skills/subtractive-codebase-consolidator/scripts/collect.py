"""Execute declared tools in a disposable container and retain actual output."""
import argparse
import io
import json
import os
from pathlib import Path, PurePosixPath
import selectors
import subprocess
import tempfile
import tarfile
import time
import uuid

from contracts import Checks, Execution, Receipt, Runtime
from snapshot import current, digest, entrypoint, load_run, read, require, scan, unchanged, write

BOOTSTRAP = """import os,sys,tarfile,shutil,pathlib
os.makedirs('/tmp/source')
with tarfile.open(fileobj=sys.stdin.buffer,mode='r|') as archive:
    for member in archive:
        path = pathlib.PurePosixPath(member.name)
        if member.isdir() and str(path) == 'source':
            continue
        if not member.isfile() or path.is_absolute() or '..' in path.parts or not (str(path) == 'cloc.pl' or path.parts[0] in {'source','cloc-lib'}):
            raise ValueError('Invalid sandbox input')
        target = pathlib.Path('/tmp') / path
        target.parent.mkdir(parents=True,exist_ok=True)
        with target.open('wb') as output:
            shutil.copyfileobj(archive.extractfile(member),output)
        target.chmod(member.mode & 0o777)
os.chdir('/tmp/source')
os.execvpe(sys.argv[1],sys.argv[1:],dict(os.environ))
"""


def engine_hash():
    return digest({p.name: digest(p.read_bytes()) for p in sorted(Path(__file__).parent.glob("*.py"))})


class Sandbox:
    def __init__(self, runtime, logs):
        self.runtime = Runtime.model_validate(runtime).model_dump()
        self.logs = Path(logs).resolve()
        self.logs.mkdir(parents=True, exist_ok=True)
        require(Path(runtime["docker"]).is_absolute() and Path(runtime["docker"]).is_file(), "Docker executable unavailable")
        require(Path(runtime["socket"]).is_absolute() and Path(runtime["socket"]).is_socket(), "A local Unix Docker socket is required")
        require(Path(runtime["cloc"]).is_absolute() and Path(runtime["cloc"]).is_file(), "A preinstalled standalone cloc Perl script is required")
        require(Path(runtime["cloc"]).read_bytes().startswith(b"#!/usr/bin/perl"), "Use the cloc Perl script, not a platform-specific shell wrapper")
        self.library = Path(self.runtime["cloc_library"]).resolve() if self.runtime["cloc_library"] else None
        self.counter_hash = self.counter_digest()
        self.binding = digest({"runtime": self.runtime, "counter": self.counter_hash, "engine": engine_hash()})

    def counter_digest(self):
        return digest({"script": digest(Path(self.runtime["cloc"]).read_bytes()),
                       "library": scan(self.library) if self.library else {}})

    def execute(self, source, argv, label):
        require(argv and all(isinstance(x, str) and x and "\x00" not in x for x in argv), "Invalid command argument vector")
        source = Path(source).resolve()
        files = scan(source)
        require(all(v["kind"] == "file" for v in files.values()), "Sandbox inputs must be regular files")
        require(self.counter_digest() == self.counter_hash, "Counter changed")
        token = uuid.uuid4().hex
        name = "subtractive-" + token
        log = self.logs / f"{label}-{token}.log"
        attempt_path = self.logs / f"{label}-{token}.attempt.json"
        attempt = {"container": name, "argv": argv, "state": "running"}
        write(attempt_path, attempt)
        with tempfile.TemporaryDirectory(prefix="subtractive-config-", dir=self.logs.parent) as config:
            archive = Path(config) / "input.tar"
            with tarfile.open(archive, "w") as bundle:
                directory = tarfile.TarInfo("source")
                directory.type, directory.mode = tarfile.DIRTYPE, 0o755
                bundle.addfile(directory)
                for path, entry in files.items():
                    data = (source / path).read_bytes()
                    require(digest(data) == entry["sha256"], "Input changed while preparing sandbox")
                    info = tarfile.TarInfo("source/" + path)
                    info.size, info.mode = len(data), 0o755 if entry["mode"] & 0o111 else 0o644
                    bundle.addfile(info, io.BytesIO(data))
                data = Path(self.runtime["cloc"]).read_bytes()
                info = tarfile.TarInfo("cloc.pl")
                info.size, info.mode = len(data), 0o444
                bundle.addfile(info, io.BytesIO(data))
                if self.library:
                    for path, entry in scan(self.library).items():
                        require(entry["kind"] == "file", "Counter libraries must contain regular files")
                        data = (self.library / path).read_bytes()
                        info = tarfile.TarInfo("cloc-lib/" + path)
                        info.size, info.mode = len(data), 0o444
                        bundle.addfile(info, io.BytesIO(data))
            env = {"PATH": "/usr/local/bin:/usr/bin:/bin", "HOME": config}
            docker = [self.runtime["docker"], "--host", "unix://" + self.runtime["socket"], "--config", config]
            inspected = subprocess.run(docker + ["image", "inspect", "--format", "{{json .Config.Volumes}}", self.runtime["image"]],
                                       env=env, capture_output=True, text=True, timeout=self.runtime["timeout_seconds"], check=False)
            require(inspected.returncode == 0, "The pinned local tool image is unavailable")
            volumes = json.loads(inspected.stdout) or {}
            require(isinstance(volumes, dict), "Unrecognized image volume metadata")
            volume_options = []
            for destination in sorted(volumes):
                path = PurePosixPath(destination)
                require(path.is_absolute() and ".." not in path.parts and str(path) == destination and
                        destination not in {"/", "/tmp", "/proc", "/sys", "/dev"} and
                        not destination.startswith(("/tmp/", "/proc/", "/sys/", "/dev/")) and
                        not any(c in destination for c in ":,\n\r\x00"), "Image volume overlaps a required execution path")
                volume_options += ["--tmpfs", destination + ":ro,nosuid,nodev,size=1m"]
            attempt["masked_volumes"] = sorted(volumes)
            write(attempt_path, attempt)
            command = docker + ["run", "--interactive", "--rm", "--name", name, "--pull", "never", "--network", "none",
                "--platform", self.runtime["platform"],
                "--read-only", "--cap-drop", "ALL", "--security-opt", "no-new-privileges", "--no-healthcheck",
                "--pids-limit", "128", "--memory", "1g", "--memory-swap", "1g", "--cpus", "2",
                "--user", "65534:65534", "--tmpfs", "/tmp:rw,nosuid,nodev,size=512m,mode=1777"] + volume_options + [
                "--entrypoint", "/usr/bin/env", self.runtime["image"], "-i",
                "PATH=/usr/local/bin:/usr/bin:/bin", "HOME=/tmp", "TMPDIR=/tmp", "LANG=C.UTF-8",
                "PERL5LIB=/tmp/cloc-lib",
                "PYTHONDONTWRITEBYTECODE=1", "python3", "-c", BOOTSTRAP] + argv
            timed_out, limited, total = False, False, 0
            completed = False
            started = time.monotonic()
            input_stream = archive.open("rb")
            process = subprocess.Popen(command, stdin=input_stream, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, env=env)
            try:
                with log.open("wb") as output, selectors.DefaultSelector() as selector:
                    selector.register(process.stdout, selectors.EVENT_READ)
                    while selector.get_map():
                        if time.monotonic() - started > self.runtime["timeout_seconds"]:
                            timed_out = True
                            break
                        for key, _ in selector.select(0.2):
                            data = os.read(key.fd, 65536)
                            if not data:
                                selector.unregister(key.fileobj)
                                continue
                            total += len(data)
                            if total > 8 * 1024 * 1024:
                                limited = True
                                break
                            output.write(data)
                            output.flush()
                        if limited:
                            break
                if timed_out or limited:
                    process.kill()
                code = process.wait(timeout=10)
                completed = True
            finally:
                if process.poll() is None:
                    process.kill()
                    process.wait()
                process.stdout.close()
                input_stream.close()
                if not completed or timed_out or limited:
                    try:
                        cleanup = subprocess.run(docker + ["rm", "--force", name], env=env, capture_output=True,
                                                 text=True, timeout=15, check=False)
                        deadline = time.monotonic() + 15
                        while True:
                            remaining = deadline - time.monotonic()
                            require(remaining > 0, f"Sandbox cleanup could not confirm removal of {name}: {cleanup.stderr.strip()}")
                            listed = subprocess.run(docker + ["container", "ls", "--all", "--filter", "name=" + name,
                                                     "--format", "{{.Names}}"], env=env, capture_output=True,
                                                    text=True, timeout=remaining, check=False)
                            require(listed.returncode == 0, f"Sandbox cleanup could not inspect {name}: {listed.stderr.strip()}")
                            if name not in {entry for line in listed.stdout.splitlines() for entry in line.split(",")}:
                                break
                            time.sleep(0.1)
                    except subprocess.TimeoutExpired as error:
                        raise ValueError(f"Sandbox cleanup timed out; remove only container {name}") from error
                attempt["state"] = "finished" if completed else "interrupted"
                write(attempt_path, attempt)
            result = {"argv": argv, "exit_code": 124 if timed_out else 125 if limited else code,
                      "log": str(log), "log_hash": digest(log.read_bytes()), "timed_out": timed_out}
            Execution.model_validate(result)
            return result


def run_checks(directory, run, sandbox, checks, subject):
    source = Path(directory) / subject
    snapshot_hash = digest(scan(source, run["inventory"]))
    receipts = []
    for check in checks["checks"]:
        version = sandbox.execute(source, check["version_argv"], subject + "-" + check["id"] + "-version")
        require(version["exit_code"] != 0 or Path(version["log"]).read_text().strip(), "Tool version output is empty")
        execution = sandbox.execute(source, check["argv"], subject + "-" + check["id"])
        receipt = {"subject": subject, "snapshot_hash": snapshot_hash, "check": check,
                   "image": sandbox.runtime["image"], "rules_hash": digest(check),
                   "version": version, "execution": execution}
        Receipt.model_validate(receipt)
        receipts.append(receipt)
        require(digest(scan(source, run["inventory"])) == snapshot_hash, "Snapshot changed during check execution")
        unchanged(run)
    return receipts


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("run")
    p.add_argument("--checks", required=True)
    p.add_argument("--runtime", required=True)
    p.add_argument("--subject", choices=["baseline", "candidate"], default="baseline")
    args = p.parse_args()
    run = load_run(args.run)
    unchanged(run)
    require(not run["gaps"], "Resolve inventory gaps before executing tools")
    if args.subject == "candidate":
        current(args.run, run)
    checks = read(args.checks, Checks)
    sandbox = Sandbox(read(args.runtime, Runtime), Path(args.run) / "logs")
    receipts = run_checks(args.run, run, sandbox, checks, args.subject)
    output = Path(args.run) / f"{args.subject}-receipts.json"
    write(output, {"runtime_hash": sandbox.binding, "receipts": receipts})
    print(output)
    if any(r["execution"]["exit_code"] or r["version"]["exit_code"] for r in receipts):
        raise SystemExit(1)


if __name__ == "__main__":
    entrypoint(main)
