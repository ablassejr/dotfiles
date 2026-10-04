"""Behavioral tests through CLI requests, real Git repositories, and local artifacts."""

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "simplify.py"
OBLIGATIONS = ["consumers", "dynamic_use", "contracts", "behavior", "replacement",
               "failure_paths", "state_ownership", "history", "test_preservation"]
BASE = '''def _select(name):
    if not isinstance(name, str):
        raise TypeError("name must be text")
    if not name.strip():
        raise ValueError("name must not be empty")
    return name.strip().lower()

def _old_select(name):
    if not isinstance(name, str):
        raise TypeError("name must be text")
    if not name.strip():
        raise ValueError("name must not be empty")
    return name.strip().lower()

def resolve(name):
    return _old_select(name)
'''
TARGET = BASE[:BASE.index("def _old_select")] + '''def resolve(name):
    return _select(name)
'''
CONTRACT = '''import unittest
from provider import resolve

class ProviderContract(unittest.TestCase):
    def test_identity(self):
        self.assertEqual(resolve(" AWS "), "aws")
    def test_missing_identity(self):
        with self.assertRaisesRegex(ValueError, "name must not be empty"):
            resolve(" ")
    def test_nontext_identity(self):
        with self.assertRaisesRegex(TypeError, "name must be text"):
            resolve(None)
'''


def load(path):
    return json.loads(path.read_bytes())


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2) + "\n")


