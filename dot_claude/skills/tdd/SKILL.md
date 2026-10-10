---
name: tdd
description: Test-driven development. Use when the user wants to build features or fix bugs test-first, mentions "red-green-refactor", or wants integration tests.
---

# Test-Driven Development

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


TDD is the red → green loop. This skill is the reference that makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle: consult them before and during the loop, not after.

When exploring the codebase, read `CONTEXT.md` (if it exists) so test names and interface vocabulary match the project's domain language, and respect ADRs in the area you're touching.

## What a good test is

Tests verify behavior through public interfaces, not implementation details. Code can change entirely; tests shouldn't. A good test reads like a specification: "user can checkout with valid cart" tells you exactly what capability exists, and it survives refactors because it doesn't care about internal structure.

See [tests.md](tests.md) for examples and [mocking.md](mocking.md) for mocking guidelines.

## Minimal acceptance suite

Use the smallest nonredundant suite of behavior-driven acceptance tests that verifies the stated functionality, fix, or other change. Map the minimal acceptance criteria to observable outcomes and reuse or adapt existing coverage before adding tests. Prefer end-to-end tests through the real user or system entry point when a usable environment can exercise the path. When end-to-end execution is unavailable or impractical, use integration tests through the closest stable public boundary with the real affected components; state the concrete limitation, the boundary exercised, and what remains unverified. Do not silently substitute unit tests or count mocked provider behavior as end-to-end proof. Add separate integration checks only for material contract gaps the selected suite does not exercise, not automatically for every seam. Cover intended success and meaningful in-scope failure or recovery cases without multiplying tests for internal paths or arbitrary coverage quotas.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior without reaching inside. Tests live at seams, never against internals.

Choose the boundary from the stated behavior, existing public interfaces, and available test environment. Reuse coverage before adding tests. Resolve routine test choices autonomously; ask only when a material ambiguity changes the intended behavior or scope. Do not request approval for each criterion or seam.

## Anti-patterns

- **Implementation-coupled**: mocks internal collaborators, tests private methods, or verifies private storage details instead of the declared interface; persisted state is appropriate when it is itself the public contract. The tell: the test breaks when you refactor but behavior hasn't changed.
- **Tautological**: the assertion recomputes the expected value the way the code does (`expect(add(a, b)).toBe(a + b)`, a snapshot derived by hand the same way, a constant asserted equal to itself), so it passes by construction and can never disagree with the code. Expected values must come from an independent source of truth: a known-good literal, a worked example, the spec.
- **Horizontal slicing**: writing all tests first, then all implementation. Bulk tests verify _imagined_ behavior: you test the _shape_ of things rather than user-facing behavior, the tests go insensitive to real changes, and you commit to test structure before understanding the implementation. Work in **vertical slices** instead: one test → one implementation → repeat, each test a **tracer bullet** that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first, then only enough code to pass it. Don't anticipate future tests or add speculative features.
- **One slice at a time.** One coherent behavior and the smallest useful test change per cycle. Several assertions may establish the same scenario; do not force one test per seam or function.
- **Refactoring is not part of the loop.** It belongs to the review stage (see the `code-review` skill), not the red → green implementation cycle.

## Verify the implemented result

For a fix, use diagnosis to identify the missing observable contract and reuse, rewrite, or add the minimal acceptance scenario that would have caught it. Preserve valid behavior; do not test the incident's private repair mechanism. Run the scenario against the unfixed baseline when feasible and against the final change. If the baseline cannot be exercised, state that limit rather than claiming red/green evidence or deleting existing work.

Inspect request-relevant tests for implementation coupling and preserve their useful behavioral coverage when repairing them. Run the selected acceptance suite and required repository checks. Report the criteria exercised, actual results, E2E or integration boundary, and any remaining gaps in the existing review record. A proposed, skipped, or blocked test does not prove the functionality works.
