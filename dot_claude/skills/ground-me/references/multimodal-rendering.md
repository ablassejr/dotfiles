# Multimodal rendering

Always provide a concise textual model, an evidence timeline, a decision-lineage graph, and a small set of decisive linked excerpts. Choose additional views by communication job.

Use LikeC4 for formal system boundaries, component ownership, runtime communication, dependencies, data flow, or deployment structure. Produce current-state and historical-state views only when the evidence supports both.

Use Archify for validated interactive architecture, workflow, sequence, data-flow, or lifecycle explanation when it serves the grounding question. Compile the normalized model through [ArchifyArtifactAdapter](bundled/epic-spec-workflow/references/archify-adapter.md), retaining source hashes, immutable generations, and operation receipts. Preserve existing required formal and curated views.

Use Figma Design, LikeC4, or Archify for connected chronology, contradiction maps, decision trees, and ticket-to-commit lineage. FigJam can hold non-graph workshop material. Use Figma when the explanation needs high-fidelity stakeholder communication, compares multiple architecture states, belongs in the canonical specification, or concerns user interaction.

For an implementation target, include relevant current code, introducing and current diffs, protecting tests, and a structural view when they are decisive. Do not create a polished visual for a local helper when the timeline and linked source explain it. Do not omit an architecture view when a cross-system boundary is the material question.

After every visual write, read back its structure and inspect its rendered form. A successful write is not evidence that the visual accurately reflects the grounding packet.


## Select the minimum useful representation

| Question | Representation |
|---|---|
| Why a decision evolved | Evidence timeline |
| Which sources support intent | Evidence graph |
| Ticket, PR, commit, and symbol lineage | Provenance graph |
| Current structure | LikeC4 formal model, with an Archify interactive projection when useful |
| Historical and current architecture | Source-supported side-by-side LikeC4 or Figma views |
| Open alternatives | Figma Design or Archify decision map |
| Stakeholder explanation | Figma narrative frame |
| Exact implementation change | Code diff |
| Structural blast radius | LikeC4 or Archify view grounded in CodeGraph evidence |
| Requirement-to-implementation coverage | Traceability matrix |
| State, interaction, and failure behavior | State-machine or sequence view |
| Parallel execution dependencies | Figma Design, LikeC4, or Archify projection of the selected dependency graph |
| Confidence and disagreement | Evidence table with explicit, inferred, conflicted, and unknown labels |

Do not generate every representation. Use the smallest set that makes the current question and its evidence understandable, preserving the packet's required evidence and applicable architecture/interaction views. Keep unsupported historical structure unknown instead of drawing it as fact.

All graph-like representations in this table follow the [graph visual policy](bundled/epic-spec-workflow/references/graph-visual-policy.md). Graph JSON and source-system graphs are evidence inputs; the presented graph needs an allowed renderer and a validated receipt. Non-graph timelines and traceability tables remain ordinary data views.
