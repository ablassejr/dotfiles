---
name: linear-ticket-implementation
description: Compatibility entry point for issue-implementation. Use the current project's chosen sources and destinations; the historical name does not select a provider.
---

# Issue implementation compatibility entry point

Read and execute [the issue implementation skill](../issue-implementation/SKILL.md). It owns the workflow and its current contracts. This name remains available for existing invocations and configured automation; it does not select an organization, issue tracker, documentation home, or process engine.

Preserve the current request and any explicit project-specific provider or runtime binding. If the project selects a provider-specific adapter, use that adapter's actual contract. Otherwise follow the neutral workflow, including portable preparation when no publication destination is chosen. Do not create an extra copy of the output or repeat an approval because this entry point was used.
