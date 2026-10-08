# Camunda runtime

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](workspace-and-destinations.md) for the portable workflow and actual adapter limits.

The Python 3.10+ `specflow` runtime uses Camunda 8.9 REST v2 at `http://localhost:8097`. `SPECFLOW_CAMUNDA_URL` and `SPECFLOW_CAMUNDA_TENANT` select another endpoint and tenant. `SPECFLOW_CAMUNDA_TOKEN` supplies a bearer token when needed. Commands accept `--url`, `--tenant`, `--config <json-file>` and `--json`. The default tenant is `<default>`.

## Commands and side effects

`specflow inventory-project-artifacts <directory> --source <program-binding.json> --json` reads every artifact file in the dedicated directory and returns a complete hashed inventory. It does not write files or contact Linear. The program workflow has an automatic `specflow.publish-project-resources` job after supervisor approval and immediately before issue creation. Its configured `project-resources` worker uploads through the Linear adapter, verifies current project resources and access, and binds the result before continuing. See [the project resource contract](project-resources.md) for worker configuration, adapter phases, publication fields, and recovery.

`specflow deploy` deploys the seven packaged BPMN definitions. All carry version tag `v1`; call activities use deployment binding so child definitions belong to the same deployment. The engine assigns numeric versions. Running instances remain pinned; this client exposes neither migration nor process modification.

`specflow start epic:EPIC-042 --variables input.json` creates an epic root using the highest deployed numeric version with the selected tag. `--version-tag v1` and `--definition epic-spec-workflow` select explicitly. Prefixes `grounding:`, `research:`, `program:`, and `ticket:` select their separate entry points. A matching indexed active root is returned unchanged. Concurrent start protection requires the cluster's `camunda.process-instance-creation.business-id-uniqueness-enabled: true`; a 409 is a rejected duplicate. Completed roots permit a later new run with the same ID. Search is eventually consistent; preserve the returned process key when the create response is available.

`specflow status epic:EPIC-042` reads root metadata and work items and displays the current scope, stage, branches, and waiting state. `specflow inspect epic:EPIC-042` reads root and child variables, jobs, tasks, incidents, elements, and message subscriptions. `specflow resume epic:EPIC-042 --key 2251799813686561` additionally checks declared artifact references and configured validators, and reports current work items. `specflow validate epic:EPIC-042` runs those same checks. These commands never change process position. A mismatched version tag or ambiguous active roots returns an error. The snapshot is eventually consistent, not atomic. Local artifacts use `artifactRefs: [{"path":"/absolute/evidence.json","sha256":"sha256:..."}]`; remote references use a named `validator` matched to an explicitly configured validator. Checks cover only declared references and validators, not all possible evidence.

`specflow activate specflow.draft-basis --timeout-ms 60000` activates at most one job. Save the returned job object to `job.json`. The actor performs the corresponding framework skill, then supplies `{"status":"completed","variables":{"basisBinding":{"ref":"FPB-042-001","hash":"sha256:..."}}}` in `result.json`. `specflow complete-job job.json result.json` submits that result. The engine, not a local manifest, determines the next element.

`specflow complete-task response.json` completes the exact native user task after matching its tenant, process key, element, declared action, actor, and reviewed-content binding:

```json
{
  "user_task_key": "2251799813687001",
  "process_instance_key": "2251799813686561",
  "element_id": "approve_basis",
  "actor": "Named reviewer",
  "action": "approved",
  "binding": {"ref": "FPB-042-001", "hash": "sha256:..."}
}
```

Task custom headers declare `bindingVariable`, `responseVariable`, and permitted `actions`. Evidence-producing workers supply the binding before reaching the task. Decision bindings include question and frontier revisions; grounding bindings include packet revision and source question. The CLI preserves the whole response envelope. Direct Camunda API operators remain responsible for equivalent evidence controls; the CLI is not an authorization boundary.

`specflow fail-job job.json failure.json` accepts `{"status":"transient","message":"upstream unavailable","retryBackOff":1000}`, `{"status":"unrecoverable","message":"invalid configuration"}`, or `{"status":"business_error","errorCode":"REVISE_FIRST_PRINCIPLES","message":"basis contradicted"}`. Transient failure decrements retries with backoff; unrecoverable failure exhausts retries and leaves an incident. The epic's applicable service tasks model the basis-revision error. Other unmodeled error codes produce incidents.

