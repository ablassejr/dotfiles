---
name: notion-canonicalizer
description: Compatibility entry point for specification-publisher. Use the current project's chosen sources and destinations; the historical name does not select a provider.
---

# Specification publisher compatibility entry point

Read and execute [the specification publisher skill](../specification-publisher/SKILL.md). It owns the workflow and its current contracts. This name remains available for existing invocations and configured automation; it does not select an organization, issue tracker, documentation home, or process engine.

Preserve the current request and any explicit project-specific provider or runtime binding. If the project selects a provider-specific adapter, use that adapter's actual contract. Otherwise follow the neutral workflow, including portable preparation when no publication destination is chosen. Do not create an extra copy of the output or repeat an approval because this entry point was used.
