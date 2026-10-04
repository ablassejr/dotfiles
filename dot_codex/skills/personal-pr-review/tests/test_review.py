"""Behavior tests through the public CLI, real Git repositories, and report files."""

import copy
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
import uuid


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "review.py"


class ReviewBehavior(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="pr-review-test-", dir=os.environ.get("REVIEW_TEST_ROOT"))
        self.root = Path(self.temp.name).resolve()
        self.repo = self.root / "source"
        self.repo.mkdir()
        self.env = {"PATH": os.environ.get("PATH", os.defpath), "LC_ALL": "C",
                    "GIT_CONFIG_GLOBAL": os.devnull, "GIT_CONFIG_NOSYSTEM": "1",
                    "GIT_AUTHOR_NAME": "Review Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
                    "GIT_COMMITTER_NAME": "Review Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        self.git("init", "-q", "-b", "main")
        self.write("a.py", "def calculate(amount):\n    return amount\n")
        self.write("test_contract.py", "def test_contract():\n    assert True\n")
        self.base = self.commit("Fixture baseline")
        self.write("a.py", "def calculate(amount):\n    return amount * 2\n")
        self.head = self.commit("Fixture behavior change")

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, value):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(value if isinstance(value, bytes) else value.encode())

    def git(self, *args, repo=None):
        result = subprocess.run(["git", "-C", str(repo or self.repo), "-c", "commit.gpgsign=false", *args],
                                env=self.env, capture_output=True, check=False)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        return result.stdout.decode().strip()

    def commit(self, message):
        self.git("add", "--all")
        self.git("commit", "-q", "-m", message)
        return self.git("rev-parse", "HEAD")

    def cli(self, *args, expected=0):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                                capture_output=True, text=True, check=False)
        self.assertEqual(result.returncode, expected, result.stdout + result.stderr)
        return json.loads(result.stdout) if result.stdout.strip() else json.loads(result.stderr)

    def prepare(self, *args, repo=None, output=None, expected=0):
        output = output or self.root / ("review-" + uuid.uuid4().hex)
        self.cli("prepare", "--repo", repo or self.repo, "--output", output,
                 *(args or ("--base", self.base)), expected=expected)
        return output

    def read(self, output, name):
        return json.loads((output / name).read_text())

    def source_evidence(self, output, path="a.py", side="head", lines=True):
        args = ["evidence", "--output", output, "--path", path, "--side", side,
                "--relation", "changed", "--reason", "Fixture changed contract"]
        if lines:
            args += ["--start", "1", "--end", "2"]
        return self.cli(*args)["id"]

    def receipt(self, output, kind, body=None):
        path = self.root / (uuid.uuid4().hex + ".json")
        path.write_text(json.dumps(body or {"fixture": True, "kind": kind,
                                           "analysis_id": self.read(output, "context-packet.json")["identity"]["analysis_id"]}))
        return self.cli("receipt", "--output", output, "--kind", kind, "--file", path,
                        "--reason", "Synthetic host-boundary fixture; not a real model/check execution")["id"]

    def completed(self, output):
        assessment = self.read(output, "assessment.json")
        evidence = {}
        for item in assessment["coverage"]:
            evidence[item["path"]] = self.source_evidence(output, item["path"], lines=False)
            item.update(status="reviewed", evidence_ids=[evidence[item["path"]]], explanation="Fixture boundary inspected")
        source = self.source_evidence(output)
        isolation = self.receipt(output, "isolation")
        assessment["host"] = {"model": "local", "isolation_evidence_id": isolation}
        assessment["behavior_summary"] = "When the fixture receives an amount, it returns twice that amount."
        for lens in assessment["lenses"]:
            lens.update(status="reviewed", explanation="Fixture semantic input at the public assessment boundary")
        assessment["checks"] = [{"name": "fixture-contract", "status": "passed", "analysis_id": assessment["analysis_id"],
                                  "command": ["fixture-runner", "contract"], "provenance": "supplied-fixture-contract",
                                  "evidence_id": self.receipt(output, "tool_log"), "isolation_evidence_id": isolation,
                                  "exit_code": 0, "explanation": "Synthetic external-check receipt for contract validation"}]
        assessment["checks_explanation"] = "Fixture supplies one relevant check receipt"
        assessment["challenge"] = {"status": "completed", "evidence_id": self.receipt(output, "challenge"),
                                    "reviewer": "fresh-local-fixture-context", "covered_finding_ids": []}
        assessment["unresolved_questions"] = []
        return assessment, source

    def finish(self, output, assessment, expected=0):
        path = output / "assessment.json"
        path.write_text(json.dumps(assessment))
        return self.cli("finalize", "--output", output, "--assessment", path, expected=expected)

    def finding(self, evidence, **changes):
        finding = {"id": "FND-001", "kind": "defect", "title": "Fixture behavior violates supplied contract",
                   "root_cause": "amount transformation", "severity": "HIGH", "confidence": "HIGH",
                   "derivation": "BEHAVIORAL", "relationship": "INTRODUCED", "blocking": True,
                   "disposition": "kept", "location": {"path": "a.py", "side": "head", "start_line": 2, "end_line": 2},
                   "claim": "The fixture transforms an amount at the public boundary.", "impact": "The consumer receives a different amount.",
                   "recommendation": "Resolve the supplied fixture contract.", "evidence_ids": [evidence],
                   "counterevidence_search": "Inspected the complete fixture function for a surrounding guard.",
                   "counterevidence_ids": [evidence], "deletion": None}
        finding.update(changes)
        return finding

    def repository_state(self, root=None):
        root = root or self.repo
        result = {}
        for path in root.rglob("*"):
            info = path.lstat()
            if path.is_symlink():
                value = ("symlink", os.readlink(path), stat.S_IMODE(info.st_mode))
            elif path.is_file():
                value = ("file", path.read_bytes(), stat.S_IMODE(info.st_mode))
            else:
                value = ("directory", stat.S_IMODE(info.st_mode))
            result[str(path.relative_to(root))] = value
        return result

    def test_range_pins_objects_and_preserves_dirty_index_untracked_ignored_and_refs(self):
        self.write("a.py", "def calculate(amount):\n    return amount * 3\n")
        self.git("add", "a.py")
        self.write("a.py", "def calculate(amount):\n    return amount * 4\n")
        self.write("notes.txt", "untracked personal notes")
        self.write(".gitignore", "cache/\n")
        self.write("cache/input.txt", "ignored content")
        original = self.repository_state()
        output = self.prepare()
        packet = self.read(output, "context-packet.json")
        self.assertEqual((packet["identity"]["base_commit"], packet["identity"]["head_commit"]), (self.base, self.head))
        self.assertEqual(packet["identity"]["working_tree_clean"], False)
        ev = self.source_evidence(output)
        record = next(e for e in self.read(output, "context-manifest.json")["evidence"] if e["id"] == ev)
        self.assertIn("amount * 2", record["excerpt"])
        self.assertEqual(self.repository_state(), original)

    def test_staged_and_working_tree_have_distinct_contents_and_untracked_scope(self):
        self.write("a.py", "def calculate(amount):\n    return amount * 3\n")
        self.git("add", "a.py")
        self.write("a.py", "def calculate(amount):\n    return amount * 4\n")
        self.write("new.py", "new = 1\n")
        staged, working = self.prepare("--staged"), self.prepare("--working-tree")
        for output, expected in ((staged, "amount * 3"), (working, "amount * 4")):
            key = self.source_evidence(output)
            record = next(e for e in self.read(output, "context-manifest.json")["evidence"] if e["id"] == key)
            self.assertIn(expected, record["excerpt"])
        self.assertEqual({c["path"] for c in self.read(staged, "context-packet.json")["changes"]}, {"a.py"})
        self.assertEqual({c["path"] for c in self.read(working, "context-packet.json")["changes"]}, {"a.py", "new.py"})
        self.assertNotEqual(self.read(staged, "context-packet.json")["identity"]["analysis_id"], self.read(working, "context-packet.json")["identity"]["analysis_id"])

    def test_renames_binary_and_unusual_paths_remain_visible(self):
        path = "renamed\tfile\n.py"
        (self.repo / "a.py").rename(self.repo / path)
        self.write("binary.dat", b"\x00\xff\x01")
        self.commit("Move and binary fixture")
        output = self.prepare("--base", self.head)
        items = {c["path"]: c for c in self.read(output, "context-packet.json")["changes"]}
        self.assertEqual((items[path]["old_path"], items[path]["added_lines"], items[path]["removed_lines"]), ("a.py", 0, 0))
        self.assertTrue(items["binary.dat"]["binary"])
        self.assertIsNone(items["binary.dat"]["added_lines"])
        self.assertEqual(self.read(output, "code-mass.json")["maintained_added"], None)

    def test_root_commit_and_unborn_index_are_supported(self):
        output = self.prepare("--commit", self.base)
        self.assertIsNone(self.read(output, "context-packet.json")["identity"]["comparison_base"])
        unborn = self.root / "unborn"
        unborn.mkdir()
        self.git("init", "-q", "-b", "main", repo=unborn)
        (unborn / "first.txt").write_text("first\n")
        self.git("add", "first.txt", repo=unborn)
        staged = self.prepare("--staged", repo=unborn)
        self.assertEqual([c["path"] for c in self.read(staged, "context-packet.json")["changes"]], ["first.txt"])

    def test_merge_base_and_explicit_direct_comparison_differ(self):
        self.git("checkout", "-q", "-b", "other", self.base)
        self.write("other.txt", "Other branch\n")
        other = self.commit("Other branch change")
        self.git("checkout", "-q", "main")
        normal = self.prepare("--base", other)
        direct = self.prepare("--base", other, "--comparison", "direct")
        self.assertEqual(self.read(normal, "context-packet.json")["identity"]["comparison_base"], self.base)
        self.assertEqual({c["path"] for c in self.read(normal, "context-packet.json")["changes"]}, {"a.py"})
        self.assertEqual({c["path"] for c in self.read(direct, "context-packet.json")["changes"]}, {"a.py", "other.txt"})

    def test_merge_commit_requires_a_parent_and_multiple_merge_bases_are_explicit(self):
        tree = self.git("rev-parse", "HEAD^{tree}")
        other = self.git("commit-tree", tree, "-p", self.base, "-m", "Other parent")
        merge1 = self.git("commit-tree", tree, "-p", self.head, "-p", other, "-m", "Merge one")
        merge2 = self.git("commit-tree", tree, "-p", other, "-p", self.head, "-m", "Merge two")
        self.prepare("--commit", merge1, expected=2)
        valid = self.prepare("--commit", merge1, "--parent", "2")
        self.assertEqual(self.read(valid, "context-packet.json")["identity"]["comparison_base"], other)
        ambiguous = self.prepare("--base", merge1, "--head", merge2, expected=2)
        self.assertEqual(self.read(ambiguous, "analysis-summary.json")["verdict"], "INCOMPLETE")

    def test_missing_local_ref_does_not_modify_repository(self):
        before = self.repository_state()
        output = self.prepare("--base", "origin/missing", expected=2)
        self.assertEqual(self.repository_state(), before)
        self.assertIn("no fetch", self.read(output, "analysis-summary.json")["error"])
        missing_blob = self.git("rev-parse", "HEAD:a.py")
        (self.repo / ".git" / "objects" / missing_blob[:2] / missing_blob[2:]).unlink()
        transport_marker = self.root / "transport-was-run"
        transport = self.root / "transport.sh"
        transport.write_text("#!/bin/sh\necho unexpected > '" + str(transport_marker) + "'\n")
        transport.chmod(0o755)
        with (self.repo / ".git" / "config").open("a") as stream:
            stream.write(f'\n[remote "origin"]\n url = ext::{transport}\n promisor = true\n partialclonefilter = blob:none\n')
        missing_before = self.repository_state()
        self.prepare(expected=2)
        self.assertEqual(self.repository_state(), missing_before)
        self.assertFalse(transport_marker.exists(), "Missing objects must not trigger remote transport")

    def test_worktree_uses_shared_git_integrity_and_allows_detached_head(self):
        linked = self.root / "linked"
        self.git("worktree", "add", "--detach", str(linked), self.head)
        before = self.repository_state()
        output = self.prepare("--base", self.base, repo=linked)
        self.assertEqual(self.repository_state(), before)
        self.assertEqual(self.read(output, "context-packet.json")["identity"]["head_commit"], self.head)
        self.git("update-ref", "refs/heads/another", self.base)
        self.cli("finalize", "--output", output, "--assessment", output / "assessment.json", expected=4)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "STALE")

    def test_output_can_be_explicitly_inside_repo_but_cannot_replace_input(self):
        output = self.prepare(output=self.repo / ".review" / "run")
        self.source_evidence(output)
        self.cli("prepare", "--repo", self.repo, "--base", self.base, "--output", output, expected=2)
        for bad in (self.repo, self.repo / ".git" / "report"):
            self.cli("prepare", "--repo", self.repo, "--base", self.base, "--output", bad, expected=2)
        alias = self.root / "alias"
        alias.symlink_to(self.repo, target_is_directory=True)
        self.cli("prepare", "--repo", self.repo, "--base", self.base, "--output", alias / "escape", expected=2)

    def test_source_symlinks_are_evidence_without_following_targets(self):
        outside = self.root / "private.txt"
        outside.write_text("outside input\n")
        (self.repo / "pointer").symlink_to(outside)
        output = self.prepare("--working-tree")
        record = self.cli("evidence", "--output", output, "--path", "pointer", "--side", "head",
                          "--start", "1", "--end", "1", "--relation", "changed", "--reason", "Symlink contract")
        self.assertEqual(record["excerpt"], str(outside))
        self.assertEqual(outside.read_text(), "outside input\n")

    def test_nested_gitlink_changes_are_visible_and_not_reported_as_clean(self):
        nested = self.repo / "nested"
        nested.mkdir()
        external_git = self.root / "nested-git-storage"
        self.git("init", "-q", "-b", "main", "--separate-git-dir", str(external_git), repo=nested)
        (nested / "dependency.py").write_text("def amount():\n    return 1\n")
        self.git("add", "dependency.py", repo=nested)
        self.git("commit", "-q", "-m", "Nested baseline", repo=nested)
        self.commit("Track nested dependency")
        (nested / "dependency.py").write_text("def amount():\n    return 999\n")
        before = self.repository_state()
        before_git = self.repository_state(external_git)
        output = self.prepare("--working-tree")
        packet = self.read(output, "context-packet.json")
        self.assertEqual({c["path"] for c in packet["changes"]}, {"nested"})
        self.assertFalse(packet["identity"]["working_tree_clean"])
        self.assertIn("separate pinned review", packet["changes"][0]["limitation"])
        self.assertEqual(self.repository_state(), before)
        self.assertEqual(self.repository_state(external_git), before_git)
        self.git("commit", "--allow-empty", "-q", "-m", "Nested reference movement", repo=nested)
        self.cli("evidence", "--output", output, "--side", "head", "--path", "nested",
                 "--relation", "changed", "--reason", "Inspect nested change", expected=2)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "STALE")

    def test_preparation_cannot_pass_and_receipt_driven_finalization_produces_reports(self):
        output = self.prepare()
        self.finish(output, self.read(output, "assessment.json"), expected=3)
        self.assertEqual(self.read(output, "analysis-summary.json")["complete"], False)
        assessment, _ = self.completed(output)
        self.finish(output, assessment)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "PASS")
        for name in ("review.md", "technical-debt.md", "findings.json", "analysis-summary.json", "tool-results.json", "code-mass.json", "context-manifest.json", "report.html"):
            self.assertGreater((output / name).stat().st_size, 0)
        self.assertIn("twice that amount", (output / "review.md").read_text())
        self.assertEqual(self.read(output, "tool-results.json")["origin"], "supplied-local-evidence")

    def test_independent_challenge_and_available_checks_are_completion_requirements(self):
        for missing in ("challenge", "check", "host", "coverage", "lens"):
            with self.subTest(missing=missing):
                output = self.prepare()
                assessment, _ = self.completed(output)
                if missing == "challenge":
                    assessment["challenge"]["status"] = "unavailable"
                elif missing == "check":
                    assessment["checks"][0]["status"] = "unavailable"
                elif missing == "host":
                    assessment["host"]["model"] = "unverified"
                elif missing == "coverage":
                    assessment["coverage"] = []
                else:
                    assessment["lenses"] = []
                self.finish(output, assessment, expected=3)
                self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "INCOMPLETE")

    def test_supported_defect_and_executed_failure_hold_even_with_gaps(self):
        output = self.prepare()
        assessment, ev = self.completed(output)
        assessment["findings"] = [self.finding(ev)]
        assessment["challenge"]["covered_finding_ids"] = ["FND-001"]
        assessment["unresolved_questions"] = ["An additional environment is unavailable"]
        self.finish(output, assessment, expected=1)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "HOLD")
        self.assertFalse(self.read(output, "analysis-summary.json")["complete"])
        assessment["findings"] = []
        assessment["checks"][0].update(status="failed", exit_code=1)
        self.finish(output, assessment, expected=1)
        self.assertIn("Deterministic check failed", self.read(output, "analysis-summary.json")["blocking_reasons"][0])

    def test_debt_is_separate_deduplicated_and_ratio_is_advisory(self):
        output = self.prepare()
        assessment, ev = self.completed(output)
        debt = self.finding(ev, kind="debt", blocking=False, relationship="UNLOCKED", severity="MEDIUM")
        assessment["findings"] = [debt, dict(debt, id="TD-DUPLICATE"), self.finding(ev, id="UNRELATED", relationship="UNRELATED")]
        assessment["code_mass"].update(added=100, removed=0, evidence_id=self.receipt(output, "code_mass"),
                                        method="Synthetic maintained-line delta receipt", ratio_added=5, ratio_removed=6,
                                        ratio_basis="Fixture's explicitly chosen advisory ratio")
        self.finish(output, assessment)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "PASS_WITH_DEBT")
        self.assertEqual(len(self.read(output, "findings.json")["findings"]), 1)
        self.assertEqual(self.read(output, "code-mass.json")["ratio_status"], "BELOW_ADVISORY_TARGET")
        self.assertIn(debt["title"], (output / "technical-debt.md").read_text())

    def test_unverified_deletion_and_mismatched_assessment_are_rejected(self):
        output = self.prepare()
        assessment, ev = self.completed(output)
        valid = copy.deepcopy(assessment)
        self.finish(output, valid)
        assessment["findings"] = [self.finding(ev, kind="debt", blocking=False, severity="MEDIUM",
                                                deletion={"safe": True, "replacement_evidence_ids": [],
                                                          "consumer_evidence_ids": [ev], "compatibility_evidence_ids": [ev], "unresolved_risks": []})]
        self.finish(output, assessment, expected=2)
        self.assertEqual(self.read(output, "analysis-summary.json")["verdict"], "INCOMPLETE")
        valid["analysis_id"] = "another-review"
        self.finish(output, valid, expected=2)

    def test_edited_untracked_file_stales_review_even_if_git_status_shape_is_same(self):
        self.write("notes.txt", "before")
        output = self.prepare()
        assessment, _ = self.completed(output)
        self.finish(output, assessment)
        self.write("notes.txt", "after")
        self.finish(output, self.read(output, "assessment.json"), expected=4)
        self.assertEqual(self.read(output, "analysis-summary.json")["integrity"], "CHANGED")
        self.assertEqual((self.repo / "notes.txt").read_text(), "after")
        self.assertIn("STALE", (output / "review.md").read_text())
        self.assertIn("STALE", (output / "report.html").read_text())

    def test_local_artifact_integrity_coordinates_and_schema_are_checked(self):
        for invalid in ("hash", "coordinate", "one-coordinate", "exit", "unknown", "fractional", "missing-evidence", "prepared-snapshot", "manifest-array", "manifest-entry"):
            with self.subTest(invalid=invalid):
                output = self.prepare()
                assessment, ev = self.completed(output)
                self.finish(output, assessment)
                if invalid == "hash":
                    item = next(e for e in self.read(output, "context-manifest.json")["evidence"] if e["kind"] == "tool_log")
                    (output / item["artifact"]).write_text("tampered")
                elif invalid == "coordinate":
                    assessment["findings"] = [self.finding(ev, location={"path": "a.py", "side": "head", "start_line": 100, "end_line": 102})]
                elif invalid == "one-coordinate":
                    assessment["findings"] = [self.finding(ev, location={"path": "a.py", "side": "head", "start_line": 1, "end_line": None})]
                elif invalid == "exit":
                    assessment["checks"][0]["exit_code"] = 1
                elif invalid == "unknown":
                    assessment["publish"] = True
                elif invalid == "fractional":
                    assessment["code_mass"]["added"] = 1.5
                elif invalid == "prepared-snapshot":
                    packet = self.read(output, "context-packet.json")
                    packet["trees"]["head"]["a.py"] = packet["trees"]["base"]["a.py"]
                    (output / "context-packet.json").write_text(json.dumps(packet))
                elif invalid == "manifest-array":
                    (output / "context-manifest.json").write_text("[]")
                elif invalid == "manifest-entry":
                    manifest = self.read(output, "context-manifest.json")
                    manifest["evidence"] = [None]
                    (output / "context-manifest.json").write_text(json.dumps(manifest))
                else:
                    assessment["checks"][0]["evidence_id"] = "EV-missing"
                self.finish(output, assessment, expected=2)
                self.assertEqual(self.read(output, "analysis-summary.json")["complete"], False)
                self.assertIn("INCOMPLETE", (output / "report.html").read_text())

    def test_hostile_filters_hooks_and_pagers_are_not_executed(self):
        marker = self.root / "unexpected-execution"
        hook = self.root / "hostile.sh"
        hook.write_text("#!/bin/sh\necho executed > '" + str(marker) + "'\n")
        hook.chmod(0o755)
        with (self.repo / ".git" / "config").open("a") as stream:
            stream.write(f'\n[core]\n fsmonitor = {hook}\n pager = {hook}\n[diff]\n external = {hook}\n[diff "hostile"]\n textconv = {hook}\n[filter "hostile"]\n clean = {hook}\n smudge = {hook}\n')
        self.write(".gitattributes", "*.py diff=hostile filter=hostile\n")
        output = self.prepare("--working-tree")
        self.source_evidence(output)
        self.assertFalse(marker.exists(), "The declared boundary requires no execution of repository-supplied tools")

    def test_html_treats_review_content_as_text(self):
        output = self.prepare()
        assessment, _ = self.completed(output)
        assessment["behavior_summary"] = '<script src="https://example.invalid/a.js"></script>'
        self.finish(output, assessment)
        from html.parser import HTMLParser
        class Reader(HTMLParser):
            def __init__(self):
                super().__init__()
                self.scripts = []
                self.text = []
            def handle_starttag(self, tag, attrs):
                if tag == "script":
                    self.scripts.append(attrs)
            def handle_data(self, data):
                self.text.append(data)
        reader = Reader()
        reader.feed((output / "report.html").read_text())
        self.assertEqual(reader.scripts, [], "Self-contained report must render evidence without executing it")
        self.assertIn(assessment["behavior_summary"], "".join(reader.text))


if __name__ == "__main__":
    unittest.main()
