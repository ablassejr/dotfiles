from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from html.parser import HTMLParser
from pathlib import Path


SCRIPT = Path(__file__).parents[1] / "scripts" / "render_resume.py"


class VisibleText(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self.parts: list[str] = []
        self.root_labels: list[str] = []
        self.headings: list[tuple[str, str]] = []
        self.list_roles: list[str] = []
        self._heading_tag: str | None = None
        self._heading_parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attributes = dict(attrs)
        if tag == "article" and attributes.get("aria-label"):
            self.root_labels.append(attributes["aria-label"] or "")
        if tag in {"ol", "ul"} and attributes.get("role"):
            self.list_roles.append(attributes["role"] or "")
        if tag in {"h1", "h2", "h3"}:
            self._heading_tag = tag
            self._heading_parts = []

    def handle_endtag(self, tag: str) -> None:
        if tag == self._heading_tag:
            self.headings.append((tag, " ".join(self._heading_parts)))
            self._heading_tag = None
            self._heading_parts = []

    def handle_data(self, data: str) -> None:
        value = data.strip()
        if value:
            self.parts.append(value)
            if self._heading_tag:
                self._heading_parts.append(value)

    @property
    def text(self) -> str:
        return " ".join(self.parts)


class RenderResumeEndToEndTests(unittest.TestCase):
    def run_renderer(self, payload: dict) -> tuple[subprocess.CompletedProcess[str], Path, str]:
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        root = Path(temporary.name)
        source = root / "brief.json"
        output = root / "nested" / "resume.html"
        source.write_text(json.dumps(payload), encoding="utf-8")
        result = subprocess.run(
            [sys.executable, str(SCRIPT), str(source), str(output)],
            capture_output=True,
            text=True,
            check=False,
        )
        rendered = output.read_text(encoding="utf-8") if output.exists() else ""
        return result, output, rendered

    def test_renders_the_resume_contract_at_the_visual_boundary(self) -> None:
        payload = {
            "title": "Export <account> data",
            "as_of": "2026-09-03 14:20 CDT",
            "status": {
                "value": "in-progress",
                "evidence": {"status": "verified-now", "source": "active task state"},
            },
            "objective": {
                "text": "Add the export flow without changing existing clients.",
                "evidence": {"status": "recorded", "source": "user request"},
            },
            "why": [
                {
                    "decision": {
                        "text": "Preserve the envelope",
                        "evidence": {"status": "recorded", "source": "approved decision"},
                    },
                    "rationale": {
                        "text": "Existing consumers depend on it.",
                        "evidence": {
                            "status": "inferred",
                            "source": "compatibility analysis",
                        },
                    },
                }
            ],
            "current": {
                "text": "The system-boundary export behavior passes.",
                "evidence": {"status": "verified-now", "source": "end-to-end test"},
            },
            "narrative": [
                {
                    "phase": "Verification",
                    "title": "Boundary behavior passes",
                    "detail": "The public flow returns the expected export.",
                    "state": "current",
                    "evidence": {"status": "verified-now", "source": "test run"},
                }
            ],
            "next": {
                "text": "Review the diff before deciding whether to publish.",
                "kind": "proposed",
                "evidence": {"status": "inferred", "source": "current frontier"},
            },
            "open_questions": [
                {
                    "text": "Should this task publish the change?",
                    "evidence": {"status": "unknown", "source": "not authorized"},
                }
            ],
        }

        result, output, rendered = self.run_renderer(payload)

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertTrue(output.exists())
        parser = VisibleText()
        parser.feed(rendered)
        for visible_claim in (
            "Export <account> data",
            "Add the export flow without changing existing clients.",
            "Existing consumers depend on it.",
            "approved decision",
            "compatibility analysis",
            "The system-boundary export behavior passes.",
            "You are here",
            "Review the diff before deciding whether to publish.",
            "Should this task publish the change?",
        ):
            self.assertIn(visible_claim, parser.text)
        self.assertEqual(parser.root_labels, ["Session resume for Export <account> data"])
        for orientation_heading in (("h2", "What"), ("h2", "Why"), ("h2", "Now")):
            self.assertIn(orientation_heading, parser.headings)
        self.assertIn("list", parser.list_roles)
        self.assertNotIn("<account>", rendered)

    def test_rejects_a_brief_without_a_required_objective(self) -> None:
        result, output, _ = self.run_renderer(
            {
                "title": "Sparse session",
                "current": {"text": "Target not established."},
            }
        )

        self.assertEqual(result.returncode, 2)
        self.assertFalse(output.exists())
        self.assertIn("objective must be an object", result.stderr)

    def test_renders_sparse_and_conflicting_evidence_without_inventing_history(self) -> None:
        result, _, rendered = self.run_renderer(
            {
                "title": "Unresolved deployment",
                "status": {
                    "value": "blocked",
                    "evidence": {"status": "recorded", "source": "task state"},
                },
                "objective": {"text": "Resume the deployment investigation."},
                "current": {"text": "The live outcome has not been rechecked."},
                "blockers": [
                    {
                        "text": "Current provider state is unavailable.",
                        "evidence": {"status": "unknown", "source": "no live observation"},
                    }
                ],
                "conflicts": [
                    {
                        "text": "An earlier success report conflicts with a later failure.",
                        "evidence": {"status": "recorded", "source": "task history"},
                    }
                ],
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        parser = VisibleText()
        parser.feed(rendered)
        for visible_claim in (
            "Blocked",
            "Reason not captured",
            "No work history was established",
            "No continuation has been recorded.",
            "Current provider state is unavailable.",
            "An earlier success report conflicts with a later failure.",
        ):
            self.assertIn(visible_claim, parser.text)

    def test_inserts_the_current_frontier_before_a_recorded_next_step(self) -> None:
        result, _, rendered = self.run_renderer(
            {
                "title": "Continue the migration",
                "objective": {"text": "Migrate the public workflow safely."},
                "current": {
                    "text": "Compatibility verification is still pending.",
                    "evidence": {"status": "verified-now", "source": "current test state"},
                },
                "narrative": [
                    {
                        "phase": "Work",
                        "title": "Migration implemented",
                        "state": "done",
                    },
                    {
                        "phase": "Continuation",
                        "title": "Publish after verification",
                        "state": "next",
                    },
                ],
            }
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        parser = VisibleText()
        parser.feed(rendered)
        self.assertEqual(parser.text.count("You are here"), 1)
        self.assertLess(
            parser.text.index("Compatibility verification is still pending."),
            parser.text.index("Publish after verification"),
        )

    def test_rejects_unqualified_evidence_and_ambiguous_frontiers(self) -> None:
        cases = [
            (
                {
                    "title": "Missing source",
                    "objective": {
                        "text": "Resume safely.",
                        "evidence": {"status": "verified-now"},
                    },
                    "current": {"text": "Inspection is pending."},
                },
                "source must identify the basis for verified-now evidence",
            ),
            (
                {
                    "title": "Unsupported completion",
                    "status": {
                        "value": "complete",
                        "evidence": {"status": "recorded", "source": "earlier message"},
                    },
                    "objective": {"text": "Finish the task."},
                    "current": {"text": "Current state was not checked."},
                },
                "complete status requires recorded or verified status and current-state evidence",
            ),
            (
                {
                    "title": "Two frontiers",
                    "objective": {"text": "Resume the task."},
                    "current": {"text": "Two activities claim to be current."},
                    "narrative": [
                        {"title": "First frontier", "state": "current"},
                        {"title": "Second frontier", "state": "current"},
                    ],
                },
                "narrative may contain at most one current item",
            ),
            (
                {
                    "title": "Guessed continuation",
                    "objective": {"text": "Resume the task."},
                    "current": {"text": "The next action was not agreed."},
                    "next": {
                        "text": "Publish the change.",
                        "kind": "recorded",
                        "evidence": {
                            "status": "inferred",
                            "source": "likely workflow",
                        },
                    },
                },
                "recorded next.kind requires recorded or verified evidence",
            ),
        ]

        for payload, expected_error in cases:
            with self.subTest(title=payload["title"]):
                result, output, _ = self.run_renderer(payload)
                self.assertEqual(result.returncode, 2)
                self.assertFalse(output.exists())
                self.assertIn(expected_error, result.stderr)


if __name__ == "__main__":
    unittest.main()
