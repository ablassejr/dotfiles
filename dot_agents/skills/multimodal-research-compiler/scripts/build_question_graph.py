#!/usr/bin/env python3
"""Compile a mode-aware research question graph from a Research Request."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import emit_failure, read_json, stable_id, unwrap, write_json

MODES = {"DISCOVERY", "GROUNDING", "DECISION_SUPPORT", "IMPLEMENTATION", "VERIFICATION", "IMPACT_ANALYSIS"}

COMMON_QUESTIONS = [
    ("What does the applicable current system or subject do?", ["current_behavior"], ["repository", "contracts", "runtime_evidence"]),
    ("Which approved goals, invariants, and decisions govern the answer?", ["architectural_constraints"], ["first_principles_basis", "approved_specification"]),
    ("Which version, time, scope, or environment constraints apply?", ["external_constraints"], ["official_documentation", "current_configuration"]),
    ("Which material claims remain uncertain or contradicted?", ["contradictions", "uncertainty"], ["all_applicable_sources"]),
]

MODE_QUESTIONS = {
    "DISCOVERY": [
        ("Which materially different options exist?", ["alternatives"], ["primary_external_sources", "official_documentation"]),
        ("What evidence-backed tradeoffs distinguish the options?", ["implementation_consequences", "alternatives"], ["primary_external_sources", "repository"]),
    ],
    "GROUNDING": [
        ("When and how did the current shape emerge?", ["historical_rationale"], ["git", "github", "linear", "adrs"]),
        ("Which original constraints were explicit and which are inferred?", ["original_constraint"], ["adrs", "linear", "github", "git"]),
        ("Which original constraints still apply?", ["constraint_validity"], ["repository", "official_documentation", "historical_comparison"]),
    ],
    "DECISION_SUPPORT": [
        ("Which viable options satisfy the approved basis?", ["alternatives", "first_principles_alignment"], ["approved_specification", "repository", "official_documentation"]),
        ("What would each option add, remove, preserve, and risk?", ["implementation_consequences"], ["repository", "codegraph", "official_documentation"]),
        ("Which option is the minimum sufficient mechanism?", ["recommendation"], ["synthesized_evidence"]),
    ],
    "IMPLEMENTATION": [
        ("Which public behaviors, owners, files, and symbols are in scope?", ["code_surface", "current_behavior"], ["repository", "codegraph", "claude_context"]),
        ("Which contracts, failures, seams, concurrency boundaries, and migrations matter?", ["implementation_consequences"], ["contracts", "tests", "repository", "official_documentation"]),
        ("Which observable tests and verification evidence prove the change?", ["verification"], ["behavioral_tests", "integration_tests", "runtime_evidence"]),
        ("Which existing mechanisms become safely unnecessary?", ["deletion_candidates"], ["repository", "history", "impact_analysis"]),
    ],
    "VERIFICATION": [
        ("Which claim-appropriate evidence would prove or disprove the target?", ["verification"], ["primary_authorities"]),
        ("What counterevidence or scope mismatch challenges the target?", ["contradictions", "scope"], ["all_applicable_sources"]),
    ],
    "IMPACT_ANALYSIS": [
        ("Which callers, consumers, data, state, and boundaries depend on the target?", ["impact"], ["codegraph", "repository", "contracts"]),
        ("Which migrations, compatibility effects, failures, and recovery paths follow?", ["implementation_consequences"], ["repository", "official_documentation", "runtime_evidence"]),
    ],
}


def build(request_document: Any) -> dict[str, Any]:
    request = unwrap(request_document, "research_request")
    if not isinstance(request, dict):
        raise ValueError("research_request must be an object")
    request_id = str(request.get("request_id", "")).strip()
    mode = request.get("mode")
    statement = str(request.get("question", {}).get("statement", "")).strip() if isinstance(request.get("question"), dict) else ""
    if not request_id or mode not in MODES or not statement:
        raise ValueError("research_request requires request_id, a recognized mode, and question.statement")

    root_id = str(request.get("question", {}).get("id", "")).strip() or stable_id("QST", request_id, statement)
    questions: list[dict[str, Any]] = [
        {
            "question_id": root_id,
            "question": statement,
            "claim_types": ["direct_answer"],
            "preferred_sources": [],
            "fallback_sources": [],
            "human_judgment_required": mode == "DECISION_SUPPORT",
            "materiality": "blocking",
            "root": True,
        }
    ]
    edges: list[dict[str, str]] = []
    seen_text = {statement.casefold()}
    for text, claim_types, preferred_sources in COMMON_QUESTIONS + MODE_QUESTIONS[mode]:
        if text.casefold() in seen_text:
            continue
        seen_text.add(text.casefold())
        question_id = stable_id("QST", request_id, mode, text)
        questions.append(
            {
                "question_id": question_id,
                "question": text,
                "claim_types": claim_types,
                "preferred_sources": preferred_sources,
                "fallback_sources": ["labeled_inference"],
                "human_judgment_required": text.startswith("Which option is"),
                "materiality": "blocking",
                "root": False,
            }
        )
        edges.append({"from": root_id, "to": question_id, "relationship": "DEPENDS_ON"})

    graph = {
        "request_id": request_id,
        "mode": mode,
        "root_question": root_id,
        "questions": questions,
        "edges": sorted(edges, key=lambda edge: edge["to"]),
    }
    graph["graph_id"] = stable_id("QG", graph)
    return {"question_graph": graph}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic research question graph from a Research Request JSON document.")
    parser.add_argument("request", help="Research Request JSON path")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        write_json(build(read_json(args.request)), args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