`specflow resolve-incident INCIDENT_KEY --retries 1` updates an incident job's retries, then requests incident resolution. Repair the underlying problem first. `specflow correlate specflow.pr.merged ticket:LIN-204 --message-id github-pr-204-merged --variables merge.json` publishes the merge event. `--ttl-ms 60000` permits buffering before a subscription exists. An accepted publication does not prove correlation; inspect the engine. The program completion event is `specflow.program.completed` correlated by `program:...` business ID.

## Worker and adapter protocol

`specflow worker --config worker.json --once` activates one job per configured type and exits. Without `--once` it polls until interrupted; `--poll-seconds` defaults to 2. The runtime never invents semantic work or approvals. Unconfigured job types wait durably in Camunda.

```json
{
  "operation_store": "/absolute/runtime/artifacts",
  "handlers": {
    "specflow.draft-basis": {
      "command": ["/absolute/approved-agent-handler"],
      "timeout_seconds": 120
    },
    "specflow.compile-visuals": {
      "command": ["/absolute/approved-visual-handler"],
      "timeout_seconds": 120
    }
  },
  "validators": [{"name":"evidence-validator","command":["/absolute/validator"],"timeout_seconds":60}]
}
```

The visual handler invokes an allowed renderer through `apply-operation` and returns its receipt in `visualBinding.visuals`.

Every service job carries `customHeaders.skill` and `customHeaders.phase`, selecting its installed framework skill and phase. The worker invokes the handler configured for that job type. The built-in `specflow.resume-grounded-decision` handler verifies and forwards explicit combined human answers; it performs no authoring or provider mutation. Read/computation handlers receive `{"job": <activated-job>}` on stdin and emit one structured completion or failure object on stdout. Their commands are explicit argument arrays, executed without a shell and with bounded timeouts. External mutations use adapter handlers with `operationRequest` and `operationIntent` in job variables. The intent supplies stable operation ID, target ID, generation, semantic revision, and expected target revision. The runtime binds the input hash, process, element, business ID, adapter, fresh attempt ID, and issue time.

`specflow hash-operation request.json` computes the normalized input hash, including bytes of artifact source files. `specflow apply-operation request.json token.json --store /absolute/artifacts --config adapters.json` applies a token-aware operation outside worker activation, returning a durable receipt. This command does not complete a Camunda job.

Artifact storage publishes `{"files":{"view.html":"/absolute/staged/view.html"}}`. Archify accepts `{"view_type":"architecture","model":{...},"renderer_version":"2.17.0-dev.1"}` and runs the configured CLI's showcase validation and HTML delivery. Its published model and HTML are an interactive projection; static exports use a configured `export_command` that accepts staging path, formats, and input hash on stdin and emits JSON after producing every requested `view.<format>` file. Missing exporters or files block publication. Browser visual review remains separate work. LikeC4 accepts artifact files and requires a configured `validate_command` that reads request/staging JSON and returns a JSON object on success.

The shared local SQLite operation registry and immutable directories supply `GUARDED_PUBLISH` for artifact storage, Archify, and validated LikeC4 sets. The authoritative pointer and operation receipt commit in one database transaction after publication checks. Use one registry on one local filesystem for all competing workers. This is not a distributed storage or lease protocol. Preserve both registry and published files together. An operation ID is bound to its complete stable identity. Attempt IDs and times do not change that identity. A target generation is bound across operation IDs; older generations return `SUPERSEDED`. A successor still pending publication makes a worker retry until it can resolve a published result.

Notion, Linear, GitHub, and Figma are configurable external command adapters. They require destination implementation and configuration; the package does not embed provider credentials or claim live provider writes. The adapter receives `{"phase":"reconcile","token":{...},"request":{...}}` and returns `{"status":"found","result":{...}}` or `{"status":"absent"}`. Only an established absence permits an `apply` request, which must return `{"status":"completed","result":{...}}` after durable readback. Configure its verified `IDEMPOTENT`, `CONDITIONAL_WRITE`, `RECONCILED`, or `BEST_EFFORT` guarantee. A materially harmful best-effort effect requires an accepted `risk_record`. The downstream implementation must implement that declared guarantee, including concurrent retry behavior; the local receipt cache cannot confer remote fencing.

