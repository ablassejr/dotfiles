# <Issue, fix, or feature>: single-PR specification

Use this outline proportionally. Replace placeholders with actual evidence or explicit unknowns. Combine short sections, omit irrelevant detail, and link shared records instead of duplicating them. Template prompts are not product requirements or proof of approval.

## Identity and current status

Work reference: <local identifier or existing issue>.
Specification revision: <current revision>.
Planning status: <current activity, decision wait, or result label>.
Authority mode: <standalone request or actual managed binding>.
Source baseline: <repository/checkout/revision and relevant dirty changes>.
Related artifacts: <handoff, actual source approvals, evidence, visuals>.

## The problem and proposed outcome

Explain the affected actor, what happens today, why it matters, and the one useful outcome proposed. Separate reported symptoms, verified observations, causal hypotheses, and intended behavior. A supervisor arriving without the conversation should understand the recommendation and the decision requested.

## First-principles basis and scope

State the desired state, underlying problem, irreducible behavior, simplification opportunity, minimum sufficient change, invariants, authoritative constraints, forbidden tradeoffs, user-approved non-goals, and success evidence that actually apply.

Record the source of this intent and any exact inherited approval. Explain material alternative frames, the provisional selected frame, and what evidence could change it. Preserve assumptions and unresolved choices as such.

Explain why this outcome fits one independently useful PR. Identify affected responsibilities, real dependencies, migration or release implications, and what would invalidate the scope hypothesis. Do not add a numeric gate or quietly exclude required work.

## Requirements and authority

| ID | Observable requirement or constraint | Authoritative source and approval state | Rationale | Human steward, if known | Verification |
|---|---|---|---|---|---|
| <stable reference> | <actual requirement> | <user statement, approved record, or applicable contract; label proposals> | <connection to the outcome> | <actual person or unknown> | <scenario reference> |

## Current behavior, cause, and evidence

Describe the current path through relevant entry points, callers, state, dependencies, side effects, failures, and observable outcomes. For a fix, include expected versus actual behavior, reproduction conditions and actual results, competing explanations, causal evidence, and any unverified hypothesis.

Explain how current context confirms, constrains, or contradicts intent. Keep expired constraints and unsupported inherited assumptions visible.

| Evidence ID | Source and applicable revision/date | Observation | Interpretation and uncertainty | Affected requirement or decision |
|---|---|---|---|---|
| <reference> | <precise source> | <what it establishes> | <limits, contradiction, or inference> | <references> |

## Proposed behavior — plain-English pseudocode

Explain the actor and initiating action in complete sentences. Walk through meaningful choices, state changes, integrations, side effects, concurrency, failures, and recovery in the order they affect the user or caller. End with the observable outcome. Distinguish proposed behavior from existing verified behavior.

## Public interface changes

Identify each added, removed, changed, or proposed public surface and its owning file or artifact. Show a realistic request/response, configuration, event, command, file format, component use, or user interaction. For a change, show before and after and explain defaults, compatibility, meaningful errors, and any required consumer action. If none applies, write `Public interface changes: none`.

## Minimal design and consequences

Explain the selected mechanism and its material alternatives. Record justified retention, deletion, reuse, simplification, and restoration, including behavior and consumer consequences. Label unknown deletion safety and proposed replacements honestly.

Describe applicable ownership, architecture, state/data, concurrency, security, compatibility, migration, rollout, rollback, observability, user-experience, performance, and cost consequences. Link detailed source targets and estimates in the handoff. Use only grounded estimates or explicit unknowns; preserve inherited accounting rules where they actually apply.

Include a visual when it improves understanding. Label observed and proposed states and retain actual rendering and access evidence where required.

## Decisions, grounding, and research readiness

| Decision or question | Exact human answer and actor, when present | Basis and evidence revision | Analysis or material concern | Current disposition |
|---|---|---|---|---|
| <stable question/reference> | <actual response or pending> | <binding> | <consequences and supported concerns> | <resolved, grounding, reconsideration, or waiting> |

Link any grounding packet and its actual understanding checkpoint. Preserve the distinction between understanding alignment and a decision answer. Record the current research gate result, its decisive evidence, and any remaining material question or inaccessible source.

## Behavioral verification matrix

| Requirement/scenario | Trigger and meaningful conditions | Expected observable result | Stable test boundary and integration seam | Existing coverage / planned change | Evidence state and execution dependency |
|---|---|---|---|---|---|
| <reference> | <representative input/context> | <public behavior> | <end-to-end or integration observation> | <relevant existing test or proposed coverage> | <planned, inspected, or actually run with result> |

Cover applicable success, failure, recovery, concurrency, compatibility, and permission paths without redundant tests. Record request-relevant tests whose implementation-coupled assertions need replacement. State uncovered behavior, why it cannot be tested, and the consequence for confidence.

## Review and remaining work

Record the actual reviewers or self-review limit, applicable review lenses, source package/revision, findings, evidence, repairs, and current outcome. Identify unresolved design decisions separately from later execution prerequisites. A review pass is not human approval or implementation verification.

## Final approval binding

Specification and handoff revision/content binding: <actual values>.
Relevant baseline, decision/evidence, and visual bindings: <actual values>.
Publication/readback, if required: <actual destination, fetched revision, and evidence>.
Approving actor and response reference: <actual response or pending>.
Approval scope and state: <exact current proposal; pending or actually approved>.

Do not fill an approval placeholder from expectation. A final change to the approved content requires the affected review and approval to be refreshed before `HANDOFF_READY`.
