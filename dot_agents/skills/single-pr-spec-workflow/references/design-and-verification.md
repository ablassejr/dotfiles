# Design and verification

## Diagnosis for a fix

Establish the expected outcome from a user statement, approved behavior, public contract, or applicable source. Compare it with the reported or observed result under concrete inputs, configuration, versions, and environmental conditions. Preserve sensitive data outside the record; use safe representative inputs.

Trace the symptom from the public entry point to the mechanism that could cause it. Check plausible alternative explanations, including caller behavior, invalid assumptions, dependency behavior, persisted state, concurrency, configuration, and evidence from later repair or reversion. A nearby code change is a hypothesis until the causal link is established.

Reproduce the issue only through authorized safe operations. Running an existing test, exercising a local public boundary, or using a disposable reproduction can provide useful baseline evidence. This skill does not require an implementation patch to validate the specification. When reproduction is unavailable, state which claims remain hypotheses and what specific observation would resolve them. If the gap could change the design materially, keep it on the research or human frontier.

Describe why the proposed correction removes the cause, what valid behavior it preserves, and which observable verification would distinguish it from an ineffective workaround. The specification does not prove that an unimplemented correction works.

## Behavioral contract

Use stable IDs when they aid traceability. A small change may need only a few requirements and scenarios; do not create empty records to satisfy an ID taxonomy.

For each requirement, retain its authorized source, rationale, human steward when known, expected externally observable behavior, affected public surface, and linked verification scenario. An inferred implementation preference is a proposal, not an approved requirement. An unknown source or steward is labeled rather than filled with a guessed person or policy.

Narrate the behavior in natural language. Introduce the actor, context, and initiating action; explain what the system observes and changes; include material choices, side effects, failures, and recovery where they happen; finish with what the user or caller can observe. Describe concurrency and repeated attempts where they affect the outcome. Avoid pseudocode that merely imitates source syntax.

For every added, removed, changed, or proposed public interface, show a realistic consumer-facing shape: a request and response, command, configuration, event, component use, data format, or user interaction. For a change, show before and after and explain compatibility, defaults, error behavior, and migration effects. Do not substitute private helper signatures or an inventory of internal classes for consumer impact. When there is no affected public interface, say so.

## Design coverage

Apply these lenses to the affected behavior. Include what matters, briefly explain material non-applicability when it could otherwise look like an omission, and do not create work solely because a row exists.

| Lens | Questions to resolve where relevant |
|---|---|
| Actors and boundaries | Who initiates the behavior, who owns it, who consumes the result, and which system or trust boundary is crossed? |
| State and data | What is created, read, changed, retained, or removed; which invariants apply; and what is durable or transient? |
| Concurrency and retries | What happens with simultaneous, duplicate, delayed, repeated, or partially completed operations? Where does idempotency actually matter? |
| Failure and recovery | What can fail, what the user or caller sees, what persists, who retries, and how the system recovers or compensates? |
| Compatibility | How existing callers, data, configuration, versions, and defaults behave during and after the change? |
| Security and permissions | Which existing authority checks, sensitive data boundaries, or abuse cases the change affects? |
| Migration and rollout | What compatibility window, deployment order, operational action, and rollback or restoration are needed for this PR? |
| User experience | How meaningful states, feedback, errors, recovery, and applicable accessibility behavior appear to the user? |
| Performance and cost | Which evidenced constraints or user-approved targets apply, and what remains unmeasured? |
| Observability | What existing or proposed signals establish the intended outcome and meaningful failures without exposing sensitive data? |

Do not invent a timeout, throughput threshold, retention period, new permission model, compatibility promise, or mandatory migration because it is familiar. Distinguish preserving an existing contract from proposing a new one. Use a material question when the choice belongs to the user.

## Minimum sufficient implementation proposal

Tie the proposal to the observed baseline and evidence-backed source locations. Identify the behavior owner, entry points, affected files and symbols, integration seams, existing mechanisms to reuse, obsolete responsibilities to remove, and necessary data or configuration changes. Tentative targets remain labeled as tentative.

Explain why deletion alone, an existing mechanism, or a simpler correction is sufficient or insufficient. Record material alternatives and consequences, including conceptual complexity, public API and dependency changes, operational risk, migration effort, and reversibility. Do not enumerate implausible options merely to favor the preferred design.

Estimate scope only when grounded in actual source and the proposed contract. Explain uncertainty and use `UNKNOWN` for unsupported numeric values. A high-level estimate is not committed code mass. If an approved managed accounting contract applies, hand off its exact current budget and planning evidence rather than inventing a new calculation or weakening a requirement.

Order the work within one PR by its real dependencies: the relevant contract and test harness, implementation changes, seam integration, migration where needed, and verification. This is a proposal for the later executor. It does not authorize code edits, run migrations, or open a PR during specification.

Identify other work only as a declared prerequisite, an explicit user-approved non-goal, or a separate scope choice. Do not hide a required second code change in a “later cleanup” item. A reviewer should be able to see why this PR is complete and independently useful.

## Behavioral verification plan

Build a compact matrix that maps the affected requirements and meaningful scenarios to expected observations and stable boundaries. Record existing relevant coverage, missing or unsuitable coverage, the planned check, required environment or fixture, and whether any check has actually run.

Plan at least one end-to-end test for each affected feature and integration coverage across each affected component, service, or external seam. A single test can cover multiple contracts when it observes them meaningfully. This is not a requirement for redundant suites or an arbitrary test count.

Inspect all request-relevant existing tests. Identify assertions against private helpers, internal state, internal call order/counts, source text, or incidental data structures. The handoff specifies the in-scope replacement at an observable boundary while preserving the intended behavioral coverage. Leave unrelated tests out of scope.

Assert intended positive outcomes through returned values, rendered behavior, persisted state, emitted events, documented errors, or external protocol behavior. Negative assertions belong where absence itself is the declared observable contract. Fake only real external or nondeterministic boundaries. Do not mock the internal worker or helper whose behavior is under test.

For a fix, identify the missing observable contract that allowed the defect and plan coverage of that contract's meaningful cases. Do not add a one-off test tied to the incident's internal mechanism. When the current harness has no stable boundary, propose the smallest boundary or harness improvement and include its scope in the one-PR assessment.

Cover applicable successful, invalid-input, failure, partial-effect, recovery, concurrency, idempotency, compatibility, and permission paths. Use the smallest nonredundant set that covers the enumerated affected behavior. “Complete” means coverage of that behavior matrix, not 100 percent line, branch, function, or private implementation coverage.

Keep three evidence states distinct: a proposed test, an existing test inspected, and a check actually executed with a result. Record observed baseline failures honestly. Do not call a planned test passing, claim provider behavior from a fake, or call a unit test end-to-end because it has that filename.

When a relevant behavior cannot be exercised, state the uncovered contract, why, its consequence for confidence, and the next observable verification. Distinguish a release or execution prerequisite from a material unknown that prevents approval of the design.

## Handoff readiness

Check the proposed behavior against every authorized requirement and the scope rationale. Confirm that affected interfaces, data and compatibility consequences, material failure and recovery paths, evidence limits, and verification requirements are visible. Resolve contradictions between the narrative, contract examples, implementation proposal, visuals, and tests.

The plan must be understandable to an executor who has not seen the conversation. It names the first action, source baseline, files or surfaces to inspect, allowed implementation judgment, escalation conditions, planned verification, existing blockers, and the specification revision it implements.

This is design readiness. It does not prove that code builds, tests pass after implementation, a deployment succeeds, an external provider is accessible, or production behavior matches the proposal.
