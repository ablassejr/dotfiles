# Individual issue HITL before team assignment

This reference describes the explicitly selected Linear/Notion/Camunda adapter profile. Apply its provider-specific schemas and operations only in that configured workflow. For other projects use [workspace and destinations](workspace-and-destinations.md) and the provider-neutral scope contracts.

After the approved issues are created and read back in Linear, Camunda runs every issue through its own ticket planning and HITL loop. The whole created issue set finishes review before any issue is assigned to the three-person team. Planned workstream ownership remains in the approved program; Linear issue assignees stay empty during review.

The program displays separate **Issue creation**, **Individual issue HITL**, and **Team assignment** stages. Within Individual issue HITL, status identifies the current Linear issue and its active decision, design, or supervisor-review step. The issue queue is sequential so the supervisor receives one issue's decision frontier at a time. Automatic work continues between human decisions.

When an issue enters review, its ticket process verifies an inherited basis or obtains approval for genuinely distinct intent. It loads current context, including the project's uploaded artifacts, reconciles the basis, prepares the bounded design, and calls the existing decision workflow. Human answers remain open-ended. Each answer is analyzed; material disagreement, conflict, or decision-changing evidence produces a suggested change and human disposition. Ground Me returns to the same issue's decision. A frontier with no material question completes automatically. Apply [review and artifact design](review-and-artifact-design.md): present the ticket’s bounded contribution and any unresolved difference from the approved program, reuse settled decisions, and do not repeat the epic interview or expose the full frontier. The existing exact ticket-design approval remains; its prompt explains what is being approved and why this issue needs that review.

Once the frontier resolves, `specflow.finalize-ticket-design` performs the existing alignment, Code Mass Auditor planning pass, and adversarial design review. It returns `ticketReviewOutcome` as `READY`, `NEEDS_DECISIONS`, or `REVISE_DESIGN`. Remaining choices return to the decision workflow; a design defect returns to design. A ready design proceeds to its published, read-back-verified supervisor document and exact human approval. Presentation feedback republishes the document; substantive changes return to design and its decision loop.

Execution blockers do not prevent this planning review merely because another issue has not been implemented. Ground design dependencies against the approved predecessor contracts and surface any unresolved decision that affects the proposed design. Native `blocks` relations still prevent execution until their prerequisites are satisfied. Changes to approved program scope, issue membership, or workstream ownership return to program planning; a ticket review cannot silently repartition the program.

A review-only ticket process records `issueReviewReceipt` and completes without creating an implementation job. Camunda collects one receipt per created issue. `specflow.verify-all-issue-reviews` reads each completed child process and its native ticket approval, verifies issue and program identity, and compares the approved design and document binding. A missing, duplicate, mismatched, canceled, incomplete, or stale review prevents assignment. No extra program-wide approval is requested.

After the full set verifies, `specflow.dispatch-tickets`, displayed as **Assign Reviewed Issues to the Team**, applies the approved issue owners. Its handler reconciles interrupted writes, preserves matching assignments, and reads back the actual assignees. It must verify current issue and document revisions against the reviewed design before applying the external effect. The runtime performs the native review checks before invoking the assignment command and validates the returned assignment binding before completing the job. External Linear writes use the existing operation-aware adapter contract; the CLI is not an authorization boundary for direct API operators.

Assigned execution receives the issue's receipt. `specflow.verify-ticket-review` re-reads the completed review and the program's recorded assignment, then supplies the original approved design directly to implementation. It does not repeat unchanged planning approvals. Relevant source changes require a fresh ticket review and affected assignment verification; a static receipt does not establish continuous provider freshness. Per-ticket design documents and their linked evidence remain available in Linear. The pre-creation program resource inventory stays an immutable publication set, with later ticket artifacts kept in their own scope.

## Publication output

`specflow.publish-linear-program` creates all approved issues **without assignees** and returns `createdIssues`. Preserve the plan key alongside each provider identity:

```json
{
  "status": "completed",
  "variables": {
    "createdIssues": [
      {
        "plan_key": "W-API",
        "id": "linear-issue-uuid",
        "identifier": "EXAMPLE-204",
        "project_id": "approved-project-uuid",
        "assignee_id": null,
        "content": {
          "title": "Recover interrupted billing exports",
          "body": "Billing operators must restart interrupted exports. They need to recover the export and see its result without duplicate records.",
          "comments": [],
          "document_attachments": []
        },
        "verified_at": "2026-09-09T12:00:00Z",
        "evidence": "provider-readback-reference"
      }
    ]
  }
}
```

The array covers every issue in `linearPlan.issues`, without duplicates; reference-only relation endpoints are not newly created work and are not included. The runtime adds `programProcessInstanceKey`. The program call activity supplies each child's `createdIssue`, `programBinding`, `programProcessInstanceKey`, and `ticketMode: "REVIEW_ONLY"`, and isolates each child's variables. A failure during creation reconciles the partial issue set before retrying, including the unassigned state.

## Automatic review handlers

The three evidence-only jobs use the same built-in worker. They perform Camunda reads and validated completion, without inventing a human answer or writing to Linear:

