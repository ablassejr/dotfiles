---
name: adversarial-specification-review
description: Review an epic specification from fresh context for goal drift, contradictions, unsupported claims, missing states, security and recovery gaps, non-observable contracts, and needless complexity, then route each defect to the earliest repair stage.
---

# Adversarial specification review

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Review a bounded package containing approved basis lineage, current semantic records, evidence ledger, accepted decisions, relevant source artifacts, and current formal/visual models. Do not receive the author's hidden reasoning, preferred solution, drafting conversation, or unapproved conclusions. Resolve missing explanations through cited source evidence. Apply [the shared review contract](../epic-spec-workflow/references/research-and-review.md); semantic, provenance, architecture, implementation, and integration reviews retain distinct purposes and contexts.

Try to disprove the specification. Construct concrete counterexamples. Look for a favored frame that escaped comparison, requirements or constraints without an authoritative source, rationale, or current named human steward, unjustified retention, deletion that discards an essential control, local optimization of a part or process that should not exist, acceleration before direction and design are sound, outcome automation before the process is understood and stable, contradictory records, assumptions presented as facts, missing actors or lifecycle states, unowned decisions, unsafe failure or recovery behavior, security boundary errors, irreversible actions without recovery, acceptance conditions that cannot be observed, visual claims without semantic IDs, and complexity with no causal benefit.

Each finding contains:

- `BLOCKER`, `MATERIAL_HITL_DECISION`, `AGENT_REPAIR`, or `NONBLOCKING_OBSERVATION`, tied to consequence;
- the violated goal, principle, requirement, or approved quality condition;
- the affected stable IDs;
- the concrete counterexample or contradictory evidence;
- the earliest repair stage or `$framed-engineering-sequence` step: framestorming, requirement challenge, deletion, simplification, acceleration, automation, semantic kernel, research, human decision, visual projection, specification publication, implementation compilation, or ticket design;
- downstream artifacts invalidated and whether each existing approval remains valid;
- a specific repair question or disproof condition.

Combine repeated findings about the same defect into one actionable finding at its earliest owner. Keep repaired findings in verification history and present unresolved consequential findings first; do not make the user read each reviewer’s full report. Return `pass` only when no material finding remains. A pass is review evidence, not human approval. Do not rewrite the specification in the review response. The owning workflow applies repairs and reruns only affected checks.

Follow [approval economy](../epic-spec-workflow/references/approval-economy.md) for the scope’s evidence-bound automatic routes, combined final visual/design review, targeted revision, and existing authorization. Automatic review records remain distinct from human approval.
