---
name: ground-me
description: Reconstruct why a code, architecture, ticket, interface, or behavior exists by tracing current implementation, history, decisions, and still-valid forces; use standalone or from a pending framework decision.
---

# Ground Me

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Ground Me reconstructs the provenance, forces, evolution, and present validity of a decision or implementation state. It is not a general codebase summary and it does not assume that current code is justified.

Use it from any material decision question or as a standalone investigation. An integrated invocation receives the current unresolved decision, approved First-Principles Basis, target, current-state map, and known source references. A standalone invocation infers the target, the decision or understanding this work will support, and whether its rationale is semantic, architectural, implementation, or operational; ask only when one cannot be responsibly inferred. Integrated mode also inherits the exact repository baseline and source revisions. Standalone mode does not initialize an epic or require an unrelated epic basis.

Follow [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md). If the configured Camunda profile governs this scope, integrated grounding uses its actual call activity and user-task bindings under [the Camunda contract](../epic-spec-workflow/references/camunda-orchestration.md). Otherwise use the current conversation and governing records for the understanding checkpoint; a standalone investigation does not require a process engine or a particular tracker.

Read [source traversal](references/source-traversal.md), [evidence ranking](references/evidence-ranking.md), and [provenance classification](references/provenance-classification.md). Read [multimodal rendering](references/multimodal-rendering.md) when a visual would materially improve the explanation.

## Research sequence

1. Establish what exists now and pin repository identity, baseline, and source revisions. Follow [shared tool routing](../epic-spec-workflow/references/tool-routing.md), including stricter explicit session rules. Use CodeGraph before direct structural search when indexed, semantic retrieval for relevant source and tests, and verify decisive claims in source.
2. Trace the relevant path or symbol through Git. Find modifying commits and the introducing commit; do not mistake a later refactor for the original decision. Verify nontrivial or version-sensitive Git and lineage-helper operations through the shared CLI capability-record policy.
3. Resolve commits and branches to pull requests. Inspect descriptions, linked issues, review conversations, failed checks, follow-ups, reversions, and replacements.
4. Traverse the related issue graph in the current project outward through parents, projects, milestones, native relations, comments, predecessors, and successors. The rationale may live outside the implementation ticket.
5. Establish chronology across approved specification revisions, decision records, ADRs, LikeC4, Archify, FigJam, Figma, and prior implementation specifications. Determine whether documentation preceded the implementation or documented it after the fact.
6. Use exact-version documentation and primary-source external research only where an external platform, library, protocol, regulation, or former version may have supplied the force. Compare the historical version with the current one.
7. Reconstruct the evidence graph from goal to requirement, decision, ticket, pull request, commit, symbol, test, and current behavior. Preserve conflicts and gaps.

Run a separate provenance review of the source evidence before the understanding checkpoint. Challenge post-hoc intent, correlation presented as causation, unsupported inference, and historical constraints presented as permanent. Record findings with affected IDs, evidence, earliest repair stage, downstream invalidation, and approval impact using the shared review contract. Rank evidence and classify provenance using the packaged references. Keep explicit rationale separate from inference. Never manufacture a respectable reason when evidence is absent. Distinguish constraints that remain current from expired constraints and unresolved ones.

For a `deletion_candidate`, determine why the code was introduced, which requirement or incident motivated it, what constraint existed, whether that constraint remains, which tests and consumers depend on it, whether it was temporary, whether another implementation supersedes it, and whether removal changes behavior or only machinery. Record `SAFE`, `SAFE_WITH_REPLACEMENT`, `REQUIRES_GROUNDING`, `BLOCKED_BY_CURRENT_CONSTRAINT`, `BEHAVIOR_STILL_REQUIRED`, or `UNKNOWN`. A replacement is safe only when its observable behavior is verified.

## Grounding Packet

Produce internal verification evidence conforming to [the packaged schema](schemas/grounding-packet.schema.json). Present a clearly titled answer to the triggering question in the existing proposal or evidence section: what the sources establish, what remains uncertain, and how that changes the decision. Keep the full packet available as optional shared evidence when needed, with its purpose, status, and source binding explicit; do not make schema fields, a local path, or the full traversal history the review experience. It always contains a concise current model, dependencies and affected surfaces, explicit coverage results for current state, Git, pull requests, issue history, semantic authority, and external forces, an evidence timeline, decision-lineage graph, a small set of decisive linked excerpts, confidence, provenance classification, decision implications, the understanding checkpoint, and an explicit ephemeral-workspace disposition. A deletion packet also records introduction sources, original reason and constraint, current replacement, deletion recommendation, required behavioral verification, and removal-credit state. A missing source is recorded as searched but not found, unavailable, or not applicable rather than filled with invented rationale. Add LikeC4, Archify, FigJam, Figma, code, or diff views when their communication job warrants them; an architecture target requires a Figma, LikeC4, or Archify graph, and an interaction target requires Figma.

