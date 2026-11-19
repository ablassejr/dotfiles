# Camunda orchestration contract

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](workspace-and-destinations.md) for the portable workflow and actual adapter limits.

## Scope and delivery status

Camunda 8.9 is the framework's orchestration control plane. The bundle includes seven executable BPMN definitions, a REST v2 client, a bounded worker protocol, a shared local operation registry, guarded artifact and Archify publication, and configurable provider adapter boundaries. The [runtime reference](camunda-runtime.md) describes implemented commands, inputs, and deployment. Semantic work and provider mutations use explicitly configured handlers; the runtime does not fabricate their results. Missing runtime or handler access leaves the dependent engine work item waiting.

Camunda owns durable process position, accepted work-item completion, human waits, retries, timers, escalations, incidents, parallel branches, process-definition versions, operational visibility, and execution history. BPMN defines the legal forward paths. Human decisions use native Camunda user tasks. Workers execute under at-least-once delivery and must be retry-safe. External writes use the [operation-adapter contract](operation-adapters.md).

Activation reserves a job until completion, failure, or activation timeout. A timed-out attempt may still execute while another worker receives the job. Only one completion advances that job, but duplicate external effects may already exist. Activation timeout does not itself consume retries. Neither activation nor resume creates an exclusive session or distributed epic/ticket lease. Neither local validation nor Camunda establishes exactly-once external effects, universal stale-worker fencing, or atomic effects across the engine and external destinations. See [Camunda job workers](https://docs.camunda.io/docs/components/concepts/job-workers/).

## Process identity and versions

Use a stable domain business ID for each root workflow, distinct from Camunda's system-generated process-instance key. Examples are `epic:EPIC-042`, `ticket:LIN-204`, `grounding:GRD-IMP-DEC-014-001`, and `research:RSR-LIN-204-003`. The grounding and research forms apply to standalone root instances. Call-activity children inherit the parent's business ID; their own packet IDs remain process variables or artifact references.

Enable `camunda.process-instance-creation.business-id-uniqueness-enabled` for active epic and ticket roots. Camunda scopes this uniqueness to the process definition and tenant. A repeated start conflict resolves the existing root instead of deliberately starting another. Completed or terminated roots permit reuse, so a late repeated start must reconcile the intended run before creating a successor. Migration can bypass the uniqueness check. An ambiguous lookup must report the matching roots for reconciliation rather than choose one arbitrarily. See [process creation and business IDs](https://docs.camunda.io/docs/components/concepts/process-instance-creation/).

Pin each runtime to Camunda 8.9 semantics and record the deployed definition ID, key, engine version, and framework version tag. The initial definition contracts are:

| Definition | Framework version tag | Scope |
|---|---|---|
| `epic-spec-workflow` | `v1` | Semantic specification through `HANDOFF_READY` |
| `ground-me-workflow` | `v1` | Integrated call activity or standalone grounding root |
| `multimodal-research-workflow` | `v1` | Research packet and controlled research result |
| `implementation-ticket-workflow` | `v1` | One ticket, its decisions, and one PR |

Program compilation and milestone coordination use versioned definitions selected by the explicitly invoked implementation compiler. The version tag is not assumed to equal Camunda's numeric deployment version. New instances use the selected deployed definition; running instances ordinarily finish on their original definition. Migration is an explicit operator action with a migration plan, validation, and tests. Existing jobs, user tasks, and variables survive migration; active job properties and mappings are not automatically recreated or reevaluated. See [process migration](https://docs.camunda.io/docs/components/concepts/process-instance-migration/).

## BPMN behavior in plain English

When a person starts an epic, the process drafts the First-Principles Basis from the permitted intake material and waits at a basis-approval user task. A request for changes returns to drafting. Approval of the exact basis version permits context gathering and reconciliation. Evidence that changes originating intent returns to the appropriate basis task with a successor record.

During design, a worker prepares the next unblocked question and the process waits at a decision user task. An answer is assessed against intent, evidence, and accepted decisions. A clean assessment is recorded automatically; material concerns activate an open-ended follow-up that presents evidence and a suggested change before the answer is recorded. A Ground Me action calls the grounding subprocess while preserving the unresolved question. That subprocess gathers code and dependency evidence, Git/GitHub and Linear lineage, Notion and ADR evidence, and useful LikeC4, Archify, or Figma projections. It waits at a separate understanding user task. Corrections or deeper investigation repeat that work. An explicit combined alignment and answer enters the same automatic decision assessment after exact packet and question verification. Alignment alone or changed evidence presents the current unresolved question. An aligned, validated finding that disproves the premise follows the modeled invalidation path and recomputes only affected decisions.

When factual research and human decisions permit review, semantic and architecture reviewers inspect the applicable evidence. Findings follow modeled routes to the earliest affected stage. A clean structured review continues automatically, and basis-bound repairs repeat drafting and review. Unresolved judgment uses a review-disposition user task. The final Linear proposal combines visual and specification approval in one bound user task; exceptions retain their human decisions. A passed automated validator supplies a gate result; it cannot complete a human task on the human's behalf.

Canonicalization workers publish normalized Notion drafts through adapters and verify readback. The process waits for approval of the exact reviewed content before finalizing the immutable release and handoff. The semantic process ends at `HANDOFF_READY`. An explicit implementation-compiler invocation consumes that handoff, compiles the Linear program, and starts permitted milestone and ticket work. Parallel BPMN branches follow approved ownership and native Linear dependencies. Ticket processes conduct single-PR implementation; integrated reconciliation and provenance-bounded cleanup finish the authorized delivery scope.

Camunda user tasks supply assignment, scheduling, forms, updates, and variable mappings. Chat or Linear can present an authorized task interaction, but a comment or local answer record alone does not advance the process. Bind the response to the active task and reviewed artifact revisions. See [native user tasks](https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/) and [response binding](workflow-records.md).

## Resume and client surface

`specflow` is a client and validation utility, with no independent workflow state machine. The following commands are implemented by the packaged runtime:

| Interface | Observable behavior |
|---|---|
| `specflow start <workflow-business-id>` | Start the selected deployed definition or reconcile the matching intended root. |
| `specflow status <workflow-business-id>` | Report root metadata and a readable current-stage summary with active branches, completed work, and waiting states. |
| `specflow inspect <workflow-business-id>` | Read process details and referenced evidence. |
| `specflow resume <workflow-business-id>` | Reconstruct permitted work from the current Camunda wait state. |
| `specflow correlate` | Submit an explicitly selected modeled event using its declared correlation contract; arguments depend on that deployed model. |
| `specflow validate` | Validate declared references and configured gates; see the [runtime command arguments](camunda-runtime.md). |

The installed CLI also exposes `init`, `validate-spec`, `validate-linear-plan`, `code-mass-policy`, and `cleanup-check`. Its local validators remain usable without claiming engine control. `init` creates artifact workspaces and does not start a Camunda process.

When resuming, resolve the active root by business ID within the configured cluster, tenant, and process definition. Confirm its recorded definition and version, then read current variables and artifact references. Resolve jobs, user tasks, incidents, and waiting events through the instance keys; those entities cannot be searched directly by business ID. Inspect all active branches, including relevant called subprocesses, instead of reducing parallel execution to one stage string.

Verify referenced artifact hashes and revisions, exact existing approvals, baseline freshness, incomplete write receipts, and configured static gate results. Reconcile incomplete external effects using their existing operation identities. A user task presents its pending human interaction. A service task permits normal worker activation. An event wait reports the required modeled event. An incident presents recovery. A completed process reports its final state. If a read is incomplete, stale, or inconsistent, refresh or report the unresolved state before taking its dependent action.

Resume does not activate or terminate arbitrary BPMN elements, acquire a workflow lease, or move process position to match a manifest. Process progress occurs only when Camunda accepts the active task/job completion or modeled event. Process-instance modification belongs to controlled operational repair: the engine cannot detect every invalid state an operator might construct. See [process modification](https://docs.camunda.io/docs/components/concepts/process-instance-modification/).

## Worker and incident behavior

Every worker uses stable operation identity, a deterministic normalized input hash, retry-safe computation, an operation-aware adapter for external mutations, explicit failure classification, a bounded activation timeout, and structured result/failure records. Preserve operation identity across attempts; issue a fresh attempt ID for each execution.

| Failure class | Worker and process outcome |
|---|---|
| Transient technical failure | Fail the job with the appropriate remaining retries and backoff. |
| Modeled business reaction | Throw the BPMN error handled by that model. |
| Unrecoverable technical failure | Fail with no retries, allowing Camunda to create an incident. |
| Superseded operation | Return a structured `SUPERSEDED` no-op result through the modeled branch. That branch resolves the current intended effect before dependent gates consume publication evidence; it never labels the stale effect as a successful current publication. |

After an external publication succeeds, a lost completion response must reconcile the publication and engine state. It must not create a new operation or republish blindly. A completion rejection does not undo external effects. The adapter receipt is recovery evidence, not proof that Camunda accepted completion.

An incident preserves the blocked execution point. An operator corrects the cause, restores job retries when needed, and resolves the incident through Camunda. A recurring cause may create another incident. Other parallel branches may still progress; an incident is not global workflow exclusivity. See [incidents and recovery](https://docs.camunda.io/docs/components/concepts/incidents/).

## Process data and validation

Process variables carry compact control data and references. Large research packets, source excerpts, diagrams, screenshots, and artifact sets stay in their owning storage systems. Camunda's 4 MB payload limit includes engine-internal data, so that value is not an available evidence-packet budget. See [variable limits](https://docs.camunda.io/docs/components/concepts/variables/).

```yaml
workflowBusinessId: epic:EPIC-042
epicId: EPIC-042
linearProjectId: PROJECT-042
linearIssueId: LIN-204
basisRef: FPB-LIN-204-001
basisHash: sha256:<basis-content-digest>
specReleaseRef: SPEC-REL-003
specReleaseHash: sha256:<release-content-digest>
activeDecisionRef: IMP-DEC-014
groundingPacketRef: GRD-IMP-DEC-014-001
researchPacketRef: RSR-REL-009
likeC4ViewRef: VIEW-006
archifyArtifactRef: ARCH-VIEW-006-003
figmaNodeRef: <reviewed-node-reference>
currentGateResults:
  firstPrinciples: PASSED
  research: PASSED
  adversarialReview: PASSED
```

Fields that are not yet established remain absent or explicitly unresolved. Parallel worker outputs use their declared mappings and references without blindly overwriting unrelated process data.

Static validation and Camunda orchestration establish different properties. Spec Kit, `specflow`, architecture, schema, and artifact validators establish structural validity and declared gate consistency. Camunda establishes durable BPMN position and accepted work-item completion. Neither establishes exactly-once side effects. The adapter declares which effects it can deduplicate, guard, conditionally write, or reconcile.

Runtime verification must exercise these observable contracts at the process and external-system boundaries: repeated starts, human waits and response binding, timeout/redelivery, duplicate effects and identity conflicts, superseded publication, exhausted retries and recovery, parallel waits, completion-response loss, and versioned resume. Local package tests are not evidence that those live integrations work.

## Supervisor design publication

The three planning processes use `publish_design_proposal` before their existing final user task. Follow the [document contract](supervisor-design-document.md) for composition, Linear publication, readback, and editorial review. The job returns `designProposalBinding` containing the current source and published document identity, revision, hash, matching readback, and visual references. The runtime validates that receipt before completing the job and validates the final response against the current source and document binding. Publication failures use the established retry and incident paths; requested changes repeat design and publication. The ordinary resume path preserves the deployed definition of running instances.

Definitions carrying `approvalPolicy: approval-economy-v1` implement [approval economy](approval-economy.md). Runtime evidence distinguishes inherited basis approval, automated verification, and human responses; a deployment does not migrate active instances.

[Stage visibility](stage-visibility.md) defines the shared agent heading and runtime stage projection. `status` observes the current work items; `resume` adds referenced-evidence checks. These reads do not move process position.

Follow [automatic step continuation](stage-visibility.md#automatic-step-continuation). Accepted completions lead directly to the next authorized work item, including routine checks and bounded retries. Stage headings report progress and introduce no additional approval. A continuous worker services configured handlers; a directly acting agent continues the same execution loop without a user continuation prompt.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.

## Individual issue review before assignment

The implementation program creates issues without assignees, then runs each issue’s complete ticket decision and supervisor-review loop. **Individual issue HITL** remains current until the entire created set finishes. Only then does **Team assignment** apply the approved workstream owners. Ticket execution reuses an exact, verified review. Follow [the issue review and assignment contract](issue-review-before-assignment.md) for jobs, publication variables, worker configuration, native approval checks, and provider readback.
