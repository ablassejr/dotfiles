---
name: speckit-first-principles
description: Expand or audit an approved First-Principles Basis into the first-principles semantic kernel of a Spec Kit epic workspace after context reconciliation.
---

# Spec Kit first principles

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

Invoke `$first-principles-specification` only after `$first-principles-intake` has produced an explicitly approved basis and `$basis-context-reconciler` has classified the gathered context. Keep the semantic expansion in the active Spec Kit feature workspace. This adapter does not establish the pre-context basis and must not expose repository or historical context to that intake gate.

Give every material record a stable semantic ID. Separate observed facts, interpretations, proposals, human decisions, and unresolved questions. Compare plausible problem frames before choosing a provisional one, and identify evidence that could falsify the frame or a surviving requirement.

Return the exact basis version, updated semantic records, the evidence or authority behind them, reconciled contradictions, unresolved factual gaps, and the human-owned decision frontier. Do not silently rewrite the approved basis or advance a provisional record merely because the document is complete.
