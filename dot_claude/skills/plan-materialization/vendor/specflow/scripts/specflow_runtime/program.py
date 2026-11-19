"""Validate the exact program snapshot before planning and publication advance."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory

from .client import RuntimeFailure, canonical, digest
from .workstreams import POLICY


def validate_completion(job, result):
    headers = job.get("customHeaders", {})
    if result.get("status") != "completed" or headers.get("programPolicy") != POLICY:
        return
    output = result.get("variables", {})
    compiling = headers.get("phase") == "compile_program"
    snapshot = output if compiling else job.get("variables", {})
    plan, manifest, binding = (
        snapshot.get(key)
        for key in ("linearPlan", "semanticManifest", "programBinding")
    )
    if (
        not isinstance(plan, dict)
        or not isinstance(manifest, dict)
        or not isinstance(binding, dict)
    ):
        raise RuntimeFailure(
            "invalid_program_plan",
            "Supply linearPlan, semanticManifest, and programBinding for the three-person program.",
        )
    if (
        not isinstance(binding.get("ref"), str)
        or not binding["ref"].strip()
        or binding.get("hash") != digest(canonical(plan))
    ):
        raise RuntimeFailure(
            "invalid_program_plan",
            "programBinding must identify and hash the exact canonical JSON linearPlan.",
        )
    if not compiling and any(
        key in output and output[key] != snapshot.get(key)
        for key in ("linearPlan", "semanticManifest", "programBinding")
    ):
        raise RuntimeFailure(
            "invalid_program_plan",
            "Publication and dispatch must preserve the validated planning snapshot; revise it through program planning.",
        )
    with TemporaryDirectory(prefix="specflow-program-") as directory:
        root = Path(directory)
        (root / "plan.json").write_text(json.dumps(plan), encoding="utf-8")
        (root / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
        checked = subprocess.run(
            [
                sys.executable,
                "-B",
                str(Path(__file__).resolve().parents[1] / "specflow"),
                "validate-linear-plan",
                str(root / "plan.json"),
                "--manifest",
                str(root / "manifest.json"),
                "--json",
            ],
            capture_output=True,
            text=True,
            timeout=60,
            check=False,
        )
    try:
        report = json.loads(checked.stdout)
    except ValueError as error:
        raise RuntimeFailure(
            "invalid_program_plan",
            "The plan validator did not return its declared JSON contract.",
        ) from error
    if checked.returncode != 0:
        raise RuntimeFailure(
            "invalid_program_plan",
            "The program must pass validate-linear-plan before advancing.",
            report.get("errors"),
        )
