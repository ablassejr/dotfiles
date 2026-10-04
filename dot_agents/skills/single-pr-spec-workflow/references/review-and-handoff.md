# Review and handoff

## Distinct review lenses

Keep the review package bounded to the approved request/basis, current specification and handoff, accepted decisions, evidence ledger, relevant source artifacts and tests, public contract examples, and current visuals. A reviewer should reconstruct the rationale from this package. Do not give an independent reviewer the authoring conversation, a preferred verdict, or private reasoning.

Use an independent reviewer agent when available and authorized for a meaningful adversarial pass. If unavailable, perform the separate review lenses yourself and explicitly label the independence limit. Record actual review results rather than inventing a reviewer identity or a passing check.

| Review lens | What it challenges |
|---|---|
| First-principles alignment | Whether the frame fits the problem, each requirement has authority, constraints remain valid, deletion and retention are justified, and complexity produces causal benefit. |
| Specification review | Whether the observable behavior, scope, public contracts, invariants, exceptions, compatibility, and verification cover the approved outcome without adding obligations. |
| Provenance review | Whether historical intent is documented, sources are chronological and applicable, inference is labeled, and original forces still hold. |
| Architecture review | Whether affected ownership, coupling, authority, state, data flows, failure propagation, and deployment implications support the outcome. |
| Implementation-design review | Whether the concrete proposal can fulfill the contract in one PR, handle applicable concurrency/recovery/migrations, preserve callers, and be tested at stable boundaries. |

Apply provenance and architecture review when the proposal makes those material claims; do not force an irrelevant diagram or a history investigation into a trivial documented correction. Distinct lenses can share one bounded reviewer pass, but a generic “looks good” cannot stand in for their recorded conclusions. As-built integration and production verification belong to later implementation, not a speculative planning pass.

For each finding, record its classification, violated approved requirement or challenged claim, evidence, consequence, affected records, earliest repair stage, downstream invalidation, approval impact, and a concrete repair or disproof question. Use `BLOCKER`, `MATERIAL_HITL_DECISION`, `AGENT_REPAIR`, or `NONBLOCKING_OBSERVATION`.

Repair factual mistakes, incomplete explanations, and in-scope design defects autonomously. Ask the human when the repair changes intended behavior, scope, priority, or acceptable risk. Reviewers may question an approved choice but cannot add new acceptance criteria or silently substitute their preferences.

Recheck the finding and affected downstream artifacts after repair. Keep unresolved disagreement visible. A passed review is evidence that the proposal was evaluated; it is not a human approval or proof that unimplemented behavior works.

## A proposal the supervisor can understand

Lead with who faces the problem, what happens, why it matters, and the proposed outcome. Explain the design from initiation through observable result, with material failure and recovery paths. Use plain-English pseudocode that reads as normal prose. Label current facts, proposed behavior, assumptions, and unresolved choices.

Prefer a visual when it carries the idea more clearly: a relationship or state view, an annotated interface, a small comparison table, or an interactive demonstration when interaction matters. Choose media for explanatory value. Do not require every tool, a fixed number of views, or redundant prose around a clear visual.

Keep approved current and proposed states visibly distinct. Check labels, reading order, source consistency, accessibility, rendering, and the intended reader's access. Provide a readable in-document fallback when an external interactive artifact adds depth but cannot render inline.

Managed graphs use the active framework's renderer, artifact, and receipt contract. Standalone work uses applicable session and repository visualization instructions. Do not claim a renderer was used without running it or attribute a generic generated image to an architecture tool. A render receipt verifies an operation record, not the design's correctness.

Link detailed source inventories and engineering evidence for depth. The main proposal still needs enough information to evaluate scope, behavior, tradeoffs, compatibility, operational consequences, and verification without opening the authoring conversation. Remove sentences that add no necessary understanding.

## Publication and recovery