## Process behavior

When an epic starts, a worker drafts the basis and a native task waits for a named reviewer's response to the bound version. Requested changes return to drafting. Approval permits context reconciliation and research. Research can repeat, request a human decision, or return to the basis. The decision process handles one question at a time. Ground Me investigates code and lineage in parallel, reviews provenance, produces visuals, and waits for understanding alignment. Corrections and deeper requests repeat grounding. A matching explicit combined answer enters decision recording; alignment alone presents the unresolved question, and validated invalidation recomputes the frontier. The parent drafts semantics and routes structured adversarial review to automatic continuation, scoped repair, or human judgment. It compiles visuals and publishes the Notion draft and Linear supervisor proposal, obtains one combined design and visual approval, then verifies the immutable handoff before ending at `HANDOFF_READY`.

When a separately requested program starts, it verifies unchanged basis inheritance or obtains approval of new intent, then presents its compiled program for final human review. Its compilation and publication jobs enforce [the three-person program contract](../../implementation-specification-compiler/references/three-person-workstreams.md) against the exact plan snapshot. Its Linear publication and dispatch workers create independently identified ticket roots for three milestone workstreams according to approved native Linear dependencies. The program waits for its completion event and reconciles before ending. Each ticket verifies its approved basis and receives final design review, runs single-PR implementation, waits for a verified merge event, then reconciles and cleans up. Dispatch and external evidence verification belong to configured handlers; the engine does not infer provider state from an event name.

## Sources

