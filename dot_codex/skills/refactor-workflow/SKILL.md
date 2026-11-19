---
name: refactor-workflow
description: Plan a refactor or tech-debt reduction with plan-materialization's rigor — approve what becomes simpler and which behavior must not change, find what can be removed or consolidated, lock observable behavior with boundary tests, attack the proposal from fresh context, and hand off one or more behavior-preserving PRs. Use for refactors, cleanups, consolidation, dead-code removal, restructuring, or "pay down tech debt" requests.
---

# Refactor workflow

Make the code simpler while every observable behavior stays the same, then hand off. The invariant is the whole point: a change that alters behavior is a feature or fix and goes through `$single-pr-spec-workflow`, even when it is small and convenient to include.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally or from memory does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. A required stage still pending blocks the final review and the handoff.

## Human checkpoints

Ask the user only for: approval of the refactor basis (stage 1); material choices evidence cannot settle, such as removing something whose purpose is still uncertain (stage 4), one at a time with `$ground-me` offered; and approval of the exact proposal (stage 8).

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Refactor basis | `$first-principles-intake` | The user approves what should become simpler or disappear and why it matters, the behavior and interfaces that must not change, explicit non-goals, and the evidence that will show both simplification and preservation. |
| 2 | Context | `$post-basis-context-loader`, then `$basis-context-reconciler` | The affected responsibility, its consumers, tests, and history are pinned to a baseline. |
| 3 | Subtraction analysis | `$local-simplification` for one bounded responsibility, `$subtractive-codebase-consolidator` for duplicates across responsibilities, then `$subtractive-design-analyzer` | Each removal or consolidation candidate states its original purpose, current consumers, and whether that purpose still holds. Lack of observed usage alone never establishes safe deletion. |
| 4 | Decisions | `$decision-frontier-manager`, then `$human-decision-loop` | No material choice remains open. Candidates with uncertain purpose went through `$ground-me` before the user decided. |
| 5 | Behavior lock | The proposal's verification plan | Every observable contract in scope is covered by a behavior-only test at its public boundary that passes before the change. White-box tests in scope are rewritten to assert behavior. Any behavior change the analysis uncovered is split out to `$sdlc-router`. |
| 6 | Code mass | `$code-mass-auditor` when a code-mass budget applies | The planned net reduction is budgeted from measurements, not estimates. Planned deletion is not credit until committed and verified. |
| 7 | Adversarial review | `$adversarial-implementation-review` | Material findings are resolved. The reviewer receives the basis, analysis, behavior lock, and plan, not the author's reasoning, and looks especially for hidden behavior changes and removed controls. |
| 8 | Final review | The user | The user approves the exact proposal revision: what is removed or consolidated, why it is safe, the behavior lock, and the PR boundaries. |

## Handoff

When one independently useful PR can hold the change, hand off to `$single-pr-executor`. When it needs several, hand off to `$implementation-specification-compiler`, and keep every intermediate PR behavior-preserving on its own. The handoff names the basis and proposal revisions, the baseline, the behavior lock, the code-mass evidence, and the verification performed. Report `HANDOFF_READY`, `AWAITING_APPROVAL`, `SCOPE_DECISION_REQUIRED` when behavior must change, or `BLOCKED`.
