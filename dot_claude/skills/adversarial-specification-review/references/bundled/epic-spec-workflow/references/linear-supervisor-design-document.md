# Supervisor design document

This reference describes the explicitly selected Linear/Notion/Camunda adapter profile. Apply its provider-specific schemas and operations only in that configured workflow. For other projects use [workspace and destinations](workspace-and-destinations.md) and the provider-neutral scope contracts.

At the end of planning, publish one self-contained design proposal in Linear for the team and its design reviewer. It explains the recommendation and consequential choices for this scope; the existing final approval reviews this document with its exact source revision. Apply [review and artifact design](review-and-artifact-design.md) for artifact ownership, document identity, focused prompts, and team-accessible references.

## Explain the design

Use a descriptive project-and-role title. Open with the document’s purpose, intended reader, responsible owner or team, draft or approval status, governing source, and the review action needed now. Establish who faces the problem, what happens today, why it matters, and the outcome being proposed. Introduce unfamiliar actors and terms where the reader first needs them. Make the recommendation and the decision requested of the supervisor easy to find.

Choose the clearest medium for each idea. When either a visual or text could communicate it, prefer the visual. Use diagrams for relationships, boundaries, flows, state changes, and failure recovery; annotated screens or prototypes for user experience; and compact comparison tables for alternatives and tradeoffs. Use an interactive view or short demonstration when interaction or motion explains something a static view cannot. Select media for their explanatory value, without a fixed diagram count or a requirement to use every tool.

Give each visual a clear reading order, meaningful labels, and the context needed to interpret it. Distinguish observed current behavior, the proposed design, assumptions, and unresolved choices within the visual. The reader must be able to understand the proposal inside the Linear document; an external interactive artifact can add depth. Provide a readable static view when an embed cannot render for the intended reader.

Show how the design behaves from the initiating action through its observable outcome, including material alternatives, concurrency, failures, and recovery. Explain the boundaries, compatibility, data consequences, rollout, rollback, and verification that affect this decision. Include relevant costs and uncertainty without inventing estimates. Comprehensiveness means the supervisor can evaluate the whole proposal; supporting inventories, audit evidence, source evidence, and detailed implementation records belong behind descriptive, verified shared links unless they are necessary to understand the choice. Repository evidence uses hosted revision permalinks. No required explanation or evidence may depend on a local file, scratch path, localhost view, or opaque artifact name.

Do not repeat in prose information already conveyed by a visual. Add text only when it supplies missing context, explains a consequence or tradeoff, qualifies uncertainty, or states the decision. Useful alt text is an accessibility equivalent, not a second narrative section. Links provide evidence and optional depth; following them must not be a prerequisite for understanding the proposal.

## Edit for the reader

Read the complete document as a teammate arriving without the conversation. Identify duplicated content in other artifacts and keep the full treatment only in its owning record or section. Preserve enough scoped context to make this proposal understandable on its own. Do not create a separate executive summary or decision packet that repeats this narrative. Question every sentence: what does the reader learn from it, why does that matter to this decision, and is it already communicated elsewhere? Delete it when it adds nothing necessary. Shorten or visualize it when that improves understanding. Apply this pass to captions and labels as well as paragraphs. Keep the sentence-by-sentence reasoning out of the published proposal.

Review the rendered result for legibility, visual accuracy, broken media, missing context, unnecessary repetition, meaningful link labels, and access for the intended team audience. A content hash or successful API response cannot establish these qualities. If a visual exposes a flaw in the design, return to the owning design decision and regenerate affected views before requesting approval.

## Planning boundaries

| Scope | Source being explained | Existing final review | Linear home |
|---|---|---|---|
| Epic specification | Read-back-verified Notion semantic draft | `approve_release` | Resolved epic issue or existing authorized project, initiative, or team |
| Implementation program | Validated milestone-first plan | `approve_program` | Resolved carrier project, or another authorized existing parent while carrier creation is pending |
| Ticket design | Reviewed implementation design | `approve_ticket_design` | The ticket's existing design document or an issue document |

