---
name: issue-implementation
description: Orchestrate one issue or work item from an approved basis through post-basis grounding, sequential decisions, implementation review, and one verified pull request.
---

# Issue implementation

## Invoke every named step

Each `$name` in this skill and its references is a required step, and that skill performs it. When a step is reached, invoke the named skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing the step's work yourself, reproducing it from memory, folding it into another step, or handing it to a general-purpose agent or generic review does not complete it, even when the result looks equivalent. A subagent may supply the fresh context a step requires, provided it invokes the named skill.

A step completes without its own invocation only in these ways, and never silently:

- **Verified reuse.** [Approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) allows an existing approval to be reused. Record the evidence and tell the user what was reused.
- **Approved skip or substitution.** Before moving past the step, tell the user which step it is, why it should not run as written, what replaces it, and what assurance is lost. Continue only after the user approves. That message is a decision prompt under [Explain every decision before asking it](#explain-every-decision-before-asking-it).
- **Unavailable skill.** When the named skill is not available in the session, stop and report it. Do not approximate it.

A user instruction that reorders the work, such as "check the premise against the code first", changes when a step runs, not whether it runs. Run each displaced step at the earliest point it still applies and tell the user. When the instruction makes a step impossible as written, such as an intake meant to run before any repository context when that context is already loaded, treat it as a skip that needs approval.

Keep a step ledger in the task list or the design record. Each step is `invoked`, `reused` with its evidence, `skipped` or `substituted` with who approved it, or `pending`. Reconcile the ledger before every question to the user, before presenting a design for approval, before writing code, and in the final report. A required step still `pending` at its gate stops the work. The final report lists every step and its status.

| Thought | Reality |
|---|---|
| "The change is small, so the full workflow is overhead." | Size is not an exemption. If a step looks like overhead, ask to skip it. |
| "I'll do this analysis informally; it's equivalent." | Only the named skill completes its step. |
| "A general-purpose agent gives the same fresh-context review." | It is a substitution and needs approval. |
| "The user told me to read the code first, so intake no longer applies." | The order changed; the step did not. Run it afterwards or ask to skip it. |
| "I don't know the document home, so I'll skip publication." | Ask for the destination, or prepare the portable draft this skill describes. |
| "I'll catch up on skipped steps later." | The ledger is checked at every gate; later does not come first. |
| "The owner wants this today." | Time pressure is a reason to tell the user, not to skip silently. |

## Explain every decision before asking it

Every decision put to the user is preceded, in the same message, by a thorough explanation. This covers design questions, choices between options, approvals of a basis, design, write or push, requests to skip or substitute a step, and go-ahead questions. The explanation covers:

- **The decision point.** What exactly is being decided, why it needs this person's judgment, and why it needs it now.
- **The context.** The current state and the evidence that led here, the constraints and earlier decisions it depends on, and what is still unknown. Name the systems, files, issues and terms involved, and assume the reader has not followed the session.
- **The implications.** For each option, including doing nothing: what it changes, what it costs, what it rules out or makes harder, its risks, whether it can be reversed, and what happens next. Give the recommendation and the reason for it.

Option labels and descriptions in a question tool summarize choices the message has already explained; they do not replace the explanation. This rule applies to every question asked while this skill runs, including those its sub-skills ask, and it takes precedence over briefer prompt guidance in its references. Explain the decision, not the work log.

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Read [workspace and destinations](references/bundled/epic-spec-workflow/references/workspace-and-destinations.md). Use the current project's work item, documentation home, ownership, and dependency graph. An existing orchestrator retains authority over its active process; use its actual task bindings and permitted operations. The packaged Camunda/Linear/Notion runtime applies only to its selected profile. Without that engine, execute the authorized workflow with the scope's records and explicit human decisions; do not invent process keys or make engine installation a prerequisite.

Read [references/implementation-loop.md](references/implementation-loop.md) before changing code. This skill handles one issue and one pull request. It does not repartition the delivery program or itself bypass any orchestration gate.

First check [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) for an unchanged approved basis that covers this ticket. Verified inheritance permits context loading without a new basis task. When the ticket adds intent, begin with `$first-principles-intake` in a fresh or intentionally restricted context. Supply only the raw request, issue title and stated outcome, directly applicable approved product goals, and explicit constraints. Do not fetch implementation-oriented issue history, native relations, the repository, Git, pull requests, ADRs, or existing architecture into that intake. The named human must approve the exact ticket-level basis version before context loading.

After approval, invoke `$post-basis-context-loader` to fetch the full work item, its actual project and ownership, supported issue relations or governing dependency graph, approved specification revision, repository baseline, relevant ADRs, code, tests, and history. During program review, use approved predecessor contracts to ground design even when implementation blockers remain unresolved. Surface unresolved design dependencies through the issue HITL loop. Before execution, verify that no native `blocks` relation points from an unresolved issue to the selected issue; an execution blocker prevents implementation. Invoke `$basis-context-reconciler` before asking implementation questions. Follow [shared tool routing](references/bundled/epic-spec-workflow/references/tool-routing.md) for structural and semantic retrieval and version/environment CLI capability records, subject to stricter explicit session rules.

Keep the issue description focused on the self-contained problem, required outcome, behavioral properties, non-goals, and approved constraints. Put source authority, ticket-level basis, normalized Grounding Summaries, and recorded implementation decisions in its design proposal and structured workflow records. Do not add dependency fields, source paths, code shapes, command syntax, or detailed implementation design. Read dependency truth from the selected tracker's supported relations or the owning plan's graph; do not pretend an unsupported native relation exists. After an authorized issue update, fetch it and verify its standalone meaning and proposal-only document references. Verify basis IDs, status, and evidence links in the internal records and proposal.

Before the design loop, resolve the work item's existing design proposal and its chosen document home. At the end of planning, publish the complete [supervisor design document](references/bundled/epic-spec-workflow/references/supervisor-design-document.md) there; when no document exists, prepare the proposal in the selected home or as a portable draft until publication is requested and its destination is known. Reuse task authorization and request only missing destination information or write authority after preparing the concrete proposal. Fetch the document and its issue association after writing. Detailed engineering evidence can remain in linked supporting records. Promote a durable technical decision to an ADR when it is costly to reverse, surprising without context, and based on a real tradeoff.

Invoke `$framed-engineering-sequence` at ticket scope, then `$subtractive-design-analyzer`, before proposing code. Start from the approved product frame and ticket-level basis, but test whether the issue's implementation framing, inherited requirement, component, process, or automation survives current repository evidence. Ground uncertain or unknown deletion candidates and count only confirmed safe removal. Delete unnecessary work, simplify the whole affected system before optimizing a local part, shorten the trustworthy feedback loop, and automate stable execution only after those choices settle. Keep tests, builds, security checks, traceability, evidence capture, and readback as early guardrails. Store ticket-scope design, normalized decisions, grounding conclusions, and Code Mass Contract explanations in their owning proposal sections and structured records; the issue carries its self-contained behavioral contract.

Build the unresolved choices with `$decision-frontier-manager` and ask one material question at a time through `$human-decision-loop`. Keep accounting detail in the structured contract, and explain each question as [Explain every decision before asking it](#explain-every-decision-before-asking-it) requires. Offer `$ground-me` as optional depth, reuse settled intent, and do not repeat the epic interview for each issue. Grounding produces a validated packet. The human can align understanding alone or explicitly align and answer together. The parent records a combined answer only while the packet and question bindings still match; changed bindings reopen the current question, and premise invalidation recomputes it.

After the frontier settles, invoke `$first-principles-implementation-alignment`, the planning pass of `$code-mass-auditor`, and `$adversarial-implementation-review`, each with fresh context. Record an estimated positive delta as `net-addition:review-required`; post-implementation evidence completes that gate. Do not implement until targeted research is complete, the human approves every material decision, the planning audit returns `CODE_MASS_TARGETED`, all design reviews have no unresolved material finding, the framed engineering sequence has no unresolved material step, and the fetched supervisor design document matches the exact approved revision and source binding. Then invoke `$single-pr-executor`. One person or agent owns integration, the branch or worktree, the pull request, and the final verification result even when teammates assist.

## Issue review and assignment

Follow [individual issue HITL before team assignment](references/bundled/epic-spec-workflow/references/issue-review-before-assignment.md). Use the actual approved team and the governing program's assignment policy. Apply a whole-program review-before-assignment gate only when that policy requires it. Reuse the verified ticket review for assigned implementation; do not ask for unchanged approvals again.
