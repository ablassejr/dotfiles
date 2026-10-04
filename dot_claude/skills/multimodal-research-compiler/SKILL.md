---
name: multimodal-research-compiler
description: Compile substantial architecture, product, implementation, or decision research into a source-traceable evidence model and coordinated textual, visual, and machine-readable outputs. Use for discovery, grounding, decision support, implementation research, verification, or impact analysis; do not use for a quick fact lookup.
---

# Multimodal research compiler

Convert the user's question into one normalized Research Model, verify that model against claim-appropriate sources, and generate only the projections that help the intended audience. Every conclusion must trace to evidence, every inference must be labeled, every unresolved normative judgment must be routed to the human, and every output must preserve the meaning and confidence recorded in the model.

## Select the mode

Infer the mode from the request unless the choice would materially change the research target or permissible evidence.

| Mode | Use it to answer |
|---|---|
| `DISCOVERY` | What is true, and which options exist? |
| `GROUNDING` | Why is the current system shaped this way? |
| `DECISION_SUPPORT` | What should be chosen, given the evidence and approved principles? |
| `IMPLEMENTATION` | How should a bounded issue or one-PR change be implemented? |
| `VERIFICATION` | Is a claim, design, or proposed change supported? |
| `IMPACT_ANALYSIS` | What changes if a decision or code surface changes? |

Read [modules/frame-request.md](modules/frame-request.md), then read only the modules and references required by the active mode and stage.

## Compile the research

1. Frame the root question, the decision or action it supports, the audience, first-principles basis, source boundary, target versions and dates, requested outputs, and required confidence. Preserve user-stated non-goals. Ask only when a missing value materially changes the target or authority boundary.
2. Read [modules/compile-context.md](modules/compile-context.md) and create a Research Context Capsule. Pin the relevant repository commit, specification release, issue revision, dependency version, and visual-model revision when those sources are in scope.
3. Expand the root into material subquestions before searching. Each question records the claim types it can establish, preferred and fallback source classes, materiality, and whether human judgment is required.
4. Execute targeted research. Read the applicable code, history, documentation, or external-research modules. Follow [references/tool-routing.md](references/tool-routing.md) and [references/source-authority.md](references/source-authority.md). Supplied material is a candidate source, not automatically proof.
5. Normalize questions, entities, claims, sources, evidence links, decisions, alternatives, constraints, timelines, contradictions, uncertainty, architecture relationships, code surfaces, and output views into the shared Research Model. Use stable identifiers before records are cited by another artifact.
6. Reconcile evidence with [modules/reconcile-evidence.md](modules/reconcile-evidence.md), [references/evidence-classification.md](references/evidence-classification.md), and [references/contradiction-resolution.md](references/contradiction-resolution.md). Distinguish explicit evidence from structural, chronological, and behavioral inference.
7. Evaluate [references/research-gate.md](references/research-gate.md). Continue targeted research while a resolvable material factual gap remains. Stop with a bounded unresolved gap when further permitted research cannot resolve it. Route normative choices, risk acceptance, product semantics, and irreversible choices to the human.
8. Review the surviving recommendation against [references/first-principles-alignment.md](references/first-principles-alignment.md). Current implementation and historical precedent are evidence, not self-justifying requirements.
9. Run [modules/adversarial-review.md](modules/adversarial-review.md). Use an independent fresh-context reviewer when available and authorized. Otherwise perform the same challenge pass and label it `SELF_REVIEWED`, never `INDEPENDENT`.
10. Read [modules/compile-multimodal-output.md](modules/compile-multimodal-output.md) and compile only useful modalities. Follow [references/multimodal-output-selection.md](references/multimodal-output-selection.md) and [references/visual-projection-rules.md](references/visual-projection-rules.md).
11. Verify every projection against the same model. If a visual or narrative correction changes meaning, update the model first and regenerate affected projections.
12. Present the understanding checkpoint separately from any decision checkpoint. Persist a Research Session Manifest using [references/cross-session-resumption.md](references/cross-session-resumption.md).

## Stage routing

- For repository topology, ownership, contracts, or tests, read [modules/research-codebase.md](modules/research-codebase.md).
- For rationale and evolution, read [modules/trace-history.md](modules/trace-history.md).
- For exact API, dependency, protocol, or CLI behavior, read [modules/research-documentation.md](modules/research-documentation.md).
- For prior art, papers, current external facts, or alternatives not established locally, read [modules/research-external.md](modules/research-external.md).
- For source conflicts and confidence, read [modules/reconcile-evidence.md](modules/reconcile-evidence.md).
- For output selection and projection verification, read [modules/compile-multimodal-output.md](modules/compile-multimodal-output.md).

## Authority and permission boundaries

Use authority by claim type. Desired behavior comes from approved product intent and first-principles records; current behavior comes from pinned code, contracts, tests, and runtime evidence; historical rationale requires an explicit decision source or a labeled inference; exact dependency behavior comes from applicable official documentation.

Respect the user's source boundary. Do not widen a file-only or workspace-only request. Missing access leaves a visible gap; it does not authorize substituting a different system or inventing evidence. Generate local, ready-to-publish projections by default. Write to Notion, Linear, GitHub, Figma, FigJam, or another external system only when the request authorizes that mutation.

When repository research is in scope, invoke Claude Context before investigation. If the repository root contains `.codegraph/`, use CodeGraph before text search or direct file reading for structural questions. Before invoking any CLI, retrieve the current command documentation and side effects through Docs MCP Server; do not guess flags. If required documentation cannot be retrieved or refreshed, report that command as blocked.

## Deterministic helpers

The scripts use JSON at their public boundary and write deterministic, sorted JSON. Run a helper with `--help` before first use.

- `scripts/normalize_sources.py` assigns stable source identifiers and deduplicates the same scoped source.
- `scripts/build_question_graph.py` compiles a mode-aware material question graph.
- `scripts/build_evidence_graph.py` joins claims to sources and reports dangling references.
- `scripts/correlate_git_github_linear.py` correlates offline Git, GitHub, and Linear records by explicit identifiers.
- `scripts/validate_claims.py` checks observable claim and evidence invariants.
- `scripts/detect_contradictions.py` finds declared and value-level conflicts.
- `scripts/build_timeline.py` emits a chronologically sorted evidence timeline.
- `scripts/compile_research_packet.py` compiles the handoff packet and model digest.
- `scripts/validate_research_release.py` blocks release when evidence, review, decision, or projection consistency is incomplete.

Use the JSON Schemas in `schemas/` for interchange validation and the files in `templates/` as projection starting points. Do not copy template examples into evidence records as facts.

## Completion

Complete the run only when the question and supported use are explicit; the authoritative baseline is pinned; every material claim is supported or explicitly unresolved; source scope, version, and date are applicable; contradictions are resolved or bounded; first-principles and adversarial reviews have no unresolved blocker; all projections agree with the model; material grounding has a separate understanding checkpoint; remaining normative decisions are routed to the human; and the session manifest can resume deterministically.

For `IMPLEMENTATION`, also connect each approved requirement to the affected public behavior, code surface, implementation decision, work item, behavioral test, and verification evidence. Identify mechanisms that become unnecessary, but never treat a code-removal ratio as permission to delete behavior or hide complexity elsewhere.
