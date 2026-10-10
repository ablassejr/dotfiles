---
name: camunda-process-test
description: |
  Use this skill to author and run Camunda Process Test (CPT) suites that verify required business outcomes with minimal behavior-driven acceptance scenarios.

  Use for: scaffolding the `camunda-process-test-spring` harness, planning a minimal acceptance suite and supplemental process diagnostics, authoring `.test.json` instruction-based scenarios, running `mvn test`, parsing the CPT coverage report, deduplicating redundant segments.

  Do not use for: authoring the BPMN (use camunda-bpmn), writing FEEL or DMN expressions (use camunda-feel), deploying to a live cluster (use camunda-process-mgmt), UI or E2E tests against Operate or Tasklist.

  **Workflow skill** — behavior-driven acceptance planning and execution covering `mvn test`, coverage report parsing, and scenario deduplication.
---

# Camunda Process Test

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


## Acceptance strategy

Use the smallest nonredundant suite of behavior-driven acceptance tests that verifies the stated functionality, fix, or other change. Map the minimal acceptance criteria to observable outcomes and reuse or adapt existing coverage before adding tests. Prefer end-to-end tests through the real user or system entry point when a usable environment can exercise the path. When end-to-end execution is unavailable or impractical, use integration tests through the closest stable public boundary with the real affected components; state the concrete limitation, the boundary exercised, and what remains unverified. Do not silently substitute unit tests or count mocked provider behavior as end-to-end proof. Add separate integration checks only for material contract gaps the selected suite does not exercise, not automatically for every seam. Cover intended success and meaningful in-scope failure or recovery cases without multiplying tests for internal paths or arbitrary coverage quotas.

CPT supplies a process-engine test harness. Name its actual scope: an engine-only scenario with manually completed jobs verifies process behavior, not worker execution or external system success. When the requested change concerns a worker or connector, exercise its real implementation with the engine and assert the resulting public contract. Use a true external boundary fake only when needed and report what live behavior remains unverified.

The acceptance gate is the intended business outcome. BPMN element and sequence-flow coverage help diagnose missed scenarios; they are not a default 100% quota or sufficient evidence that a feature works. Use a separately requested structural coverage target only as an additional diagnostic requirement.

## Prerequisites and scope

Use [setup.md](references/setup.md) for Java, Maven or the repository wrapper, Docker, CPT dependencies, and the harness. Instruction-based JSON scenarios require the compatible CPT version documented in [authoring.md](references/authoring.md). Read the repository's actual dependency versions before selecting an API.

Exercise affected process routing, business decisions, observable task states, outcomes, errors, and recovery. Assert data values when they are part of the required public result; do not assert private intermediate variables solely because they exist. Process completion alone is insufficient when the requirement includes a produced value, notification, or other external effect.

CPT does not itself provide a browser workflow or proof of a production deployment. Prefer the repository's existing E2E harness when the acceptance criterion crosses the UI or a deployed service. If that environment cannot run, use the closest useful integration boundary and state the remaining gap. Routine scenario and boundary choices do not require user approval; ask only when ambiguity changes required behavior or scope.

## Workflow

### Establish behavior and existing coverage

Locate the affected BPMN, referenced decisions/forms, worker or connector implementations, and existing tests from the request and repository context. Common process locations include src/main/resources/processes/, src/main/resources/bpmn/, and ../resources/ for a separate harness. Select the affected files from evidence before asking the user to choose among unrelated processes.

Derive minimal acceptance criteria from the stated goal and established contracts. For a fix, diagnose the missing observable contract and reuse or improve coverage that would have caught it. Inspect relevant existing tests and replace private-element, internal-call, or source-pattern assertions when they do not represent a declared public contract. Keep unrelated tests out of scope.

### Plan the smallest useful suite

Use [coverage-strategy.md](references/coverage-strategy.md). Map each required outcome to an existing or proposed scenario, the entry point, the observable result, and the actual E2E or integration boundary. Include only meaningful in-scope success, failure, preservation, and recovery cases. One scenario can prove several related criteria. Do not create a test for each BPMN element or remove a test merely because its visited elements overlap another scenario.

### Author and run

Configure a missing harness through the bundled setup instructions. Use [authoring.md](references/authoring.md) for JSON instructions and [test-context.md](references/test-context.md) for the Java fallback when richer outcome assertions or real worker integration are needed. Name each scenario for its actor or trigger and expected result.

Drive the process through its actual entry point when possible. Starting at an internal element is a focused process diagnostic; it does not prove the omitted path. Assert required outputs or publicly meaningful task states, not every internal node. Keep real workers and collaborators in the path whose behavior is under test; manual job completion and worker mocks cannot prove that worker's behavior.

Run the repository's documented test command, such as mvn test for a compatible Maven harness, after the applicable CLI documentation lookup. Establish the failing baseline when feasible, implement the fix, and rerun against the final change. An unavailable baseline is a reported limitation, not a reason to claim unobserved red/green evidence.

On failure, distinguish harness problems, invalid expectations, and actual process or worker defects. Use [troubleshooting.md](references/troubleshooting.md) and [run-and-diagnose.md](references/run-and-diagnose.md). Repair and rerun affected checks; a skipped scenario or infrastructure error is not a passing acceptance result.

### Assess and report

Compare actual observations with the minimal acceptance criteria. Use the CPT report at target/coverage-report/report.html, when generated, to investigate suspicious gaps. An uncovered internal element does not automatically require another test, and a fully covered model does not establish correct outputs. Missing report generation leaves structural coverage unverified; static inspection cannot substitute for executed behavior.

Complete selected acceptance tests and repository-required checks. Report which outcomes passed, the boundary actually exercised, the suite size, and any blocked or unverified behavior. Include a coverage report link when useful for diagnosis. Keep this evidence in the existing review record rather than creating a duplicate artifact. Use [evaluation.md](references/evaluation.md) to assess gaps and [ci.md](references/ci.md) for CI integration.

## References

- [setup.md](references/setup.md) — Java, Maven, Docker prereqs; CPT dependency; test scaffold layout; Spring Boot 4.x pin
- [coverage-strategy.md](references/coverage-strategy.md) — minimal outcome-based scenario selection and process diagnostics, including ad-hoc subprocess tool activation
- [authoring.md](references/authoring.md) — `.test.json` schema, full 8.9 instruction reference, Java fallback
- [test-context.md](references/test-context.md) — `CamundaProcessTestContext` Java API surface (job/decision/child-process mocking, time control, conditional behavior)
- [connectors-runtime.md](references/connectors-runtime.md) — enabling the Connectors runtime alongside Zeebe; WireMock pattern; inbound webhooks
- [troubleshooting.md](references/troubleshooting.md) — failure diagnosis table (test problem vs. process problem)
- [run-and-diagnose.md](references/run-and-diagnose.md) — test-run execution loop and failure-batch repair strategy
- [evaluation.md](references/evaluation.md) — coverage-gap assessment and recommendation workflow
- [ci.md](references/ci.md) — CI pipeline patterns for CPT execution and test-report publishing