class CLIContract(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(dir=Path(tempfile.gettempdir()).resolve(), prefix="simplify-test-")
        self.root = Path(self.temp.name)
        self.repo = self.root / "repo"
        self.repo.mkdir()
        self.run = self.root / "audit"
        self.g("init", "-b", "main", "--template=")
        self.put("provider.py", BASE)
        self.put("tests/test_provider.py", CONTRACT)
        self.commit("Define provider identity normalization and required errors")

    def tearDown(self):
        self.temp.cleanup()

    def g(self, *args):
        env = {"PATH": os.environ.get("PATH", os.defpath), "HOME": str(self.root),
               "GIT_CONFIG_NOSYSTEM": "1", "GIT_CONFIG_GLOBAL": os.devnull,
               "GIT_AUTHOR_NAME": "Fixture", "GIT_AUTHOR_EMAIL": "fixture@example.invalid",
               "GIT_COMMITTER_NAME": "Fixture", "GIT_COMMITTER_EMAIL": "fixture@example.invalid"}
        result = subprocess.run(["git", "-C", str(self.repo), "-c", "commit.gpgSign=false", *args],
                                capture_output=True, env=env, timeout=20)
        self.assertEqual(result.returncode, 0, result.stderr.decode())
        return result.stdout.decode().strip()

    def put(self, name, value):
        path = self.repo / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(value)

    def commit(self, message):
        self.g("add", "--all")
        self.g("commit", "-m", message)
        return self.g("rev-parse", "HEAD")

    def cli(self, *args, code=0):
        result = subprocess.run([sys.executable, "-B", str(SCRIPT), *map(str, args)],
                                capture_output=True, timeout=60)
        self.assertEqual(result.returncode, code, result.stdout.decode() + result.stderr.decode())
        try:
            return json.loads(result.stdout)
        except ValueError:
            self.fail("CLI did not return JSON: " + result.stdout.decode() + result.stderr.decode())

    def audit(self, *extra):
        return self.cli("audit", "--repo", self.repo, "--scope", ".", "--output", self.run, *extra)

    def bytes_fingerprint(self):
        return {str(p.relative_to(self.repo)): (p.lstat().st_mode, os.readlink(p) if p.is_symlink() else hashlib.sha256(p.read_bytes()).hexdigest())
                for p in self.repo.rglob("*") if p.is_symlink() or p.is_file()}

    def prepared_plan(self, policy=None):
        self.audit(*(["--policy", policy] if policy else []))
        ev = self.cli("evidence", "--run", self.run, "--path", "provider.py", "--start", 1,
                      "--end", 16, "--relation", "selected", "--reason", "Closed local fixture contract and consumers")
        candidates = load(self.run / "candidates.json")["candidates"]
        chosen = next(c for c in candidates if c["classification"] == "PARALLEL_IMPLEMENTATION")
        history = self.cli("ground", "--run", self.run, "--candidate", chosen["candidate_id"])
        assessment = load(self.run / "assessment.json")
        card = next(c for c in assessment["candidates"] if c["candidate_id"] == chosen["candidate_id"])
        assessment["candidates"] = [card]
        card.update(responsibility="Normalize provider identity", target_owner="provider.py::_select",
                    remove=["provider.py::_old_select"], rationale="Both paths enforce the same local contract",
                    rollback="Restore this single code change; there is no persisted state or external coordination",
                    unresolved=[], behaviors=[{"id": "identity", "description": "Return normalized identity and declared errors",
                                              "crosses_seam": False, "check_ids": ["provider-contract"]}])
        for key, value in card["obligations"].items():
            value.update(status="SUPPORTED", explanation="The synthetic local fixture declares this complete contract",
                         evidence_ids=[history["evidence_id"] if key == "history" else ev["evidence_id"]])
        card["surface"]["authoritative_owners"] = {"before": ["provider.py::_old_select", "provider.py::_select"],
                                                   "after": ["provider.py::_select"]}
        card["surface"]["runtime_paths"] = {"before": ["old-selection", "selection"], "after": ["selection"]}
        assessment["checks"] = [{"id": "provider-contract", "kind": "end_to_end",
                                  "argv": ["{python}", "-B", "-m", "unittest", "discover", "-s", "tests"],
                                  "contract_ids": ["identity"], "timeout_seconds": 15}]
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        return assessment, card

    def target_review(self, verification, conclusion="SUPPORTED"):
        manifest = load(verification / "manifest.json")
        value = load(verification / "target-review.json")
        value["reviewer"] = "Local synthetic-fixture contract evaluator"
        for card in value["candidates"]:
            card.update(conclusion=conclusion, covered_obligations=OBLIGATIONS, unresolved=[],
                        statement="The canonical mechanism preserves normalization and both public error behaviors",
                        evidence=[{"side": "head", "path": "provider.py", "start": 1, "end": 9,
                                   "source_sha256": manifest["snapshots"]["head"]["files"]["provider.py"]["sha256"],
                                   "reason": "Canonical owner and public entrypoint in this exact implementation"}])
        save(verification / "target-review.json", value)
        return value

    def test_audit_preserves_source_and_git_and_never_claims_completion(self):
        before = self.bytes_fingerprint()
        result = self.audit()
        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertFalse(result["complete"])
        self.assertGreaterEqual(result["candidate_count"], 1)
        self.assertEqual(self.bytes_fingerprint(), before)

    def test_archive_attributes_do_not_omit_tests_or_substitute_source(self):
        self.put(".gitattributes", "tests export-ignore\nprovider.py export-subst\n")
        self.put("provider.py", BASE + '\nSTAMP = "$Format:%H$"\n')
        self.commit("Set archive policy")
        self.audit()
        snap = load(self.run / "manifest.json")["snapshots"]["head"]
        self.assertIn("tests/test_provider.py", snap["files"])
        self.assertEqual((self.run / "blobs" / snap["files"]["provider.py"]["sha256"]).read_bytes(),
                         (self.repo / "provider.py").read_bytes())

    def test_comments_and_docstrings_do_not_produce_code_credit(self):
        base = self.g("rev-parse", "HEAD")
        self.put("provider.py", '"""Documentation\nnot counted as implementation\n"""\n' + '# comment\n' * 100 + BASE)
        head = self.commit("Document behavior")
        result = self.audit("--base", base, "--head", head)
        self.assertEqual(result["code_mass"]["net"], 0)
        self.assertEqual(result["code_mass"]["ratio_status"], "NO_CHANGE")
        self.assertIsNone(result["code_mass"]["validated_removal_credit"])

    def test_format_compression_is_not_eligible_deletion(self):
        base = self.g("rev-parse", "HEAD")
        self.put("provider.py", BASE.replace('    if not isinstance(name, str):\n        raise TypeError("name must be text")', '    if not isinstance(name, str): raise TypeError("name must be text")'))
        head = self.commit("Compress formatting")
        result = self.audit("--base", base, "--head", head)
        self.assertLess(result["code_mass"]["net"], 0)
        self.assertEqual(result["code_mass"]["removed"], 0)
        self.assertIn("provider.py", result["code_mass"]["formatting_only_paths"])

    def test_mixed_formatting_and_changed_value_earn_only_changed_code_credit(self):
        base = self.g("rev-parse", "HEAD")
        compact = BASE.replace('    if not isinstance(name, str):\n        raise TypeError("name must be text")',
                               '    if not isinstance(name, str): raise TypeError("name must be text")')
        self.put("provider.py", compact.replace(".lower()", ".upper()", 1))
        head = self.commit("Change one expression and compact unaffected code")
        mass = self.audit("--base", base, "--head", head)["code_mass"]
        self.assertLess(mass["net"], 0)
        self.assertEqual((mass["removed"], mass["added"]), (1, 1))
        self.assertEqual(mass["ratio_status"], "BELOW_TARGET")

    def test_json_formatting_is_separate_from_configuration_changes(self):
        self.put("config.json", '{\n  "region": "west",\n  "retry": 3\n}\n')
        base = self.commit("Declare fixture configuration")
        self.put("config.json", '{"region":"east","retry":3}\n')
        head = self.commit("Change region and compact layout")
        mass = self.audit("--base", base, "--head", head)["code_mass"]
        self.assertEqual(mass["components"]["configuration"]["net"], -3)
        self.assertEqual((mass["removed"], mass["added"]), (1, 1))

    def test_exact_move_has_zero_deletion_credit(self):
        base = self.g("rev-parse", "HEAD")
        (self.repo / "renamed.py").write_bytes((self.repo / "provider.py").read_bytes())
        (self.repo / "provider.py").unlink()
        head = self.commit("Move the implementation")
        result = self.audit("--base", base, "--head", head)
        self.assertEqual(result["code_mass"]["net"], 0)
        self.assertEqual(result["code_mass"]["removed"], 0)

    def test_scope_escape_is_unknown(self):
        base = self.g("rev-parse", "HEAD")
        (self.repo / "outside.py").write_bytes((self.repo / "provider.py").read_bytes())
        self.put("provider.py", "value = 1\n")
        head = self.commit("Move implementation outside selected file")
        result = self.cli("audit", "--repo", self.repo, "--scope", "provider.py", "--base", base,
                          "--head", head, "--output", self.run)
        self.assertEqual(result["code_mass"]["status"], "UNKNOWN")
        self.assertIsNone(result["code_mass"]["removed"])

    def test_unsupported_language_cannot_be_fabricated_as_zero(self):
        self.put("service.ts", "export const start = () => 42;\n")
        self.commit("Add another maintained language")
        result = self.audit()
        self.assertEqual(result["code_mass"]["status"], "UNKNOWN")
        self.assertIn("service.ts", result["code_mass"]["unknown_paths"])
        self.assertIsNone(result["code_mass"]["before"])

    def test_generated_path_policy_excludes_code(self):
        self.put("generated/client.py", "generated = 1\n" * 50)
        self.commit("Add generated fixture")
        self.audit()
        self.assertEqual(load(self.run / "inventory.json")["head"]["generated/client.py"]["status"], "EXCLUDED")

    def test_staged_and_working_tree_use_different_bytes(self):
        self.put("provider.py", TARGET)
        self.g("add", "provider.py")
        self.put("provider.py", TARGET + "extra = 1\n")
        staged = self.audit("--staged")
        other = self.root / "working"
        working = self.cli("audit", "--repo", self.repo, "--scope", ".", "--working-tree", "--output", other)
        self.assertEqual(working["code_mass"]["after"], staged["code_mass"]["after"] + 1)

    def test_root_commit_has_empty_baseline(self):
        result = self.audit("--commit", "HEAD")
        self.assertEqual(result["code_mass"]["before"], 0)
        self.assertGreater(result["code_mass"]["after"], 0)

    def test_symbol_selection_requires_unambiguous_identity(self):
        self.put("other.py", "def resolve(name):\n    return name\n")
        self.commit("Declare an unrelated public function")
        result = self.cli("audit", "--repo", self.repo, "--symbol", "resolve", "--output", self.run, code=2)
        self.assertEqual(result["status"], "INVALID")
        specific = self.root / "specific"
        self.cli("audit", "--repo", self.repo, "--symbol", "provider.py::resolve", "--output", specific)
        self.assertEqual(load(specific / "manifest.json")["scope"]["paths"], ["provider.py"])

    def test_nonfinite_policy_values_are_invalid_json_inputs(self):
        for value in ("NaN", "Infinity", "1e999"):
            with self.subTest(value=value):
                policy = self.root / "policy.json"
                policy.write_text('{"minimum_ratio":' + value + '}')
                result = self.cli("audit", "--repo", self.repo, "--scope", ".", "--policy", policy,
                                  "--output", self.root / ("invalid-" + value), code=2)
                self.assertEqual(result["status"], "INVALID")

    def test_source_evidence_is_bound_to_exact_coordinates(self):
        self.audit()
        result = self.cli("evidence", "--run", self.run, "--path", "provider.py", "--start", 1,
                          "--end", 2, "--relation", "selected", "--reason", "Provider argument validation")
        item = load(Path(result["artifact"]))
        self.assertEqual(item["text"], "\n".join(BASE.splitlines()[:2]))
        self.assertEqual(item["source_sha256"], hashlib.sha256(BASE.encode()).hexdigest())
        self.cli("evidence", "--run", self.run, "--path", "provider.py", "--start", 10000,
                 "--relation", "selected", "--reason", "Invalid boundary", code=2)

    def test_paths_cannot_escape_evidence_store(self):
        self.audit()
        result = self.cli("evidence", "--run", self.run, "--path", "../outside", "--start", 1,
                          "--relation", "selected", "--reason", "Invalid path", code=2)
        self.assertEqual(result["status"], "INVALID")

    def test_source_drift_replaces_visible_report_with_stale(self):
        self.audit()
        self.put("provider.py", TARGET)
        result = self.cli("report", "--run", self.run, code=2)
        self.assertEqual(result["status"], "STALE")
        self.assertEqual(load(self.run / "result.json")["verdict"], "STALE")
        self.assertIn("STALE", (self.run / "simplification-report.html").read_text())

    def test_blob_corruption_is_detected(self):
        self.audit()
        manifest = load(self.run / "manifest.json")
        blob = self.run / "blobs" / manifest["snapshots"]["head"]["files"]["provider.py"]["sha256"]
        blob.write_text("tampered")
        self.assertEqual(self.cli("report", "--run", self.run, code=2)["status"], "INVALID")

    def test_incomplete_seal_is_invalid(self):
        self.audit()
        save(self.run / "seal.json", {})
        self.assertEqual(self.cli("report", "--run", self.run, code=2)["status"], "INVALID")

    def test_reports_are_rebuilt_from_evidence(self):
        self.audit()
        save(self.run / "result.json", {"verdict": "PASS", "complete": True})
        self.assertEqual(self.cli("report", "--run", self.run)["verdict"], "INCOMPLETE")
        self.cli("plan", "--run", self.run)
        save(self.run / "result.json", {"verdict": "PASS", "complete": True})
        self.assertEqual(self.cli("report", "--run", self.run)["verdict"], "INCOMPLETE")
        self.assertEqual(load(self.run / "result.json")["stage"], "PLANNED")

    def test_local_reports_render_untrusted_labels_as_text(self):
        assessment, card = self.prepared_plan()
        card["responsibility"] = '<script>alert("not executable")</script>'
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        page = (self.run / "simplification-report.html").read_text()
        self.assertIn('&lt;script&gt;alert(&quot;not executable&quot;)&lt;/script&gt;', page)
        svg = ET.parse(self.run / "responsibility-map.svg")
        text = " ".join(svg.getroot().itertext())
        self.assertIn("authoritative owners", text)
        self.assertIn("2 before / 1 after", text)

    def test_local_tree_sitter_outline_reports_declarations_with_source_binding(self):
        self.put("service.ts", 'export class Service {\n  resolve(name: string) { return name.trim(); }\n}\n')
        self.commit("Declare a TypeScript service")
        self.audit()
        before = self.bytes_fingerprint()
        result = self.cli("structure", "--run", self.run, "--path", "service.ts")
        receipt = load(Path(result["artifact"]))
        self.assertEqual(self.bytes_fingerprint(), before)
        if receipt["isolation"]["status"] == "PASS" and all(x["status"] == "PASS" for x in receipt["records"]):
            self.assertEqual(result["coverage_status"], "AVAILABLE")
            declarations = {x["name"] for x in receipt["nodes"]}
            self.assertTrue({"Service", "resolve"}.issubset(declarations))
            expected = hashlib.sha256((self.repo / "service.ts").read_bytes()).hexdigest()
            self.assertTrue(all(x["source_sha256"] == expected for x in receipt["nodes"]))
        else:
            self.assertEqual(result["coverage_status"], "INCOMPLETE")

    def test_candidate_registration_and_plan_keep_unknown_estimates(self):
        self.audit()
        result = self.cli("candidate", "--run", self.run, "--path", "provider.py", "--classification", "REDUNDANT_STATE",
                          "--statement", "Investigate duplicated identity state")
        self.assertEqual(result["safety"], "UNKNOWN")
        planned = self.cli("plan", "--run", self.run)
        self.assertIsNone(planned["expected_total"])
        self.assertEqual(planned["status"], "PROPOSED")

    def test_plan_rejects_unbound_claims_and_cycles(self):
        self.audit()
        assessment = load(self.run / "assessment.json")
        card = assessment["candidates"][0]
        card["obligations"]["behavior"].update(status="SUPPORTED", explanation="Claim", evidence_ids=["EV-missing"])
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run, code=2)
        card["obligations"]["behavior"].update(status="UNKNOWN", explanation="", evidence_ids=[])
        card["prerequisites"] = [card["candidate_id"]]
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run, code=2)

    def test_plan_totals_are_computed_from_prs(self):
        self.audit()
        assessment = load(self.run / "assessment.json")
        for card in assessment["candidates"]:
            card.update(estimated_added=3, estimated_removed=9)
        save(self.run / "assessment.json", assessment)
        result = self.cli("plan", "--run", self.run)
        self.assertEqual(result["expected_total"]["net"], -6 * len(assessment["candidates"]))

    def test_normalized_graph_import_checks_source_and_edges(self):
        self.audit()
        snap = load(self.run / "manifest.json")["snapshots"]["head"]
        value = {"schema_version": 1, "provider": "fixture-scip-export", "provider_version": "1",
                 "snapshot_digest": snap["digest"], "coverage": "Selected Python declarations only",
                 "nodes": [{"id": "provider", "path": "provider.py", "source_sha256": snap["files"]["provider.py"]["sha256"],
                            "start": 1, "end": 6, "kind": "function"}], "edges": []}
        path = self.root / "graph.json"
        save(path, value)
        accepted = self.cli("import-graph", "--run", self.run, "--file", path)
        self.assertEqual(load(Path(accepted["artifact"]))["kind"], "local_graph")
        value["edges"] = [{"from": "provider", "to": "missing", "kind": "CALLS", "confidence": "provider_claimed_precise"}]
        save(path, value)
        self.cli("import-graph", "--run", self.run, "--file", path, code=2)

    def test_output_reuse_preserves_existing_run(self):
        self.audit()
        before = (self.run / "manifest.json").read_bytes()
        self.cli("audit", "--repo", self.repo, "--scope", ".", "--output", self.run, code=2)
        self.assertEqual((self.run / "manifest.json").read_bytes(), before)

    def test_full_contract_verification_and_target_review(self):
        self.prepared_plan()
        self.put("provider.py", TARGET)
        head = self.commit("Consolidate provider resolution")
        before = self.bytes_fingerprint()
        verification = self.root / "verification"
        result = self.cli("verify", "--run", self.run, "--head", head, "--output", verification, code=3)
        self.assertEqual(result["verdict"], "INCOMPLETE")
        self.assertEqual(self.bytes_fingerprint(), before)
        if result["isolation"]["status"] != "PASS":
            self.assertEqual(result["execution_verdict"], "INCOMPLETE")
            self.assertTrue(all(x["status"] == "UNAVAILABLE" for x in result["checks"]))
            return
        self.assertEqual(result["execution_verdict"], "PASS", result)
        self.assertEqual([x["status"] for x in result["checks"]], ["PASS", "PASS"])
        self.assertIsNone(result["code_mass"]["validated_removal_credit"])
        self.target_review(verification)
        final = self.cli("finalize", "--run", verification)
        self.assertEqual(final["verdict"], "PASS")
        self.assertGreater(final["code_mass"]["validated_removal_credit"], 0)
        self.assertEqual(self.cli("report", "--run", verification)["verdict"], "PASS")
        value = load(verification / "target-review.json")
        valid = dict(value)
        value["target_snapshot_digest"] = "different"
        save(verification / "target-review.json", value)
        self.cli("finalize", "--run", verification, code=2)
        self.assertEqual(load(verification / "verification-report.json")["verdict"], "INVALID")
        self.assertEqual(load(verification / "result.json")["verdict"], "INVALID")
        save(verification / "target-review.json", valid)
        self.assertEqual(self.cli("finalize", "--run", verification)["verdict"], "PASS")
        self.put("provider.py", TARGET + "changed = True\n")
        self.cli("report", "--run", verification, code=2)
        self.assertEqual(load(verification / "verification-report.json")["verdict"], "STALE")
        self.assertIsNone(load(verification / "result.json")["code_mass"]["validated_removal_credit"])
        historical = load(verification / "result.json")
        self.assertEqual(historical["run_id"], final["run_id"])
        self.assertEqual(historical["code_mass"]["before"], final["code_mass"]["before"])
        self.assertTrue(historical["historical_only"])

    def test_behavior_failure_cannot_be_overridden_by_review(self):
        self.prepared_plan()
        self.put("provider.py", TARGET.replace(".lower()", ".upper()"))
        head = self.commit("Candidate changes identity behavior")
        verification = self.root / "verification"
        result = self.cli("verify", "--run", self.run, "--head", head, "--output", verification, code=3)
        self.target_review(verification)
        final = self.cli("finalize", "--run", verification, code=3)
        if result["isolation"]["status"] == "PASS":
            self.assertEqual(final["verdict"], "FAIL")
            self.assertTrue(any(x["status"] == "FAIL" and x["side"] == "head" for x in final["checks"]))
        else:
            self.assertEqual(final["verdict"], "INCOMPLETE")

    def test_wrong_target_review_identity_is_rejected(self):
        self.prepared_plan()
        self.put("provider.py", TARGET)
        head = self.commit("Consolidate provider resolution")
        verification = self.root / "verification"
        self.cli("verify", "--run", self.run, "--head", head, "--output", verification, code=3)
        save(verification / "verification-report.json", {"verdict": "PASS", "complete": True})
        self.assertEqual(self.cli("report", "--run", verification)["verdict"], "INCOMPLETE")
        value = self.target_review(verification)
        value["target_snapshot_digest"] = "different"
        save(verification / "target-review.json", value)
        self.cli("finalize", "--run", verification, code=2)

    def test_missing_integration_contract_remains_incomplete(self):
        assessment, card = self.prepared_plan()
        card["behaviors"][0]["crosses_seam"] = True
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        self.put("provider.py", TARGET)
        head = self.commit("Consolidate provider resolution")
        result = self.cli("verify", "--run", self.run, "--head", head, "--output", self.root / "verification", code=3)
        self.assertTrue(any("integration check" in x for x in result["gaps"]))

    def test_still_present_obsolete_owner_fails_verification(self):
        self.prepared_plan()
        self.put("provider.py", BASE.replace("    return _old_select(name)", "    return _select(name)"))
        head = self.commit("Change consumer without removing old owner")
        result = self.cli("verify", "--run", self.run, "--head", head, "--output", self.root / "verification", code=3)
        self.assertEqual(result["verdict"], "FAIL")
        self.assertTrue(any("obsolete mechanism remains" in x for x in result["failures"]))

    def test_shared_harness_observes_provider_and_persistence_contract(self):
        assessment, card = self.prepared_plan()
        card["behaviors"][0]["crosses_seam"] = True
        card["behaviors"][0]["check_ids"].append("provider-persistence")
        harness = self.root / "harness"
        harness.mkdir()
        (harness / "contract.py").write_text('''import json, pathlib, sys
sys.path.insert(0, sys.argv[1])
from provider import resolve
path = pathlib.Path("observed.json")
path.write_text(json.dumps({"identity": resolve(" AWS ")}))
assert json.loads(path.read_text()) == {"identity": "aws"}
print("provider persistence contract passed")
''')
        assessment["checks"].append({"id": "provider-persistence", "kind": "integration",
                                     "argv": ["{python}", "-B", "{harness}/contract.py", "{source}"],
                                     "contract_ids": ["identity"], "timeout_seconds": 15})
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        self.put("provider.py", TARGET)
        head = self.commit("Consolidate identity normalization")
        before = self.bytes_fingerprint()
        result = self.cli("verify", "--run", self.run, "--head", head, "--harness", harness,
                          "--output", self.root / "verification", code=3)
        self.assertEqual(self.bytes_fingerprint(), before)
        if result["isolation"]["status"] == "PASS":
            self.assertEqual(result["execution_verdict"], "PASS", result)
            checks = [x for x in result["checks"] if x["kind"] == "integration"]
            self.assertEqual([x["status"] for x in checks], ["PASS", "PASS"])
            self.assertTrue(all("provider persistence contract passed" in x["log"] for x in checks))

    def test_native_commands_observe_write_and_network_boundaries(self):
        assessment, _ = self.prepared_plan()
        sentinel = self.root / "sentinel"
        sentinel.write_text("preserved")
        code = '''import pathlib, socket, sys
pathlib.Path("output.txt").write_text("allowed")
assert pathlib.Path("output.txt").read_text() == "allowed"
try:
    pathlib.Path(sys.argv[1]).write_text("outside")
except PermissionError:
    pass
else:
    raise AssertionError("outside write succeeded")
try:
    socket.socket().bind(("127.0.0.1", 0))
except PermissionError:
    pass
else:
    raise AssertionError("network access succeeded")
print("contained command completed")
'''
        assessment["checks"].append({"id": "containment", "kind": "integration",
                                     "argv": ["{python}", "-I", "-B", "-c", code, str(sentinel)],
                                     "contract_ids": ["identity"], "timeout_seconds": 15})
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        self.put("provider.py", TARGET)
        result = self.cli("verify", "--run", self.run, "--working-tree", "--output", self.root / "verification", code=3)
        self.assertEqual(sentinel.read_text(), "preserved")
        if result["isolation"]["status"] == "PASS":
            checks = [x for x in result["checks"] if x["check_id"] == "containment"]
            self.assertEqual([x["status"] for x in checks], ["PASS", "PASS"])
            self.assertTrue(all("contained command completed" in x["log"] for x in checks))

    def test_timeout_is_an_executed_failure(self):
        assessment, _ = self.prepared_plan()
        assessment["checks"].append({"id": "bounded-check", "kind": "integration",
                                     "argv": ["{python}", "-I", "-B", "-c", "import time; time.sleep(5)"],
                                     "contract_ids": ["identity"], "timeout_seconds": 1})
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        self.put("provider.py", TARGET)
        result = self.cli("verify", "--run", self.run, "--working-tree", "--output", self.root / "verification", code=3)
        if result["isolation"]["status"] == "PASS":
            checks = [x for x in result["checks"] if x["check_id"] == "bounded-check"]
            self.assertEqual([x["status"] for x in checks], ["TIMEOUT", "TIMEOUT"])
            self.assertEqual(result["execution_verdict"], "FAIL")

    def test_explicit_ratio_exception_keeps_behavior_and_net_reduction_conditions(self):
        policy = self.root / "policy.json"
        save(policy, {"minimum_ratio": 100})
        assessment, card = self.prepared_plan(policy)
        initial_plan = self.cli("plan", "--run", self.run)["plan"]
        assessment["ratio_exception"] = {"reason": "The measured consolidation removes the duplicated owner with minimal consumer rewiring",
                                         "evidence_ids": card["obligations"]["behavior"]["evidence_ids"]}
        save(self.run / "assessment.json", assessment)
        self.cli("plan", "--run", self.run)
        self.put("provider.py", TARGET)
        head = self.commit("Consolidate identity normalization")
        declined = self.cli("verify", "--run", self.run, "--plan", Path(initial_plan).relative_to(self.run),
                            "--head", head, "--output", self.root / "without-exception", code=3)
        self.assertEqual(declined["verdict"], "FAIL")
        self.assertIsNone(declined["ratio_exception"])
        accepted = self.cli("verify", "--run", self.run, "--head", head, "--output", self.root / "with-exception", code=3)
        self.assertEqual(accepted["verdict"], "INCOMPLETE")
        self.assertEqual(accepted["ratio_exception"], assessment["ratio_exception"])
        self.assertLess(accepted["code_mass"]["net"], 0)
        if accepted["isolation"]["status"] == "PASS":
            self.assertEqual(accepted["execution_verdict"], "PASS")


if __name__ == "__main__":
    unittest.main()
