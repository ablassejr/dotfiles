---
name: adversarial-implementation-review
description: Attack an aligned implementation proposal from fresh context for contract, lifecycle, security, failure, recovery, evidence, and needless-complexity defects before execution.
---

# Adversarial implementation review

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run after first-principles implementation alignment and the corresponding independent Code Mass Auditor pass. Before execution, attack the proposal and its `CODE_MASS_TARGETED` planning result. After implementation, attack the committed result and its measured audit before the final Net Addition Gate. Give a separate fresh-context reviewer the approved basis, reconciliation, Code Mass Opportunity Map, deletion Grounding Packets, Code Mass Contract and audit, recorded decisions, implementation proposal or committed result, affected public contracts, seams, failure and recovery behavior, security boundaries, observability, and planned or completed behavioral verification. Do not provide the drafting conversation or tell the reviewer what defect to find.

Try to disprove the proposal with concrete counterexamples. Look for goal drift, a hidden implementation premise, missed lifecycle states, inconsistent public contracts, unsafe concurrency, partial failure without recovery, migration or compatibility gaps, security-boundary errors, non-observable success claims, absent end-to-end behavior, unverified external seams, and complexity that does not follow from the basis.

Attack every addition: search for existing behavior, unnecessary abstraction, responsible composition or reuse, second authorities, dependency laundering, speculative cases, and a smaller correct state space. Attack every deletion: search for compatibility behavior, implicit consumers, test erosion, denser or less comprehensible code, lost error handling or observability, relocation, hidden metaprogramming or configuration, and externalized maintenance burden.

Classify each removal finding as `VALID_REMOVAL`, `UNSAFE_REMOVAL`, `REMOVAL_REQUIRES_REPLACEMENT`, `REMOVAL_CREDIT_INVALID`, or `REMOVAL_PROVENANCE_UNKNOWN`. Only a valid removal and a behaviorally verified replacement retain credit. Route unknown provenance to `$ground-me` and invalid measurement to `$code-mass-auditor`.

Each finding names its consequence, affected basis and decision IDs, evidence, concrete counterexample, earliest repair stage, approvals invalidated by the repair, and whether code-mass credit changes. Route a false basis premise to intake, a factual gap to context loading, unknown provenance to Ground Me, a choice to the decision frontier, and a local proposal defect to implementation design. Return `NO_BLOCKERS` only when no material finding remains. A clean review is evidence for the Net Addition Gate; it is not human approval or permission to implement.
