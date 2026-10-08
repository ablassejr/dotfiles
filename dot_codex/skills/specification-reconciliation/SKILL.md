---
name: specification-reconciliation
description: Reconcile an epic after its dependency-ordered pull requests merge, verify integrated behavior, publish the as-built specification and visual state in the selected documentation home, record qualifying ADRs, and remove provenance-owned temporary specification artifacts.
---

# Specification reconciliation

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


Use the project's selected source and work records under [workspace and destinations](references/bundled/epic-spec-workflow/references/workspace-and-destinations.md). The code-mass and behavioral obligations apply to the approved scope. Commands that require a Linear/Notion manifest or fixed three-person plan apply only to that compatible profile. For other projects, perform and record the same independent normalized measurements, removal-credit checks, budgets, approved exceptions, and behavior verification against the actual source and dependency records using compatible repository tools. Do not fabricate provider fields, require three owners, or claim a packaged CLI result that was not obtained.

For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Read [references/reconciliation-and-cleanup.md](references/reconciliation-and-cleanup.md). Resolve the approved specification revision, delivery program, merged pull requests, repository baseline and final revision, Code Mass Opportunity Maps, Grounding Packets, audit reports, issue contracts, milestone ledgers, view registry, ADRs, and the epic provenance manifest.

Invoke `$framed-engineering-sequence` against the integrated system before publication and cleanup. Verify dependency-ordered integration and system behavior at public boundaries. Compare the as-built behavior with every affected semantic ID. Recheck the product frame, the current source, rationale, and named human steward for surviving requirements and constraints, every material retained, deleted, or restored item, system-level simplification, cycle outcomes, and automation premises. Re-run the Code Mass Auditor against final committed states, remove reverted or invalid removal credit, and update every milestone ledger. A mismatch is either an implementation defect or a proposed semantic change; do not silently make the documents and code agree.

Update the selected authoritative documentation and each affected LikeC4, Archify, or Figma Design graph projection and any non-graph FigJam material to the verified as-built state. Read back every external write and obtain the required human visual or semantic approval. Record a technical decision as an ADR only when it meets the repository's ADR threshold.

Remove only temporary artifacts owned by this epic and recorded in provenance. Do not delete shared Spec Kit infrastructure while another active feature uses it. For the compatible Spec Kit profile, run `specflow cleanup-check` after removal with its declared preservation rules. Otherwise verify the exact temporary removal set directly against provenance and confirm that the chosen durable records remain; a provider-specific checker is not a universal completion gate. The cleanup result identifies the temporary epic-owned work that was removed and the durable records that remain. Preserve the project's selected canonical documentation, approved plans, source-bound evidence, and ADRs, including when their chosen home is the repository. Do not remove them merely because a provider-specific cleanup profile expects external storage.

Report final production, test, and combined SLOC; milestone ratio, deficit, or exception; any remaining same-domain code-mass debt; and every residual path and owner. Do not claim cleanup completed while an in-scope temporary removal remains unfinished, a required ledger cannot close, or a required publication readback is unverified. Retained canonical documents are expected durable outputs, not cleanup residuals.

## Graph visual gate

Apply the shared [graph visual policy](references/bundled/epic-spec-workflow/references/graph-visual-policy.md) to every graph-like output. Use Figma Design, LikeC4, or Archify and retain matching render-operation and artifact evidence. Include all produced or published visuals in the current step’s inventory and run `specflow validate-visuals <manifest.json> --json` before presentation. A missing renderer or invalid receipt blocks the visual output. Non-graph media keep their own communication purpose.
