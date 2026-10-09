#!/usr/bin/env python3
"""Check, preview, or install this skill's declared utilities."""
import argparse
import json
import os
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
import urllib.request


def run(command, env, capture=False):
    result = subprocess.run(command, env=env, text=True, stdout=subprocess.PIPE if capture else sys.stderr, stderr=subprocess.PIPE if capture else sys.stderr, check=False)
    if result.returncode:
        raise RuntimeError("Command failed (%s): %s" % (result.returncode, shlex.join(command)))
    return result.stdout.strip() if capture else None


def version(value):
    found = re.search(r"(?<!\d)(\d+)\.(\d+)(?:\.(\d+))?", value)
    return tuple(int(v or 0) for v in found.groups()) if found else None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="Check selected utilities; no installation")
    mode.add_argument("--plan", action="store_true", help="Print installation commands; execute none")
    mode.add_argument("--install", action="store_true", help="Install missing selected utilities")
    parser.add_argument("--tool", action="append", default=[], help="Select a declared utility; repeatable")
    parser.add_argument("--prefix", type=Path, help="Isolated npm/Python installation directory")
    parser.add_argument("--application", type=Path, help="User-supplied .app bundle for a private desktop utility")
    parser.add_argument("--env", action="store_true", help="Print shell exports for the selected utility environment")
    args = parser.parse_args()
    root = Path(__file__).resolve().parents[1]
    manifest = json.loads((root / "dependencies.json").read_text())
    prefix = (args.prefix or Path.home() / ".local/share/agent-skill-tools" / manifest["skill"]).expanduser().resolve()
    tools = {item["id"]: item for item in manifest["tools"]}
    wanted = args.tool or [item["id"] for item in manifest["tools"] if item["required"]]
    ordered = []

    def select(name, stack=()):
        if name not in tools:
            raise ValueError("Unknown utility: " + name)
        if name in stack:
            raise ValueError("Dependency cycle: " + name)
        if name in ordered:
            return
        for dependency in tools[name].get("depends", []):
            select(dependency, stack + (name,))
        ordered.append(name)

    for name in wanted:
        select(name)
    env = dict(os.environ)
    search = [str(prefix / "node_modules/.bin"), str(prefix / "venv/bin"), str(root / "scripts"), str(Path.home() / ".local/bin"),
              "/opt/homebrew/opt/openjdk@21/bin", "/usr/local/opt/openjdk@21/bin",
              env.get("PATH", os.defpath), "/Applications/Docker.app/Contents/Resources/bin", "/Library/TeX/texbin", "/opt/homebrew/bin", "/usr/local/bin"]
    env["PATH"] = os.pathsep.join(search)
    env["PLAYWRIGHT_BROWSERS_PATH"] = str(prefix / "browsers")
    states = []

    def ready(tool):
        kind = tool["kind"]
        if kind == "bundle":
            return (root / tool["path"]).is_file(), str(root / tool["path"])
        if kind == "application":
            candidate = Path.home() / "Applications" / tool["app_name"]
            other = Path("/Applications") / tool["app_name"]
            found = candidate if candidate.is_dir() else other
            return found.is_dir(), str(found)
        if kind == "browser":
            node = shutil.which("node", path=env["PATH"])
            if not node:
                return False, None
            script = "console.log(require(%s)[%s].executablePath())" % (json.dumps(str(prefix / "node_modules/playwright")), json.dumps(tool["browser"]))
            result = subprocess.run([node, "-e", script], env=env, text=True, capture_output=True, check=False)
            candidate = Path(result.stdout.strip()) if result.stdout.strip() else None
            return result.returncode == 0 and candidate is not None and candidate.is_file(), str(candidate) if candidate else None
        if tool.get("module"):
            executable = prefix / "venv/bin/python"
            if not executable.is_file():
                return False, None
            probe = [str(executable), "-B", "-c", "import importlib, importlib.metadata; importlib.import_module(%r); print(importlib.metadata.version(%r))" % (tool["module"], tool["distribution"])]
            result = subprocess.run(probe, env=env, text=True, capture_output=True, check=False)
            value = result.stdout.strip()
            valid = result.returncode == 0
            if tool.get("min_version"):
                valid = valid and version(value) is not None and version(value) >= version(tool["min_version"])
            if "==" in tool.get("package", ""):
                valid = valid and value == tool["package"].split("==", 1)[1]
            return valid, str(executable) if valid else None
        if kind == "npm" and not tool.get("command"):
            package_name = tool["package"]
            if package_name.startswith("@"):
                package_name = "@" + package_name[1:].split("@")[0]
            else:
                package_name = package_name.split("@")[0]
            candidate = prefix / "node_modules" / package_name / "package.json"
            valid = candidate.is_file()
            if valid and tool.get("version_major"):
                installed = json.loads(candidate.read_text()).get("version", "")
                valid = version(installed) is not None and version(installed)[0] == tool["version_major"]
            if valid and tool.get("min_version"):
                installed = json.loads(candidate.read_text()).get("version", "")
                valid = version(installed) is not None and version(installed) >= version(tool["min_version"])
            return valid, str(candidate)
        candidates = []
        for directory in env["PATH"].split(os.pathsep):
            candidate = Path(directory) / tool["command"]
            if candidate.is_file() and os.access(candidate, os.X_OK) and str(candidate) not in candidates:
                candidates.append(str(candidate))
        for executable in candidates:
            if tool.get("min_version") or tool.get("version_major"):
                probe = subprocess.run([executable, *tool.get("version_args", ["--version"])], env=env,
                                       text=True, capture_output=True, check=False)
                value = version(probe.stdout + probe.stderr)
                if probe.returncode or value is None or (tool.get("min_version") and value < version(tool["min_version"])) or (tool.get("version_major") and value[0] != tool["version_major"]):
                    continue
            env["PATH"] = str(Path(executable).parent) + os.pathsep + env["PATH"]
            return True, executable
        return False, candidates[0] if candidates else None

    def installation(tool):
        kind = tool["kind"]
        if kind == "brew":
            brew = shutil.which("brew", path=env["PATH"]) or "brew"
            return [[brew, "install", *(["--cask"] if tool.get("cask") else []), tool["package"]]]
        if kind == "npm":
            npm = shutil.which("npm", path=env["PATH"]) or "npm"
            return [[npm, "install", "--prefix", str(prefix), "--no-audit", "--no-fund", tool["package"]]]
        if kind == "pip":
            commands = []
            if not (prefix / "venv/bin/python").is_file():
                commands.append([sys.executable, "-B", "-m", "venv", str(prefix / "venv")])
            commands.append([str(prefix / "venv/bin/python"), "-B", "-m", "pip", "install", tool["package"]])
            return commands
        if kind == "bundled-npm":
            npm = shutil.which("npm", path=env["PATH"]) or "npm"
            return [[npm, "install", "--prefix", str(root / tool["path"]), "--no-audit", "--no-fund"]]
        if kind == "browser":
            return [[str(prefix / "node_modules/.bin/playwright"), "install", tool["browser"]]]
        if kind == "official-script":
            return [["download", tool["url"], "TEMPORARY_INSTALLER"], ["/bin/bash", "TEMPORARY_INSTALLER", *tool["arguments"]]]
        if kind == "application":
            return [["copy-application", str(args.application or "USER_SUPPLIED_APP"), str(Path.home() / "Applications" / tool["app_name"])]]
        return []

    for name in ordered:
        tool = tools[name]
        if tool["kind"] == "bundled-npm":
            found = (root / tool["path"] / "node_modules").is_dir()
            location = str(root / tool["path"])
        else:
            found, location = ready(tool)
        commands = [] if found else installation(tool)
        state = {"tool": name, "status": "available" if found else "missing", "location": location,
                 "purpose": tool["purpose"], "commands": commands, "documentation": tool["documentation"]}
        states.append(state)
        if args.install and not found:
            if tool["kind"] == "bundle":
                raise RuntimeError("Bundled resource missing: " + tool["path"])
            if platform.system() != "Darwin" and tool["kind"] in ("brew", "application"):
                raise RuntimeError("This installation recipe targets macOS; use the linked official instructions on other systems")
            if tool["kind"] == "brew" and not shutil.which("brew", path=env["PATH"]):
                raise RuntimeError("Homebrew is missing. Run scripts/bootstrap.sh --install-homebrew, then retry")
            if tool["kind"] == "application":
                if not args.application or args.application.suffix != ".app" or not args.application.is_dir():
                    raise RuntimeError("Provide the utility's distributable .app bundle with --application; setup cannot invent a private download")
                target = Path.home() / "Applications" / tool["app_name"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(args.application, target)
            elif tool["kind"] == "official-script":
                with tempfile.TemporaryDirectory(prefix="skill-setup-") as temporary:
                    installer = Path(temporary) / "install.sh"
                    with urllib.request.urlopen(tool["url"], timeout=60) as response:
                        installer.write_bytes(response.read())
                    run(["/bin/bash", str(installer), *tool["arguments"]], env)
            else:
                for command in commands:
                    run(command, env)
            if tool["kind"] == "bundled-npm":
                found, location = (root / tool["path"] / "node_modules").is_dir(), str(root / tool["path"])
            else:
                found, location = ready(tool)
            if not found:
                raise RuntimeError("Installation did not establish the selected utility: " + name)
            state.update(status="installed", location=location)
    env["PATH"] = os.pathsep.join(dict.fromkeys([str(prefix / "node_modules/.bin"), str(prefix / "venv/bin"), *env["PATH"].split(os.pathsep)]))
    result = {"skill": manifest["skill"], "mode": "install" if args.install else "plan" if args.plan else "check",
              "prefix": str(prefix), "tools": states, "available_tools": list(tools),
              "path": env["PATH"], "external_requirements": manifest.get("external_requirements", []),
              "ready": all(item["status"] in ("available", "installed") for item in states)}
    if args.env and not result["ready"]:
        print(json.dumps(result, indent=2), file=sys.stderr)
        return 2
    if args.env:
        print("export PATH=" + shlex.quote(env["PATH"]))
        print("export NODE_PATH=" + shlex.quote(str(prefix / "node_modules")))
        print("export PLAYWRIGHT_BROWSERS_PATH=" + shlex.quote(env["PLAYWRIGHT_BROWSERS_PATH"]))
        java = shutil.which("java", path=env["PATH"])
        if "java" in ordered and java and "/openjdk@21/" in java:
            print("export JAVA_HOME=" + shlex.quote(str(Path(java).resolve().parents[1])))
    else:
        print(json.dumps(result, indent=2))
    return 0 if args.plan or result["ready"] else 2


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (OSError, ValueError, RuntimeError, KeyError, TypeError) as error:
        print(json.dumps({"status": "error", "error": str(error)}), file=sys.stderr)
        raise SystemExit(1)
