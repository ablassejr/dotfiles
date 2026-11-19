# Workflow records and implementation handoff

This reference describes the explicitly selected Linear/Notion/Camunda adapter profile. Apply its provider-specific schemas and operations only in that configured workflow. For other projects use [workspace and destinations](workspace-and-destinations.md) and the provider-neutral scope contracts.

Apply [review and artifact design](review-and-artifact-design.md) to any human-facing document or reference. The records below support execution, traceability, and recovery; they are not additional documents for the team to review. Keep internal paths and machine envelopes in operator evidence, and publish descriptive shared references for the material the team needs.

## Camunda state and external evidence

Camunda is the authoritative execution record. The existing external `specflow.manifest.json` retains its schema-v3 semantic fields, provenance, and recovery evidence. An optional `orchestration` object records a derived engine snapshot and references; it cannot authorize a transition or override the current process position. `specflow validate-spec` checks its documented semantic envelope, not live engine state or this integration envelope. See [Camunda orchestration](camunda-orchestration.md).

| Field in `orchestration` | Meaning |
|---|---|
| `engine`, `engine_version` | `camunda` and the verified 8.9 runtime version |
| `workflow_business_id`, `scope` | Stable root business identity and owning scope |
| `process_instance_key`, `tenant_id` | Engine identity in the configured cluster/tenant |
| `process_definition` | Definition ID, key, numeric deployment version, and framework version tag |
| `observed_at`, `active_work_items` | Observation time and all observed user tasks, jobs, events, incidents, and active branch references |
| `basis_ref`, `repository` | Approved basis lineage and exact repository baseline with freshness evidence |
| `sources`, `artifacts` | Stable IDs/locations, revisions, hashes, provenance, and freshness |
| `decision` | Active question, frontier revision, Grounding Packet reference, and response binding |
| `research_gate`, `reviews`, `approvers` | Gate result references, findings, and approvals bound to reviewed revisions |
| `writes` | Operation tokens, actual adapter guarantees, target revisions, receipts, readback, and reconciliation state |
| `managed_files`, `created_external_records`, `cleanup` | Provenance, authorized mutation scope, ownership, and verified disposition |
| `handoff_ref` | Immutable package location, hash, release binding, and readback result |

Do not put full packets, screenshots, or diagram content in process variables. Store compact references and hashes in Camunda, with reconstructable content in its owning artifact store. Local `stage`, `state`, or historical transition fields are compatibility summaries only; an observed snapshot can be stale as soon as it is read. A manifest revision versions an artifact and does not act as a workflow fencing token.

At intake, keep repository fields unresolved until basis approval. `specflow init` optionally creates a fresh artifact workspace; it does not create an engine instance. Existing work resolves its Camunda root and reconciles the referenced manifest without reinitialization. Historical workflows without an engine binding require an explicit, evidence-grounded onboarding or repair plan. A local `stage: approved` does not justify skipping BPMN user tasks or synthesizing approval. Reuse actual approval evidence only where the selected model and reviewed content support it.

This partial snapshot illustrates a pending visual review; its keys and timestamps are examples, not live engine evidence.

```json
{
  "orchestration": {
    "engine": "camunda",
    "engine_version": "8.9",
    "workflow_business_id": "epic:EPIC-042",
    "scope": "semantic",
    "tenant_id": "<default>",
    "process_instance_key": "2251799813686019",
    "process_definition": {
      "id": "epic-spec-workflow",
      "key": "2251799813686001",
      "version": 1,
      "version_tag": "v1"
    },
    "observed_at": "2026-09-05T22:00:00Z",
    "active_work_items": [
      {
        "kind": "USER_TASK",
        "element_id": "approve_visuals",
        "user_task_key": "2251799813686051",
        "artifact_ref": "ARCH-VIEW-006-003",
        "artifact_hash": "sha256:<artifact-manifest-digest>"
      }
    ]
  }
}
```

Read the active task and exact referenced visual/source revisions before presenting approval. A revised view or changed source invalidates the affected review binding. An old local snapshot cannot complete a different current task.

## Packet and human-response binding

The parent binds the active Camunda user task to a `response_binding` and retains a snapshot inside `orchestration.decision`. It records `process_instance_key`, `user_task_key`, `bpmn_element_id`, `question_id`, `frontier_revision`, `packet_id`, and `packet_hash`; `packet_id` copies the packet's existing `grounding_id` exactly and never allocates another identity. Packet fields are null for an ordinary decision without grounding. The parent also records the displayed checkpoint/message reference. Associate the returned human action with that displayed binding rather than attaching an old response to whichever question is current.

Before using `advance_decision.py` or accepting an understanding response, compare the binding with the active Camunda task and current question, frontier, and packet. A changed revision or packet makes the response stale; preserve it as evidence, re-present the current checkpoint when needed, and do not record a decision or alignment against unseen content. The packet and action JSON keep their existing public schemas. The envelope belongs to the Camunda task context and its referenced evidence, not as an extra packet property. Existing helper validation alone does not enforce this binding or advance Camunda. Submit the authorized human response only through the bound active user task; preserve a rejected or stale response as evidence without applying it to another task.

