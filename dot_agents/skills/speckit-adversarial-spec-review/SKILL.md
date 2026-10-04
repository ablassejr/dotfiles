---
name: speckit-adversarial-spec-review
description: Attack a Spec Kit semantic specification from fresh context for contradictions, omissions, hidden assumptions, failure modes, weak evidence, missing ownership, and unjustified complexity.
---

# Spec Kit adversarial specification review

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Invoke `$adversarial-specification-review` in fresh context with the candidate specification, manifest, evidence summary, decisions, and unresolved items. Do not inherit the drafting agent's conclusion as a premise.

Classify each finding as `BLOCKER`, `MATERIAL_HITL_DECISION`, `AGENT_REPAIR`, or `NONBLOCKING_OBSERVATION`. Tie the finding to stable semantic IDs and concrete evidence, then route it to the earliest workflow stage that can repair it.

Record findings once in the owning review record. Generate `adversarial-review.md` as an internal temporary view only when it supports the current review, and register it in provenance. Return unresolved material findings, affected approvals, and the minimum downstream checks that must run again without copying the specification into the review.
