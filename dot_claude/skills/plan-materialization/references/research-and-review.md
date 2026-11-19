# Research and review loop

## Evidence and decision records

Record each material claim once with a stable ID, source, owner, applicable version/date, retrieval time, decisive excerpt when needed, interpretation, confidence, contradictions, and affected semantic IDs. Use internal repository locations while investigating; team-facing evidence uses verified hosted permalinks. Generate a ledger, register, gap view, or dependency graph only for a distinct decision or verification need. Do not independently maintain overlapping accounts. Before publication these records are provisional; the approved release owns normalized semantics. Apply [review and artifact design](review-and-artifact-design.md) to the human-facing result.

Start from approved basis lineage, the pinned context snapshot, reconciliation, provisional frames, assumptions, and unknowns. Seek evidence that disconfirms the favored frame, challenges inherited requirements, or explains retention, deletion, and restoration. Apply [tool routing](tool-routing.md) and preserve secrets outside all records.

## Autonomous research gate

Return exactly one of `CONTINUE_RESEARCH`, `REQUEST_HITL`, `REVISE_FIRST_PRINCIPLES`, or `PROCEED`, with decisive evidence, affected IDs, blockers, and the next owning stage.

When evidence changes the desired state, problem, invariant, or basis, return `REVISE_FIRST_PRINCIPLES` and create a successor through intake. When a material factual gap has a credible accessible source, return `CONTINUE_RESEARCH`. When remaining progress needs a value judgment, risk acceptance, irreversible choice, or inaccessible privileged evidence, return `REQUEST_HITL` with its named owner and access or decision boundary. Exhausted access is not evidence sufficiency.

`PROCEED` requires every mandatory goal to have requirements; every surviving requirement to trace to a goal and approved basis; no conflict with an invariant or approved non-goal; sufficient applicable evidence for every blocking factual claim; and resolved or explicitly routed material contradictions. Each value judgment, risk acceptance, and irreversible choice has a named human owner. Each decision-critical unknown is resolved or on the human frontier. Another targeted search is unlikely to change a material decision. Record evidence for every condition without a weighted score or source-count shortcut.

`PROCEED` means factual research can stop. Blocking human choices or routed contradictions still prevent semantic review completion, approval, publication, and handoff. The next transition names and verifies its own prerequisites.

## Decision and understanding loop

Use `$decision-frontier-manager` to remove settled choices and factual gaps from the human frontier. When a material human choice remains, use `$human-decision-loop` to select that unblocked choice, present its basis and current condition, invite an open-ended answer, and offer `Ground me`. Assess the answer and its consequences through [open-ended decisions](open-decisions.md), retaining unknown estimates as `UNKNOWN`. Never ask the human to retrieve an accessible fact.

Question selection explains why the answer is needed now and what work it affects. First-principles approval does not trigger a second broad interview. A human answer is validated against the basis, semantic records, current evidence, accepted decisions, and ownership boundaries before it becomes an accepted decision with provenance. Recompute the frontier afterward. Ground Me performs its provenance investigation and separate human understanding checkpoint; confirmed understanding returns to the same unresolved choice. A disproved premise produces `QUESTION_INVALIDATED` and rebuilds affected questions without recording an answer.

## Independent review contexts

Reviewers receive a bounded package of approved basis lineage, current semantic records, evidence ledger, accepted decisions, relevant source artifacts, and current formal/visual models. They do not receive the authoring conversation, hidden reasoning, preferred solution, or unapproved conclusions. A missing explanation is retrieved from a cited source, not from the author's private rationale.

Semantic review challenges whether requirements follow from goals, whether evidence supports claims, whether goals conflict, and whether scope, failure, recovery, and abuse cases are sound. First-principles alignment also challenges unsupported or unowned constraints, unjustified retention, unsafe deletion, local optimization, premature acceleration or automation, and complexity without causal benefit.

Provenance review challenges whether intent is documented, later explanations are post-hoc, correlation is mistaken for causation, and historical constraints remain current. Architecture review separately challenges ownership, boundaries, coupling, authority, data flow, failure propagation, and deployment implications. It runs against the formal model before visual approval and publication.

Implementation review belongs to ticket scope and covers concurrency, retry, idempotency, data loss, security, migration, rollback, compatibility, tests, and parallel write conflicts. Integration/conformance review belongs after the relevant work is combined; it tests collective requirement coverage, interacting changes, and as-built drift. A generic final adversarial pass cannot substitute for these distinct evidence contexts.

## Finding and repair contract

Use `BLOCKER`, `MATERIAL_HITL_DECISION`, `AGENT_REPAIR`, or `NONBLOCKING_OBSERVATION`. Each finding states the violated goal, principle, requirement, or approved quality condition; affected stable IDs; evidence and consequence; earliest repair stage; downstream artifacts invalidated; validity of existing approvals; and a concrete disproof or repair question. Do not invent acceptance criteria while reviewing.

Combine findings about the same defect under one owning record, preserving each reviewer’s evidence. Repair agent-owned defects without sending the user the working reports. Present only unresolved material concerns and their decision implications, with optional shared evidence. Keep repaired findings as verification history and do not create an overlapping specification summary. Return pass only when material findings are resolved by the appropriate owner. A review pass is evidence, not human approval. Repair the earliest defective stage, recheck the finding, and rerun only affected downstream gates. Preserve unresolved disagreement rather than dismissing it through author confidence.
