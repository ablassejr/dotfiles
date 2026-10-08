---
name: post-basis-context-loader
description: Load repository and organizational evidence only after a First-Principles Basis has explicit human approval; use immediately after the pre-context gate.
---

# Post-basis context loader

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Accept an exact First-Principles Basis version and refuse implementation-context retrieval until `$first-principles-intake` has validated it with explicit human approval. The original approved record may cover an unchanged program or ticket when the runtime verifies [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) evidence. A missing, pending, malformed, or superseded basis keeps the gate closed. This skill never creates or approves a basis.

After the gate passes, resolve repository identity, exact baseline, target branch, worktree state, scope references, approved specification revision, and available indexes. Follow [shared tool routing](references/bundled/epic-spec-workflow/references/tool-routing.md): use CodeGraph before direct structural search when the repository owns an index, then `claude-context` for semantic retrieval, and verify decisive evidence in source. Follow stricter explicit session ordering when present. Do not initialize CodeGraph automatically.

Continue through Git lineage, the repository host's pull requests and reviews, project issues and supported relations or the governing dependency graph, approved specification records and ADRs, exact-version documentation through `docs-mcp-server`, and external primary-source research only for unresolved external facts. Maintain the shared version/environment capability record for nontrivial or version-sensitive CLI use, subject to stricter explicit session rules.

Produce an immutable Context Snapshot as internal evidence pinned to repository identity, exact baseline, worktree state, and source revisions. Surface only decision-relevant findings in the owning proposal or evidence section, with hosted source permalinks; the snapshot is not another required review document. Its current-state map contains the target behavior, symbols, callers, tests, contracts, schemas, ownership, runtime or data flow, dependencies, relevant history, semantic sources, external forces, contradictions, unknowns, and source references. Record what exists without converting it into a requirement or constraint. Keep raw extraction, indexes, scratch notes, and unapproved reconstructions outside the implementation repository and ephemeral.

Pass the approved basis and current-state map to `$basis-context-reconciler`. Do not ask implementation decisions or propose a solution from this skill.
