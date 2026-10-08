# Operation-token-aware adapters

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](workspace-and-destinations.md) for the portable workflow and actual adapter limits.

This is the external-mutation contract for the [Camunda integration](camunda-orchestration.md). The [runtime](camunda-runtime.md) implements a shared local operation store, guarded artifact publishers, and configurable command boundaries for provider adapters. Each configured provider supplies and verifies its destination-specific mutation and reconciliation behavior.

## Operation identity

An operation token identifies one intended durable effect. It does not establish exclusive workflow ownership or universally fence a worker. Reads generally need no token. Index, cache, or persistent-dataset mutations in research systems use a separate maintenance-operation token.

```yaml
operation_token:
  workflow_business_id: epic:EPIC-042
  process_instance_key: "2251799813686019"
  bpmn_element_id: publish_architecture_view
  adapter: archify
  target_id: VIEW-006
  operation_id: OP-EPIC-042-VIEW-006-003
  operation_generation: 3
  semantic_revision: SPEC-REL-003
  input_hash: sha256:<normalized-request-digest>
  expected_target_revision: 2
  attempt_id: ATT-7f28
  issued_at: "2026-09-05T22:00:00Z"
```

`operation_id` stays stable across retries; `attempt_id` identifies one execution. `operation_generation` orders intended effects for the same adapter target, including effects with different operation IDs. `input_hash` identifies the normalized source, rendering/request options, and relevant tool version. Exclude attempt identity and issue time from that normalized input. `expected_target_revision` supplies a destination precondition where supported; otherwise record it as unavailable and declare the actual guarantee.

The same operation ID and input hash resolve to the same durable result. Reusing an operation ID for conflicting input produces `OperationIdentityConflict`. A newer intended effect uses a new generation or operation ID. Keep an existing operation ID bound to its input hash; allocate a new ID for changed input. Generation-only supersession can reuse unchanged content but cannot rebind that ID to different input. The target's current-generation record spans operation IDs, so a fresh ID cannot bypass stale-publication protection.

## Declared guarantee

Every adapter reports the strongest guarantee actually supported by its destination and records the mechanism and verification evidence. Capabilities can coexist; these labels are not a claim that all providers implement the same ordering or atomicity.

| Guarantee | Declared behavior |
|---|---|
| `IDEMPOTENT` | Repeating an intended operation returns or reconstructs the same result. |
| `GUARDED_PUBLISH` | Work may repeat, but only the current intended generation can become authoritative. |
| `CONDITIONAL_WRITE` | The destination enforces an expected revision, ETag, compare-and-set, or equivalent precondition. |
| `RECONCILED` | Duplicates can occur; the adapter detects them and repairs them deterministically. |
| `BEST_EFFORT` | Stronger protection is unavailable; its actual risk is recorded. |

Every externally visible write uses an operation-aware adapter and idempotency where possible. A `BEST_EFFORT` mutation requires an explicit risk record when duplication would be materially harmful. Do not require universal exclusion from a destination that only supports reconciliation. Do not describe a read-before-write check as native conditional writing.

## Adapter behavior in plain English

When a worker requests a mutation, the adapter validates the token and normalized input. It looks up the durable operation receipt within the configured destination scope. A conflicting identity fails explicitly. A matching completed receipt returns the recorded result without issuing the effect again; if it is no longer current, the result reports that fact and does not repromote it. A superseded unfinished attempt returns the superseded outcome.

The adapter records the intended operation, target, generation, attempt, and input identity before executing or staging work. Concurrent attempts for the same operation reconcile through destination idempotency or the durable receipt mechanism. This record stores only the state needed to recover that effect; it does not select workflow stages, acquire epic leases, or maintain a second orchestrator.

Before making staged work authoritative, the adapter verifies the intended target generation and source identity. A guarded publisher makes that precondition inseparable from updating the authoritative registry. A conditional-write adapter submits the destination's revision precondition. When those mechanisms are unavailable, the adapter uses its declared deterministic reconciliation policy or records the applicable accepted best-effort risk. A successful local generation check alone cannot close the race between checking and publication.

After mutation, the adapter reads back the result, records its stable references, revisions, hashes, guarantee, and reconciliation status, and returns a structured receipt to the worker. If the process crashes after the effect but before recording completion, a retry reconstructs the result from destination identifiers or markers. Uncertain outcome remains explicit until readback or reconciliation resolves it; a new attempt is not a new intended effect.

```yaml
operation_result:
  operation_id: OP-EPIC-042-VIEW-006-003
  operation_generation: 3
  input_hash: sha256:<normalized-request-digest>
  status: COMPLETED
  guarantee: GUARDED_PUBLISH
  target_id: VIEW-006
  target_revision: 3
  result_ref: ARCH-VIEW-006-003
  result_hash: sha256:<artifact-manifest-digest>
  reconciliation_status: VERIFIED
```

`SUPERSEDED` is an explicit no-op outcome. Transient failures, modeled business reactions, and unrecoverable technical failures follow the worker contract. A receipt never asserts that a corresponding Camunda completion was accepted.

## Adapter registry

`TokenAwareAdapterRegistry` resolves these contracts by adapter and destination. Provider names alone do not establish a guarantee.

| Adapter contract | Effect and recovery mechanism |
|---|---|
| `NotionCanonicalSpecAdapter` | Stable record IDs, normalized source hashes, targeted upserts, complete readback, and release reconciliation. |
| `LinearProgramAdapter` | Deterministic external identity, existing-object resolution, native relation reconciliation, and graph readback. |
| `GitHubChangeAdapter` | Deterministic branch/PR markers, existing-PR detection, and result reconciliation before retry. |
| `FigmaProjectionAdapter` | View registry, available node revision checks, structured/rendered readback, and reconciliation. |
| `LikeC4ArtifactAdapter` | Source-hash validation, immutable rendered generations, and guarded current-view publication when storage supports it. |
| `ArchifyArtifactAdapter` | Attempt-specific staging, typed-IR validation, delivery evidence, and generation-guarded publication. |
| `ArtifactStorageAdapter` | Immutable content-addressed objects, readback hashes, and a current-generation registry with its actual concurrency guarantee. |

Notion, Linear, GitHub, and Figma capability levels are verified per destination. Archify and LikeC4 guarded publication depends on the configured artifact storage and registry; rendering software alone does not provide distributed publication protection. Authentication and destination authorization remain separate from operation identity.

## Bounded technical recovery

Command adapters may emit `{"status":"transient","message":"provider unavailable","retryBackOff":1000}` on stdout with a nonzero exit. Classified outages and uncertain external outcomes use the existing finite Camunda retry budget. Each attempt reconciles the same operation identity first. A found effect completes with its receipt; confirmed absence permits the scoped write; uncertainty permits no repeat mutation and eventually leaves a repairable incident. Invalid configuration, missing authorization, and invalid evidence remain unrecoverable until repaired. See [approval economy](approval-economy.md).