Publish one coherent proposal for the current planning scope. At ticket scope, reuse the existing Linear design document and make its main narrative serve the supervisor; link detailed engineering evidence separately. A program proposal explains the whole program through a three-lane ownership and dependency visual showing the three people, bite-sized issue outcomes, shared prerequisites, and cross-stream handoffs under [three-person delivery planning](../../implementation-specification-compiler/references/three-person-workstreams.md). A ticket proposal explains its own bounded contribution with enough context to stand alone. The Linear proposal is an explanatory projection. Notion retains semantic authority, native Linear relations retain dependency truth, and these scopes keep their separate approvals and invocation boundaries.

At program scope, prepare the deliberate publication set under [project resources](project-resources.md) and return its `projectArtifactInventory`. Keep prepared-versus-fetched comparison data, raw extracts, and publication bookkeeping in internal recovery storage. The proposal and any material required to review it already have verified team-accessible references before approval. The later resource stage organizes the complete prepared set in the carrier project before issue creation; it does not make inaccessible evidence acceptable during review.

## Publish and review

When planning and its existing design checks are ready, resolve the exact Linear parent and any existing proposal before creating a document. Use authorization already present in the task. When a destination or write authority is still missing, prepare the full document and visual assets first, then request only the missing information or authorization. A proposal does not require creating a new project solely to hold it, and semantic planning does not authorize an implementation program.

Create or update the document through the Linear operation-aware adapter, using stable document and operation identities. The Linear document tool accepts Markdown and exactly one parent on creation: `issue`, `project`, `initiative`, `cycle`, or `team`. Render graph-like visuals only through Figma Design, LikeC4, or Archify under the [graph visual policy](graph-visual-policy.md), retaining their render receipts and artifact hashes. Use images or supported embeds to deliver those verified outputs; a format change does not change their renderer requirement. Figma previews require the workspace integration and appropriate file access; arbitrary interactive HTML is a linked artifact with an in-document visual fallback.

Fetch the document after writing. Compare the title, parent, content, source references, and visuals with the prepared proposal; inspect its rendered presentation. Retain the read-back content hash and the provider revision or update timestamp. If Linear normalizes Markdown, compare the rendered meaning, adopt the fetched representation, and hash that representation consistently. Partial writes, inaccessible required media, mismatched sources, and concurrent edits remain incomplete until reconciled.

The `publish_design_proposal` Camunda job returns the compact [design proposal binding](../../implementation-specification-compiler/scripts/specflow_runtime/design-proposal.schema.json). The existing final user task binds to that document and source. The publishing handler keeps document content, visual assets, and editorial work outside Camunda. The runtime checks the binding's structure, source equality, and matching read-back revision/hash; it does not certify prose quality or independently contact Linear. The handler and presenting agent verify live document freshness before approval, using the configured provider validator when available.

If the supervisor requests changes, the existing repair path revises the affected design or presentation and republishes its explanation before returning to review. Present the affected sections, practical difference, and approval impact in the review message, while keeping the document a coherent current-state explanation. Do not repeat settled questions or request a full review of unchanged supporting material. A changed document revision requires a fresh binding. A publication retry reconciles its existing operation and document before writing again. An unconfigured publisher waits as a service job; a technical failure follows the existing retry or incident path. Approval continues only the current scope's authorized workflow.

## Sources

- [Linear documents](https://linear.app/docs/documents) and [issue documents](https://linear.app/docs/issue-documents) describe parents and collaborative editing.
- [Linear editor](https://linear.app/docs/editor) describes Markdown, diagrams, attachments, and embeds.
- [Linear Figma integration](https://linear.app/docs/figma) describes preview access and refresh behavior.

## Review response and revision

The semantic proposal includes every current compiled visual in the section where its distinct communication job belongs and receives one combined design and visual approval. Keep the complete visual inventory in verification evidence; do not turn it into a second visual review packet. Final semantic, program, and ticket tasks accept `presentation_change` to revise only explanation and publication, and `semantic_change` to return to the owning design stage. The existing `changes_requested` action follows the broad design path. Source bindings stay fixed during presentation repairs, and the revised document receives a fresh review binding. See [approval economy](approval-economy.md).
