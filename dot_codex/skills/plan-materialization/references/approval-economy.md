# Approval economy

Apply the underlying decision, approval-reuse, and progress-reporting behavior to the current scope's records and authorized interaction surface. Process keys, native user tasks, response-envelope fields, and runtime commands below apply only to an actually configured orchestrator. Without it, bind explicit human decisions to the question and exact reviewed content without fabricating engine state. See [workspace and destinations](workspace-and-destinations.md).

The workflow uses `approval-economy-v1` to reuse established intent, continue completed reviews, combine design and visual approval, limit revision work, accept explicit combined Ground Me responses, and recover transient technical failures. Initial epic intent and final supervisor proposals remain human decisions. Automatic verification has its own evidence record and never invents a human approval.

Human-facing interactions follow [review and artifact design](review-and-artifact-design.md). Initial intent and the existing final scope reviews are purposeful checkpoints. Between them, ask only when an unresolved material choice requires human judgment or missing authority; stage completion, factual research, clean review, and verified handoff require no extra permission prompt.

## Basis reuse

When an explicitly invoked program or ticket remains entirely within an approved basis, use that original basis unchanged. Supply `basisReuse: {"approvalTaskKey":"2251799813740001"}` in the child process variables and return the original binding as `programBasisBinding` or `ticketBasisBinding` from its draft-basis job. The runtime reads the source Camunda task and its process variables, verifies tenant, completed state, named approval, task identity, and the current source binding, then compares the child binding exactly. A matching basis produces `basisApprovalMode: "INHERITED"` and a `basisInheritance` record identifying the source task, process, actor, and binding. There is no new human response record.

An absent source approval or a different child binding produces `HUMAN_REQUIRED` and enters the child basis review. An invalid, incomplete, rejected, or superseded source approval cannot establish reuse. Preserve any new child outcome, constraint, or tradeoff in a successor basis and obtain its approval; do not hide a change behind the original reference. Exact reference equality checks declared identity, not the truth of an author's semantic coverage assessment. Reuse does not authorize a new implementation scope or external destination.

## Review and final proposal

The semantic draft exposes `semanticBinding`. A reviewer returns `reviewBinding` plus this completion extension:

```json
{"reviewResult":{"binding":{"ref":"SEM-1","hash":"sha256:source"},"status":"PASS","findings":[]}}
```

`binding` matches both `reviewBinding` and the current `semanticBinding` for every structured review outcome. `PASS` requires an empty findings inventory. It records `reviewVerification.kind: "AUTOMATED_REVIEW"` and continues without a review-disposition user task. `REPAIR` requires findings whose `ref` identifies the issue and whose `basis` matches the current approved basis; the parent returns to drafting and repeats review. The producing reviewer establishes that repairs are within that basis. `HUMAN`, or the absence of a structured review result, enters human disposition. Factual, risk, scope, and value judgments remain visible through that path.

Visual compilation and its renderer checks precede publication. The final supervisor proposal in the selected document home contains every current compiled visual, alongside any additional evidenced visual used in the document. The semantic release user task reviews this complete design and visual explanation once. Figma Design, LikeC4, and Archify remain the required graph renderers. The final program and ticket proposal reviews retain their respective scope boundaries.

## Revision scope

Final proposal tasks accept `approved`, `changes_requested`, `semantic_change`, and `presentation_change`. `changes_requested` retains the broad design-revision path. `semantic_change` also returns to the owning design stage. A semantic release presentation change returns to visual compilation and publication; a program or ticket presentation change returns directly to proposal publication. It does not rerun unaffected design or adversarial review.

When the human requests a presentation change, the runtime captures the current planning-source bindings in `revisionGuard`. Workers cannot change those source bindings or remove the guard during the repair. A source mismatch reports `invalid_approval_evidence`; a semantic revision clears the presentation scope and follows the design path. Every revised document receives a fresh binding and final review. Existing approval is reused only for unchanged content and authorized metadata finalization, never for a changed presentation that the human has not reviewed.

## Combined Ground Me response

When the explanation and decision are ready together, the supervisor can explicitly choose `aligned_and_answer` at `confirm_understanding`. The normal response envelope includes:

```json
{"decision":{"binding":{"ref":"DEC-1","hash":"sha256:question","frontierRevision":1},"answer":"B"}}
```

The grounding binding's `question`, the current `decisionBinding`, and the submitted decision binding must match. The selected answer is explicit human input. After grounding finalization, `resume_grounded_decision` verifies the completed grounding task and current packet/question bindings. A matching response supplies `decisionResponse` with the original human actor, answer, and `sourceGroundingResponse`, then enters automatic decision assessment. No fictitious decision user-task completion is created. Changed evidence or question bindings present the current question again. Premise invalidation recomputes the frontier without applying the old answer. Standalone grounding without a decision does not accept the combined action.

The built-in `specflow.resume-grounded-decision` worker performs this bounded bookkeeping. It needs no authoring command. Custom job-type names can configure `{"builtin":"grounded-answer"}`. Other service tasks still require their configured authoring or provider handlers.

## Prepare an exact response

```text
specflow prepare-response TASK_KEY --actor "Named supervisor" --action approved --json
specflow prepare-response TASK_KEY --actor "Named supervisor" --action aligned_and_answer --answer B --json
```

This command reads the active task and its current bindings and returns `{"response":{...},"submitted":false}` inside the CLI result envelope. It does not complete the task or authorize the proposed action. After the named human chooses that action, pass the returned `response` object to `specflow complete-task response.json --json`. The completion command rechecks the binding; a concurrent revision requires a current response. Use `--answer` for an explicitly chosen ordinary decision answer as well.

## Technical recovery and existing authorization

A command handler can return `{"status":"transient","message":"provider temporarily unavailable","retryBackOff":1000}` even with a nonzero process exit code. The worker uses the existing finite Camunda retry budget. A malformed response or an unclassified failure remains an incident; a successful-looking response with a nonzero exit cannot advance work. A nonnegative integer backoff is required.

External adapters use the same transient result during reconciliation or mutation. An unknown mutation result triggers bounded reconciliation attempts. Every retry starts with reconciliation using the same operation identity: a found result completes the job, an established absence permits the intended effect, and unresolved state does not permit another write. Exhausted retries retain the incident and evidence for repair. Configuration, authorization, invalid graph evidence, and changed intent are not classified as temporary outages.

Preparation, validation, readback, and remaining actions already covered by the user's authorization proceed without another permission question. An unconfigured provider, missing destination, or new write scope remains explicit. Existing provider adapters must still verify their own reconciliation guarantees; local tests do not establish live destination behavior.

## Compatibility and evidence limits

Definitions carrying the policy headers use these routes. Running definitions retain their original routes and user tasks; deployment does not migrate them. Old child handlers without reuse evidence continue through human basis review, and reviewers without a structured result continue through human disposition. The existing final approval response shape is retained, with optional revision and combined-decision actions. `prepare-response` is an additive read-only command.

Hashes and engine records establish declared identity and recorded actions. They do not prove that source content is truthful, a review is competent, or a renderer was honestly attributed. The runtime remains a client contract, not an authorization barrier against direct Camunda API operators.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.
