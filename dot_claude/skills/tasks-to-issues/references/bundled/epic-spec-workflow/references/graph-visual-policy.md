# Graph visual policy

Every workflow step that creates, presents, publishes, or updates a graph-like visual uses **Figma Design, LikeC4, or Archify**. This includes provisional exploration, research, Ground Me, semantic review, program and ticket proposals, publication, and as-built reconciliation. A renderer is selected for the communication need; when it is unavailable, choose another tool from this allowlist or report the blocked render.

A graph-like visual explains entities and relationships, boundaries, flow, sequence, state transitions, dependencies, provenance, decisions, connected chronology, or quantitative relationships in a chart. Classify it as `graph` regardless of whether its delivery format is HTML, PNG, SVG, an embed, or a screenshot of a diagram. Mermaid, Graphviz, ASCII diagrams, custom SVG/HTML drawing, FigJam boards, and exported CodeGraph or native issue-tracker graph views do not satisfy this renderer requirement. Those tools may supply research or structured source data; render the explanatory graph through one of the three allowed tools. Executable BPMN and graph JSON remain operational/model data, not substitute presentation artifacts.

Screenshots of non-graph interfaces, photos, video, ordinary tables, code excerpts, diffs, and UI mockups remain available for their own communication jobs. Do not label a graph as a screenshot, table, or mockup to avoid the rule. Figma means a Design file/node, not a FigJam board. LikeC4 retains its formal architecture role; curated interaction views retain their Figma requirement.

## Visual records

Every presented visual appears in the owning step's complete `visuals` inventory. A non-graph record uses an explicit content kind, for example `{"ref":"issue-screen.png","kind":"screenshot"}`. `image`, `embed`, and `png` describe formats and cannot replace the content classification.

A graph record binds its displayed reference to an allowed renderer, a completed render-operation receipt, and the exact rendered artifact. The [shared schema](../../implementation-specification-compiler/scripts/specflow_runtime/visual.schema.json) defines its shape. Schema consumers register this packaged resource under its `$id`, `https://specflow.local/schemas/visual.schema.json`, when validating Grounding Packets or design-proposal bindings; this identifier is not a network endpoint:

```json
{
  "ref": "linear-document#architecture",
  "kind": "graph",
  "renderer": "archify",
  "artifact": {
    "path": "/published/generation-000003/view.html",
    "sha256": "sha256:aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa"
  },
  "receipt": {
    "path": "/published/generation-000003/manifest.json",
    "sha256": "sha256:bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb"
  }
}
```

Example hashes and paths are placeholders. For Archify and LikeC4, use the adapter's immutable published manifest and one of its recorded output files. Validation reads the manifest and artifact, checks both hashes, and compares the manifest's adapter, completed status, operation/input identity, output path, and output hash. An artifact-storage receipt does not establish render provenance.

For Figma, `artifact` contains `ref` and `sha256`: the Design node URL and the hash of its fetched representation. Save the completed Figma operation receipt as a hashed local JSON file. Its `result.visual_artifact` contains that same `ref`, `sha256`, and `file_type: "DESIGN"`. The node URL uses `/design/` or legacy `/file/` with a `node-id`; `/board/` is rejected. The configured Figma adapter obtains this evidence through provider readback. The receipt is durable evidence to retain, not a receipt the author invents to pass validation.

Hashes detect changed evidence and mismatched artifacts. They do not authenticate a dishonest provider or worker, infer graph content from pixels, or prove that a mutable remote node remains unchanged. The configured renderer/adapter and visual review remain responsible for truthful classification and source attribution; live provider validators detect remote changes. A renamed renderer label alone cannot pass the gate without matching receipt and artifact evidence.

## Enforcement and recovery

`specflow validate-visuals visual-manifest.json --json` reads a JSON object containing `visuals`, validates all entries and local render evidence, and reports the validated count. It is read-only and makes no provider calls. Use it before presenting a visual outside an active Camunda job as well as when preparing publication. Failure returns the existing CLI error envelope with code `invalid_visual`.

The runtime checks every `visuals` array in completed job variables, human review bindings, operation requests, and resume evidence. `compile_visuals`, `ground_visuals`, and `publish_design_proposal` explicitly require the inventory in `visualBinding`, `groundingBinding`, and `designProposalBinding` respectively. Research collection, program/ticket design, specification publication/finalization, handoff verification, and as-built reconciliation explicitly return a top-level `visuals` array; an empty array records that no visual is produced or published by that step. Publication inventories include the embedded graphs, even when they were rendered earlier.

The automated worker validates incoming visual evidence before invoking its handler and validates outputs before completion. Invalid output creates a repairable incident. Operation-aware adapters validate declared visuals before applying or reusing an external effect. Adapter workers propagate an explicitly supplied `operationRequest.visuals` inventory into completion variables. Grounding Packet validation uses the same policy and retains its existing `type` field alongside the shared visual fields. Human review does not waive the renderer requirement.

When evidence is absent, mismatched, or produced with a disallowed renderer, regenerate through an allowed tool or restore the correct durable evidence, then rerun validation before completion. Preserve the existing process and retry identity. Do not claim success from a renderer name, file extension, or unverified link.

Existing visual records need their content classification and graph evidence populated before revalidation. Process variables retain compact references; media bytes stay outside Camunda. Running processes remain on their deployed definition; deployment does not migrate them or rewrite stored artifacts.
