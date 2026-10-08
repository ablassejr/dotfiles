---
name: visual-language-compiler
description: Compile approved semantic records into validated LikeC4 formal models, Archify interactive artifacts, and governed Figma projections with stable view identities and read-back visual verification.
---

# Visual language compiler

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run the visual-language stage of `$epic-spec-workflow`. Start with the communication job and approved semantic IDs. Use FigJam for non-graph exploration, LikeC4 for formal architecture structure, Archify for validated interactive technical explanation, and Figma for the curated communicative projection; none of them may change semantic intent.

Maintain stable `VIEW-*` entries that bind source semantic IDs, LikeC4 views, Archify manifests/generations, Figma or FigJam nodes, embeds in the selected documentation home, source hashes, operation receipts, revisions, and verification state. Use the approved component library, connector grammar, variants, variables, styles, and auto layout rather than inventing one-off forms.

Route external visual writes through [operation-aware adapters](references/bundled/epic-spec-workflow/references/operation-adapters.md). `ArchifyArtifactAdapter` follows [the staging and guarded-publication contract](references/bundled/epic-spec-workflow/references/archify-adapter.md), including native IR validation, delivery evidence, immutable artifacts, and conditional current-generation publication.

Validate the LikeC4 model through its documented compiler interface. After a Figma or FigJam write, fetch structure and inspect a rendered screenshot for clipping, overlap, hierarchy, connectors, and readability. Return verified shared links and any mismatch to the owning workflow. Give each view a caption explaining its distinct question and status; use the existing combined final review rather than a new prompt per visual.

Before publication, verify baseline and source freshness. Apply [visual feedback routing](references/bundled/epic-spec-workflow/references/visual-language.md): `SEMANTIC_CHANGE`, `FORMAL_ARCHITECTURE_CHANGE`, `EXPLORATORY_CHANGE`, `PRESENTATION_CHANGE`, or `SOURCE_MISMATCH`. Run architecture review against the formal model, then include those exact views and source revisions in the combined final supervisor review. A source mismatch blocks publication.

## Supervisor proposal publication

For `publish_design_proposal` jobs in semantic, program, or ticket planning, follow the [supervisor design document contract](references/bundled/epic-spec-workflow/references/supervisor-design-document.md). Compose and edit a self-contained explanation with optional depth, using only media that serve distinct communication jobs for a human with no starting context, publish it to the selected document home through its supported authorized operation, and verify content and available rendered visuals by readback. Bind the existing final approval to the exact document and source revision. When the configured runtime requires `designProposalBinding`, return that actual adapter receipt; another destination does not require a synthetic receipt. This phase explains the current proposal and does not redefine or approve its source.

## Deterministic renderer gate

Read the [graph visual policy](references/bundled/epic-spec-workflow/references/graph-visual-policy.md) before any graph-like visual work. Use only Figma Design, LikeC4, or Archify, including provisional and exploratory graphs. Classify content separately from delivery format, retain the renderer operation receipt and artifact hash, and run `specflow validate-visuals <manifest.json> --json` before presentation. Return the complete `visuals` inventory in the job’s declared binding. Non-graph exploration may use FigJam; graph-like FigJam output does not pass this gate.

Follow [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md) for the scope’s evidence-bound automatic routes, combined final visual/design review, targeted revision, and existing authorization. Automatic review records remain distinct from human approval.