- [Camunda 8.9.18 REST v2 schema](https://github.com/camunda/camunda/blob/8.9.18/zeebe/gateway-protocol/src/main/proto/v2/rest-api.yaml)
- [Business IDs and uniqueness](https://docs.camunda.io/docs/components/concepts/process-instance-creation/)
- [At-least-once job workers](https://docs.camunda.io/docs/components/concepts/job-workers/)
- [Native user tasks](https://docs.camunda.io/docs/components/modeler/bpmn/user-tasks/)
- [Call activities and binding](https://docs.camunda.io/docs/components/modeler/bpmn/call-activities/)
- [Camunda Run configuration](https://docs.camunda.io/docs/self-managed/quickstart/developer-quickstart/c8run/configuration/)

## Final planning publication contract

`specflow.publish-design-proposal` is the configured authoring/publication job before the final review in semantic, program, and ticket planning. Follow the [supervisor document instructions](supervisor-design-document.md). The job headers declare `resultContract: linear-design-proposal-v1`, `planningScope`, and `sourceBindingVariable`. The source variable is `releaseBinding`, `programBinding`, or `ticketDesignBinding` respectively. The handler composes and edits the proposal, applies the authorized Linear operation, reads back and inspects the result, then emits this completion shape (example values):

```json
{
  "status": "completed",
  "variables": {
    "designProposalBinding": {
      "schema_version": 1,
      "scope": "program",
      "source": {
        "ref": "PLAN-042-R2",
        "hash": "sha256:plan-content-digest"
      },
      "document": {
        "id": "linear-document-id",
        "url": "https://linear.app/workspace/document/design-042",
        "revision": "provider-update-timestamp",
        "hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      },
      "readback": {
        "revision": "provider-update-timestamp",
        "hash": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
      },
      "visuals": [
        {
          "ref": "#proposed-workflow",
          "kind": "graph",
          "renderer": "archify",
          "artifact": {
            "path": "/published/generation-000003/view.html",
            "sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
          },
          "receipt": {
            "path": "/published/generation-000003/manifest.json",
            "sha256": "sha256:cccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccccc"
          }
        }
      ]
    }
  }
}
```

The [schema](../../implementation-specification-compiler/scripts/specflow_runtime/design-proposal.schema.json) travels with the runtime installation. A provider revision can be the fetched update timestamp when the API exposes no revision ID. Hash the read-back document content consistently. Visual references identify meaningful visuals present in the document; they do not prove successful rendering.

Configure an authoring/publishing command under `handlers["specflow.publish-design-proposal"]` using the existing command-handler protocol. This command applies the existing `linear` operation-aware adapter for its write and returns the compact binding above. A generic adapter handler returns an operation receipt, so a publishing command must reconcile that receipt and provider readback into the design binding. An unconfigured publisher waits; the runtime never generates a proposal or fabricates a provider receipt itself.

`complete-job` rejects an incomplete receipt, wrong scope, changed source, mismatched readback, invalid document identity/hash, or missing visual references with `invalid_design_proposal`. The automated worker reports an invalid publication result as an unrecoverable failure, creating a repairable incident. Retriable publication failures retain the established backoff protocol. Human `changes_requested` returns through the existing design and publication path.

The final approval tasks use `designProposalBinding` as their `bindingVariable`. `complete-task` takes the unchanged response envelope, with the entire document binding in `binding`. The former source-only value remains available under `binding.source`; its process source variable is retained. Response variable names and existing actions retain their meanings. Final tasks also accept `presentation_change` and `semantic_change`. Both the CLI and worker validate declared publication receipts. The CLI is not an authorization boundary for direct Camunda API callers.

This contract applies to definitions containing the publication step. Running instances keep their deployed numeric version and earlier binding shape; no migration is performed. The version tag remains `v1`, and new starts resolve its highest numeric deployment. Use configured Linear validators and live readback when presenting approval to detect intervening provider edits. Static receipt validation does not establish live publication, media access, editorial quality, or exactly-once effects.

## Graph renderer validation

Follow the [graph visual policy](graph-visual-policy.md) for the shared record shape and exact boundary requirements. `specflow validate-visuals <manifest.json> --json` validates a `{"visuals": [...]}` document without network access and returns `{"status":"ok","command":"validate-visuals","result":{"validated":1,"policy":"graph-renderers-v1"}}` for one valid visual. Invalid records or changed evidence return exit code 2 and `error.code: invalid_visual`.

BPMN job and task headers declare `visualPolicy: graph-renderers-v1`; designated visual steps also declare `visualBindingVariable` or `visualInventory: required`. Their handlers return explicit inventories, and the CLI checks embedded inventories at job completion, human review, resume, and publication. Existing records need classification and render evidence before passing these checks. Running definitions retain their original inventory-presence headers; the runtime still validates every declared inventory. A JSON renderer receipt is a trusted adapter assertion bound by hashes, not a cryptographic attestation of tool execution.

## Approval economy commands and payloads

[Approval economy](approval-economy.md) specifies `basisReuse`, `reviewResult`, final revision actions, `aligned_and_answer`, and the built-in response forwarding worker. `specflow prepare-response TASK_KEY --actor "Named supervisor" --action approved --json` reads current task evidence and returns `response` with `submitted: false`; it never completes a task. `--answer B` supplies an explicitly selected answer. The caller submits the returned response object with `complete-task` only after that human action.

Structured `transient` handler output is accepted with a nonzero exit code and consumes the existing finite retry budget. External unknown results reconcile before another effect; an unresolved readback exhausts retries into an incident.

## Stage presentation

`status` and `resume` print the [stage visibility report](stage-visibility.md) by default. Machine callers use `--json`; their existing result fields are retained with additive `progress` metadata. `inspect` and `validate` retain JSON output with the same projection. Stage labels apply to existing supported instances without deployment or migration.

Follow [automatic step continuation](stage-visibility.md#automatic-step-continuation). Accepted completions lead directly to the next authorized work item, including routine checks and bounded retries. Stage headings report progress and introduce no additional approval. A continuous worker services configured handlers; a directly acting agent continues the same execution loop without a user continuation prompt.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.

## Individual issue review before assignment

The implementation program creates issues without assignees, then runs each issue’s complete ticket decision and supervisor-review loop. **Individual issue HITL** remains current until the entire created set finishes. Only then does **Team assignment** apply the approved workstream owners. Ticket execution reuses an exact, verified review. Follow [the issue review and assignment contract](issue-review-before-assignment.md) for jobs, publication variables, worker configuration, native approval checks, and provider readback.
