# Stage visibility

Apply the underlying decision, approval-reuse, and progress-reporting behavior to the current scope's records and authorized interaction surface. Process keys, native user tasks, response-envelope fields, and runtime commands below apply only to an actually configured orchestrator. Without it, bind explicit human decisions to the question and exact reviewed content without fabricating engine state. See [workspace and destinations](workspace-and-destinations.md).

The workflow presents its current scope, numbered stage, active work, and waiting state from live Camunda observations. Scope distinguishes semantic specification, implementation planning, ticket implementation, and standalone research or grounding. Stage numbers describe the order within that scope; they are not a completion percentage.

## Agent presentation

When entering or resuming framework work, read `specflow resume <business-id> --json` and begin the user-facing update with the scope, current stage, and state. Repeat this compact heading when the observed stage changes, before a human decision or approval, and when handing control back. Ordinary updates within the same stage explain the material finding, its implication, and what the next activity will resolve without repeating the stage map or tool log. Follow [review and artifact design](review-and-artifact-design.md) for focused questions and meaningful engagement.

For example, an integrated grounding checkpoint is presented as:

```text
Specification · Stage 4/9: Design decisions · Waiting for human review
Now: Ground Me / Understanding alignment
Last completed work: Ground Visuals
Human action: Confirm the explanation, correct it, request more depth,
or explicitly confirm and answer together.
```

Use the actual task's actions and assignment. Name a different assignee when the task belongs to someone else. Explain what the active stage produces and what response or event is needed to continue. When several branches are active, retain every branch and its breadcrumb under the same scope heading. A parent waiting for Ground Me remains in design decisions while its child shows the grounding substage.

When a step is revisited, say so. A presentation revision explicitly retains the planning source bindings. When the scope finishes, state its boundary: a completed specification does not itself start implementation planning. If no root is available or the live read fails, say that the engine position is unavailable; describe proposed work separately without inventing a stage number.

This presentation adds no approvals, stage gates, or process transitions. A human response is still accepted through its existing exact-bound Camunda task.

## Automatic step continuation

When a step completes, the agent checks Camunda's accepted completion and current work, then immediately carries out the next authorized step. Routine intra-stage transitions, validation, readback, reconciliation, and configured retries continue automatically. A completed substep is not a reason to end the turn or ask whether to proceed. Keep intra-stage updates brief while continuing the work.

A stage change produces the new stage heading and continues under the existing authorization. The display boundary itself does not require confirmation. Human decisions and approvals remain explicit inputs at their native user tasks; when such a task becomes active, present its actual question. If another independent authorized branch can proceed, continue it while that answer is pending. Existing external-write authorization and the separately invoked implementation scopes retain their boundaries.

Use the continuous worker when command handlers perform the stage: `specflow worker --config worker.json` keeps activating enabled job types and honors the engine's retry budget. `--once` is one polling pass, not a user checkpoint. When the agent performs jobs directly, repeat activation, skill execution, result validation, accepted completion, and live readback without requiring the user to invoke each step. A configured worker waits durably for an unhandled type; an agent with the required skill and authorization can perform that job directly.

When the next action needs an actual human choice, missing authority or information, an external event, or recovery beyond the existing capability or retry budget, report that concrete dependency with the current stage. An indexed wait, a failed completion, or an uncertain external effect never becomes a fabricated success to keep the sequence moving. Refresh incomplete observations and reconcile effects through the existing recovery contract.

## CLI presentation

```text
specflow status epic:EPIC-042
specflow resume epic:EPIC-042 --key 2251799813686561
specflow status epic:EPIC-042 --json
```

`status` and `resume` display a readable stage report by default. `status` observes execution; `resume` also checks referenced evidence and configured validators. Use `--json` for machine consumers. `inspect` and `validate` retain their JSON presentation and include the same stage projection.

The report names current tasks, human actions, events, technical retries, and incidents. It includes the latest completed work item and a stage map. `CURRENT` means active work was observed there. `VISITED` means execution evidence exists there. `NOT_OBSERVED` means this read has no such evidence; the stage may be future, skipped, inherited, or not indexed yet. Neither a visit nor a completed work item is independent proof of approval or provider verification.

An incident identifies recovery at its actual stage. Incomplete referenced evidence is shown separately and defers the pending human response until that evidence is repaired. An active process without indexed work displays a refresh state. An unknown model or element retains its raw identity with an unavailable stage label. Canceled or completed roots do not present stale active child work as current.

## JSON contract

The existing result retains its fields and adds `progress`. A shortened example is:

```json
{
  "state":"ACTIVE",
  "processInstanceKey":"2251799813686561",
  "progress":{
    "schema_version":1,
    "source":"camunda",
    "scope":"Specification",
    "state":"WAITING_FOR_HUMAN",
    "evidenceStatus":"not_checked",
    "current":[{
      "elementId":"approve_basis",
      "stage":{"id":"basis","label":"First principles","number":1,"total":9},
      "actions":["approved","changes_requested"],
      "revisited":false
    }]
  }
}
```

The full projection also includes `observedAt`, `consistency`, all current branch paths, root `stages`, `recentCompleted`, `humanActionRequired`, presentation `revision`, and the completed `scopeBoundary`. `status` retains root metadata at the top level; `inspect`, `resume`, and `validate` add the projection beside their existing `root` and `instances` fields.

The stage catalog covers the seven packaged workflow families and the retained legacy visual-review element. Family recognition uses the canonical definition ID or exact packaged process name, allowing named isolated deployments to use the same labels. Unknown elements remain unmapped. The catalog is presentation metadata; it does not select a deployed definition or grant execution authority.

## Observation boundary

Each report is a timestamped, eventually consistent read. It is not a durable stage record or an exclusive workflow lease. A later read can show a repaired, repeated, or different branch. Stage presentation works for already-running supported definitions without deployment or migration. Status reads the process's work items and called subprocesses; its additional reads require the corresponding Camunda read permissions. No status command completes a work item or publishes a provider document.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.

## Individual issue review before assignment

The implementation program creates issues without assignees, then runs each issue’s complete ticket decision and supervisor-review loop. **Individual issue HITL** remains current until the entire created set finishes. Only then does **Team assignment** apply the approved workstream owners. Ticket execution reuses an exact, verified review. Follow [the issue review and assignment contract](issue-review-before-assignment.md) for jobs, publication variables, worker configuration, native approval checks, and provider readback.
