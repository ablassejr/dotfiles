# Local artifact contract

All machine-readable artifacts declare `schema_version: "1"`. `analysis_id` binds evidence, assessments, and results to the captured local identity. Full content and Git state fingerprints make index and working-tree reviews distinguishable even with the same HEAD. The output files are personal local artifacts, not provider receipts or repository approvals.

| Artifact | Producer and purpose |
| --- | --- |
| `request.json` | Helper-normalized user input and comparison mode |
| `context-packet.json` | Helper-pinned identity, base/head trees, complete changed-file list, raw deltas, patches, and Python symbol overlap |
| `integrity-before.json` | Helper fingerprints for source/Git storage, including ignored/untracked files and symlink text |
| `prepared-hashes.json` | Digests protecting the prepared packet and initial integrity record from accidental alteration |
| `context-manifest.json` | Source coordinates/hashes and imported local evidence; the agent's source of EV identifiers |
| `assessment.json` | Agent-authored review decisions, coverage, check selection, findings, and challenger receipt |
| `assessment-final.json` | The validated assessment used for the rendered report |
| `findings.json` | Adjudicated findings plus reasons for dropped duplicate/out-of-scope candidates |
| `tool-results.json` | Supplied native-check evidence with command, outcome, provenance, and identity |
| `code-mass.json` | Raw textual changes and separately identified maintained-line measurements/unknowns |
| `analysis-summary.json` | Local advisory verdict, completeness, blockers, integrity, and gaps |
| `review.md`, `technical-debt.md`, `report.html` | Human-readable reports; HTML embeds no external content and escapes source text |

## Agent assessment

Preparation writes a valid but unfinished assessment. Edit its decision fields and reference real captured EV identifiers. The complete structural shape is in [the assessment schema](../schemas/assessment.schema.json); every property is explicit and unknown fields are rejected. The helper additionally checks cross-artifact identity, evidence existence/kind/content, coordinates, check outcome consistency, challenge coverage, scope, and deletion-safety claims. Schemas cannot determine whether a semantic claim is true.

A native-check entry looks like this after real local execution:

```json
{
  "name": "contract-tests",
  "status": "passed",
  "analysis_id": "local-review:FULL_ID_FROM_PREPARE",
  "command": ["python3", "-B", "-m", "unittest", "tests.test_contract"],
  "provenance": "pyproject.toml and checked-in CI task",
  "evidence_id": "EV-LOG_ID_FROM_RECEIPT",
  "isolation_evidence_id": "EV-ISOLATION_ID_FROM_RECEIPT",
  "exit_code": 0,
  "explanation": "Executed against the captured source snapshot; relevant public contract passed."
}
```

This is an illustrative shape, not a receipt for an executed check. Check status is passed, failed, unavailable, or not_applicable. Passed/failed entries need the actual command/provenance, a tool-log receipt, an isolation receipt, and a consistent exit code. An unavailable entry explains the missing tool/environment. If no native check applies, record one not_applicable selection with its reason instead of inventing execution. The selected checks and applicable behaviors come from the user and repository; the framework adds no application acceptance criteria.

Coverage entries address changed paths and cite pinned source evidence for those paths. Their explanations describe the responsibility domain inspected and any relevant consumer/provider/test relationships. Record unavailable or partial inspection as pending with a limitation. Read/parsed files and a successful graph query do not automatically mean reviewed behavior.

The seven lenses may be reviewed, not_applicable with an explanation, or pending. A completed challenge includes a local artifact, reviewer/context identity, and serious/blocked finding IDs that it actually challenged; its artifact should also address the overall conclusion. No-findings reviews still need this conclusion challenge. The helper validates the receipt's binding/hash and required coverage. It does not certify model independence or infer that the artifact's author was local.

## Finding shape

```json
{
  "id": "FND-001",
  "kind": "defect",
  "title": "Retry can repeat an acknowledged write",
  "root_cause": "A retry repeats the external effect after acknowledgement is lost",
  "severity": "HIGH",
  "confidence": "HIGH",
  "derivation": "BEHAVIORAL",
  "relationship": "INTRODUCED",
  "blocking": true,
  "disposition": "kept",
  "location": {"path": "src/publisher.py", "side": "head", "start_line": 24, "end_line": 28},
  "claim": "When the write succeeds and its acknowledgement is lost, the retry issues the same write again.",
  "impact": "The consumer can observe duplicate persisted events.",
  "recommendation": "Preserve an idempotent write identity across retries and verify that observable contract.",
  "evidence_ids": ["EV-SOURCE_ID"],
  "counterevidence_search": "Inspected the callee, persistence contract, and retry test for deduplication.",
  "counterevidence_ids": ["EV-CALLEE_ID", "EV-TEST_ID"],
  "deletion": null
}
```

Use full captured IDs when running the helper. The example is a proposed finding shape, not a finding about any repository in this task. Coordinates must be covered by cited source evidence on the same side. Binary/file-level locations use null for both line fields. Debt uses `kind: "debt"` and is nonblocking; a correctness consequence is represented as a separate defect only when it is actually a different behavioral claim, not merely another label for the same concern.

Deletion proposals include `safe`, `replacement_evidence_ids`, `consumer_evidence_ids`, `compatibility_evidence_ids`, and `unresolved_risks`. Evidence arrays must be populated. An unresolved external consumer prevents claiming safe deletion even if no local reference is found.

## Trust and completeness

Captured source and imported bytes can be deterministically checked. The relevance of a context edge, authority of a specification, truth of a finding, actual command execution, and fresh local model context need host/agent evidence and judgment. The report preserves this distinction. Prepared hashes detect corruption or accidental editing; they are not signatures and do not defend against a writer deliberately replacing both artifacts and hashes.

`complete: true` means the declared review work has evidence and no recorded gaps. It is independent of the verdict: a completely assessed defect can yield HOLD; a known defect with missing checks yields HOLD and `complete: false`. An unknown maintained-SLOC count is disclosed but does not itself block a review. An unknown specification permits a clearly labeled implementation-only review. Missing safety, scope, checks, or independent challenge does prevent a completed conclusion.
