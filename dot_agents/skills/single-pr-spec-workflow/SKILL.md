---
name: single-pr-spec-workflow
description: Create or resume a thorough specification and implementation handoff for one issue, bug fix, or feature expected to fit a single independently useful PR. Use for a plain-language request, linked issue, bounded change, or epic-spec depth at single-PR scope. Stops at approved specification and handoff; implementation is a separate invocation.
---

# Single-PR specification workflow

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


Turn one requested outcome into an approved, evidence-grounded specification and a concrete implementation handoff for one PR. Apply the reasoning depth of the epic specification workflow at the scale of the affected behavior. A short fix can need deep diagnosis; a long document does not establish completeness.

Accept a plain-language request, issue reference, reproduction, proposed feature, existing draft, or a bounded contribution from an approved epic. An existing ticket, epic, project, specification revision, or workflow engine is not a prerequisite for standalone use.

This skill ends at specification and handoff. It does not implement the change, create a PR, merge, deploy, or begin an implementation program. Preserve authorization from the conversation, but do not interpret approval of the specification as an instruction to execute it.

## Read the relevant contracts

- Read [scope and authority](references/scope-and-authority.md) at entry and resume. It defines the single-PR boundary, standalone and managed execution, approval reuse, and freshness.
- Read [research and decisions](references/research-and-decisions.md) before substantive investigation or a material decision. It includes the research gate and the complete Ground Me branch.
- Read [design and verification](references/design-and-verification.md) while diagnosing, specifying, and shaping the handoff.
- Read [review and handoff](references/review-and-handoff.md) before review, publication, approval, or final output.
- Use the [specification template](assets/specification-template.md) and [handoff template](assets/handoff-template.md) as adaptable artifact outlines. Merge them into one document when that improves readability; preserve the information and approval binding.

These contracts are self-contained for standalone work. When the request is already governed by the epic framework, load the currently installed `$epic-spec-workflow` and applicable ticket skills for its actual authority, adapters, schemas, and process definition. This skill does not create a new Camunda process type or bypass an existing gate.

## 1. Establish intent and the boundary

Read the request, attached materials, existing decisions, and applicable instructions before repository implementation context. State the affected actor, undesirable or missing behavior, desired observable outcome, why it matters, and what the user has actually authorized. Separate the symptom from the proposed explanation or implementation.

Capture a small first-principles basis: desired state, underlying problem, irreducible new behavior, expected simplification, minimum sufficient change, invariants, constraints, forbidden tradeoffs, explicit non-goals, success evidence, assumptions, and unresolved points. Include only applicable content. Every requirement or constraint identifies its source and rationale; record the human steward when known. An unknown steward remains unknown.

Reuse a clear statement of intent or an exact, still-valid approval already present in the conversation or authoritative record. Do not manufacture a new approval or ask the human to reconfirm unchanged intent. If a material goal, priority, risk, scope boundary, or constraint is missing, ask one open-ended question about that choice. An agent-proposed requirement remains a proposal until the human accepts it.

For an inherited epic contribution, identify the exact approved basis and requirement IDs that cover the issue. Keep their original meaning and authority. If the proposed outcome changes that meaning, record the mismatch and use the owning basis-revision route.

Make an initial single-PR hypothesis. Explain the one useful outcome, the expected responsibility boundary, and why it could be reviewed, integrated, and verified together. Do not use a guessed line limit, file count, point estimate, duration, or deletion quota as a gate. Recheck the hypothesis after diagnosis, design, and review.

## 2. Ground the current behavior

Follow the user's repository and CLI documentation rules. Invoke `claude-context` before codebase investigation when required, treat retrieved context as navigation, and verify decisive claims against current source. Retrieve current CLI documentation through `docs-mcp-server` before CLI use when required. A missing required capability remains a capability gap; do not silently substitute an unauthorized route.

Pin the repository and active checkout, commit or baseline revision, relevant uncommitted changes, issue revision, and document versions. Do not describe a dirty checkout as the clean commit. Preserve unrelated work and keep investigation artifacts outside the implementation tree unless the user chose it as the artifact destination.

Trace the affected behavior from its entry point through public contracts, state, dependencies, side effects, failure handling, and observable outcome. Inspect relevant implementation, callers, tests, configuration, documentation, and dependency versions. Follow adjacent seams only as far as necessary to understand this change and its consequences.

