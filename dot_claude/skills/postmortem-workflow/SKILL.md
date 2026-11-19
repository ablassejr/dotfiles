---
name: postmortem-workflow
description: Run a blameless postmortem with plan-materialization's rigor — approve which incident and contract are in scope, build a source-cited timeline, investigate contributing factors and competing explanations, attack the analysis from fresh context, and turn findings into self-contained issues that change the system. Use for postmortems, incident reviews, retrospectives on an outage, root-cause analysis write-ups, or "what went wrong with X".
---

# Postmortem workflow

Produce a shared, evidence-grounded account of a past failure and actions that make it less likely, then stop. The review is blameless because blame stops evidence from surfacing and produces actions that change people's caution instead of the system.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally or from memory does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. A required stage still pending blocks the final review.

## Human checkpoints

Ask the user only for: approval of the postmortem basis (stage 1); material choices evidence cannot settle, such as which factors to act on (stage 5); approval of the exact document and actions (stage 7); and a publication destination when publication is next and none is established.

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Postmortem basis | `$first-principles-intake` | The user approves which incident is in scope, the contract that was violated and its source, the impact as the user states it, and what the organization needs from the review. |
| 2 | Timeline | `$post-basis-context-loader`, then `$basis-context-reconciler` | Every timeline entry cites a primary source such as logs, metrics, deploy records, alerts, or messages. Entries that rest on recollection or inference are labeled unverified. |
| 3 | Contributing factors | `$specification-research-loop`, gated by `$speckit-autonomous-research-gate`; `$ground-me` for why a failing mechanism existed | Factors are supported by evidence, competing explanations were tested, and the analysis does not stop at a single root cause when several conditions had to coincide. |
| 4 | Adversarial review | `$adversarial-specification-review` | The reviewer receives the basis, timeline, evidence, and analysis, not the author's reasoning, and looks for hindsight bias, blame, unsupported causal claims, and missing factors. Material findings return to the earliest affected stage. |
| 5 | Actions | `$decision-frontier-manager`, then `$human-decision-loop`; `$subtractive-design-analyzer` | Each action traces to a factor, changes the system rather than asking people to be more careful, prefers removing a hazard over adding a guard, and states a minimal observable acceptance criterion. |
| 6 | Document | `$multimodal-research-compiler` | One self-contained document leads with impact and the most consequential factors, shows the timeline and evidence, separates verified from inferred, and lists the actions. |
| 7 | Final review | The user | The user approves the exact document and action set. |
| 8 | Issues and publication | `$issue-writing` for each action; `$tasks-to-issues` and `$specification-publisher` when publication is authorized | Each action is a self-contained issue whose only document reference is the postmortem. Provider writes are read back. |

## Results

Report `HANDOFF_READY` when the approved document and issues are durable and accessible to the team, `AWAITING_APPROVAL` with the draft, or `BLOCKED` with the missing source, access, or authority. Name every unverified timeline entry that remains.
