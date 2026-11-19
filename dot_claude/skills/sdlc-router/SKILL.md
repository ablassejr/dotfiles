---
name: sdlc-router
description: Classify a software-delivery request by SDLC level — initiative, epic, issue or bug fix, hotfix or incident, spike, refactor, release, or postmortem — and invoke the level skill that applies plan-materialization's rigor at that scale. Use at the start of any non-trivial planning, specification, or delivery request whose level is not already named, including vague asks like "plan this", "we need to fix prod", "should we use X", "clean this up", or "ship it".
---

# SDLC router

Pick the level, invoke its skill, and get out of the way. The router owns classification only; the level skill owns every stage after it.

## Classify from the request alone

Classify before loading any repository, history, or implementation context. Every level skill starts with `$first-principles-intake`, which must not see implementation context, so the router passes along the raw request, any linked issue's title and stated outcome, and explicit constraints, and nothing it learned by exploring.

Classify by the outcome and how it must be delivered, not by size words. "Small", "quick", "big", and "urgent" are claims to test, not levels.

| Level | The request is about | Invoke |
|---|---|---|
| Initiative | One strategic outcome that needs several independently valuable epics | `$initiative-materialization` |
| Epic | One outcome that needs several dependency-ordered PRs | `$plan-materialization` |
| Issue, feature, bug fix | One outcome that one independently useful PR can deliver | `$single-pr-spec-workflow` |
| Hotfix, incident | Production currently violates a contract it used to honor, and people are harmed now | `$hotfix-workflow` |
| Spike | A question whose answer unblocks a decision; nothing ships | `$spike-workflow` |
| Refactor | Structure changes while every observable behavior stays the same | `$refactor-workflow` |
| Release | Already-merged changes reaching named users | `$release-workflow` |
| Postmortem | Understanding a past failure and changing the system so it is less likely | `$postmortem-workflow` |

Execution and integration of an already approved scope go to the skill its handoff names: `$implementation-specification-compiler` for an epic's delivery plan, `$issue-implementation` or `$single-pr-executor` for one approved issue, and `$specification-reconciliation` after an epic's PRs merge.

## When the level is unclear

Ask one question only when the two candidate levels would lead to different approvals or deliverables; explain what each reading would produce. Otherwise pick the narrower level and say so, because every level skill rechecks its own boundary and returns when the scope does not fit.

Common confusions, with the deciding question:

- Bug fix or hotfix: is harm happening in production now, against a contract that previously held? If not, it is a bug fix.
- Refactor or feature: does any observable behavior change? If so, the behavior change is a feature or fix, and only the remainder is a refactor. A request that mixes both is split without asking: route each part to its level and tell the user about the split.
- Spike or epic: is the deliverable a decision or shipped behavior?
- Epic or initiative: could each part be dropped without making the others pointless? If yes, the parts are epics of an initiative.

## When a level skill hands back

A level skill returns `SCOPE_DECISION_REQUIRED` or reports a larger or different scope when its boundary no longer fits. Reclassify with the new evidence, tell the user which level the work moves to and why, and invoke that skill. Approved bases and decisions carry over under the receiving skill's approval-reuse rules; do not restart intake for unchanged intent.

## Report

State the chosen level, the one-sentence reason, and the skill invoked. Do not summarize or perform the level skill's stages.
