---
name: basis-context-reconciler
description: Compare an approved First-Principles Basis with a post-basis current-state map and classify discovered constraints before implementation decisions are asked.
---

# Basis-to-current-state reconciler

## Invoke every named step

When this skill assigns work to another named skill, whether written `$name` or named as the skill to invoke, run, apply, use or return to, that work is a required step and the named skill performs it. When the step is reached or its condition holds, invoke the named skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing the step's work yourself, reproducing it from memory, folding it into another step, or handing it to a general-purpose agent or generic review does not complete it, even when the result looks equivalent. A subagent may supply the fresh context a step requires, provided it invokes the named skill. A skill named only as the target of a later, separate invocation is a handoff, not a step of this run.

A step completes without its own invocation only in these ways, and never silently:

- **Verified reuse.** When the approval economy rules this skill follows allow an existing approval or result to be reused, record the evidence and tell the user what was reused.
- **Approved skip or substitution.** Before moving past the step, tell the user which step it is, why it should not run as written, what replaces it, and what assurance is lost. Continue only after the user approves. That message is a decision prompt and needs the full explanation the review and artifact design contract requires.
- **Unavailable skill.** When the named skill is not available in the session, stop and report it. Do not approximate it.

A user instruction that reorders the work changes when a step runs, not whether it runs. Run each displaced step at the earliest point it still applies and tell the user. When the instruction makes a step impossible as written, such as a step meant to run before repository context is loaded when that context is already loaded, treat it as a skip that needs approval.

Keep a step ledger in the task list or the scope's working record. Each step is `invoked`, `reused` with its evidence, `skipped` or `substituted` with who approved it, or `pending`. Reconcile the ledger before every question to the user, before presenting work for approval, before producing or publishing this skill's deliverable, and in the final report. A required step still `pending` at its gate stops the work. The final report lists every step and its status.

| Thought | Reality |
|---|---|
| "This scope is small, so the full workflow is overhead." | Size is not an exemption. If a step looks like overhead, ask to skip it. |
| "I'll do this step informally; it's equivalent." | Only the named skill completes its step. |
| "A general-purpose agent gives the same fresh-context review." | It is a substitution and needs approval. |
| "The user asked me to start elsewhere, so this step no longer applies." | The order changed; the step did not. Run it afterwards or ask to skip it. |
| "A destination or input is missing, so I'll skip the step." | Ask for what is missing, or use the fallback this skill describes. |
| "I'll catch up on skipped steps later." | The ledger is checked at every gate; later does not come first. |
| "The deadline is close." | Time pressure is a reason to tell the user, not to skip silently. |

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
