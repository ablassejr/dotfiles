---
name: speckit-autonomous-research-gate
description: Evaluate the current Spec Kit research state and route the epic to further factual research, human judgment, first-principles revision, or the next existing workflow gate.
---

# Spec Kit autonomous research gate

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Read approved basis lineage, semantic records, claim ledger, source register, gap matrix, contradictions, decisions, and readiness evidence. Verify applicability to the named version, product, environment, and semantic IDs.

Apply every hard condition in [the research-gate contract](references/bundled/epic-spec-workflow/references/research-and-review.md). Emit exactly one of `CONTINUE_RESEARCH`, `REQUEST_HITL`, `REVISE_FIRST_PRINCIPLES`, or `PROCEED`, with evidence, affected IDs, blockers, and next stage. A credible factual source routes to `$specification-research-loop`; a value, risk, or inaccessible-evidence boundary routes to the human frontier; a disproved basis routes to `$first-principles-intake` for a successor, before implementation context is reused.

Record the result in the workflow manifest and derive a readiness view only when needed. Present the result and its practical consequence without a separate readiness report or approval prompt. `PROCEED` ends factual research only when all sufficiency conditions hold; unresolved blocking human decisions still prevent later gates. Do not substitute a weighted score, approve semantics, waive contradictions, or invent acceptance criteria.
