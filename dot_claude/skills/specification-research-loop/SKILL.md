---
name: specification-research-loop
description: Resolve material factual gaps in an epic specification with repository evidence, exact-version documentation, organizational context, and primary-source web research, stopping at human judgments or exhausted evidence.
---

# Specification research loop

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Require an approved First-Principles Basis and completed post-basis context gate. Read the current epic manifest, basis lineage, reconciliation, provisional frames, goals, principles, assumptions, unknowns, requirement-challenge decisions, and evidence ledger. Work from the factual question whose answer could most change the basis, frame, or specification.

Follow [shared tool routing](references/bundled/epic-spec-workflow/references/tool-routing.md) for pinned repository evidence, structural and semantic retrieval, reusable version/environment CLI records, and current external primary sources. Prefer the organization or project that owns the fact.

Record claims separately from interpretations. For each material claim, record a stable evidence ID, source, owner, version or date, retrieval time, supported semantic IDs, contradictions, and confidence. Seek evidence that could disconfirm the favored frame, establish a requirement's authoritative source or rationale, or show that a retained, deleted, or restored item is necessary or unnecessary. Never store credentials or private tokens.

Continue while a credible source can resolve a factual gap that could alter a frame, requirement, invariant, interface, risk, constraint, retention decision, system simplification, feedback path, automation premise, or rejected alternative. If the remaining question is a value judgment, acceptable risk, priority, or intended behavior, move it to the human decision frontier. If privileged evidence is unavailable, name the access boundary. If more research cannot change the stated goals or first principles, stop.

Update the existing evidence records and present only findings that affect the design or a human choice, distinguishing supported facts, conflicts, interpretations, and unknowns. Keep search logs and exhaustive source coverage in internal evidence. Do not create a standalone research report unless it answers a distinct team question. State the earliest intake, context, reconciliation, or `$framed-engineering-sequence` step affected by each material finding. Offer `$ground-me` when the missing fact is why a current state exists or whether its original force remains valid. Do not approve your own semantic changes or overwrite an approved basis version.

Return exactly one of `CONTINUE_RESEARCH`, `REQUEST_HITL`, `REVISE_FIRST_PRINCIPLES`, or `PROCEED` using [the research-gate contract](references/bundled/epic-spec-workflow/references/research-and-review.md). Record evidence for every hard condition. Exhausted access is not sufficiency, a score cannot compensate for missing evidence, and `PROCEED` does not resolve blocking human decisions or approve publication.

## Graph visual gate

Apply the shared [graph visual policy](references/bundled/epic-spec-workflow/references/graph-visual-policy.md) to every graph-like output. Use Figma Design, LikeC4, or Archify and retain matching render-operation and artifact evidence. Include all produced or published visuals in the current step’s inventory and run `specflow validate-visuals <manifest.json> --json` before presentation. A missing renderer or invalid receipt blocks the visual output. Non-graph media keep their own communication purpose.
