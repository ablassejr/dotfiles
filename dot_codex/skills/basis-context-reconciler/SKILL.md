---
name: basis-context-reconciler
description: Compare an approved First-Principles Basis with a post-basis current-state map and classify discovered constraints before implementation decisions are asked.
---

# Basis-to-current-state reconciler

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Require the exact approved First-Principles Basis and a source-linked current-state map from `$post-basis-context-loader`. Compare them before forming implementation questions. Do not treat current behavior, a test, or an abstraction as a constraint merely because it exists.

Classify every discovered constraint or force as exactly one of:

- `EXTERNAL_HARD_CONSTRAINT`: imposed by a platform, protocol, regulation, or unavoidable boundary;
- `APPROVED_SEMANTIC_CONSTRAINT`: established by the approved semantic authority;
- `CURRENT_ARCHITECTURAL_CONSTRAINT`: real in the current system but changeable;
- `HISTORICAL_CONSTRAINT`: valid when introduced and not yet shown to remain current;
- `TEMPORARY_WORKAROUND`: deliberately provisional;
- `EMERGENT_IMPLEMENTATION`: accumulated through incremental work without a governing decision;
- `ACCIDENTAL_DETAIL`: not meaningfully connected to a requirement or decision; or
- `RATIONALE_UNKNOWN`: evidence cannot responsibly explain it.

For each classification, cite the basis entries it supports, conflicts with, or cannot explain; cite direct sources; distinguish fact from inference; and record confidence, chronology, present validity, and the effect on possible decisions. A historical, temporary, emergent, or unknown classification makes `$ground-me` the recommended action before preservation or removal is decided.

If the evidence changes the desired state, problem, irreducible new behavior, expected simplification, invariant, hard constraint, forbidden tradeoff, minimum sufficient change, or success evidence, do not silently rewrite the basis. Return to `$first-principles-intake`, create and approve a successor version, then repeat affected context reconciliation.

Update the existing constraint and evidence records with classifications, basis conflicts, expired or uncertain forces, invalidated assumptions, and unresolved decision candidates. Return a concise account of material consequences and references; do not copy the basis or context snapshot into a reconciliation report or request a general reapproval. Pass the reconciled basis and current-state map to `$subtractive-design-analyzer` before sending its opportunity map and remaining choices to `$decision-frontier-manager`; do not answer them here.