```json
{
  "response_binding": {
    "process_instance_key": "2251799813686019",
    "user_task_key": "2251799813686051",
    "bpmn_element_id": "confirm_understanding",
    "question_id": "D-7",
    "frontier_revision": 4,
    "packet_id": "GRD-queue-007",
    "packet_hash": "sha256-of-the-exact-displayed-packet"
  }
}
```

## Immutable handoff package

Prepare the handoff outside the product repository, then publish it to the authorized durable shared destination and retain that reference in the manifest and approved release. Identify it as the exact release-and-verification record for the implementation compiler, with its scope, status, and governing release apparent. It references approved content instead of repeating the design narrative. If a destination or team access is missing, retain the prepared package and request only that missing decision; do not report a local package as `HANDOFF_READY` for the team. Use `schema_version: 1` and `kind: specflow.semantic-handoff`. This is the skill's record format, not a new CLI subcommand. A successor package gets a new ID and a `supersedes_handoff_id`; preserve earlier packages and hashes.

| Field | Required content |
|---|---|
| `handoff_id`, `schema_version`, `kind`, `supersedes_handoff_id` | Immutable identity, format version and optional predecessor |
| `notion_release` | Approved immutable release ID/URL, release revision/hash, and exact constituent record revisions/hashes |
| `basis_lineage` | Approved basis IDs/versions, supersession and approval evidence |
| `repository` | Exact identity, target branch, baseline commit, and freshness verification |
| `semantic_refs` | Requirement, constraint, decision, risk, evidence, and architecture-view IDs; resolved authoritative references |
| `grounding_refs` | Normalized conclusions, provenance, understanding alignment, packet revisions and source references |
| `subtractive` | Opportunity Map, accounting assumptions, approved subtractive decisions/exceptions, and credit evidence or `UNKNOWN` estimates |
| `nonblocking_risks`, `deferred_questions` | Explicitly nonblocking residuals, rationale and named owners; never hidden blocking questions |
| `non_goals`, `prohibited_changes`, `compiler_constraints` | Approved boundaries and implementation-partitioning constraints |
| `sources`, `artifacts` | Immutable identifiers/locations, source revisions and content hashes |
| `semantic_approval` | Named approver, exact reviewed content/revisions, and approval time |
| `verification` | Readback evidence, reference integrity, baseline freshness, visual/source alignment, removal-credit disposition, blocking-question check, verifier and time |

Use explicit empty collections when no record is applicable; do not invent risks, exceptions, requirements, acceptance conditions, or visuals to populate the package. Preserve `UNKNOWN` estimates as hypotheses with no removal credit. Block handoff for blocking semantic questions, unresolved publication mismatch, stale baseline, unapproved visual source mismatch, ungrounded removal credit, or missing authoritative references.

After writing the package, read it back, verify its contents and hash, and publish its reference through the owning Camunda work item, retaining a snapshot in `orchestration.handoff_ref`. Carry forward the already satisfied semantic approval when exact content and revisions still match; package verification and the `HANDOFF_READY` checkpoint do not create an additional approval gate. Report `HANDOFF_READY` only with verified shared release, design proposal, and handoff links labeled by their distinct purpose and the intended team’s access checked. A later explicit implementation-compiler invocation verifies this package and its current source binding. The compiler verifies unchanged approved basis reuse or obtains approval for new program intent before context loading; ticket scopes preserve the same lineage and reuse rules.

## Supervisor proposal evidence

Retain the scope’s Linear supervisor design document reference, source binding, published revision/hash, matching readback, visual references, and existing final approval response with the durable workflow evidence. The runtime shape is [design proposal schema v1](bundled/implementation-specification-compiler/scripts/specflow_runtime/design-proposal.schema.json). The document explains its source; it does not become a second semantic or dependency authority.

## Graph renderer enforcement

The [graph visual policy](graph-visual-policy.md) requires Figma Design, LikeC4, or Archify for every graph-like output, including provisional, published, and as-built views. Record the content kind, renderer, exact artifact, and completed render receipt; validate them before presentation or gate completion. FigJam remains available for non-graph exploration. Delivery formats and screenshots of diagrams do not bypass the policy.

## Approval economy evidence

The [approval economy contract](approval-economy.md) defines `basisReuse` input, engine-derived `basisInheritance`, reviewer `reviewResult`, derived `reviewVerification`, and presentation `revisionGuard` snapshots. A combined Ground Me response adds `decision.binding` and an explicit `decision.answer` to the existing human-response envelope. Forwarding retains `sourceGroundingResponse` and the human actor; it creates no decision task key. Keep these records distinct from an independent human approval.

The [stage visibility contract](stage-visibility.md) presents scope, active branches, revisited stages, latest completed work, and the current waiting state. Its timestamped projection is derived from Camunda and is not a persisted execution authority.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.
