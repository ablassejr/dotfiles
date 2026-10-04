---
name: human-decision-loop
description: Run the one-question human decision loop for a design, program, or issue in the current project, including open-ended answers, evidence-based assessment, reconsideration, and a Ground Me branch that returns to the same decision.
---

# Human decision loop

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Use the authorized interaction surface for this scope, including the current conversation, a selected document, or an issue. Bind the answer to the actual question, revision, and reviewed content under [workflow records](../epic-spec-workflow/references/workflow-records.md). If an existing orchestrator owns the decision, also satisfy its actual user-task binding and completion contract. Without one, record the explicit answer in the scope's governing record; do not require a tracker or create engine identities. Follow [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md).

Receive one unresolved human choice selected by `$decision-frontier-manager`. Explain the consequential choice, what the answer unlocks, and why it needs the user’s judgment now, then invite an open-ended answer. A subskill completion or stage change is not itself a reason for a question. Supply useful context without requiring the human to choose from a menu or confirm an unanticipated but clear answer.

After the human answers, run the [decision assessment](../epic-spec-workflow/references/open-decisions.md). Preserve the exact words and analyze their consequences against the approved basis, current evidence, and accepted decisions. A clean assessment records the choice automatically. Material disagreement, conflicts, decision-changing evidence, or consequential ambiguity produce a concise explanation and suggested change at the current decision. Keep the choice unresolved until that concern has a human disposition; an explicit decision to retain the choice is respected and recorded with its rationale. Reassess revised answers without an extra continuation prompt.

When the human chooses `Ground me`, suspend the question and invoke `$ground-me` with the decision, approved basis, current-state map, reconciliation, target, and source references. After the Grounding Packet is validated, present understanding alignment with the optional explicit combined answer from [approval economy](../epic-spec-workflow/references/approval-economy.md). If the human requests deeper grounding, continue without advancing the frontier. The parent assesses an explicit combined answer only while its packet and question bindings still match. Otherwise, revise the evidence and options as necessary and present the current unresolved decision. Only `QUESTION_INVALIDATED` may remove that question without an answer; it causes context and frontier recomputation.

Reference the existing approved basis and record the grounding conclusion, evidence, material option consequences, and decision once in their authoritative records. Update only the relevant section of the existing design proposal. Issue descriptions and comments carry the scoped behavioral consequence and only the optional proposal link; detailed sources belong in the proposal or internal evidence. Keep dependency and escrow truth in supported native relations or the selected plan's structured graph, with the provider's capability limits explicit.
