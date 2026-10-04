---
name: first-principles-specification
description: Expand an approved pre-context First-Principles Basis and reconciled evidence into an epic semantic kernel, with stable IDs, falsifiable claims, explicit assumptions, and human-owned value decisions.
---

# First-principles specification

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Require the exact human-approved basis version, post-basis current-state map, and basis-context reconciliation. This skill does not replace `$first-principles-intake` and must not create the initial basis after implementation context has been loaded. Work in the active Spec Kit feature directory and preserve its temporary status. Read the epic manifest first. Create stable IDs before other artifacts cite a record.

Reuse the approved basis without another intake interview. Keep its intent in the basis and reference it instead of drafting another intent document. Begin from the basis's desired state, underlying problem, irreducible new behavior, expected simplification, minimum sufficient change, invariants, hard constraints, forbidden tradeoffs, non-goals, success evidence, assumptions, and unresolved points. Separate direct observations from interpretations. Before solution brainstorming, create plausible alternative frames by varying the affected actor, desired outcome, central obstacle, and system boundary. Compare what each frame reveals, excludes, and assumes, then select a provisional frame through the existing evidence and human-decision boundary. Explain the causal mechanism instead of merely naming symptoms. Record goals and measurable outcomes, principles, invariants, reconciled constraints, non-goals, actors and decision rights, assumptions, unknowns, falsification conditions, and exact links back to the basis version.

Use these ID families:

```text
FRAME-### GOAL-###       PRINCIPLE-###  INVARIANT-###
ACTOR-### REQ-###        SCENARIO-###   CONSTRAINT-###
DECISION-### RISK-###    EVIDENCE-###   VIEW-###
QUESTION-###
```

Do not manufacture a requirement because a familiar implementation usually has one. Before a proposed requirement or constraint becomes current, challenge it through `$framed-engineering-sequence`. Each survivor identifies its authoritative source, rationale, and current named human steward; an external authority remains the source even though a person owns re-evaluation. Trace every proposed requirement to the provisional frame and a stated goal, first principle, verified constraint, or human decision. Record material candidates as retained, deleted, or restored with their evidence instead of using the ten-percent add-back heuristic as a quota. Mark inferred claims as proposals and factual claims without evidence as unknowns.

When facts are missing, invoke `$specification-research-loop`. When a choice depends on values, priority, acceptable risk, or intended product behavior, add it to `$decision-frontier-manager`; only unresolved material human choices reach `$human-decision-loop`, with optional `$ground-me`. State the consequence and why the answer is needed now; facts and routine choices covered by approved intent stay with the agent. Do not settle it for the user. When evidence changes the basis, create and approve a successor version rather than editing history. After updates, give a fresh agent the bounded specification and use the first-principles alignment contract in `$epic-spec-workflow`.

Update the owning semantic records and return their references with the decision-relevant changes and remaining blockers. Keep frames, trace links, challenge outcomes, counterexamples, and the frontier as supporting records or generated views; do not produce a parallel narrative for each. Do not publish to an external documentation or issue service from this skill.
