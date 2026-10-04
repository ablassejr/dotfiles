---
name: speckit-context-gathering
description: Gather project, organizational, repository, architecture, and source context for a Spec Kit epic only after its First-Principles Basis is approved.
---

# Spec Kit context gathering

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run `$post-basis-context-loader` at epic scope. Require the exact First-Principles Basis version and validate explicit human approval before resolving or searching implementation context. After the gate passes, follow [shared tool routing](../epic-spec-workflow/references/tool-routing.md) to pin identity, baseline, worktree state, and source revisions, use structural and semantic retrieval, and maintain applicable CLI capability records. Use external research only for unresolved external facts.

Maintain context and evidence once in their owning records. Generate a context map, source view, claim ledger, or gap matrix only when it answers a distinct current question; no separate file is required for each. Keep these views internal and add created temporary files to provenance. Record source owner, applicable version or date, retrieval time, scope, confidence, contradictions, and affected semantic IDs.

Return the approved basis identity, verified context, competing evidence, stale or missing sources, and the next retrieval actions. Treat search output as a lead, verify decision-critical claims at their source, and hand the package to `$basis-context-reconciler` before semantic expansion or design.
