---
name: issue-implementation-designer
description: Produce a concrete repository-grounded implementation proposal for one issue or work item and store it in the issue's linked design record rather than its description or comments.
---

# Issue implementation designer

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

Resume `$issue-implementation` after the ticket-level basis is approved, `$post-basis-context-loader` returns evidence sufficient for the design decisions, and `$basis-context-reconciler` classifies its relationship to the basis. Apply `$framed-engineering-sequence` at ticket scope before choosing code shape.

Invoke `$subtractive-design-analyzer` against the ticket's responsibility domain and use `$ground-me` for uncertain or unknown deletion safety before proposing code. Describe the entry point, exact behavior introduced and removed, affected public contracts, files and symbols added and removed, production and test SLOC estimates, conceptual-complexity delta, public-API delta, dependency delta, data and state changes, concurrency, failure and recovery behavior, security boundaries, migrations and rollback, observability, and behavior-focused verification. Explain why deletion-only and existing-mechanism reuse are insufficient and why the selected mechanism is the minimum correct and comprehensible design.

Keep the proposal to one issue, one owner, and one pull request. Fill the issue's structured Code Mass Contract and explain its implications in the design proposal. If the issue cannot remain independently useful and reviewable, return `ISSUE_SPLIT_REQUIRED` rather than hiding a second change inside it.

During [program issue review](references/bundled/epic-spec-workflow/references/issue-review-before-assignment.md), unresolved execution blockers do not by themselves prevent design. Ground the proposal in approved predecessor contracts, resolve material design dependencies, and leave implementation blocked until its native prerequisites are satisfied. Return prepared design evidence to the modeled ticket decision loop; finalize alignment and review in the governing records after that loop resolves; use `specflow.finalize-ticket-design` only for its configured runtime profile.

Use `$decision-frontier-manager` and `$human-decision-loop` to resolve material choices one question at a time. Keep required estimates and accounting in the structured Code Mass Contract. Surface only the grounded consequences that materially help the current choice, such as reversibility, operational risk, migration cost, or code-mass impact; do not require the supervisor to parse a full accounting table for every question. When the human selects `Ground me`, suspend the choice, invoke `$ground-me`, align understanding, and accept an explicit combined answer through [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) when the evidence and question still match. Without that answer, return to the current question; an invalid premise requires recomputation.

Run `$first-principles-implementation-alignment`, the planning pass of `$code-mass-auditor`, and `$adversarial-implementation-review` in that order before presenting the concise final decision frontier. The planning audit returns `CODE_MASS_TARGETED`; it does not claim committed measurements or approve a Net Addition Gate. At the end of planning, publish the resulting proposal as the linked [supervisor design document](references/bundled/epic-spec-workflow/references/supervisor-design-document.md), using the existing record when available. Its main narrative explains and proposes the design to a human with no starting context, prefers visuals over equivalent text, and retains only sentences that add necessary understanding. Keep detailed engineering evidence behind precise links unless the decision needs it. Fetch and inspect the document before the existing final design approval in the selected review surface, then bind approval to its exact source, revision, and content hash. The issue body retains the approved behavioral contract and only its optional design proposal reference; code-mass details remain in the proposal and structured records.

## Graph visual gate

Apply the shared [graph visual policy](references/bundled/epic-spec-workflow/references/graph-visual-policy.md) to every graph-like output. Use Figma Design, LikeC4, or Archify and retain matching render-operation and artifact evidence. Include all produced or published visuals in the current step’s inventory and run `specflow validate-visuals <manifest.json> --json` before presentation. A missing renderer or invalid receipt blocks the visual output. Non-graph media keep their own communication purpose.

Follow [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) for the scope’s evidence-bound automatic routes, combined final visual/design review, targeted revision, and existing authorization. Automatic review records remain distinct from human approval.
