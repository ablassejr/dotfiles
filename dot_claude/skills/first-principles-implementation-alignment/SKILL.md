---
name: first-principles-implementation-alignment
description: Review an implementation proposal from fresh context against the approved First-Principles Basis and reconciled constraints before code work begins.
---

# First-principles implementation alignment

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run after the implementation decision frontier is resolved and before adversarial implementation review. Give a fresh-context agent only the approved basis and its lineage, reconciled constraints, recorded human decisions, proposed observable behavior and public contracts, failure and recovery behavior, and source-linked evidence needed to assess alignment. Do not give it the drafting discussion or the preferred conclusion.

Test whether the proposal produces the desired state, addresses the underlying problem, stays within the minimum sufficient change, preserves every invariant and hard constraint, respects forbidden tradeoffs and non-goals, and can produce the approved success evidence. Challenge implementation details that have been promoted into requirements and detect a proposal that merely preserves current structure without a basis-linked reason.

Establish whether every added responsibility is required by the approved desired state, whether removal or replacement can produce the outcome, whether two mechanisms own the same fact or behavior, whether every abstraction represents a real variability boundary, and whether the completed system is conceptually smaller. Compare authority count and conceptual complexity before and after. Verify the proposal's expected code-mass ratio without treating fewer lines as a substitute for correctness or comprehensibility.

Return `ALIGNED`, `IMPLEMENTATION_REVISION_REQUIRED`, or `HUMAN_DECISION_REQUIRED`. Include `addition_necessity` with `PROVEN` or `NOT_PROVEN`, `subtractive_design` with status and missed opportunities, authority counts before and after, conceptual-complexity descriptions before and after, and the expected code-mass ratio and `PASS` or `DEFICIT` status. A parallel mechanism that can responsibly replace the old one returns `IMPLEMENTATION_REVISION_REQUIRED`.

Every repair or decision cites the affected basis and decision IDs, the concrete mismatch, observable consequence, and earliest stage that can correct it. Do not approve a repair invented by the reviewer. A material basis error returns to `$first-principles-intake`; a missing fact returns to post-basis context; a current-state rationale gap offers `$ground-me`; an implementation choice returns to the decision frontier.
