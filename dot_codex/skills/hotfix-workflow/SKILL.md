---
name: hotfix-workflow
description: Handle a production hotfix or incident with plan-materialization's rigor under time pressure — restore a previously honored contract through an approved reversible mitigation, diagnose the verified cause, then specify and ship the smallest durable fix and record any deferred assurance. Use when production is broken now, an alert or customer report shows active harm, or the user says hotfix, outage, incident, sev, rollback, or "prod is down".
---

# Hotfix workflow

Restore a broken production contract fast without giving up the parts of the rigor that prevent a second incident. Time pressure changes how short each explanation is, not which stages run.

## Why the rigor still fits

The expensive part of first-principles intake is deciding what ought to be true. A hotfix already has that answer: a contract production honored before and violates now, such as documented behavior, the previous release's behavior, or an agreed service level. Intake therefore stays before implementation context and usually needs one sentence of approval. If no previously honored contract exists, this is new behavior, not a hotfix; return `SCOPE_DECISION_REQUIRED` so `$sdlc-router` moves it to `$single-pr-spec-workflow`.

Mitigation and fix are separate on purpose. A mitigation such as a rollback, a feature-flag change, or a configuration revert needs evidence that it restores the contract and can be undone; it does not need a root cause. The durable fix needs a verified root cause.

## Stage rules

- Each stage names the skill that performs it. Invoke that skill through the agent's skill mechanism (the `Skill` tool in Claude Code). Doing its work informally or from memory does not complete the stage.
- A stage completes without its skill only through verified reuse of an unchanged earlier result, which you name, or through a skip the user approved after you said what assurance it loses. Under incident pressure that explanation can be two sentences, but it is still required. When a named skill is unavailable, stop and report it.
- Track every stage in the task list as done, reused, skipped (with its approver), or pending. Anything skipped becomes a stage 6 record.

## Human checkpoints

Ask the user only for: approval of the contract basis (stage 1); approval of the exact mitigation action before it touches production (stage 2); material fix choices evidence cannot settle (inside stage 4); and the fix approval that `$single-pr-spec-workflow` owns. Production changes, deployments, and messages to other people happen only with the user's explicit authorization for that exact action; otherwise give the user the exact commands to run.

## Workflow

| # | Stage | Performed by | Done when |
|---|---|---|---|
| 1 | Contract basis | `$first-principles-intake` | The user approves a basis naming the affected actors, the violated contract and its authoritative source, the observed harm, what must not get worse during recovery, and the observation that will show the contract is restored. The report's symptoms are allowed inputs; repository and deploy history are not yet. |
| 2 | Mitigation | `$post-basis-context-loader` for recent changes and live signals; the user approves the action | A reversible action is chosen from evidence that it restores the contract, its undo path is stated, the user approves that exact action, and restoration is confirmed by observing the success signal from stage 1, not by the action's exit code. If no safe reversible action exists, say so and go straight to stage 3. |
| 3 | Diagnosis | `$systematic-debugging`, with `$basis-context-reconciler` | The cause is verified by reproduction or direct evidence and distinguished from competing explanations. A plausible hypothesis is reported as unverified. |
| 4 | Durable fix specification | `$single-pr-spec-workflow`, reusing the stage 1 basis | The smallest change that restores the contract at its cause is specified, reviewed, and approved inside that skill. Tests target the missing observable contract that let the defect through, not the incident's internal mechanism. If the fix needs more than one PR, that skill returns `SCOPE_DECISION_REQUIRED`. |
| 5 | Fix delivery | `$single-pr-executor`, only when the user authorized implementation | One verified PR exists. Merge and deploy follow the repository's own tooling and the user's authorization. After deploy, the stage 1 success signal is observed again and the mitigation is undone if it is no longer needed. |
| 6 | Deferred assurance | `$issue-writing` for each deferred item | Every skipped or shortened stage, temporary mitigation still in place, and unverified claim is a self-contained issue. When the impact warrants it, offer `$postmortem-workflow`; the user decides. |

## Results

Report one of: `MITIGATED` (contract restored by observation, durable fix pending), `HANDOFF_READY` (fix specification approved, implementation not requested), `FIXED` (fix deployed and the success signal observed), `SCOPE_DECISION_REQUIRED`, or `BLOCKED` with the missing access or authority. Name what is verified, what is inferred, and every open stage 6 item.
