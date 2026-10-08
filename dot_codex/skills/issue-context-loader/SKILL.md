---
name: issue-context-loader
description: Load and verify authoritative context for one implementation issue or work item after its First-Principles Basis is approved.
---

# Issue context loader

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Use `$post-basis-context-loader` at ticket scope. Require the exact ticket-level First-Principles Basis version and validate explicit human approval before fetching implementation context. A missing, pending, malformed, or superseded basis keeps this stage closed.

After the basis gate passes, fetch the exact work item, its actual project and owner, supported relations or governing dependency graph, approved specification revision, semantic IDs, repository baseline, linked implementation-design record, relevant ADRs, current code, tests, and history. Verify unresolved incoming `blocks` relations before continuing. Invoke `claude-context` before repository investigation. When the repository owns a `.codegraph` index, use CodeGraph for structural relationships, then retrieve semantic context and exact-version documentation. Use external research only for unresolved external facts.

Return the approved basis identity, resolved source identities and revisions, applicable semantic contracts, implementation surface, repository conventions, contradictions, stale inputs, and blockers. Hand that package to `$basis-context-reconciler`. Use the current project's selected sources under [workspace and destinations](references/bundled/epic-spec-workflow/references/workspace-and-destinations.md). Missing sources remain explicit gaps. Do not mutate the issue tracker or documentation store, create a design record, or begin implementation from this skill.
