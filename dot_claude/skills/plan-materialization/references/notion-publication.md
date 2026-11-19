# Normalized Notion publication

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](workspace-and-destinations.md) for the portable workflow and actual adapter limits.

Apply [review and artifact design](review-and-artifact-design.md) to record titles, purpose, status, reference meaning, team access, and the division of content from the Linear design proposal.

## Semantic authority and release contents

The immutable approved Spec Release owns epic intent, basis lineage, normalized grounding conclusions, goals, outcomes, principles, invariants, actors, decision rights, requirements, scenarios, constraints, non-goals, assumptions, decisions and alternatives, interfaces, risks, evidence, approved acceptance conditions, and the architecture-view registry. Retain material framing, requirement-challenge, retention, deletion, restoration, simplification, learning-cycle, and automation decisions. Every surviving requirement and constraint has an authoritative source, rationale, and named human steward.

Each semantic record retains a stable ID, lifecycle state, source revision, and supersession links. References use IDs instead of copied prose. An editable page is a draft or projection, not an immutable release. A release binds to exact constituent revisions and content hashes. Preserve the snapshot content or version-addressable records needed to reconstruct those revisions; a link to a mutable current page alone cannot do that. Semantic changes create a successor release and leave prior intent traceable.

## Draft and write plan

Refresh the repository baseline assessment and source revisions. Compile a normalized intermediate representation that separates authoritative records from purpose-specific views. The Linear proposal owns the coherent review narrative; do not publish a second full narrative or independently authored executive summary in Notion. Validate required fields, stable IDs, reference integrity, counts, supersession, source revisions, view links, and approval metadata before generating a dry-run write plan.

Resolve the authenticated Notion workspace, exact destinations, current revisions, and authorized mutation set. Use existing authorization or obtain missing permission for the concrete plan. Route writes through `NotionCanonicalSpecAdapter` under [the operation-token contract](operation-adapters.md). Record intended effects, source hashes, expected revisions, stable operation IDs, and reconciliation keys before dispatch. Use native revision preconditions where supported; otherwise declare and implement the actual idempotency or reconciliation guarantee. A conflict or uncertain outcome is reconciled before retry. Materially harmful best-effort duplication needs an explicit risk record.

Write draft normalized records and their selected views. Persist returned IDs and receipts. Wait for asynchronous operations to finish, then fetch every created or modified record from the exact destinations.

## Readback and failure recovery

Compare identifiers, counts, relationships, normalized content hashes, required fields, supersession, source revisions, embeds, and approval fields with the intermediate representation. Inspect the rendered narrative and embedded views as well as structured data. Missing objects, incomplete asynchronous work, unexpected revisions, or mismatched content produce `PUBLICATION_FAILED` and block approval.

Keep provisional Markdown, intermediate representation, write plan, receipts, and mismatch evidence. On resume, inspect the written records and outstanding operations before retrying. Reuse established IDs and reconcile only the incomplete portion; do not publish a duplicate release or treat partial success as completion.

## Human approval and immutable release

Only after complete draft readback succeeds, publish and verify the [Linear design proposal](supervisor-design-document.md) and present it through the existing combined final Camunda approval user task. The proposal explains the exact verified source; do not request separate approval of every record, visual, or Notion draft. Bind the human response to that task and the reviewed revision; a Linear comment or local record alone cannot advance the process. Approval records identify the reviewed content hash and constituent revisions, approver, and time. Before finalizing, verify they still match. A concurrent semantic or source change invalidates the affected approval and returns to its earliest repair stage.

Writing approval metadata can change a provider's revision without changing semantic content. Compare the semantic payload separately from approval metadata, read back the final records, and explicitly bind the same human approval to the final immutable snapshot only when the content is identical. A changed semantic payload requires renewed review; never silently reinterpret approval of older content.

Create the immutable Spec Release record after approval, retaining the exact snapshot and constituent revision/hash map. Read back that record and all referenced content, then return its ID, immutable revision, hash, approval, and verification references to the owning Camunda work item and retain receipts in the external manifest. A failed finalization remains incomplete even if the human already approved the draft. Approval of a draft alone is not a published release.

## Handoff and cleanup

Compile and read back the immutable handoff package after the release is verified. Temporary semantic Markdown becomes eligible for provenance-bounded cleanup only when normalization, reference validation, visual review, named-human approval, immutable release readback, and durable handoff verification all succeed. Keep recovery evidence while anything remains incomplete. Preserve the external workflow manifest and shared infrastructure needed by other active work. Product-repository cleanup remains part of final reconciliation.
