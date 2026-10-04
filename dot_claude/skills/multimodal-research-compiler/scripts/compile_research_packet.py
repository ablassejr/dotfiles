#!/usr/bin/env python3
"""Compile reviewed research inputs into a deterministic Research Packet."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import digest, emit_failure, open_blocking_types, read_json, stable_id, unwrap, write_json


def confidence_for(claims: list[dict[str, Any]], synthesis: dict[str, Any]) -> str:
    direct = synthesis.get("direct_answer", {})
    if isinstance(direct, dict) and direct.get("confidence"):
        return str(direct["confidence"])
    material = [claim for claim in claims if claim.get("materiality", "material") in {"blocking", "material"}]
    if any(claim.get("status") == "conflicted" or claim.get("confidence") == "conflicted" for claim in material):
        return "conflicted"
    if material and all(claim.get("confidence") == "corroborated" for claim in material):
        return "corroborated"
    if any(claim.get("status") in {"supported", "inferred"} for claim in material):
        return "single_source"
    return "unknown"


def compile_packet(
    request_document: Any,
    evidence_document: Any,
    synthesis_document: Any,
    alignment_document: Any,
    adversarial_document: Any,
    question_graph_document: Any | None = None,
    contradiction_document: Any | None = None,
    views_document: Any | None = None,
    packet_id: str | None = None,
) -> dict[str, Any]:
    request = unwrap(request_document, "research_request")
    evidence = unwrap(evidence_document, "evidence_graph")
    synthesis = unwrap(synthesis_document, "synthesis")
    alignment = unwrap(alignment_document, "alignment")
    adversarial = unwrap(adversarial_document, "adversarial_review")
    question_graph = unwrap(question_graph_document, "question_graph") if question_graph_document is not None else {}
    contradiction_result = unwrap(contradiction_document, "contradiction_result") if contradiction_document is not None else {}
    views = unwrap(views_document, "views") if views_document is not None else synthesis.get("views", {}) if isinstance(synthesis, dict) else {}

    for name, value in (("research_request", request), ("evidence_graph", evidence), ("synthesis", synthesis), ("alignment", alignment), ("adversarial_review", adversarial)):
        if not isinstance(value, dict):
            raise ValueError(f"{name} must be a JSON object")
    if not isinstance(question_graph, dict) or not isinstance(contradiction_result, dict) or not isinstance(views, dict):
        raise ValueError("question graph, contradiction result, and views must be JSON objects")

    request_id = str(request.get("request_id", "")).strip()
    mode = request.get("mode")
    question_statement = str(request.get("question", {}).get("statement", "")).strip() if isinstance(request.get("question"), dict) else ""
    if not request_id or not mode or not question_statement:
        raise ValueError("research_request requires request_id, mode, and question.statement")

    claims = evidence.get("claims", [])
    sources = evidence.get("sources", [])
    if not isinstance(claims, list) or not isinstance(sources, list):
        raise ValueError("evidence_graph claims and sources must be arrays")

    direct_answer = synthesis.get("direct_answer", {})
    if isinstance(direct_answer, str):
        direct_answer = {"statement": direct_answer}
    if not isinstance(direct_answer, dict) or not str(direct_answer.get("statement", "")).strip():
        raise ValueError("synthesis requires direct_answer.statement")
    direct_answer = dict(direct_answer)
    direct_answer["confidence"] = confidence_for(claims, synthesis)

    contradictions = contradiction_result.get("contradictions", evidence.get("contradictions", []))
    if not isinstance(contradictions, list):
        raise ValueError("contradictions must be an array")
    unresolved = list(synthesis.get("unresolved", [])) if isinstance(synthesis.get("unresolved", []), list) else []
    known_unresolved = {str(item.get("claim_ref", "")) for item in unresolved if isinstance(item, dict)}
    for claim in claims:
        if claim.get("status") in {"unresolved", "conflicted"} and claim.get("claim_id") not in known_unresolved:
            unresolved.append(
                {
                    "claim_ref": claim.get("claim_id"),
                    "materiality": claim.get("materiality", "material"),
                    "reason": claim.get("status"),
                }
            )

    research_model = {
        "request": request,
        "question_graph": question_graph,
        "evidence_graph": evidence,
        "synthesis": synthesis,
        "alignment": alignment,
        "adversarial_review": adversarial,
        "contradictions": contradictions,
        "views": views,
    }
    model_digest = digest(research_model)

    packet_views: dict[str, Any] = {}
    for name, view in sorted(views.items()):
        if isinstance(view, dict):
            view_record = dict(view)
            view_record.setdefault("model_digest", model_digest)
            view_record.setdefault("verification", {"status": "PENDING"})
            packet_views[name] = view_record
        else:
            packet_views[name] = view

    basis_status = alignment.get("status")
    adversarial_status = adversarial.get("status")
    gate_outcome = synthesis.get("gate_outcome")
    evidence_blocked = evidence.get("status") == "INVALID" or bool(evidence.get("errors"))
    adversarial_blockers = open_blocking_types(adversarial)
    non_hitl_adversarial_blockers = adversarial_blockers - {"HITL_DECISION_REQUIRED"}
    if basis_status == "BASIS_REVISION_REQUIRED":
        status = "BASIS_REVISION_REQUIRED"
    elif evidence_blocked or basis_status == "MISALIGNED" or non_hitl_adversarial_blockers:
        status = "BLOCKED"
    elif gate_outcome == "REQUEST_HITL" or "HITL_DECISION_REQUIRED" in adversarial_blockers or any(
        isinstance(item, dict) and item.get("type") in {"normative", "risk_acceptance", "product_semantics", "irreversible_choice"}
        for item in unresolved
    ):
        status = "HITL_REQUIRED"
    elif basis_status == "ALIGNED" and adversarial_status == "PASSED":
        status = "REVIEWED"
    else:
        status = "PARTIAL"

    root_question = question_graph.get("root_question") or request.get("question", {}).get("id") or stable_id("QST", request_id, question_statement)
    findings = synthesis.get("findings")
    if not isinstance(findings, list):
        findings = [
            {"claim_ref": claim.get("claim_id"), "materiality": claim.get("materiality", "material")}
            for claim in claims
            if claim.get("materiality", "material") in {"blocking", "material"}
        ]

    resolved_packet_id = packet_id or stable_id("RSR-REL", request_id, model_digest)
    packet = {
        "packet_id": resolved_packet_id,
        "status": status,
        "mode": mode,
        "question": {"id": root_question, "statement": question_statement},
        "basis": request.get("first_principles_basis", {}),
        "authority": {
            "semantic": request.get("semantic_authority", {}),
            "implementation": request.get("implementation_context", {}),
        },
        "direct_answer": direct_answer,
        "claims": claims,
        "findings": findings,
        "alternatives": synthesis.get("alternatives", []),
        "recommendation": synthesis.get("recommendation", {}),
        "implementation_effects": synthesis.get("implementation_effects", {}),
        "contradictions": contradictions,
        "unresolved": unresolved,
        "sources": sources,
        "views": packet_views,
        "reviews": {
            "first_principles": alignment,
            "adversarial": adversarial,
            "human_understanding": synthesis.get("human_understanding", "PENDING"),
            "human_decision": synthesis.get("human_decision", "PENDING"),
        },
        "model_digest": model_digest,
        "research_model": research_model,
    }
    return {"research_packet": packet}


def main() -> int:
    parser = argparse.ArgumentParser(description="Compile reviewed research inputs into a deterministic Research Packet JSON document.")
    parser.add_argument("--request", required=True, help="Research Request JSON path")
    parser.add_argument("--evidence", required=True, help="Evidence Graph JSON path")
    parser.add_argument("--synthesis", required=True, help="Synthesis JSON path")
    parser.add_argument("--alignment", required=True, help="First-principles alignment JSON path")
    parser.add_argument("--adversarial", required=True, help="Adversarial review JSON path")
    parser.add_argument("--question-graph", help="Optional Question Graph JSON path")
    parser.add_argument("--contradictions", help="Optional contradiction result JSON path")
    parser.add_argument("--views", help="Optional views JSON path")
    parser.add_argument("--packet-id", help="Optional explicit release identifier")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        result = compile_packet(
            request_document=read_json(args.request),
            evidence_document=read_json(args.evidence),
            synthesis_document=read_json(args.synthesis),
            alignment_document=read_json(args.alignment),
            adversarial_document=read_json(args.adversarial),
            question_graph_document=read_json(args.question_graph) if args.question_graph else None,
            contradiction_document=read_json(args.contradictions) if args.contradictions else None,
            views_document=read_json(args.views) if args.views else None,
            packet_id=args.packet_id,
        )
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 0


if __name__ == "__main__":
    sys.exit(main())