Local Markdown is a valid final home for standalone work. If the user or existing workflow specifies an external home, resolve the exact authorized parent and current document, then prepare the complete proposal and assets before requesting missing write authority or a destination. Reuse the existing design document where applicable.

Use purpose-built configured adapters and existing authorization. Do not create a project or issue merely to hold the specification. Follow the active platform's approved publication process; a standalone skill does not supply provider credentials, process tokens, or destination permissions.

For a managed write, retain stable artifact and operation identities with the source binding, destination revision, and applicable concurrency guards. Read back the result and compare the destination, content, source references, visuals, and current revision with the intended effect. Inspect presentation and audience access when they are part of the publication contract. A successful API call alone does not establish a correct, accessible document.

After an uncertain mutation, reconcile by the original identity before any retry. A verified existing effect can be adopted, verified absence can permit the already authorized effect, and an unresolved result remains a recovery dependency. Preserve evidence for the next attempt. Do not create duplicates, invent receipts, or treat a local artifact helper as provider readback.

Bound transient retries using the active tool or workflow policy. Authorization failures, missing configuration, changed intent, or stale source bindings are not transient outages. Continue unaffected local work while reporting a required publication dependency honestly.

## Final approval

Present the complete current specification, implementation proposal, verification plan, and applicable visuals together. Ask the named decision owner for approval of that exact revision if it is not already present. Use clear natural language and preserve the actual response and its binding.

The approval identifies the work, source/baseline, specification and handoff revision or content hashes, applicable visual/source bindings, actor, and actual response reference. Managed workflows retain their actual native approval task and source binding requirements. Do not invent those records for standalone work.

Check freshness immediately before treating approval as current. The approved artifact must match the artifact handed off. A changed semantic source, materially changed relevant baseline, or different final document invalidates the affected approval. An approval of a plan does not approve an implementation or authorize provider effects beyond its recorded scope.

If the human requests presentation changes, keep the source semantics fixed, repair the explanation, and obtain approval of the current presentation. If their request changes behavior, revise the affected source decisions and repeat the affected design and review work. Do not rerun unrelated research simply because formatting changed.

## The implementation handoff

Provide one executable-in-principle plan for the approved one-PR outcome. “Executable” here means a capable engineer can follow it; the handoff itself performs no implementation action.

The handoff includes the exact approved specification and baseline, behavior and public contracts, scoped source targets, a dependency-aware order within the PR, applicable data/migration/recovery consequences, behavior and integration verification, required environments, approved decisions, actual review results, uncertainty, and escalation triggers. Link supporting evidence precisely.

Separate planning status from execution readiness. An environment credential, scheduled deployment window, or authorized external access may remain an execution prerequisite while the design is complete. A missing required predecessor PR or unknown contract that determines the design must instead affect scope or design readiness; do not conceal it in an executor checklist.

State which implementation choices the executor can resolve through judgment while preserving the contract. If implementation evidence changes intended behavior, a public interface, an invariant, approved risk, or the one-PR boundary, return to a targeted specification decision and refresh dependent approval. Do not silently broaden the work or restart all unaffected planning.

In managed work, name the actual next supported ticket/execution workflow and its remaining prerequisites. In standalone work, a later implementation request can reference this handoff directly. Merely mentioning `$single-pr-executor` does not satisfy its requirements for a issue or work item, current process/basis, accounting contract, and design approval. The skill does not automatically invoke that executor.

## Completion record

Return the applicable result label, or the current stage and pending human question for in-progress work, with a concise explanation grounded in actual evidence. Link the specification and handoff. Identify actual review and approval status, checks performed, unperformed implementation tests, and remaining dependencies. Report public interface proposals with consumer examples, or `Public interface changes: none`. Include a labeled plain-English pseudocode summary of the proposed behavior.

After authorized artifact edits, follow the active session's memory policy. Persist only a concise summary of the completed work and verification in the available approved memory system. Keep secrets, raw source dumps, speculative rationale, and fabricated provider state out of memory.
