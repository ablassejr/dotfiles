# Minimal behavioral coverage strategy

Start with the business behavior the request requires and what a user or caller can observe. Existing BPMN nodes, branches, and decision rules help locate relevant paths; they do not independently create acceptance requirements.

## Select acceptance scenarios

Read the affected contract and existing tests. Map each minimal acceptance criterion to its triggering situation, action, expected result, and the E2E or integration boundary that can exercise it. Prefer the actual entry point and real affected components. If E2E cannot run, record why and select the closest integration path that still proves the intended outcome.

Reuse a scenario when it already proves the criterion. Add or adapt a scenario only when a distinct required outcome or meaningful failure, recovery, or preservation case remains unverified. Several assertions can establish one coherent result. Do not split scenarios because they cross multiple services or nodes, and do not add a parallel integration suite for seams already exercised adequately.

For example, if a request concerns approval routing, assert the publicly meaningful approval task and final decision for the required business situations. If it concerns sending a notification, process completion alone is insufficient: exercise the real worker and assert the notification contract at the receiving boundary. A manually completed notification job cannot establish that result.

A compact plan can state the criterion, scenario and expected outcome, existing or missing coverage, E2E/integration boundary, and environment limitation. Keep the plan in the existing verification record; do not duplicate the issue criteria in another standalone document.

## Use structural coverage as diagnosis

When available, inspect the CPT report at target/coverage-report/report.html. Check whether a missed branch or boundary suggests a missing required business scenario. Add a test only when that analysis identifies a meaningful gap. A 100% element or flow score does not establish correct outputs, worker execution, or external effects.

When a user explicitly requests a structural coverage target, report it separately from behavioral acceptance. A short segment starting at an internal element may help isolate a routing defect, but leaves the skipped entry path unverified. Static path predictions are planning evidence; only executed results support runtime claims.

Two scenarios that visit the same nodes may establish different output values or failure behavior. Remove a scenario only when the remaining suite still observes all its required outcomes, not merely when visited-element sets overlap. A passing scenario without an assertion of the intended outcome is not acceptance evidence.

## Process harness mechanics

The following patterns drive process routing in the harness. When they replace worker execution, treat them as focused engine diagnostics and state that limit. They are not examples of E2E verification of the worker or external service.

## Ad-hoc subprocess and tool activation

Inner activities of an `<bpmn:adHocSubProcess>` have **no inbound sequence flow** — they are activated dynamically, either declaratively (internal mode, via `activeElementsCollection`) or programmatically (job-worker mode, via the worker's `activateElements` result). A static walker treats them as dead code and drops them from coverage. They are not dead code: the AHSP itself is the entry point, and activities relevant to required outcomes belong in the scenario analysis.

**Planner rule.** For an inner activity needed to exercise a required outcome, consider one candidate segment rooted at the AHSP and ending when that inner activity completes. The candidate's predicted set includes the inner activity, its outgoing internal flow (if any), and the AHSP itself.

**Authoring** depends on the AHSP mode (the internal-mode vs. job-worker-mode distinction is covered in **camunda-bpmn**):

- **Internal mode** (no `<zeebe:taskDefinition>` on the AHSP): pass `activeElementsCollection` and any tool inputs as variables on `CREATE_PROCESS_INSTANCE`; each inner activity then becomes a normal job — `COMPLETE_JOB` against `jobSelector.elementId` for each. No outer AHSP job exists.
- **Job-worker mode** (has `<zeebe:taskDefinition>`, e.g. the AI Agent Sub-process connector): the AHSP is itself a job. Stub the agent loop with a Java orchestrator — `context.mockJobWorker(ahsType).withHandler(handler)` returns activation results, and `context.when(condition).then(action)` *(8.9+)* completes each activated tool once it becomes active. A plain `COMPLETE_JOB_AD_HOC_SUB_PROCESS` JSON instruction can drive a single activation cycle but cannot react to per-iteration state.

Worked stub-orchestrator pattern (Java, AI-agent-style AHSP):

```java
context.mockJobWorker("io.camunda.agenticai:aiagent:1").withHandler((client, job) -> {
    // 1. Inspect job variables to decide which tools to activate next.
    // 2. Build an ad-hoc result with .activateElement("Tool_X").variables(...).
    // 3. Mark .completionConditionFulfilled(true) when the agent decides it is done.
});

context
    .when(() -> CamundaAssert.assertThat(processInstance).hasActiveElements("Tool_FetchOrder"))
    .then(() -> context.completeJob(JobSelectors.byElementId("Tool_FetchOrder"),
                                    Map.of("toolCallResult", Map.of("status", "ok"))));
```

Cross-links: **camunda-ai-agents** for the BPMN shape and tool-modelling rules; [authoring.md § COMPLETE_JOB_AD_HOC_SUB_PROCESS](authoring.md#complete_job_ad_hoc_sub_process) for the JSON instruction; [test-context.md § Conditional behavior](test-context.md#conditional-behavior-89) for `when().then()` semantics.