For a fix, establish expected behavior from an authoritative contract, capture the reported behavior and reproduction conditions, and investigate competing causal explanations. Distinguish a verified cause from a plausible hypothesis. Do not turn a workaround into the intended product behavior. Follow [the diagnosis contract](references/design-and-verification.md#diagnosis-for-a-fix).

Reconcile the observed system with the basis: identify confirming evidence, implementation constraints, contradictions, expired constraints, and irrelevant context. Current implementation establishes what happens; it does not establish what ought to happen. A contradiction that changes intended behavior returns to the affected human decision.

## 3. Frame, challenge, subtract, and simplify

Separate direct observations from interpretation. Consider material alternative frames by changing the actor, desired outcome, obstacle, or boundary. Select a provisional frame and record why it fits. Return to it when evidence changes the problem; do not manufacture alternatives merely to fill a template.

Challenge each proposed requirement and constraint against its authority, current rationale, and desired outcome. Preserve explicit user requirements unless the competent human changes them. Record unsupported assumptions as such rather than inheriting them as obligations.

Consider deletion, correction of an existing mechanism, and reuse before introducing another mechanism. For material candidates, explain what is retained, removed, or restored; affected behavior and consumers; evidence of current necessity; and recovery implications. Investigate uncertain historical purpose through Ground Me. A lack of observed usage does not establish safe deletion.

Simplify the surviving design across the whole affected flow. Consider states, seams, ownership, dependencies, special cases, failure propagation, recovery, and comprehension. A local improvement that worsens the approved outcome is not sufficient justification.

Keep the learning batch to the requested single PR. Use early tests, builds, traceability checks, and evidence capture where they provide reliable feedback. Propose automation of product or delivery work only when its purpose and behavior are understood; do not add automation merely because the task is repetitive.

This reasoning sequence is re-entrant. Record material decisions in the specification, and reopen only dependent work when a premise changes. It creates no additional product acceptance criteria.

## 4. Research and resolve the decision frontier

Maintain a compact evidence ledger with stable references, relevant source/version, what was observed, interpretation, confidence or uncertainty, contradictions, and the requirements or decisions affected. Link decisive evidence rather than copying whole sources. Search for evidence that could disprove the favored design.

Resolve factual questions through accessible authorized sources. Use repository context and history for local behavior, exact-version official documentation for platform contracts, and primary external sources when needed. Do not ask the human to retrieve an accessible fact or decide an empirical question the agent can investigate.

Apply the nonweighted research gate in [research and decisions](references/research-and-decisions.md). Return `CONTINUE_RESEARCH`, `REQUEST_HITL`, `REVISE_FIRST_PRINCIPLES`, or `PROCEED`, with the decisive evidence and next action. `PROCEED` closes factual research; it does not close unresolved human decisions or approve the specification.

Ask one currently unblocked material question at a time. Explain the consequence and invite an answer in the human's own words. Offer Ground Me. Alternatives and a recommendation may help but do not limit valid answers. Resolve routine implementation-detail proposals through evidence and judgment without inventing another approval checkpoint.

Assess the actual answer against the approved basis, evidence, prior decisions, and the human's priorities. Continue automatically when it has no material concern. When there is a conflict, decision-changing evidence, reasoned disagreement, or consequential ambiguity, explain the concern and suggest a concrete change. Preserve the human's authority to retain or revise the choice. Do not repeat an acknowledged concern without materially new evidence.

When the human asks for grounding, suspend the affected choice and follow the full provenance and understanding loop. Understanding alone is not a decision. An explicit combined understanding-and-answer response can resolve both only while the question and evidence still match. Deeper grounding keeps the choice unresolved. A disproved premise rebuilds the affected frontier without applying the old answer.

## 5. Specify the behavior and shape one PR

Write the chosen behavior in complete, plain-English paragraphs from the initiating action through the observable outcome. Explain material alternatives, concurrency, failures, and recovery where they occur. Distinguish verified current behavior, the proposed design, assumptions, and unresolved choices throughout.

Trace each requirement to an authorized goal or constraint and to observable verification. Preserve user wording where its exact meaning matters. Do not invent acceptance criteria, quality thresholds, rollout gates, retention periods, performance targets, mandatory roles, or exclusions because they are common in similar designs.

Describe affected public interfaces with realistic consumer-facing examples. For changed interfaces show before and after, defaults, compatibility, and meaningful failure behavior. Include data, lifecycle, permissions, migrations, deployment ordering, rollback, and observability to the extent the affected behavior requires them. Use the [applicability lens](references/design-and-verification.md#design-coverage) to find omissions, not to add scope.

Prepare a repository-grounded implementation proposal: entry points, affected files and symbols, responsibilities, reuse and deletion opportunities, relevant contracts, the implementation order within one PR, and the reasons the selected approach is sufficient. Cite the baseline. Distinguish evidence-backed targets from tentative targets and unknown estimates. Keep detailed implementation material in the linked design or handoff, not in an issue body that excludes implementation details.

When an inherited issue has an approved Code Mass Contract, preserve its budgeting, subtraction, exception, and planning-audit rules through the active ticket workflow. A standalone issue gets a reasoned complexity and size assessment, not an invented numeric ratio. Planned deletion is not committed or verified removal credit.

Build the affected behavior matrix and verification plan. Plan end-to-end coverage at the user or system boundary for each feature and integration coverage for affected seams. Inspect the request-relevant existing tests for implementation coupling; identify the in-scope rewrites needed to assert behavior. Cover meaningful success, failure, recovery, and compatibility paths. Specification work records planned checks separately from any baseline or reproduction checks actually run.

Reassess single-PR feasibility using the actual contract, dependencies, code surface, migrations, test burden, and operational consequences. If completing the agreed outcome requires a separate prerequisite PR, an independently delivered second outcome, or a rollout that cannot be handled coherently within the proposed PR, return `SCOPE_DECISION_REQUIRED`. Explain the evidence and possible scope choices. Do not silently reduce the outcome, split tickets, create a program, or call an oversized bundle a single PR merely because Git can contain it.

## 6. Review and repair the complete proposal

Perform first-principles alignment, adversarial specification review, and implementation-design review as distinct lenses with recorded outcomes. Include provenance and architecture review where the claims require them. Use an independent agent with the bounded source package when available and authorized; otherwise label the review as self-review and state the independence limit.

Give reviewers the request, current basis and decisions, specification, evidence, relevant source artifacts, contract matrix, and proposed handoff. Withhold the authoring conversation, hidden rationale, and desired verdict. Ask them to challenge actual requirements and claims rather than inventing new acceptance criteria.

Classify findings as `BLOCKER`, `MATERIAL_HITL_DECISION`, `AGENT_REPAIR`, or `NONBLOCKING_OBSERVATION`. Tie each to evidence, an approved requirement or claim, consequence, and earliest repair point. Correct in-scope defects autonomously and rerun affected checks. Route changes to intent or material tradeoffs to the human. An automated pass is review evidence, not approval.

Prepare a supervisor-readable explanation that stands on its own. Prefer a visual when it makes relationships, user experience, state changes, or failure recovery easier to understand. Use only applicable renderer and publication policies; do not make a diagram count a gate. Verify actual rendered artifacts, their source consistency, readability, and access before relying on them. Do not claim a source file or provider receipt proves rendering quality.

## 7. Obtain final approval and hand off

Present one coherent proposal covering the specification, relevant visuals, and implementation handoff. State the one outcome, the proposed behavior, material tradeoffs, compatibility, evidence limits, one-PR rationale, verification plan, and exact decision requested. The reviewer should not need the authoring conversation to understand it.

Reuse an existing authorized design document. In standalone work, local Markdown is a complete specification destination. If a linked issue or managed workflow requires provider publication, prepare the content first, then use existing authorization and the configured adapter to publish and read it back. Ask only for a missing destination or write authority; follow [publication and recovery](references/review-and-handoff.md#publication-and-recovery).

Bind final approval to the exact current specification, handoff, applicable visuals, source baseline, and evidence revisions. Preserve the actual approving actor and response reference. Clear natural-language approval is sufficient when the context identifies those exact artifacts; silence, a review pass, a generated response, or preparation of the handoff is not approval.

If the human requests presentation changes, retain unaffected source decisions and review work, update the explanation, and present the current revision for approval. If semantics or relevant source evidence changes, return to the earliest affected stage and refresh dependent review and approval. Do not reuse a stale approval.

Return `HANDOFF_READY` only when the agreed single-PR specification and handoff are current, reviewed, and actually approved, and no unresolved material design decision remains. Record any separate implementation prerequisites so the next executor can verify them. If final approval is still pending, return `AWAITING_SPEC_APPROVAL` with the complete proposal. Use `SCOPE_DECISION_REQUIRED` for the single-PR conflict or `BLOCKED` for an unavailable required capability, evidence, or authority. These are local report labels, not Camunda task completions or new runtime schema fields.

During ordinary investigation or a human understanding/decision wait, report the current stage and exact pending question directly. Do not force in-progress work into a final result label. A routine human checkpoint is not `BLOCKED` unless a separate required dependency is actually unavailable.

End at this boundary. Name the handoff artifact and how a later, explicitly requested implementation can consume it. `$single-pr-executor` or `$issue-implementation` remains subject to its own actual prerequisites; a standalone handoff does not fabricate a issue or work item, Code Mass Contract, or managed-process approval.

## Progress and final reporting

At entry, resume, a material stage change, a human wait, and handoff, report the scope, current activity, established facts, and the next action or dependency. For managed work, derive process position and waiting state from live authority. For standalone work, describe the observed local stage without presenting it as engine state or a completion percentage.

Continue authorized research, drafting, repair, and independent work during a real human wait. Do not ask whether to continue after a completed substep. Stop only at this skill's handoff boundary, an actual decision, or a dependency that prevents further useful authorized work.

The final report includes the applicable result label or active stage and human wait, specification and handoff links, exact scope and approval state, meaningful verification performed, remaining limitations and prerequisites, a **Public interface changes** section with examples or an explicit `none`, and a concise **Plain-English pseudocode** explanation of the proposed behavior. Clearly state that implementation verification is planned unless it was actually performed against existing behavior.

## Issue writing

Whenever this workflow creates or edits issue prose, apply [the shared issue-writing contract](references/bundled/issue-writing/SKILL.md). Each issue must stand on its own; its only optional document reference is its actual design proposal. Put supporting source documents and technical records in the proposal or internal workflow evidence. Validate the prepared content and provider readback, and repeat the automatic readability review after material edits. This rule creates no new issue, publication authority, or human approval.

## Pull request writing

When this workflow authors PR content, apply [the shared PR-writing contract](references/bundled/pull-request-writing/SKILL.md). The description explains the change and verification on its own, and its sole optional document reference is the design proposal. Validate prepared content and provider readback automatically within existing publication authority.
