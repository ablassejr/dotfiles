---
name: initiative-materialization
description: Turn a strategic initiative that spans several epics into an approved basis, an evidence-grounded decomposition into independently valuable epics with explicit dependencies, and per-epic handoffs for plan-materialization. Use when one outcome needs more than one epic, for roadmaps, programs, quarterly goals, platform migrations, or "multi-team" efforts. Stops at HANDOFF_READY; each epic is materialized separately.
---

# Initiative materialization

Turn one strategic outcome into an approved set of epics, each with its own inherited basis, then stop. This skill does not specify the epics' internals, create delivery issues, or start implementation. Publishing to a tracker or documentation home happens only when the request authorizes it.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally, from memory, or through a generic agent does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name to the user, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. A required stage still pending blocks the final review and the handoff. A user instruction that reorders work changes when a stage runs, not whether it runs.

## Human checkpoints

Ask the user only for: approval of the initiative basis (stage 1); material choices evidence cannot settle (stage 4), one at a time with `$ground-me` offered; approval of the exact decomposition proposal (stage 8); and a publication destination when publication is next and none is established. Everything else continues without a prompt.

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Initiative basis | `$first-principles-intake` | The user approves the exact basis: the strategic outcome, why it matters now, what must stay true, what becomes unnecessary, and the evidence that would show success. Success measures come from the user or an approved goal; do not invent targets. |
| 2 | Context | `$post-basis-context-loader`, then `$basis-context-reconciler` | Existing epics, owners, systems, commitments, and constraints in scope are pinned and reconciled with the basis. Inaccessible sources are recorded as evidence gaps. |
| 3 | Research | `$specification-research-loop`, gated by `$speckit-autonomous-research-gate` | The gate returns `PROCEED`. `REQUEST_HITL` goes to stage 4; `REVISE_FIRST_PRINCIPLES` returns to stage 1 for a successor basis. |
| 4 | Decisions | `$decision-frontier-manager`, then `$human-decision-loop` | No material choice about priority, sequencing, ownership, or acceptable risk remains open. |
| 5 | Decomposition | `$subtractive-design-analyzer`, then `$framed-engineering-sequence` | Every candidate epic traces to basis requirement IDs and is independently valuable: dropping it leaves the others still useful. Epics that only carry another epic's work are merged into it. Dependencies between epics are explicit and minimal, and anything the initiative makes unnecessary is named for removal. |
| 6 | Adversarial review | `$adversarial-specification-review` | Material findings are resolved. The reviewer receives the basis, decomposition, evidence, and decisions, not the author's reasoning. Repairs return to the earliest affected stage. |
| 7 | Proposal | `$design-document`; `$visual-language-compiler` when a dependency or ownership graph helps | One self-contained proposal shows the outcome, the epics, why each exists, their dependencies, and what is out of scope. Rendering, links, and media are checked. |
| 8 | Final review | The user | The user approves the exact proposal revision. A semantic change returns to stage 5; a presentation change returns to stage 7. |
| 9 | Handoff | `$specification-publisher` when publication is authorized | `HANDOFF_READY`, or a delivered draft naming the unmet condition. |

## Child bases

Each epic's handoff carries the initiative basis lineage and the requirement IDs the epic covers. When `$plan-materialization` later runs for that epic, its intake reuses the initiative basis if the epic is wholly covered by it, and drafts a successor basis only for new intent or constraints. Do not pre-approve epic bases on the user's behalf, and do not run `$plan-materialization` for the epics unless the user asks.

## Resume

Read the basis and its approvals, the decomposition revision, the context baseline, pending decisions, and incomplete writes. Reuse unchanged approvals, continue at the earliest incomplete stage, and refresh evidence that changed since the baseline before stages 6 and 9.

## Handoff

The handoff names the approved basis and proposal revisions, each epic with its covered requirement IDs and dependencies, decisions, non-goals, residual questions, and verification performed, without retelling the design. Use shared, descriptive links; local paths stay internal. Report `HANDOFF_READY` only when approval, freshness, durable content, and team access are verified; otherwise report `AWAITING_APPROVAL` with the proposal, or `BLOCKED` with the missing capability or authority. When the scope turns out to be one epic, return `SCOPE_DECISION_REQUIRED` so `$sdlc-router` can move it to `$plan-materialization`.