Validate the packet with:

```text
python3 scripts/validate_grounding_packet.py <grounding-packet.json> --json
```

At the existing understanding checkpoint, present the concise reconstructed conclusion and the decision implication, then ask whether that understanding matches, needs correction, or needs deeper grounding. Do not restart first-principles intake or ask the human to approve each source or visual. Alignment alone leaves the implementation decision unresolved. In an integrated decision, offer the explicit `aligned_and_answer` action described by [approval economy](../epic-spec-workflow/references/approval-economy.md) when the human can choose both together. Preserve the separate packet and decision bindings.

Keep deletion credit `PROVISIONAL` while understanding is pending or deeper grounding is requested. A confirmed or corrected understanding with `SAFE` or behaviorally verified `SAFE_WITH_REPLACEMENT` can establish packet-level `VALIDATED` evidence. Budgeted or committed removal credit additionally requires identified requirements and consumers, evaluated current necessity, applicable restoration/rollback, and named-human approval of semantic consequences. An unapproved semantic-stage candidate remains a hypothesis regardless of packet validation. Required behavior, blocked constraints, unknown provenance, and unverified replacements receive no credit.

Before returning from the grounding branch, validate the confirmed or corrected checkpoint with:

```text
python3 scripts/validate_grounding_packet.py <grounding-packet.json> --require-aligned-understanding --json
```

For an integrated invocation, keep the triggering decision unresolved. Ground Me may advance neither the decision nor its frontier. When evidence invalidates the premise, record the finding while understanding remains pending; complete understanding alignment and the aligned-packet validation before emitting workflow result `QUESTION_INVALIDATED` with the helper's existing JSON result `question_invalidated`. Return the evidence to the parent decision workflow. The parent verifies the current question and response binding, using the modeled result path and actual user-task identity when a configured engine governs the scope. It preserves the old question as evidence, removes it from the active frontier, and publishes the recomputed affected frontier through an operation-aware adapter without selecting an answer. When the premise survives, the parent verifies and records an explicit combined answer against the same packet and question, or presents the current unresolved question. Ground Me returns the evidence and human response; the parent owns decision recording.

Use [the manifest response binding](../epic-spec-workflow/references/workflow-records.md) to bind the packet and human action to the question, frontier revision, and packet hash. The published packet schema has no frontier-revision field and rejects extra fields; do not insert one or change helper JSON. The parent validates the envelope, including the actual engine user-task key when applicable, before invoking helpers or accepting a response. Keep render receipts and source bindings in the view registry. Each `visuals` entry retains `type` and `ref` and adds the shared content `kind`; graph entries also include `renderer`, `artifact`, and `receipt` according to the packaged schema. This additional projection does not replace the packet's existing LikeC4/Figma requirements.

Persist only the normalized grounding conclusion and source references in the authoritative records in the documentation or issue home selected by the current scope. Keep raw extraction, temporary timelines, scratch notes, indexes, unapproved reconstructions, and temporary visual exports outside the implementation repository and ephemeral.

## Graph visual gate

Apply the shared [graph visual policy](../epic-spec-workflow/references/graph-visual-policy.md) to every graph-like output. Use Figma Design, LikeC4, or Archify and retain matching render-operation and artifact evidence. Include all produced or published visuals in the current step’s inventory and run `specflow validate-visuals <manifest.json> --json` before presentation. A missing renderer or invalid receipt blocks the visual output. Non-graph media keep their own communication purpose.

Use `source_coverage.issues` and `deletion_safety.introduced_by.issue` for provider-neutral packet records. The validator and schema also accept the legacy `linear` and `linear_issue` fields. Source coverage may be `not_applicable` when the project has no tracker; record real work-item provenance without inventing provider IDs. Normalized evidence may live in the project's canonical repository documentation. The persistence restriction applies to raw scratch artifacts, not the selected durable documentation.
