from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SKILL_ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = SKILL_ROOT / "scripts"


class ResearchCompilerCliTests(unittest.TestCase):
    def write_json(self, directory: Path, name: str, value: object) -> Path:
        path = directory / name
        path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")
        return path

    def run_script(self, name: str, *arguments: object, expected_exit: int = 0) -> subprocess.CompletedProcess[str]:
        completed = subprocess.run(
            [sys.executable, str(SCRIPTS / name), *[str(argument) for argument in arguments]],
            cwd=SKILL_ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(expected_exit, completed.returncode, msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}")
        return completed

    def test_complete_research_packet_reaches_release_boundary(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            work = Path(temporary_directory)
            raw_sources = self.write_json(
                work,
                "raw-sources.json",
                {
                    "sources": [
                        {
                            "source_id": "SRC-001",
                            "source_type": "repository",
                            "title": "Behavioral contract",
                            "locator": "repo://example@abc123/tests/behavior.json",
                            "revision": "abc123",
                            "published_at": "2026-08-30",
                            "authority_for": ["current_behavior"],
                        },
                        {
                            "source_id": "SRC-DUP",
                            "source_type": "repository",
                            "title": "The same behavioral contract",
                            "locator": "repo://example@abc123/tests/behavior.json",
                            "revision": "abc123",
                            "published_at": "2026-08-30",
                            "authority_for": ["verification"],
                        },
                        {
                            "source_id": "SRC-002",
                            "source_type": "official_documentation",
                            "title": "Pinned API contract",
                            "locator": "https://example.invalid/api/v2/contract",
                            "version": "2.0",
                            "published_at": "2026-08-31",
                            "authority_for": ["external_constraints"],
                        },
                    ]
                },
            )
            sources = work / "sources.json"
            self.run_script("normalize_sources.py", raw_sources, "--output", sources)
            normalized_sources = json.loads(sources.read_text(encoding="utf-8"))
            self.assertEqual(2, normalized_sources["normalization"]["output_count"])
            self.assertEqual(["SRC-001", "SRC-002"], [source["source_id"] for source in normalized_sources["sources"]])
            second_sources = work / "sources-second.json"
            self.run_script("normalize_sources.py", raw_sources, "--output", second_sources)
            self.assertEqual(sources.read_text(encoding="utf-8"), second_sources.read_text(encoding="utf-8"))

            request = self.write_json(
                work,
                "request.json",
                {
                    "research_request": {
                        "request_id": "RSR-EXAMPLE-001",
                        "mode": "DECISION_SUPPORT",
                        "question": {"statement": "Where should dependency resolution occur?"},
                        "first_principles_basis": {
                            "basis_ref": "FPB-001",
                            "desired_state": ["Execution plans remain deterministic"],
                            "invariants": ["Execution does not depend on mutable discovery state"],
                        },
                        "semantic_authority": {"specification_release": "SPEC-001"},
                        "implementation_context": {"repository_commit": "abc123", "linear_issue": "LIN-204"},
                    }
                },
            )
            question_graph = work / "question-graph.json"
            self.run_script("build_question_graph.py", request, "--output", question_graph)
            graph = json.loads(question_graph.read_text(encoding="utf-8"))["question_graph"]
            self.assertEqual("DECISION_SUPPORT", graph["mode"])
            self.assertGreaterEqual(len(graph["questions"]), 5)

            claims = self.write_json(
                work,
                "claims.json",
                {
                    "claims": [
                        {
                            "claim_id": "CLM-001",
                            "statement": "Compilation-time resolution preserves deterministic execution inputs.",
                            "claim_type": "recommendation_support",
                            "materiality": "blocking",
                            "status": "supported",
                            "confidence": "corroborated",
                            "support": [
                                {"source_ref": "SRC-001", "evidence_type": "BEHAVIORALLY_INFERRED"},
                                {"source_ref": "SRC-002", "evidence_type": "EXPLICIT"},
                            ],
                            "claim_key": "resolution_stage",
                            "normalized_value": "compilation",
                            "scope": {"repository": "example", "revision": "abc123"},
                        }
                    ]
                },
            )
            claim_report = work / "claim-report.json"
            self.run_script("validate_claims.py", claims, "--sources", sources, "--output", claim_report)
            self.assertTrue(json.loads(claim_report.read_text(encoding="utf-8"))["claim_validation"]["valid"])

            evidence = work / "evidence.json"
            self.run_script("build_evidence_graph.py", "--sources", sources, "--claims", claims, "--output", evidence)
            evidence_graph = json.loads(evidence.read_text(encoding="utf-8"))["evidence_graph"]
            self.assertEqual("VALID", evidence_graph["status"])
            self.assertEqual(2, len(evidence_graph["evidence_links"]))

            contradiction_report = work / "contradictions.json"
            self.run_script("detect_contradictions.py", claims, "--output", contradiction_report)
            self.assertEqual([], json.loads(contradiction_report.read_text(encoding="utf-8"))["contradiction_result"]["contradictions"])

            timeline_input = self.write_json(
                work,
                "timeline-input.json",
                {"sources": normalized_sources["sources"]},
            )
            timeline = work / "timeline.json"
            self.run_script("build_timeline.py", timeline_input, "--output", timeline)
            timeline_events = json.loads(timeline.read_text(encoding="utf-8"))["timeline"]["events"]
            self.assertEqual(["2026-08-30", "2026-08-31"], [event["at"] for event in timeline_events])

            correlation_input = self.write_json(
                work,
                "correlation-input.json",
                {
                    "git": [{"commit_sha": "abc123", "issue_ids": ["LIN-204"]}],
                    "github": [{"pr_number": 7, "commits": ["abc123"]}],
                    "linear": [{"issue_id": "LIN-204", "pr_numbers": [7]}],
                },
            )
            correlations = work / "correlations.json"
            self.run_script("correlate_git_github_linear.py", correlation_input, "--output", correlations)
            correlation_result = json.loads(correlations.read_text(encoding="utf-8"))["correlation_result"]
            self.assertEqual(1, len(correlation_result["correlations"]))
            self.assertEqual(["git", "github", "linear"], correlation_result["correlations"][0]["systems"])

            synthesis = self.write_json(
                work,
                "synthesis.json",
                {
                    "synthesis": {
                        "direct_answer": {"statement": "Resolve dependencies during compilation."},
                        "recommendation": {"option": "compilation", "rationale_claims": ["CLM-001"]},
                        "alternatives": [{"option_id": "runtime"}, {"option_id": "compilation"}],
                        "unresolved": [],
                        "gate_outcome": "PROCEED_TO_SYNTHESIS",
                        "human_understanding": "CONFIRMED",
                        "human_decision": "PENDING",
                    }
                },
            )
            alignment = self.write_json(work, "alignment.json", {"alignment": {"status": "ALIGNED", "basis_ref": "FPB-001"}})
            adversarial = self.write_json(
                work,
                "adversarial.json",
                {"adversarial_review": {"status": "PASSED", "review_kind": "SELF_REVIEWED", "findings": []}},
            )
            packet = work / "packet.json"
            self.run_script(
                "compile_research_packet.py",
                "--request",
                request,
                "--question-graph",
                question_graph,
                "--evidence",
                evidence,
                "--synthesis",
                synthesis,
                "--alignment",
                alignment,
                "--adversarial",
                adversarial,
                "--contradictions",
                contradiction_report,
                "--output",
                packet,
            )
            research_packet = json.loads(packet.read_text(encoding="utf-8"))["research_packet"]
            self.assertEqual("REVIEWED", research_packet["status"])
            self.assertEqual("corroborated", research_packet["direct_answer"]["confidence"])
            self.assertEqual(64, len(research_packet["model_digest"]))

            release_report = work / "release-report.json"
            self.run_script("validate_research_release.py", packet, "--output", release_report)
            self.assertTrue(json.loads(release_report.read_text(encoding="utf-8"))["release_validation"]["valid"])

    def test_unsupported_claim_returns_a_public_validation_error(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            work = Path(temporary_directory)
            claims = self.write_json(
                work,
                "claims.json",
                {
                    "claims": [
                        {
                            "claim_id": "CLM-UNSUPPORTED",
                            "statement": "This conclusion has no evidence.",
                            "claim_type": "direct_answer",
                            "status": "supported",
                            "confidence": "unknown",
                            "support": [],
                        }
                    ]
                },
            )
            report = work / "report.json"
            self.run_script("validate_claims.py", claims, "--output", report, expected_exit=1)
            result = json.loads(report.read_text(encoding="utf-8"))["claim_validation"]
            self.assertFalse(result["valid"])
            self.assertIn("UNSUPPORTED_CLAIM", {error["code"] for error in result["errors"]})

    def test_unverified_projection_blocks_release(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            work = Path(temporary_directory)
            packet = {
                "research_packet": {
                    "packet_id": "RSR-REL-VIEW",
                    "status": "REVIEWED",
                    "mode": "VERIFICATION",
                    "question": {"id": "QST-1", "statement": "Is the visual consistent?"},
                    "direct_answer": {"statement": "The visual remains unverified.", "confidence": "single_source"},
                    "claims": [],
                    "sources": [],
                    "reviews": {
                        "first_principles": {"status": "ALIGNED"},
                        "adversarial": {"status": "PASSED", "review_kind": "INDEPENDENT", "findings": []},
                    },
                    "unresolved": [],
                    "contradictions": [],
                    "views": {"figma": {"model_digest": "wrong", "verification": {"status": "PENDING"}}},
                    "research_model": {"synthesis": {}},
                }
            }
            import hashlib
            import json as json_module

            model_digest = hashlib.sha256(
                json_module.dumps(packet["research_packet"]["research_model"], ensure_ascii=False, separators=(",", ":"), sort_keys=True).encode("utf-8")
            ).hexdigest()
            packet["research_packet"]["model_digest"] = model_digest
            packet_path = self.write_json(work, "packet.json", packet)
            report = work / "report.json"
            self.run_script("validate_research_release.py", packet_path, "--output", report, expected_exit=1)
            errors = json.loads(report.read_text(encoding="utf-8"))["release_validation"]["errors"]
            codes = {error["code"] for error in errors}
            self.assertIn("VIEW_MODEL_MISMATCH", codes)
            self.assertIn("VIEW_NOT_VERIFIED", codes)

    def test_adversarial_blocker_routes_to_the_matching_public_status(self) -> None:
        with tempfile.TemporaryDirectory() as temporary_directory:
            work = Path(temporary_directory)
            request = self.write_json(
                work,
                "request.json",
                {
                    "research_request": {
                        "request_id": "RSR-ROUTING",
                        "mode": "DECISION_SUPPORT",
                        "question": {"statement": "Which option should be chosen?"},
                    }
                },
            )
            evidence = self.write_json(
                work,
                "evidence.json",
                {"evidence_graph": {"status": "VALID", "errors": [], "sources": [], "claims": []}},
            )
            synthesis = self.write_json(
                work,
                "synthesis.json",
                {
                    "synthesis": {
                        "direct_answer": {"statement": "A human decision remains."},
                        "gate_outcome": "REQUEST_HITL",
                        "unresolved": [],
                    }
                },
            )
            alignment = self.write_json(work, "alignment.json", {"alignment": {"status": "ALIGNED"}})

            evidence_blocker = self.write_json(
                work,
                "evidence-blocker.json",
                {
                    "adversarial_review": {
                        "status": "FAILED",
                        "review_kind": "INDEPENDENT",
                        "findings": [{"type": "EVIDENCE_BLOCKER", "status": "OPEN"}],
                    }
                },
            )
            blocked_packet = work / "blocked-packet.json"
            self.run_script(
                "compile_research_packet.py",
                "--request",
                request,
                "--evidence",
                evidence,
                "--synthesis",
                synthesis,
                "--alignment",
                alignment,
                "--adversarial",
                evidence_blocker,
                "--output",
                blocked_packet,
            )
            self.assertEqual("BLOCKED", json.loads(blocked_packet.read_text(encoding="utf-8"))["research_packet"]["status"])

            decision_blocker = self.write_json(
                work,
                "decision-blocker.json",
                {
                    "adversarial_review": {
                        "status": "PASSED",
                        "review_kind": "INDEPENDENT",
                        "findings": [{"type": "HITL_DECISION_REQUIRED", "status": "OPEN"}],
                    }
                },
            )
            hitl_packet = work / "hitl-packet.json"
            self.run_script(
                "compile_research_packet.py",
                "--request",
                request,
                "--evidence",
                evidence,
                "--synthesis",
                synthesis,
                "--alignment",
                alignment,
                "--adversarial",
                decision_blocker,
                "--output",
                hitl_packet,
            )
            self.assertEqual("HITL_REQUIRED", json.loads(hitl_packet.read_text(encoding="utf-8"))["research_packet"]["status"])

    def test_json_schemas_and_projection_json_are_parseable(self) -> None:
        for path in sorted((SKILL_ROOT / "schemas").glob("*.json")):
            parsed = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual("https://json-schema.org/draft/2020-12/schema", parsed["$schema"])
        for name in ("figjam-timeline.json", "figjam-decision-lineage.json"):
            parsed = json.loads((SKILL_ROOT / "templates" / name).read_text(encoding="utf-8"))
            self.assertIn("view", parsed)
            self.assertEqual("PENDING", parsed["verification"]["status"])


if __name__ == "__main__":
    unittest.main()
