---
name: first-principles-specification
description: Expand an approved pre-context First-Principles Basis and reconciled evidence into an epic semantic kernel, with stable IDs, falsifiable claims, explicit assumptions, and human-owned value decisions.
---

# First-principles specification

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

Require the exact human-approved basis version, post-basis current-state map, and basis-context reconciliation. This skill does not replace `$first-principles-intake` and must not create the initial basis after implementation context has been loaded. Work in the active Spec Kit feature directory and preserve its temporary status. Read the epic manifest first. Create stable IDs before other artifacts cite a record.

Reuse the approved basis without another intake interview. Keep its intent in the basis and reference it instead of drafting another intent document. Begin from the basis's desired state, underlying problem, irreducible new behavior, expected simplification, minimum sufficient change, invariants, hard constraints, forbidden tradeoffs, non-goals, success evidence, assumptions, and unresolved points. Separate direct observations from interpretations. Before solution brainstorming, create plausible alternative frames by varying the affected actor, desired outcome, central obstacle, and system boundary. Compare what each frame reveals, excludes, and assumes, then select a provisional frame through the existing evidence and human-decision boundary. Explain the causal mechanism instead of merely naming symptoms. Record goals and measurable outcomes, principles, invariants, reconciled constraints, non-goals, actors and decision rights, assumptions, unknowns, falsification conditions, and exact links back to the basis version.

Use these ID families:

```text
FRAME-### GOAL-###       PRINCIPLE-###  INVARIANT-###
ACTOR-### REQ-###        SCENARIO-###   CONSTRAINT-###
DECISION-### RISK-###    EVIDENCE-###   VIEW-###
QUESTION-###
```

Do not manufacture a requirement because a familiar implementation usually has one. Before a proposed requirement or constraint becomes current, challenge it through `$framed-engineering-sequence`. Each survivor identifies its authoritative source, rationale, and current named human steward; an external authority remains the source even though a person owns re-evaluation. Trace every proposed requirement to the provisional frame and a stated goal, first principle, verified constraint, or human decision. Record material candidates as retained, deleted, or restored with their evidence instead of using the ten-percent add-back heuristic as a quota. Mark inferred claims as proposals and factual claims without evidence as unknowns.

When facts are missing, invoke `$specification-research-loop`. When a choice depends on values, priority, acceptable risk, or intended product behavior, add it to `$decision-frontier-manager`; only unresolved material human choices reach `$human-decision-loop`, with optional `$ground-me`. State the consequence and why the answer is needed now; facts and routine choices covered by approved intent stay with the agent. Do not settle it for the user. When evidence changes the basis, create and approve a successor version rather than editing history. After updates, give a fresh agent the bounded specification and use the first-principles alignment contract in `$epic-spec-workflow`.

Update the owning semantic records and return their references with the decision-relevant changes and remaining blockers. Keep frames, trace links, challenge outcomes, counterexamples, and the frontier as supporting records or generated views; do not produce a parallel narrative for each. Do not publish to an external documentation or issue service from this skill.
