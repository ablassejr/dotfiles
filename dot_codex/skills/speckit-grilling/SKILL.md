---
name: speckit-grilling
description: Build the unresolved decision graph for a Spec Kit epic and ask only the currently unblocked human-owned product, value, risk, or irreversible decisions.
---

# Spec Kit grilling

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Invoke `$decision-frontier-manager` and invoke `$grilling` only if an unresolved human choice remains, with the approved First-Principles Basis, reconciled current-state map, semantic records, evidence ledger, contradiction record, and gap matrix. Resolve factual questions through research before asking the human.

Present one currently unblocked material decision. Explain the context in plain language, invite an answer in the human's own words, and offer `Ground me`. Assess the actual answer and surface material concerns with a suggested change before recording it. Grounding returns to the same unresolved decision unless it invalidates the premise.

Record the answer, steward, rationale, affected basis and semantic IDs, and invalidated downstream work once in the existing decision log. Generate `hitl-decisions.md` only as an internal view when needed; publish the decision through its owning shared record rather than a second decision narrative. Recompute the frontier after each answer. An unanswered material decision remains open.
