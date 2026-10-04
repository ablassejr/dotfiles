"""Behavioral tests of the command-line and local artifact contracts."""
import json
import os
import signal
from pathlib import Path
import subprocess
import sys
import tempfile
import time
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
RUNTIME = os.environ.get("SUBTRACTIVE_TEST_RUNTIME")
EXPIRY = "2099-01-01T00:00:00+00:00"

BASELINE = '''import sys

def api_normalize(value):
    text = value.strip()
    if not text:
        raise ValueError("empty input")
    return text.lower()

def batch_normalize(value):
    text = value.strip()
    if not text:
        raise ValueError("empty input")
    return text.lower()

if __name__ == "__main__":
    try:
        mode, value = sys.argv[1:]
        if mode == "api":
            print(api_normalize(value))
        elif mode == "batch":
            print(batch_normalize(value))
        else:
            raise ValueError("unknown mode")
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
'''
CANDIDATE = '''import sys

def normalize(value):
    text = value.strip()
    if not text:
        raise ValueError("empty input")
    return text.lower()

if __name__ == "__main__":
    try:
        mode, value = sys.argv[1:]
        if mode not in {"api", "batch"}:
            raise ValueError("unknown mode")
        print(normalize(value))
    except ValueError as error:
        print(str(error), file=sys.stderr)
        sys.exit(2)
'''
BOUNDARY_TEST = '''import subprocess
import sys
import unittest

class AppContract(unittest.TestCase):
    def test_supported_modes_and_errors(self):
        for mode in ["api", "batch"]:
            for value, expected in [(" ALPHA ", "alpha"), (" ÉCOLE ", "école")]:
                with self.subTest(mode=mode, value=value):
                    result = subprocess.run([sys.executable, "app.py", mode, value], capture_output=True, text=True)
                    self.assertEqual(result.returncode, 0)
                    self.assertEqual(result.stdout.strip(), expected)
            result = subprocess.run([sys.executable, "app.py", mode, " "], capture_output=True, text=True)
            self.assertEqual((result.returncode, result.stderr.strip()), (2, "empty input"))
        result = subprocess.run([sys.executable, "app.py", "unknown", "value"], capture_output=True, text=True)
        self.assertEqual((result.returncode, result.stderr.strip()), (2, "unknown mode"))
'''


