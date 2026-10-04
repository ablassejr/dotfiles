# Reconciliation and cleanup contract

## Reconcile

Fetch the completed delivery program and its actual dependency graph. Confirm every issue's pull request and verification outcome. Test the integrated release at user and system boundaries. Compare observed behavior with the approved stable semantic IDs. Apply `$framed-engineering-sequence` to current evidence: revisit the provisional frame, requirement source, rationale, and named steward; challenge remaining parts and processes; restore a deletion when evidence proves it necessary; simplify the surviving whole; examine whether cycle-time changes preserved stability; and reassess whether outcome or process automation is still justified. Classify differences before changing anything.

An implementation defect returns to the owning issue. A desired product-semantic or frame change returns to the semantic and specification approval flow. Evidence that changes only a later framed-engineering decision returns to that earliest affected step. An implementation-only tradeoff belongs in the linked design record and may qualify for an ADR. A projection mismatch updates the projection after the semantic and operational states agree.

## Publish as-built state

Update the selected specification revision or create its approved successor. Wait for asynchronous writes and fetch the exact destination. Update affected views, inspect structure and screenshots, and obtain human approval. Record the final repository revision and work-item completion state.

## Clean

Start from the provenance manifest. Present the exact removal set and identify shared files. Remove only files created for the epic or explicitly approved generated copies. Preserve repository code, tests, migrations, current-state operational documentation, the project's selected canonical specification and proposals, approved plans, required recovery evidence, unrelated work, and ADRs. Remove the feature's temporary Spec Kit records, staging Markdown, evidence working notes, local compiler payloads, agent scratch output, and generated local view files after their verified publication.

Shared `.specify` infrastructure remains while any other active Spec Kit feature depends on it. When the epic is the last user and removal is explicitly approved, remove that shared infrastructure as a separately resolved target.

Only for a selected compatible Spec Kit cleanup profile, derive each `specflow cleanup-check --allow <relative-path>` argument only from `provenance.preserved_artifacts` entries that the human has chosen to retain. A provenance path is relative to the directory containing the manifest: resolve it there, confirm the result is inside the repository, then convert it to a repository-relative path for `--allow`. Never pass the raw provenance path when the manifest is nested. Show that translation before running the check. Never use `--allow` to suppress an unreviewed residual. A nonzero result is an incomplete cleanup with explicit residual paths. Never broaden the deletion target to make the check pass.

For other repository layouts, compare the authorized temporary removal set with the actual filesystem and provenance directly. Verify retained canonical documentation and recovery records in their chosen home. Report exact remaining temporary work without treating approved repository documents as residuals or manufacturing an adapter manifest.
