# Accounting and evidence

The accounting unit is the completed, bounded responsibility transition. The default policy includes first-party production code, tests, infrastructure, build logic, and configuration. Generated/vendored paths, lockfiles, documentation, binary assets, and build products receive no deletion credit. The run stores the effective policy so later changes cannot alter its denominator.

## Supported measurements

The Python adapter parses source with the standard-library AST and tokenizer. It counts physical lines carrying non-comment tokens, excluding module, class, and function docstrings. A multiline string that supplies runtime data remains code. Python syntax or encoding failures produce unknown measurements. The JSON adapter parses valid JSON and counts nonempty physical lines. Unsupported formats and unresolved symlink/nested content produce unknown maintained totals rather than zero. Known component subtotals remain available alongside the unknown paths.

Changes with equal parsed structures receive no addition/removal credit, even when formatting lowers physical code lines. Other supported changes compare non-comment token sequences and count the physical lines touched by changed tokens. This excludes formatting-only lines even when a file also contains a real edit. Identical changed-line signatures removed and added across selected paths are reconciled as movement. This deliberately conservative matching may understate gross churn; it does not prove behavioral equivalence. Exact-content movement into an excluded or unmeasured path makes eligible deltas unknown, and verification identifies maintained changes outside the planned responsibility.

`before`, `after`, and `net` describe measured physical maintained SLOC. `added` and `removed` describe eligible changed code lines after structural and movement reconciliation. Their difference need not equal physical net change when formatting-only edits are excluded. `validated_removal_credit` remains null until all verification and semantic-review conditions pass. No estimate is promoted to a measurement.

For finite additions the ratio is eligible removals divided by eligible additions. Removal with no additions has `ratio_kind: INFINITE` and `ratio: null`, avoiding invalid JSON Infinity. No eligible changes has `ratio_kind: NOT_APPLICABLE` and `ratio_status: NO_CHANGE`. Missing measurements have `ratio_kind: UNKNOWN`. A ratio at least 1.2 passes its own policy check; a completed simplification additionally requires negative measured net code, actual eligible removal, preserved required behavior, and conceptual reduction. An optional assessment-level `ratio_exception` provides a nonempty `reason` and bound `evidence_ids` for an explicitly justified below-target transition. The exception is recorded in verification and never bypasses negative net code, preserved behavior, conceptual reduction, missing evidence, or final semantic review. Zero-net work does not count as a completed simplification. The 1.2 target is a framework policy, not an empirical law.

The configurable fields are `exclude`, `test_paths`, `infrastructure_paths`, `build_paths`, and `minimum_ratio`. Classification lists contain repository-relative glob patterns. Supply the complete list when overriding a field. Explicit path policy is needed for repository-specific generated files and unconventional test/infrastructure paths. The stock adapters do not infer all generated code from file contents or `.gitattributes`.

Example policy fragment:

```json
{
  "exclude": ["generated/**", "vendor/**", "dist/**", "**/*.lock", "package-lock.json"],
  "test_paths": ["tests/**", "**/test_*.py"],
  "minimum_ratio": 1.2
}
```

## Responsibility and evidence

Conceptual dimensions contain entity identities: authoritative owners, state representations, runtime paths, public contracts, internal abstractions, configuration switches, and runtime dependencies. Reports show each dimension separately. A scalar total is not used to exchange a public contract for a configuration switch or otherwise imply equal maintenance cost.

The reviewing agent or analyst supplies interpretations, target maps, preservation judgments, and rollback reasoning. Source excerpts bind those statements to specific bytes and coordinates. History receipts establish what Git returned at a pinned revision; chronology is not proof of causation or current necessity. Normalized graphs bind nodes to snapshots and preserve provider-declared confidence; they do not establish complete coverage of reflection, plugins, configuration, or external consumers.

The helper's built-in candidate generators detect Python declarations whose syntax matches after normalizing their names and simple returned-call wrappers. Other taxonomy categories are recorded explicitly through `candidate` after local investigation. Candidate discovery does not rank syntax similarity as semantic safety. All automatic candidates begin `UNKNOWN`.

The preservation obligations are consumers, dynamic use, contracts, behavior, replacement, failure paths, state ownership, history, and test preservation. Supported or not-applicable judgments require an explanation and bound evidence. Unknown or conflicted evidence cannot yield a completed pass. The target review is a separate record for the actual implementation and must cover every proposed candidate and obligation.

## Evidence integrity and limits

Content hashes and seals detect ordinary artifact corruption and stale identities. They are local self-consistency checks, not a defense against an actor rewriting every artifact and its hashes. An evidence receipt does not prove semantic truth, reviewer independence, or indexer execution. Native-check results originate from this helper's runner and are sealed separately from user-supplied review assertions.

The source fingerprint includes the working checkout and Git metadata, including separate/shared Git storage. Unrelated source changes can make a saved analysis stale even if its selected files did not change. Historical plan verification intentionally reuses captured immutable bytes and records a new source fingerprint for the implementation run. Missing history is not fetched.

The local HTML report escapes untrusted text and denies network content through a content security policy. It is a projection of local evidence; editing the report does not change execution records or source evidence.
