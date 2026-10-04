# <Issue, fix, or feature>: implementation handoff

This document proposes implementation of one specification in one PR. Its binding states whether approval of that exact specification and handoff is pending or complete. It does not itself authorize implementation, create a PR, or prove any unimplemented behavior. Reuse linked specification content rather than copying it into a second source of truth.

## Binding and readiness

Work reference: <local identifier or existing issue>.
Specification: <exact artifact and revision/content binding>.
Handoff revision: <current revision>.
Approval: <actual actor/response/binding or pending>.
Planning result: <actual current result label>.
Source baseline: <repository, checkout, commit, relevant dirty state, and source revisions>.
Execution prerequisites: <only actual environment, access, or release dependencies>.

If required code must land in another PR or a material design contract remains unresolved, explain the scope/design conflict rather than hiding it among execution prerequisites.

## Outcome and behavioral contract

Explain the one useful outcome and link its authorized requirements. Narrate the proposed flow in plain-English pseudocode from entry point to observable result, including material failures and recovery. State the affected public interfaces and link realistic before/after examples, compatibility, and data consequences.

## Scoped implementation surfaces

| File/symbol or public surface | Current responsibility and source evidence | Proposed responsibility/change | Why it belongs in this PR |
|---|---|---|---|
| <evidence-backed target or labeled tentative target> | <baseline link> | <behavior-preserving or behavior-changing proposal> | <requirement reference> |

Record existing mechanisms to reuse, unnecessary responsibilities to remove, uncertain deletion candidates, dependencies, and justified new complexity. Retain applicable approved Code Mass Contract references. Otherwise provide a reasoned scope estimate without inventing a ratio or numeric threshold.

## Proposed sequence within the PR

Explain where the executor begins, how the contract or harness is exercised, how the scoped changes fit together, how affected seams and any migration are integrated, and how the complete outcome is verified. Keep prerequisites and safe ordering explicit. This is one implementation plan, not a set of separately deliverable tickets.

## Verification to perform

Link the behavior matrix and enumerate only useful nonredundant checks. Identify each feature's end-to-end boundary and affected seams' integration contracts. Include the actual environment/fixtures, expected positive observations, meaningful failures/recovery, compatibility, and required evidence.

Identify request-relevant existing tests to preserve or rewrite at a public boundary. Do not assert internal collaborators, call counts, private state, or source patterns. If the harness lacks a stable observable boundary, describe the scoped harness improvement.

Baseline checks actually run: <check, baseline, observed result, and evidence>.
Implementation verification not yet performed: <planned checks>.
Uncovered behavior and reason: <actual limits>.

## Operational consequences

Describe applicable state changes, migrations, deployment order, compatibility windows, recovery, rollback/restoration, external effects, and outcome/failure signals. Mark non-applicable topics proportionally. Do not invent product or release requirements to fill this section.

## Decisions, review, and revision triggers

Link accepted decisions, actual review findings and disposition, any grounding conclusions, and evidence limits. Explain which implementation details remain normal executor judgment under the approved contract.

When implementation evidence changes the intended behavior, public interface, invariant, approved risk, source assumption, or single-PR boundary, the executor returns that evidence for a targeted specification revision. Preserve unaffected decisions and recheck only dependent work. A new requirement is not silently added to the PR.

## Next invocation

The user can request implementation using this exact handoff after approval. In a managed issue, name the actual owning execution workflow and its remaining verified prerequisites. In a standalone issue, a later implementation request can consume this document directly; do not claim that it satisfies an executor's unfulfilled Linear or runtime requirements.

Current handoff status: <approved and current, or precise pending decision/dependency>.
