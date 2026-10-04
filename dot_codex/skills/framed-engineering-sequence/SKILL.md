---
name: framed-engineering-sequence
description: Apply the framework's evidence-led, re-entrant framing and engineering sequence when defining epic semantics, compiling delivery plans, designing implementation tickets, or reconciling completed work.
---

# Framed Engineering Sequence

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Use this skill whenever an epic, plan, ticket, or reconciliation decision could add, retain, remove, simplify, accelerate, or automate part of the system or its delivery process.

## Operating rule

Treat this sequence as a reusable reasoning order, not as a rigid phase gate. Start with a provisional frame, work through the engineering steps in order, and return to the earliest affected step whenever evidence changes the problem, a requirement, or the system boundary. Reopen only decisions and checks that depend on the changed evidence. Do not use the sequence to invent acceptance criteria, restrictions, counts, or timeboxes.

Apply it at the level currently being designed:

- Epic semantics use it to define the problem, requirements, constraints, and desired outcomes.
- Delivery planning uses it to shape milestones, issues, dependencies, handoffs, and verification work.
- Ticket design and implementation use it to choose the smallest coherent behavior and implementation that satisfies the approved contract.
- Reconciliation uses it to compare delivered behavior with approved semantics and remove, restore, or revise work in light of current evidence.

## Sequence

### Framestorm provisionally

Before generating solutions, separate observations and evidence from interpretation. Develop plausible alternative ways to understand the problem by varying the affected actor, desired outcome, obstacle, and system boundary. Compare what each frame reveals, excludes, assumes, and would cause the team to optimize.

Select a provisional frame that best fits the available evidence and authority. The frame remains open to revision: research, prototypes, delivery evidence, and operational outcomes can require returning here. Framestorming is a deliberate pause before solution brainstorming, not a one-way stage that prevents problem and solution understanding from co-evolving.

Record the selected frame, material alternatives, supporting evidence, assumptions, and unresolved questions in the semantic specification or the existing manifest `decision_log` and `evidence_ledger`.

### Challenge requirements

Before deleting or designing anything, challenge every proposed requirement and constraint. A surviving requirement or constraint identifies:

- the authoritative source that imposes or approves it;
- the rationale that connects it to the selected frame and desired outcome; and
- a current named human steward who can explain its continued relevance and coordinate re-evaluation.

The named steward does not replace the authority of law, regulation, policy, contract, approved product intent, or another external source. Preserve the distinction between who owns re-evaluation and what authoritatively requires the behavior.

Resolve unsupported inherited requirements by seeking their source and rationale, narrowing them to what the evidence supports, or making their status explicit for an authorized decision. Do not silently turn an unverified assumption into a requirement.

Record the challenge outcome and its evidence in the semantic specification or existing manifest logs. Reconciliation refreshes the steward and checks whether the source and rationale remain current.

### Delete the part or process

Challenge every requirement, constraint, component, process step, handoff, artifact, dependency, and automation that survives framing and requirement review. Classify each material candidate as:

- value-producing work needed for the approved outcome;
- essential non-value-producing work required by an authoritative constraint or a necessary control; or
- waste that can be removed.

Trace material outcomes as `retained`, `deleted`, or `restored`, including the reason, authority, evidence, affected consumers, and recovery path when one is material. Use bounded, reversible experiments when deletion consequences are uncertain. Restore a deleted item when evidence shows that it is necessary; restoration is feedback that the deletion test worked, not failure.

The claim that deletion is insufficient unless some items are later added back is a qualitative pressure test against additive bias. The quoted ten-percent figure is not a quota, target, KPI, acceptance criterion, or universal measure. Never delete an approved safety, security, legal, regulatory, accessibility, audit, data-protection, or recovery control without evidence and the competent authority required to change it.

Use the existing semantic records and manifest `decision_log` and `evidence_ledger`; do not add a schema field merely to represent this classification.

### Simplify or optimize the surviving system

Simplify only after unsupported work has been challenged or removed. Evaluate the whole system against its approved outcome rather than improving an isolated component metric. Prefer fewer states, seams, dependencies, handoffs, special cases, and recovery modes when they preserve the required behavior and controls.

Optimize only a part that still needs to exist. Record material tradeoffs in the durable decision record, including any local improvement that would worsen system-level behavior, operability, cost, risk, or recovery.

### Accelerate the learning cycle

After the direction and surviving design are sound, divide work into the smallest independently useful and verifiable batches supported by the approved semantics. Shorten the path from a change to trustworthy feedback, and keep dependencies and handoffs explicit.

Judge acceleration with both delivery flow and operational quality in view. Observe stability, failure, recovery, and rework alongside throughput or elapsed time. Faster output is not progress when it increases avoidable failure or advances the wrong frame.

Do not create an arbitrary batch-size target, velocity target, or timebox. Choose batch boundaries from observable behavior, dependency safety, and the evidence needed for the next decision.

### Automate stable execution last

Automate outcome-producing or process-executing work only after its purpose, requirement, necessity, design, and feedback path are understood and sufficiently stable. Preserve an observable failure mode, a recovery path, and the evidence needed to decide whether the automation remains beneficial.

This ordering does not postpone engineering guardrails. Automate tests, builds, security checks, traceability validation, reproducible evidence capture, and publication readback as early as they provide reliable feedback. These guardrails help test and govern the sequence; they are distinct from prematurely automating an unstable product or delivery process.

When new evidence invalidates an automation's premise, stop optimizing it and return to the earliest affected step. When that evidence shows an active automation violating an authoritative control, contain the affected execution through the system's existing incident and authority path while the dependent decisions are reopened. The correct outcome can be simplification, partial manual execution while learning, or deletion.

## Durable record contract

Use the framework's existing records rather than changing its schemas or CLI:

- The semantic specification holds the provisional frame, authoritative requirements and constraints, desired outcomes, assumptions, questions, and evidence-backed decisions.
- The manifest `decision_log` holds material frame selection, requirement challenge, retention, deletion, restoration, simplification, cycle, and automation decisions.
- The manifest `evidence_ledger` links those decisions to current evidence and distinguishes verified facts from assumptions, proposals, and unresolved choices.
- The implementation-design record applies the same sequence at ticket scope and identifies the observable behavior, affected seams, smallest useful batch, verification, side effects, recovery, and any automation decision.

Keep the record proportional to the decision. Do not duplicate the same narrative across artifacts, and do not move authority or dependency truth into issue-body prose when the framework assigns it to a native system or a different authoritative artifact.

## Output contract

Work produced with this skill makes the following clear without relying on private reasoning:

- the selected provisional frame and the material alternatives considered;
- which requirements and constraints survived, with each authoritative source, rationale, and current named human steward;
- which material parts or processes were retained, deleted, or restored, and the evidence and authority for each outcome;
- how the surviving design was simplified or optimized at the system level;
- how the plan or implementation shortens trustworthy feedback while observing stability and rework;
- which outcome or process automation is justified as stable, which guardrail automation begins early, and what failure and recovery paths remain;
- what new evidence would send the work back to an earlier step; and
- where each durable decision and its evidence are recorded.

If a point is unresolved, label it as an assumption, proposal, or open decision and route it to the framework's existing authority boundary. Do not present it as implemented, verified, or approved.
