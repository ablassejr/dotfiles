---
name: release-workflow
description: Prepare and verify a release with plan-materialization's rigor — approve what users should get and which contracts must hold, reconcile merged changes against what is claimed, attack rollout and rollback from fresh context, obtain the go decision, and confirm the shipped result by observation. Use for releases, version cuts, deploy readiness, go/no-go reviews, release notes, and "ship it" requests.
---

# Release workflow

Get already-merged changes to their users with every included change accounted for, a stated way back, and the result observed rather than assumed. This skill neither writes features nor fixes defects; a defect found during readiness goes to `$sdlc-router`.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally or from memory does not complete the stage. A subagent can supply fresh context when it invokes the named skill.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name, or through a skip the user approved after you explained what assurance it loses. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. A required stage still pending blocks the go decision.

## Human checkpoints

Ask the user only for: approval of the release basis (stage 1); material choices evidence cannot settle, such as including or holding a change (stage 4); and the go decision on the exact release candidate (stage 6). Tagging, publishing, deploying, and announcing happen only with the user's explicit authorization for that exact action, through the repository's own release tooling.

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Release basis | `$first-principles-intake` | The user approves who receives the release and what they should be able to do afterward, the contracts that must keep holding, the expected way back if it goes wrong, and the observation that will show success. |
| 2 | Inventory | `$post-basis-context-loader`, then `$basis-context-reconciler` | Every change between the previous release and the candidate is listed from version control, each traced to its approved specification or issue where one exists. Changes without a traceable intent and claimed changes that are missing are both flagged. |
| 3 | Research | `$specification-research-loop`, gated by `$speckit-autonomous-research-gate` | Facts about migration order, compatibility, dependency versions, and configuration differences are settled from evidence. |
| 4 | Decisions | `$decision-frontier-manager`, then `$human-decision-loop` | No material inclusion, ordering, or risk choice remains open. |
| 5 | Readiness review | `$adversarial-specification-review` | The reviewer receives the basis, inventory, rollout and rollback plan, and evidence, and tries to break the release: irreversible steps without recovery, migrations that cannot roll back, ordering hazards, incompatible clients, and success signals that cannot be observed. Material findings are resolved. |
| 6 | Go decision | The user | The user approves the exact candidate revision and plan. Release notes describe the shipped behavior as it is, written for its users. |
| 7 | Rollout and verification | The repository's release tooling, with the user's authorization | The release is performed and the stage 1 success signal is observed in the target environment. On failure, the stated way back is offered with its exact action. |

## Results

Report `RELEASE_READY` (go approved, rollout not authorized), `RELEASED` (rolled out and the success signal observed), `HELD` with the deciding finding, or `BLOCKED` with the missing access or authority. Name every inventory flag and how it was settled.
