---
name: speckit-first-principles
description: Expand or audit an approved First-Principles Basis into the first-principles semantic kernel of a Spec Kit epic workspace after context reconciliation.
---

# Spec Kit first principles

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Invoke `$first-principles-specification` only after `$first-principles-intake` has produced an explicitly approved basis and `$basis-context-reconciler` has classified the gathered context. Keep the semantic expansion in the active Spec Kit feature workspace. This adapter does not establish the pre-context basis and must not expose repository or historical context to that intake gate.

Give every material record a stable semantic ID. Separate observed facts, interpretations, proposals, human decisions, and unresolved questions. Compare plausible problem frames before choosing a provisional one, and identify evidence that could falsify the frame or a surviving requirement.

Return the exact basis version, updated semantic records, the evidence or authority behind them, reconciled contradictions, unresolved factual gaps, and the human-owned decision frontier. Do not silently rewrite the approved basis or advance a provisional record merely because the document is complete.
