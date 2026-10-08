---
name: plannotator-review
description: Open Plannotator's browser-based code review UI for the current worktree or a pull request URL, then act on the feedback that comes back.
allowed-tools: Bash(plannotator:*)
disable-model-invocation: true
---

# Plannotator Review

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


## Code review feedback

!`plannotator review $ARGUMENTS`

## Your task

If the review above contains feedback or annotations, address them in the same conversation. If no changes were requested (an approval/LGTM-style result), acknowledge that review passed and continue.
