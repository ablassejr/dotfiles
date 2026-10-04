#!/usr/bin/env python3
"""Join claims to sources and report graph-level reference defects."""

from __future__ import annotations

import argparse
import sys
from typing import Any

from research_compiler_lib import digest, emit_failure, extract_list, read_json, stable_id, validation_issue, write_json


def build(sources_document: Any, claims_document: Any) -> dict[str, Any]:
    sources = extract_list(sources_document, "sources")
    claims = extract_list(claims_document, "claims")
    errors: list[dict[str, Any]] = []

    source_ids: dict[str, dict[str, Any]] = {}
    for source in sources:
        source_id = str(source.get("source_id", "")).strip()
        if not source_id:
            errors.append(validation_issue("MISSING_SOURCE_ID", "Source has no source_id"))
        elif source_id in source_ids:
            errors.append(validation_issue("DUPLICATE_SOURCE_ID", "source_id is not unique", source_id=source_id))
        else:
            source_ids[source_id] = source

    claim_ids: dict[str, dict[str, Any]] = {}
    for claim in claims:
        claim_id = str(claim.get("claim_id", "")).strip()
        if not claim_id:
            errors.append(validation_issue("MISSING_CLAIM_ID", "Claim has no claim_id"))
        elif claim_id in claim_ids:
            errors.append(validation_issue("DUPLICATE_CLAIM_ID", "claim_id is not unique", claim_id=claim_id))
        else:
            claim_ids[claim_id] = claim

    links: list[dict[str, Any]] = []
    for claim_id, claim in sorted(claim_ids.items()):
        support = claim.get("support", []) if isinstance(claim.get("support", []), list) else []
        for link in support:
            if not isinstance(link, dict):
                errors.append(validation_issue("INVALID_EVIDENCE_LINK", "Evidence link must be an object", claim_id=claim_id))
                continue
            source_ref = str(link.get("source_ref", "")).strip()
            if source_ref not in source_ids:
                errors.append(validation_issue("UNKNOWN_SOURCE_REF", "Evidence link references an unknown source", claim_id=claim_id, source_ref=source_ref))
            evidence_link = {
                "claim_ref": claim_id,
                "source_ref": source_ref,
                "evidence_type": link.get("evidence_type"),
            }
            if link.get("excerpt_ref"):
                evidence_link["excerpt_ref"] = link["excerpt_ref"]
            evidence_link["link_id"] = stable_id("EVL", evidence_link)
            links.append(evidence_link)
        for contradicted_id in claim.get("contradicts", []):
            if contradicted_id not in claim_ids:
                errors.append(validation_issue("UNKNOWN_CONTRADICTED_CLAIM", "Claim contradicts an unknown claim", claim_id=claim_id, contradicted_claim=contradicted_id))

    graph: dict[str, Any] = {
        "version": 1,
        "status": "INVALID" if errors else "VALID",
        "sources": sorted(source_ids.values(), key=lambda source: source["source_id"]),
        "claims": sorted(claim_ids.values(), key=lambda claim: claim["claim_id"]),
        "evidence_links": sorted(links, key=lambda link: link["link_id"]),
        "errors": sorted(errors, key=lambda issue: (issue["code"], str(issue.get("claim_id", "")), str(issue.get("source_ref", "")))),
    }
    graph["model_digest"] = digest(graph)
    return {"evidence_graph": graph}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build a deterministic evidence graph from source and claim JSON documents.")
    parser.add_argument("--sources", required=True, help="JSON document containing sources")
    parser.add_argument("--claims", required=True, help="JSON document containing claims")
    parser.add_argument("-o", "--output", default="-", help="Output JSON path, or - for standard output")
    args = parser.parse_args()
    try:
        result = build(read_json(args.sources), read_json(args.claims))
        write_json(result, args.output)
    except (OSError, ValueError) as exc:
        return emit_failure(exc)
    return 1 if result["evidence_graph"]["errors"] else 0


if __name__ == "__main__":
    sys.exit(main())
