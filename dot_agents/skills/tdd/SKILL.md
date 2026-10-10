---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
---

# Test-Driven Development (TDD)

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


## Acceptance strategy

Use the smallest nonredundant suite of behavior-driven acceptance tests that verifies the stated functionality, fix, or other change. Map the minimal acceptance criteria to observable outcomes and reuse or adapt existing coverage before adding tests. Prefer end-to-end tests through the real user or system entry point when a usable environment can exercise the path. When end-to-end execution is unavailable or impractical, use integration tests through the closest stable public boundary with the real affected components; state the concrete limitation, the boundary exercised, and what remains unverified. Do not silently substitute unit tests or count mocked provider behavior as end-to-end proof. Add separate integration checks only for material contract gaps the selected suite does not exercise, not automatically for every seam. Cover intended success and meaningful in-scope failure or recovery cases without multiplying tests for internal paths or arbitrary coverage quotas.

Read the affected request, behavior, and existing tests before choosing scenarios. Explain the expected result in domain language before deciding how to exercise it. Ask only when an unresolved choice materially changes the intended behavior or scope; do not require approval of each test boundary.

## Red, green, refactor

When starting a behavior change, choose one missing acceptance scenario and run it against the current implementation. A useful red result fails because the intended behavior is absent or wrong; a setup error is not evidence of that gap. Implement the smallest coherent change, rerun the scenario, and continue until the selected acceptance criteria are covered. Refactor while preserving the observable contract and rerun the affected checks.

For a bug, use diagnosis to identify the missing behavioral contract. Reuse or improve an existing acceptance test, or add the smallest scenario that would have caught the gap, including valid behavior the fix must preserve. Do not add a separate incident-specific test that asserts the internal repair mechanism.

When implementation already exists, verify it against independently derived expectations. Do not delete working code merely to stage a red result. Where feasible, exercise the same scenario against the unfixed baseline in isolation; otherwise state that the failing baseline was not observed. Never claim a red/green result that was not executed.

## Observable assertions

Use real affected components and assert results at a stable public boundary: rendered output, returned values, retrievable persisted state, emitted events, documented errors, or external protocol behavior. Several assertions may establish one coherent scenario. Do not require one test per function, method, component, seam, or internal branch.

Use independent expected outcomes from the request or established contract. Do not recompute the expected answer using the implementation's algorithm. Negative assertions are appropriate when absence is itself a required observable result.

Fake only true external boundaries or nondeterminism. Do not mock the feature, internal worker, or collaborator whose behavior is being verified. A provider fake supports an integration claim about the application contract; it does not verify that provider. See [testing-anti-patterns.md](testing-anti-patterns.md).

## Example of a minimal suite

When the requirement is that a saved display name remains visible after reopening a profile, exercise editing, saving, and reopening through the actual application and assert the displayed name. If the browser environment cannot run, exercise the real update and read endpoints with the real persistence layer and report that UI interaction remains unverified. Add a rejected-update scenario only if that behavior is part of the affected contract. Do not add tests solely for the repository helper or the number of save calls.

## Verification and completion

Inspect request-relevant existing tests and replace implementation-coupled assertions while preserving their useful behavior coverage. Reuse scenarios that already prove the requirement. A new test is useful when it covers a distinct required outcome, failure, or recovery condition; do not duplicate a passing acceptance scenario at each level of the stack.

Run the selected acceptance suite against the final change and complete repository-required checks. Broaden testing when affected behavior or new failures justify it. Report the scenario, boundary, actual result, and any untested behavior briefly in the existing review or delivery record. A passing command with skipped scenarios, setup failures, or only unit tests does not establish acceptance of the unexercised behavior.