class CommandCase(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="subtractive-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.repo, self.run = self.root / "repo", self.root / "run"
        self.repo.mkdir()
        (self.repo / "app.py").write_text(BASELINE)
        (self.repo / "test_app.py").write_text(BOUNDARY_TEST)
        self.policy = {"rules": [{"pattern": "test_*.py", "category": "tests", "reason": "Boundary tests"},
                                  {"pattern": "generated/*", "category": "generated", "reason": "Derived fixture"},
                                  {"pattern": "*.py", "category": "production", "reason": "Owned source"},
                                  {"pattern": "buildtool", "category": "tooling", "reason": "Owned extensionless script"},
                                  {"pattern": "*.txt", "category": "support", "reason": "Supporting text"}]}
        self.basis = {"authorization": "Synthetic fixture authorizes static audit and verification",
                      "preserve": [{"id": "normalization", "behavior": "Both CLI modes normalize text and report documented errors"}],
                      "roots": ["app.py CLI"], "variants": ["api", "batch"], "seams": ["CLI to normalization"],
                      "unknown_consumers": [], "approved_retirements": []}
        self.checks = {"checks": [{"id": "cli-contract", "kind": "e2e", "argv": ["python3", "-m", "unittest", "-v"],
                                   "version_argv": ["python3", "--version"], "obligations": ["normalization"],
                                   "seams": ["CLI to normalization"], "exercised_scope": ["Both modes, Unicode, empty input, unsupported mode"],
                                   "skipped_scope": []}]}
        self.env = dict(os.environ, PYTHONDONTWRITEBYTECODE="1")

    def save(self, name, value):
        path = self.root / name
        path.write_text(json.dumps(value, indent=2))
        return path

    def command(self, script, *arguments, code=0):
        result = subprocess.run([sys.executable, str(PACKAGE / "scripts" / script)] + list(map(str, arguments)),
                                capture_output=True, text=True, env=self.env, timeout=900)
        self.assertEqual(result.returncode, code, result.stdout + result.stderr)
        return result

    def initialize(self):
        self.command("snapshot.py", "init", self.repo, self.run, "--inventory", self.save("inventory.json", self.policy),
                     "--basis", self.save("basis.json", self.basis))
        return json.loads((self.run / "run.json").read_text())

    def candidate(self):
        snapshot = self.initialize()
        auth = {"baseline_hash": snapshot["baseline_hash"], "source": "Synthetic fixture permits editing this disposable copy",
                "allowed_paths": ["*.py", "buildtool"], "expires": EXPIRY}
        self.command("snapshot.py", "experiment", self.run, "--authorization", self.save("authorization.json", auth))
        (self.run / "candidate" / "app.py").write_text(CANDIDATE)
        return snapshot

    def proposal(self, name="C1", unknown=None, depends=None):
        return {"id": name, "responsibility": "Text normalization", "change": "consolidation", "canonical_owner": "normalize",
                "preserve": ["normalization"], "consumers": ["api CLI", "batch CLI"], "unknown_consumers": unknown or [],
                "retired_behavior": [], "eliminate": ["Duplicate normalizer"], "removal_paths": ["app.py"],
                "evidence": ["Both supported modes are exercised through the CLI"], "rationale": "replaceable",
                "depends_on": depends or [], "target": "Both supported modes call one normalizer and keep their existing errors."}

    def review(self, result):
        return self.save("review-input.json", {"patch_hash": result["patch_hash"], "evidence_hash": result["evidence_hash"],
                    "reviewer": "Synthetic contract reviewer", "structural_improvement": "Two active normalizers share one implementation",
                    "counterexamples": [], "unresolved": [], "anti_gaming": "The maintained tests retain all declared CLI contracts"})


class StaticBehavior(CommandCase):
    def test_inventory_and_snapshot_preserve_dirty_files_and_metadata(self):
        (self.repo / ".git").mkdir()
        (self.repo / ".git" / "index").write_bytes(b"dirty index fixture")
        (self.repo / "untracked.py").write_text("VALUE = 1\n")
        before = {p.relative_to(self.repo).as_posix(): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()}
        record = self.initialize()
        self.assertEqual(record["files"]["untracked.py"]["category"], "production")
        self.assertEqual((self.run / "baseline" / "untracked.py").read_bytes(), before["untracked.py"])
        after = {p.relative_to(self.repo).as_posix(): p.read_bytes() for p in self.repo.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        (self.repo / ".git" / "index").write_bytes(b"new index state")
        self.command("report.py", self.run, code=2)
        self.assertEqual((self.repo / ".git" / "index").read_bytes(), b"new index state")

    def test_unknown_inventory_is_visible_and_prevents_execution(self):
        (self.repo / "unknown.asset").write_bytes(b"unclassified")
        record = self.initialize()
        self.assertEqual(record["files"]["unknown.asset"]["category"], "unclassified")
        self.assertTrue(record["gaps"])
        self.command("collect.py", self.run, "--checks", self.save("checks.json", self.checks),
                     "--runtime", self.root / "missing-runtime.json", code=2)

    def test_classification_does_not_hide_owned_build_paths(self):
        (self.repo / "build").mkdir()
        (self.repo / "build" / "owned.py").write_text("VALUE = 1\n")
        record = self.initialize()
        self.assertEqual(record["files"]["build/owned.py"]["category"], "production")
        self.assertEqual((self.run / "baseline" / "build" / "owned.py").read_text(), "VALUE = 1\n")

    def test_symlinks_are_inventoried_without_copying_their_targets(self):
        outside = self.root / "outside.txt"
        outside.write_text("outside authorized source")
        (self.repo / "link.py").symlink_to(outside)
        inventory = self.root / "discovery.json"
        self.command("snapshot.py", "inventory", self.repo, inventory)
        self.assertEqual(json.loads(inventory.read_text())["files"]["link.py"]["kind"], "symlink")
        self.command("snapshot.py", "init", self.repo, self.run, "--inventory", self.save("inventory.json", self.policy),
                     "--basis", self.save("basis.json", self.basis), code=2)
        self.assertEqual(outside.read_text(), "outside authorized source")

    def test_original_and_existing_output_are_protected(self):
        self.command("snapshot.py", "init", self.repo, self.repo / "run", "--inventory", self.save("inventory.json", self.policy),
                     "--basis", self.save("basis.json", self.basis), code=2)
        self.initialize()
        self.command("snapshot.py", "init", self.repo, self.run, "--inventory", self.root / "inventory.json", "--basis", self.root / "basis.json", code=2)
        (self.repo / "app.py").write_text("user edit\n")
        self.command("report.py", self.run, code=2)
        self.assertEqual((self.repo / "app.py").read_text(), "user edit\n")

    def test_plan_deduplicates_closures_and_blocks_dependent_unknowns(self):
        snapshot = self.initialize()
        proposals = {"baseline_hash": snapshot["baseline_hash"], "candidates": [self.proposal(unknown=["dynamic plugin consumer"]),
                      self.proposal("C2", depends=["C1"])]}
        self.command("plan.py", self.run, self.save("candidates.json", proposals))
        plan = json.loads((self.run / "plan.json").read_text())
        self.assertEqual(plan["unique_removal_paths"], ["app.py"])
        self.assertEqual(plan["overlaps"], {"app.py": ["C1", "C2"]})
        self.assertEqual(set(plan["blocked"]), {"C1", "C2"})
        self.assertEqual(plan["estimated_source_reduction"], "UNKNOWN")

    def test_plan_rejects_cycles_and_unapproved_retirements_remain_blocked(self):
        snapshot = self.initialize()
        first, second = self.proposal(depends=["C2"]), self.proposal("C2", depends=["C1"])
        self.command("plan.py", self.run, self.save("cycle.json", {"baseline_hash": snapshot["baseline_hash"], "candidates": [first, second]}), code=2)
        first["depends_on"], first["change"], first["retired_behavior"] = [], "retirement", ["batch support"]
        self.command("plan.py", self.run, self.save("retirement.json", {"baseline_hash": snapshot["baseline_hash"], "candidates": [first]}))
        self.assertIn("C1", json.loads((self.run / "plan.json").read_text())["blocked"])

    def test_experiment_requires_current_authorization_and_preserves_original(self):
        snapshot = self.initialize()
        auth = {"baseline_hash": "0" * 64, "source": "Test approval", "allowed_paths": ["*.py"], "expires": EXPIRY}
        self.command("snapshot.py", "experiment", self.run, "--authorization", self.save("authorization.json", auth), code=2)
        auth.update(baseline_hash=snapshot["baseline_hash"], expires="2000-01-01T00:00:00+00:00")
        self.command("snapshot.py", "experiment", self.run, "--authorization", self.save("authorization.json", auth), code=2)
        self.assertEqual((self.repo / "app.py").read_text(), BASELINE)

    def test_declared_passes_and_loose_exception_flags_cannot_verify(self):
        self.candidate()
        for malformed in [{}, {"measurement": {}, "checks": {"all": "PASS"}}, {"measurement": {"before": -1, "after": True}}]:
            with self.subTest(record=malformed):
                (self.run / "verification.json").write_text(json.dumps(malformed))
                self.command("verify.py", self.run, "--finalize", "--review", self.root / "unused.json", code=2)
        self.command("verify.py", self.run, "--allow-ratio-exception", code=2)

    def test_root_and_test_contract_gaps_block_verification(self):
        self.basis["unknown_consumers"] = ["Public library exports and dynamic registrations require investigation"]
        self.candidate()
        self.command("verify.py", self.run, "--checks", self.save("checks.json", self.checks), "--runtime", self.save("runtime.json", {}), code=2)

    def test_prepared_candidate_copy_and_excluded_material(self):
        (self.repo / ".env").write_text("SYNTHETIC_VALUE=example\n")
        self.policy["rules"].insert(0, {"pattern": ".env", "category": "excluded", "reason": "Private runtime state"})
        self.initialize()
        prepared = self.root / "prepared"
        prepared.mkdir()
        (prepared / "app.py").write_text(CANDIDATE)
        (prepared / "test_app.py").write_text(BOUNDARY_TEST)
        self.command("snapshot.py", "candidate", self.run, prepared)
        self.assertEqual((self.run / "candidate" / "app.py").read_text(), CANDIDATE)
        self.assertFalse((self.run / "baseline" / ".env").exists())
        self.assertEqual((self.repo / ".env").read_text(), "SYNTHETIC_VALUE=example\n")
        self.command("snapshot.py", "candidate", self.run, prepared, code=2)

    def test_linked_git_metadata_changes_are_detected(self):
        common, worktree = self.root / "git-common", self.root / "git-worktree"
        common.mkdir()
        worktree.mkdir()
        (self.repo / ".git").write_text(f"gitdir: {worktree}\n")
        (worktree / "commondir").write_text(str(common))
        (worktree / "index").write_bytes(b"index state")
        (common / "packed-refs").write_text("initial references")
        self.initialize()
        (common / "packed-refs").write_text("changed references")
        self.command("report.py", self.run, code=2)
        self.assertEqual((common / "packed-refs").read_text(), "changed references")


@unittest.skipUnless(RUNTIME, "Set SUBTRACTIVE_TEST_RUNTIME to a preinstalled local Docker/cloc runtime JSON")
class LiveIntegration(CommandCase):
    def collect(self, expected=2):
        self.command("verify.py", self.run, "--checks", self.save("checks.json", self.checks), "--runtime", RUNTIME, code=expected)
        return json.loads((self.run / "verification.json").read_text())

    def test_real_execution_measurement_review_and_drift(self):
        (self.repo / "one.py").write_text("VALUE = 1\n")
        (self.repo / "two.py").write_text("VALUE = 1\n")
        (self.repo / "generated").mkdir()
        (self.repo / "generated" / "copy.py").write_text("VALUE = 1\n")
        (self.repo / "buildtool").write_text("#!/usr/bin/env python3\nprint('tool')\n")
        self.candidate()
        (self.run / "candidate" / "one.py").rename(self.run / "candidate" / "moved.py")
        self.env["SUBTRACTIVE_TEST_SECRET"] = "synthetic-host-value"
        sentinel = self.root / "host-only.txt"
        sentinel.write_text("host file")
        probe = "\n".join(["import os, pathlib, socket", "assert os.getuid() > 0",
                            "assert 'SUBTRACTIVE_TEST_SECRET' not in os.environ", f"assert not pathlib.Path({str(sentinel)!r}).exists()",
                            "assert not pathlib.Path('/var/run/docker.sock').exists()", "pathlib.Path('/tmp/scratch').write_text('ok')",
                            "try:", "    pathlib.Path('/forbidden-host-write').write_text('bad')", "except OSError:", "    pass",
                            "else:", "    raise AssertionError('root write permitted')", "s=socket.socket(); s.settimeout(0.3)",
                            "try:", "    s.connect(('192.0.2.1', 9))", "except OSError:", "    pass", "else:",
                            "    raise AssertionError('network available')", "finally:", "    s.close()", "print('isolation contract passed')"])
        self.checks["checks"].append({"id": "isolation", "kind": "behavior", "argv": ["python3", "-c", probe],
                                      "version_argv": ["python3", "--version"], "obligations": [], "seams": [],
                                      "exercised_scope": ["Scratch writes, denied egress, no host files, no inherited secret"], "skipped_scope": []})
        result = self.collect()
        self.assertEqual(result["status"], "INCOMPLETE")
        m = result["measurement"]
        self.assertGreater(m["before"], m["after"])
        self.assertEqual(m["file_counts"]["baseline"]["one.py"], 1)
        self.assertEqual(m["file_counts"]["baseline"]["two.py"], 1)
        self.assertIn("generated/copy.py", m["excluded_files"]["baseline"])
        self.assertGreater(m["by_category"]["tests"]["baseline"], 0)
        self.assertGreater(m["by_category"]["tooling"]["baseline"], 0)
        self.assertEqual(m["moved_files"], [["one.py", "moved.py"]])
        review = self.review(result)
        self.command("verify.py", self.run, "--finalize", "--review", review)
        self.command("report.py", self.run)
        self.assertIn("**VERIFIED**", (self.run / "report.md").read_text())
        self.assertEqual((self.repo / "app.py").read_text(), BASELINE)
        final = json.loads((self.run / "verification.json").read_text())
        for value in [{}, dict(m, before=-1), dict(m, after=True), dict(m, added=0, removed=0), dict(m, ratio_met=not m["ratio_met"])]:
            damaged = dict(final, measurement=value)
            (self.run / "verification.json").write_text(json.dumps(damaged))
            self.command("verify.py", self.run, "--finalize", "--review", review, code=2)
        (self.run / "verification.json").write_text(json.dumps(final))
        log = Path(final["receipts"][0]["execution"]["log"])
        original_log = log.read_bytes()
        log.write_bytes(b"declared PASS")
        self.command("verify.py", self.run, "--finalize", "--review", review, code=2)
        log.write_bytes(original_log)
        (self.run / "candidate" / "app.py").write_text(CANDIDATE + "\nEXTRA = 1\n")
        self.command("verify.py", self.run, "--finalize", "--review", review, code=2)
        self.command("report.py", self.run)
        self.assertIn("**INCOMPLETE**", (self.run / "report.md").read_text())

    def test_ratio_exception_is_scoped_and_cannot_waive_missing_measurements(self):
        (self.repo / "data.py").write_text("".join(f"VALUE_{i} = {i}\n" for i in range(80)))
        self.candidate()
        (self.run / "candidate" / "data.py").write_text("".join(f"VALUE_{i} = {i+1}\n" for i in range(80)))
        result = self.collect()
        self.assertFalse(result["measurement"]["ratio_met"])
        review = self.review(result)
        self.command("verify.py", self.run, "--finalize", "--review", review, code=1)
        exception = {"patch_hash": result["patch_hash"], "waived": ["ratio"], "source": "Synthetic numeric-policy approval",
                     "rationale": "Exercise the ratio exception contract without changing preservation obligations", "expires": EXPIRY}
        self.command("verify.py", self.run, "--finalize", "--review", review, "--exception", self.save("exception-input.json", exception))
        final = json.loads((self.run / "verification.json").read_text())
        self.assertEqual(final["status"], "VERIFIED_WITH_EXCEPTIONS")
        exception["patch_hash"] = "0" * 64
        self.command("verify.py", self.run, "--finalize", "--review", review, "--exception", self.save("exception-input.json", exception), code=2)
        final["measurement"] = {}
        (self.run / "verification.json").write_text(json.dumps(final))
        self.command("verify.py", self.run, "--finalize", "--review", review, "--exception", self.root / "exception-input.json", code=2)

    def test_baseline_failure_remains_failed_with_passing_candidate_and_waiver(self):
        (self.repo / "app.py").write_text(BASELINE.replace("return text.lower()", "return text.upper()"))
        self.candidate()
        result = self.collect(expected=1)
        baseline = [r for r in result["receipts"] if r["subject"] == "baseline"]
        candidate = [r for r in result["receipts"] if r["subject"] == "candidate"]
        self.assertTrue(any(r["execution"]["exit_code"] for r in baseline))
        self.assertTrue(all(r["execution"]["exit_code"] == 0 for r in candidate))
        exception = {"patch_hash": result["patch_hash"], "waived": ["ratio", "net_growth"], "source": "Synthetic numerical approval",
                     "rationale": "Numerical permission cannot convert a failed contract into a pass", "expires": EXPIRY}
        self.command("verify.py", self.run, "--finalize", "--review", self.review(result),
                     "--exception", self.save("exception-input.json", exception), code=1)
        self.assertEqual(json.loads((self.run / "verification.json").read_text())["status"], "FAILED")

    def test_command_timeout_is_recorded_as_a_nonpassing_execution(self):
        self.initialize()
        runtime = json.loads(Path(RUNTIME).read_text())
        runtime["timeout_seconds"] = 2
        self.checks["checks"][0]["argv"] = ["python3", "-c", "import time; time.sleep(30)"]
        self.command("collect.py", self.run, "--checks", self.save("checks.json", self.checks),
                     "--runtime", self.save("timeout-runtime.json", runtime), code=1)
        receipts = json.loads((self.run / "baseline-receipts.json").read_text())["receipts"]
        self.assertEqual(receipts[0]["execution"]["exit_code"], 124)
        self.assertTrue(receipts[0]["execution"]["timed_out"])

    def test_cancellation_removes_the_reported_container(self):
        self.initialize()
        self.checks["checks"][0]["argv"] = ["python3", "-c", "import time; print('running boundary check', flush=True); time.sleep(60)"]
        checks = self.save("checks.json", self.checks)
        process = subprocess.Popen([sys.executable, str(PACKAGE / "scripts" / "collect.py"), str(self.run),
                                    "--checks", str(checks), "--runtime", RUNTIME],
                                   stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, env=self.env)
        try:
            deadline = time.monotonic() + 90
            while time.monotonic() < deadline:
                if any("running boundary check" in p.read_text() for p in (self.run / "logs").glob("*.log")):
                    break
                if process.poll() is not None:
                    self.fail("Collector stopped before the cancellable command began: " + str(process.communicate()))
                time.sleep(0.1)
            else:
                self.fail("The cancellable command did not start")
            process.send_signal(signal.SIGINT)
            output, errors = process.communicate(timeout=30)
            self.assertEqual(process.returncode, 130, output + errors)
            attempts = [json.loads(p.read_text()) for p in (self.run / "logs").glob("*.attempt.json")]
            interrupted = [a for a in attempts if a["state"] == "interrupted"]
            self.assertEqual(len(interrupted), 1)
            runtime = json.loads(Path(RUNTIME).read_text())
            inspected = subprocess.run([runtime["docker"], "--host", "unix://" + runtime["socket"], "container", "inspect",
                                        "--format", "{{.State.Running}}", interrupted[0]["container"]],
                                       capture_output=True, text=True, timeout=15)
            self.assertNotEqual(inspected.returncode, 0)
            self.assertIn("No such", inspected.stderr)
        finally:
            if process.poll() is None:
                process.send_signal(signal.SIGINT)
                process.communicate(timeout=30)

    def test_unsupported_maintained_file_produces_incomplete_measurement(self):
        (self.repo / "opaque.unknown-language").write_text("owned executable content\n")
        self.policy["rules"].insert(0, {"pattern": "*.unknown-language", "category": "production", "reason": "Owned executable fixture"})
        self.candidate()
        result = self.command("verify.py", self.run, "--checks", self.save("checks.json", self.checks), "--runtime", RUNTIME, code=2)
        self.assertEqual(json.loads(result.stdout)["status"], "INCOMPLETE")

    def test_missing_tool_version_is_incomplete(self):
        self.initialize()
        self.checks["checks"][0]["version_argv"] = ["python3", "-c", "pass"]
        result = self.command("collect.py", self.run, "--checks", self.save("checks.json", self.checks), "--runtime", RUNTIME, code=2)
        self.assertEqual(json.loads(result.stdout)["status"], "INCOMPLETE")

    def test_output_limit_is_a_nonpassing_execution(self):
        self.initialize()
        self.checks["checks"][0]["argv"] = ["python3", "-c", "import sys; sys.stdout.write('x' * (9 * 1024 * 1024))"]
        self.command("collect.py", self.run, "--checks", self.save("checks.json", self.checks), "--runtime", RUNTIME, code=1)
        receipt = json.loads((self.run / "baseline-receipts.json").read_text())["receipts"][0]
        self.assertEqual(receipt["execution"]["exit_code"], 125)
        self.assertLessEqual(Path(receipt["execution"]["log"]).stat().st_size, 8 * 1024 * 1024)

    def test_test_only_growth_needs_separate_growth_authorization(self):
        self.candidate()
        additions = "".join(f"TEST_CASE_{i} = {i}\n" for i in range(40))
        (self.run / "candidate" / "test_extra.py").write_text(additions)
        result = self.collect()
        self.assertGreater(result["measurement"]["net"], 0)
        self.assertGreater(result["measurement"]["by_category"]["tests"]["candidate"], result["measurement"]["by_category"]["tests"]["baseline"])
        exception = {"patch_hash": result["patch_hash"], "waived": ["ratio"], "source": "Synthetic ratio approval",
                     "rationale": "Growth is a separate policy decision", "expires": EXPIRY}
        review = self.review(result)
        self.command("verify.py", self.run, "--finalize", "--review", review,
                     "--exception", self.save("exception-input.json", exception), code=1)
        exception["waived"].append("net_growth")
        self.command("verify.py", self.run, "--finalize", "--review", review,
                     "--exception", self.save("exception-input.json", exception))


if __name__ == "__main__":
    unittest.main()
