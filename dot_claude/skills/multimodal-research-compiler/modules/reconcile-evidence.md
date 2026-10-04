# Reconcile evidence

Normalize retrieved observations before synthesis. Deduplicate sources by scoped identity, not title alone. Give questions, entities, claims, sources, evidence links, contradictions, decisions, alternatives, and views stable identifiers.

For every material claim, verify that each evidence link points to an existing applicable source and accurately classifies the relationship. Separate what a source says from the conclusion drawn from it. Downgrade confidence when evidence is single-source, indirect, stale, out of scope, or credibly contradicted.

Run `scripts/validate_claims.py`, `scripts/detect_contradictions.py`, and, when useful, `scripts/build_evidence_graph.py`. Inspect the reported public errors rather than treating a zero exit code from an earlier stage as release evidence.

Resolve differences in date, version, environment, desired versus current state, and intent versus observation before declaring a contradiction. Preserve unresolved material conflict and route it through the research gate.
