---
name: subtractive-design-analyzer
description: Analyze approved, repository-grounded work for safe replacement, consolidation, simplification, and removal opportunities before implementation decisions or code-mass budgeting.
---

# Subtractive design analyzer

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run after the exact First-Principles Basis is approved, implementation context is loaded, and the basis-to-context reconciliation is current. Run before implementation questions, ticket design, or delivery-program compilation. The analysis finds unnecessary machinery; it does not treat deletion as an outcome by itself.

Read the approved basis, especially `irreducible_new_behavior`, `expected_simplification`, invariants, forbidden tradeoffs, and success evidence. Limit the search to the responsibility domain of the requested outcome. Use CodeGraph first when the repository owns an index, then `claude-context`, current source and tests, Git lineage, pull requests, the selected issue-tracker history, and authoritative specifications. Current code is evidence, not justification.

Search for duplicate implementation paths, superseded abstractions, compatibility branches whose constraints may have expired, dead or unreachable behavior, redundant adapters, parallel state representations, repeated validation or transformation, pass-through layers, one-implementation abstractions, temporary migrations, retireable feature flags, and repetitive tests. Treat configuration, generated code, dependencies, and external services as possible relocations of complexity rather than automatic reductions.

Produce one Code Mass Opportunity Map conforming to [the packaged schema](schemas/code-mass-opportunity-map.schema.json). Every candidate names its responsibility, current symbols or paths, estimated normalized maintained SLOC, proposed action, evidence by source domain, affected behavior and tests, provenance classification and confidence, and one deletion-safety state:

- `SAFE`
- `SAFE_WITH_REPLACEMENT`
- `REQUIRES_GROUNDING`
- `BLOCKED_BY_CURRENT_CONSTRAINT`
- `BEHAVIOR_STILL_REQUIRED`
- `UNKNOWN`

Keep `REQUIRES_GROUNDING` and `UNKNOWN` candidates uncredited. Investigate only candidates that could materially improve the scoped design; defer unused hypotheses in the internal map rather than creating a user interview for every possible deletion. Use `Ground me` before relying on an uncertain candidate for removal credit. A candidate receives removal credit only after Ground Me confirms the understanding and records `VALIDATED` credit for `SAFE` or `SAFE_WITH_REPLACEMENT`. Keep blocked and required behavior visible without budgeting it as removal.

Reject opportunities that delete useful tests, weaken correctness, validation, typing, security, error handling, observability, operations, or comprehensibility; compress readable code; move behavior between files or systems; add opaque metaprogramming; launder code through a dependency; or use unrelated cleanup as an offset. Return `NO_SAFE_SUBTRACTION_FOUND` with the searched evidence when the domain contains no responsible deletion. Never manufacture credit to satisfy the ratio.

Finish with the opportunity-map ID, basis reference, repository baseline, responsibility domain, candidate totals by safety state, candidates that require Ground Me, and the exact evidence gaps that prevent a confident recommendation.
