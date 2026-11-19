---
name: plan-materialization
description: Turn a large epic or plan into an approved, team-legible specification and handoff before implementation. Approve first principles, reconcile evidence, resolve only material human decisions, review adversarially, and stop at HANDOFF_READY in the project's chosen destinations.
---

# Plan materialization

Turn a plan into an approved specification and a verified handoff, then stop. This skill does not start implementation, create delivery issues, or publish to an external service unless the request authorizes publication.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally, from memory, or through a generic agent does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name to the user, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. Check that list before the final review and at handoff; a required stage still pending blocks both. A user instruction that reorders work changes when a stage runs, not whether it runs.

## Human checkpoints

Ask the user only for:

1. Approval of the First-Principles Basis (stage 1).
2. Material choices that evidence and approved intent cannot settle (stage 4), one at a time, with `$ground-me` offered.
3. Approval of the exact design proposal and its visuals together (stage 8).
4. A publication destination or authorization, only when publication is the next action and none is established.

Stage transitions, research, clean reviews, repairs within the approved basis, and readback continue without a prompt. Before any question or team-facing artifact, follow [review and artifact design](references/review-and-artifact-design.md).

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | First principles | `$first-principles-intake` | The user approves the exact basis. Give intake only the raw request, applicable approved goals, stated outcomes, and explicit constraints; load no implementation context yet. Reuse an unchanged approved basis that already covers the scope. |
| 2 | Context | `$post-basis-context-loader`, then `$basis-context-reconciler` | Repository identity, baseline, current sources, and relevant organizational evidence are pinned and reconciled with the basis. An inaccessible source is recorded as an evidence gap. See [tool routing](references/tool-routing.md). |
| 3 | Research | `$specification-research-loop`, gated by `$speckit-autonomous-research-gate` | The gate returns `PROCEED`. `CONTINUE_RESEARCH` loops; `REQUEST_HITL` goes to stage 4; `REVISE_FIRST_PRINCIPLES` returns to stage 1 for a successor basis. See [research and review](references/research-and-review.md). |
| 4 | Decisions | `$decision-frontier-manager`, then `$human-decision-loop` | No material human choice remains open. Settled choices, accessible facts, and routine details covered by approved intent never reach the user. |
| 5 | Semantic design | `$subtractive-design-analyzer`, `$first-principles-specification`, `$framed-engineering-sequence` | Each requirement has a stable ID and traces to the basis, the smallest sufficient mechanism survives, and code-mass obligations are recorded where [subtractive code mass](references/subtractive-code-mass.md) applies. New facts return to stage 3; new choices return to stage 4. |
| 6 | Adversarial review | `$adversarial-specification-review` | Material findings are resolved. The reviewer receives the basis, semantic records, evidence, decisions, and sources, not the author's reasoning. A repair returns to the earliest affected stage, and only affected downstream stages rerun. |
| 7 | Proposal | `$design-document` under the [supervisor proposal contract](references/supervisor-design-document.md); `$visual-language-compiler` when graph visuals help | One self-contained proposal exists in the chosen document home, and its rendering, links, and media are checked. Graph visuals follow the [graph visual policy](references/graph-visual-policy.md). |
| 8 | Final review | The user | The user approves the exact proposal revision. A semantic change returns to stage 5; a presentation-only change returns to stage 7. |
| 9 | Handoff | `$specification-publisher` when publication is authorized | `HANDOFF_READY`, or a delivered draft that names the unmet condition. |

Spec Kit and `specflow` are optional integrations. Initialize a specification workspace only when it is useful and authorized, and preserve existing files and conventions.

## Resume

Read the governing records first: the basis and its approvals, the specification revision, the repository baseline, pending decisions, and incomplete writes. Reuse unchanged approvals and settled choices under [approval economy](references/approval-economy.md), and continue at the earliest incomplete stage. Before stage 6 and stage 9, compare the baseline with current changes and refresh affected evidence without rewriting earlier approvals.

## Destinations

Use the destinations the user named or the project already governs: repository documentation, a wiki, a shared document, a tracker, or a portable Markdown or HTML draft. No provider is a default, and the workflow never creates a project or account to fit a layout. Without a destination, deliver the draft with its verification limits. See [workspace and destinations](references/workspace-and-destinations.md) and [specification publication](references/specification-publication.md).

## Orchestrated runs

When a configured Camunda process (definition `epic-spec-workflow`) governs this scope, its live position and accepted task completion are the authority. Follow the [Camunda integration](references/camunda-orchestration.md), [runtime](references/camunda-runtime.md), and [stage visibility](references/stage-visibility.md) contracts, and never simulate engine completion. Without that process, the `specflow`, Camunda, Linear, and Notion adapter references do not apply.

## Handoff

The handoff names the approved specification revision, basis lineage, repository baseline, decisions, non-goals, residual questions, code-mass evidence, approval, and verification without retelling the design (see [workflow records](references/workflow-records.md)). Use shared, descriptive links and keep local paths internal. Report `HANDOFF_READY` only when approval, freshness, durable content, and team access are verified. Otherwise deliver the draft and name the exact unmet condition. Remove only temporary artifacts this run created, after their durable replacement exists.

Delivery planning is a separate, explicit `$implementation-specification-compiler` invocation; `$issue-implementation` and the reconciliation skills own execution and integration.

## Utilities

When a stage needs a missing utility such as `specflow`, `likec4`, Archify, `cloc`, or `c8ctl`, use the [setup instructions](references/setup.md) and [dependency manifest](dependencies.json).