```json
{
  "handlers": {
    "specflow.record-issue-review": {"builtin": "issue-reviews"},
    "specflow.verify-all-issue-reviews": {"builtin": "issue-reviews"},
    "specflow.verify-ticket-review": {"builtin": "issue-reviews"}
  }
}
```

Use `specflow worker --config worker.json --once --json` for bounded processing. Existing authoring handlers perform ticket design, decision selection, answer analysis, decision recording, design finalization, and proposal publication. An unavailable handler leaves its explicit job waiting.

`specflow.complete-job` uses the same checks through the existing `specflow complete-job job.json result.json` command. A successful evidence-only result can be `{"status":"completed","variables":{}}`; the runtime derives the review receipt or verified reuse variables. Contract failures return `invalid_issue_review`. When an approval or completed review has not yet appeared in Camunda readback, `pending_engine_readback` keeps completion pending; the configured worker fails that attempt transiently and retries with the existing budget. The same handling preserves an explicit combined Ground Me answer while its completed task becomes visible. Provider transients follow existing retries, and invalid evidence remains repairable through the incident workflow.

## Assignment and execution input

### Standalone review completion

A standalone `REVIEW_ONLY` ticket finishes through the same `specflow.record-issue-review` job. The runtime verifies its native completed design approval, tenant, resolved decisions, ready design and exact proposal binding. The root's business ID is `ticket:<linearIssueId>`; it carries `ticketBasisBinding` and may carry `linearIssueUuid`. Its native parent and the `programProcessInstanceKey`, `programBinding` and `createdIssue` variables are absent or null. A parented review or partially supplied program identity cannot become standalone by omitting a field.

The resulting `issueReviewReceipt` identifies its actual scope:

```json
{
  "schema_version": 1,
  "scope": "standalone",
  "issue": {"identifier": "EXAMPLE-204", "id": "linear-issue-uuid"},
  "basis": {"ref": "FPB-204-001", "hash": "sha256:basis-content"},
  "review_process_instance_key": "2251799813686561",
  "approval_task_key": "2251799813687001",
  "design": {"ref": "DESIGN-204-001", "hash": "sha256:design-content"},
  "proposal": {
    "id": "linear-document-id",
    "url": "https://linear.app/workspace/document/design-204",
    "revision": "provider-revision",
    "hash": "sha256:document-content"
  }
}
```

The optional issue `id` is retained when supplied; the identifier remains required. Completion preserves the approved inputs and derives the receipt from native task readback. Delayed approval visibility follows the existing transient retry path. Invalid identity, lineage or approval leaves completion rejected. This receipt completes the standalone planning review without starting implementation. Program assignment and assigned execution require a program receipt and reject standalone receipts, including ones with added program fields. Provider identity and document freshness still depend on the configured authenticated readback.

### Program review and assignment

`issueReviewReceipt` contains schema version 1, the exact program `source`, the created `issue`, `program_process_instance_key`, `review_process_instance_key`, `approval_task_key`, the approved `design` binding, and the approved `proposal` document identity/revision/hash. Camunda collects these as `issueReviewReceipts` in creation order.

The assignment handler returns `teamAssignmentBinding` with schema version 1, the same program source, `review_set_hash` (SHA-256 of the canonical JSON receipt array), and one row per issue:

```json
{
  "issue_id": "linear-issue-uuid",
  "owner": "approved-workstream-owner",
  "assignee_id": "resolved-linear-user-uuid",
  "readback_assignee_id": "resolved-linear-user-uuid"
}
```

The binding also carries `verified_at` and an `evidence` reference. All issue owners must match the approved plan, and the three workstream owners must resolve to three distinct Linear users. This records actual assignment after review; the plan's owner field expresses intended ownership before assignment.

When starting authorized ticket execution, pass `programBinding`, `programProcessInstanceKey`, `createdIssue`, and the matching `issueReviewReceipt` in the normal `specflow start ticket:EXAMPLE-204 --variables execution.json --json` input. The runtime verifies the completed review and recorded assignment before exposing implementation. A standalone ticket without a receipt follows the full ticket review path. Existing process instances remain on their deployed definitions; no migration is implicit.

The [issue review schema](bundled/implementation-specification-compiler/scripts/specflow_runtime/issue-review.schema.json) describes the provider issue inventory, review receipt, and assignment binding. The Linear plan schema stays version 4. Declared provider receipts are not proof of actual Linear state unless the configured authenticated adapter performs the documented readback.

## Engine references

The program uses a [sequential multi-instance activity](https://docs.camunda.io/docs/components/modeler/bpmn/multi-instance/) to collect every review, with no early completion condition. Its [call activity](https://docs.camunda.io/docs/components/modeler/bpmn/call-activities/) uses deployment binding and explicit variable mappings. The nested decision workflow retains the [open-ended decision contract](open-decisions.md).

## Created issue content

Each created issue also returns `content` with its fetched title, body, optional `design_proposal_url`, and explicit `comments` and `document_attachments` arrays under [the shared content contract](bundled/implementation-specification-compiler/references/issue-content.md). Validate the exact approved projection before starting its HITL review. Keep later grounding and decision source links inside the design proposal; preserve self-contained issue meaning after review edits.
