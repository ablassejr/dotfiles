# Visual language and review

## Model and projections

LikeC4 records systems, containers, components, actors, boundaries, and typed relationships in reviewable text. Use it when the specification makes structural architecture claims. Archify renders validated interactive technical explanations from normalized semantic or research models through [ArchifyArtifactAdapter](archify-adapter.md). FigJam holds temporary non-graph exploration and workshops; use it only when collaborative spatial exploration adds value. Figma Design holds polished, reviewed communication views; use it when an audience needs a durable visual explanation. An epic uses only the projections that serve a distinct communication need under [review and artifact design](review-and-artifact-design.md). Give each view a descriptive title, purpose, status, and readable caption; do not reproduce the same explanation across multiple tools. Internal model paths belong in verification records, while shared outputs use verified durable view or source links. The semantic need selects the projection, and the specification's view registry links each selected projection to the records it explains.

When Figma is selected, use one file per epic. Keep a visual-system page and only the named pages the approved communication need requires, such as overview, context, architecture, flows, state, alternatives, decisions, risks, implementation mapping, or superseded views. Every durable frame has a stable `VIEW-###` identity.

## Core grammar

Represent actors, systems, services, capabilities, operations, data stores, external boundaries, decisions, risks, invariants, open questions, evidence, and execution state as named components. Variants carry proposal state, authority, boundary, lifecycle, and emphasis. Connectors have a typed relationship and direction. Color never carries meaning alone.

Every visual element that asserts semantic content includes or links a stable semantic ID. Decorative layout has no semantic authority.

## View registry

For each view record its ID, epic ID, title, type, notation, projected semantic IDs, LikeC4 source path or model element, Archify artifact/manifest and generation, Figma or FigJam node URL, projection status, source hash, operation receipt, last verification time, superseded view, audience, and reviewer.

## Review loop

Read the semantic records and current canvas before changing a view. Resolve the exact LikeC4 path, Archify view registry, or Figma/FigJam file and page, produce a scoped patch plan, and show the planned mutation. Use existing human authorization for that destination and scope; obtain authorization only when the intended write is not already covered. Route each external mutation through its operation-aware adapter and preserve approved layout unless source structure changed. After the write, read the structured projection and inspect its rendered form. Archify publication additionally validates native IR, stages per attempt, retains immutable generations, and conditionally updates the current-view registry. Record deterministic delivery evidence, browser evidence, and perceptual review separately. Check labels, stable IDs, clipping, connector direction, overlap, text overflow, hierarchy, and accessibility. Show the exact view in the final supervisor proposal, which combines design and visual review under [approval economy](approval-economy.md). Record `approved` only after the human accepts that exact rendered result through the scope's bound approval record or actual engine user task when configured. A layout request changes the projection; a semantic request returns to the semantic workflow.

## Review response routing

Classify each response before changing an artifact.

| Response | Owning action |
|---|---|
| `SEMANTIC_CHANGE` | Return to the earliest affected requirement, decision, or basis; invalidate dependent approval. |
| `FORMAL_ARCHITECTURE_CHANGE` | Update and validate LikeC4, run the architecture review, then regenerate affected projections. |
| `EXPLORATORY_CHANGE` | Update non-graph FigJam exploration without changing canonical semantics. |
| `PRESENTATION_CHANGE` | Update the selected Archify or Figma projection while preserving meaning and formal structure. |
| `SOURCE_MISMATCH` | Stop publication and reconcile the projection with its authoritative source. |

An architecture reviewer separately challenges ownership, coupling, boundaries, authority, data flow, failure propagation, and deployment implications before the formal model is accepted. A visually polished result cannot compensate for a source mismatch.

Before publishing a visual, verify the repository baseline and source revisions, mark affected views stale when inputs change, and reconcile them. Read back structure and rendered form after mutation, then bind human approval to that exact view and source hash. A concurrent edit invalidates the affected verification; an earlier approval cannot be applied to a different frame revision.

## Graph renderer enforcement

The [graph visual policy](graph-visual-policy.md) requires Figma Design, LikeC4, or Archify for every graph-like output, including provisional, published, and as-built views. Record the content kind, renderer, exact artifact, and completed render receipt; validate them before presentation or gate completion. FigJam remains available for non-graph exploration. Delivery formats and screenshots of diagrams do not bypass the policy.
