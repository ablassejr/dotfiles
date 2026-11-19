# Archify visual-artifact adapter

`ArchifyArtifactAdapter` is the specified operation-aware publisher for validated interactive technical projections. Archify means [tt-a1i/archify](https://github.com/tt-a1i/archify), whose typed JSON source produces self-contained HTML for architecture, workflow, sequence, data-flow, and lifecycle views, with static or animated exports. It is an external rendering capability, not an orchestration or semantic authority. The [runtime adapter](camunda-runtime.md) validates typed Archify input and publishes HTML with generation guards. Requested static formats use a configured export command and must all exist before publication. Browser visual review remains a separate evidence step.

## Visual authority and input

LikeC4 expresses formal architectural relationships and boundaries. Archify explains a normalized semantic or research model interactively. FigJam supports non-graph exploration and collaborative notes. Figma supplies curated high-fidelity publication. Select the representations needed by the question; Archify does not replace the formal model or ratify source semantics.

The following request envelope belongs to the adapter. `architecture_ir` is the normalized source model, not a claim that the illustrated fields are the native Archify JSON schema. Compile it to the installed Archify version's matching schema and record that version and the generated source hash. Use `architecture`, `workflow`, `sequence`, `dataflow`, or `lifecycle` as the view type.

```yaml
archify_render_request:
  view_id: VIEW-006
  view_type: architecture
  source:
    semantic_revision: SPEC-REL-003
    research_release: RSR-REL-009
    likec4_model_hash: sha256:<formal-model-digest>
  architecture_ir:
    components:
      - id: orchestration
        label: Camunda 8.9
      - id: visual_adapter
        label: Archify artifact adapter
    connections:
      - source: orchestration
        target: visual_adapter
        relationship: Activates rendering jobs
    boundaries: []
  rendering:
    theme: system
    motion: false
    exports: [html, svg, png]
  operation_token:
    workflow_business_id: epic:EPIC-042
    process_instance_key: "2251799813686019"
    bpmn_element_id: publish_architecture_view
    adapter: archify
    target_id: VIEW-006
    operation_id: OP-EPIC-042-ARCH-VIEW-006-003
    operation_generation: 3
    semantic_revision: SPEC-REL-003
    input_hash: sha256:<normalized-request-digest>
    expected_target_revision: 2
    attempt_id: ATT-7f28
    issued_at: "2026-09-05T22:00:00Z"
```

Source fields apply only when that source exists; record unavailable or inapplicable sources honestly. `view_id`, target identity, semantic revision, requested exports, and the token's normalized input must agree. Rendering options, source identities, and renderer version contribute to input identity. A retry preserves those inputs and operation ID.

## Rendering and publication in plain English

When Camunda activates the rendering job, the adapter applies the shared [operation-token checks](operation-adapters.md). A matching completed operation returns the existing artifact receipt. A superseded attempt cannot make its result current. Otherwise, the adapter compiles and validates typed Archify source and renders every requested export in an attempt-specific staging directory. Rendering is allowed to happen more than once.

The adapter uses the installed version's documented validation and delivery gate, then inspects the exact delivered artifact. Deterministic delivery receipts, browser evidence, and perceptual visual review are distinct evidence. Requested exports must exist and match the recorded source before the set is publishable. Failed validation or incomplete exports preserve diagnostics and leave the current published view intact.

After validation, the adapter rechecks the target's desired generation, source hash, and expected registry revision. It promotes a complete immutable artifact set and conditionally updates the current-view registry using a storage primitive that enforces that precondition at the publication point. A newer intended generation or a conflicting input prevents publication. The generation guard applies across operation IDs; checking only one operation record is insufficient.

The authoritative publication point is the conditional registry update. An immutable set can be staged or uploaded beforehand and remain unreferenced if that update loses a race. That state is recoverable evidence, not partial authoritative publication. An atomic local rename alone cannot protect a registry shared with other writers. Without a suitable registry primitive, report the actual weaker guarantee and do not claim `GUARDED_PUBLISH`.

After publication, read back the manifest and current registry, record artifact references and hashes, and return their compact receipt to Camunda. If the worker stops after publication but before receipt completion, its retry discovers the immutable generation and reconciles the registry. If another generation is current, it returns the earlier result as superseded rather than promoting it again. Discard or clean only that attempt's obsolete staging artifacts, preserving incomplete-operation recovery evidence.

## Artifact paths and receipt

The local runtime uses `<store>/staging/<operation-id-sha256>/<attempt-id-sha256>/` and `<store>/published/<target-identity-sha256>/generation-000003/`. The target identity is the workflow business ID, adapter, and target ID. Directory names are encoded; consumers use the returned manifest path. Each Archify set contains its typed model, validation and delivery JSON receipts, HTML, and every requested static export. These paths belong to the configured external artifact workspace.

The artifact manifest binds view ID, generation, operation identity, semantic/research references, renderer version, normalized input hash, native IR hash, validation/delivery evidence, and each output's path, media type, and content hash. The current-view registry is a separate pointer:

```yaml
view_id: VIEW-006
current_generation: 3
input_hash: sha256:<normalized-request-digest>
artifact_manifest: <store>/published/<target-identity-sha256>/generation-000003/manifest.json
published_by_operation: OP-EPIC-042-ARCH-VIEW-006-003
```

The registry also tracks the currently intended generation and its identity while an update is being rendered, so an older attempt cannot publish after newer intent supersedes it. The last published view may remain readable while its successor is pending.

```yaml
adapter: archify
guarantee: GUARDED_PUBLISH
guarantees:
  duplicate_generation_is_reused: true
  stale_generation_can_publish: false
  published_artifacts_are_immutable: true
  source_hash_is_recorded: true
  validation_required_before_publish: true
does_not_guarantee:
  worker_executes_only_once: true
  duplicate_compute_is_prevented: true
```

This declaration is valid only after the configured publisher demonstrates those behaviors. Integration verification must cover duplicate delivery, conflicting input identity, an older generation racing a newer one, validation/export failure, and recovery after publication but before recording completion. No runtime verification of this adapter is supplied by the local framework tests.

## Graph renderer enforcement

The [graph visual policy](graph-visual-policy.md) requires Figma Design, LikeC4, or Archify for every graph-like output, including provisional, published, and as-built views. Record the content kind, renderer, exact artifact, and completed render receipt; validate them before presentation or gate completion. FigJam remains available for non-graph exploration. Delivery formats and screenshots of diagrams do not bypass the policy.
