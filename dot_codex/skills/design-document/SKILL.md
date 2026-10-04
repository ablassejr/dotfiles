---
name: design-document
description: Autonomously explain a proposed engineering design in a concise, self-contained visual document with useful diagrams, prototypes, rrweb replays, and asciinema demonstrations. Use for design proposals, RFCs, and design-review documents that explain intended behavior, recommendations, tradeoffs, and unresolved choices; use an implementation overview to describe an already built system.
---

# Design document

Create one clear explanation of a proposed design that a teammate can understand and review without the conversation. Establish the problem, the recommendation, how the design would work, its consequential tradeoffs, and any decision still needed. Let purposeful visuals and demonstrations carry the explanation, with short context, implications, and evidence limits.

## Establish the proposal's job and authority

Infer the audience, scope, intended outcome, useful technical depth, and destination from the request and accessible material. Reuse stated constraints and settled decisions. When the user supplies a design to document, explain it faithfully and surface material inconsistencies. When developing a recommendation is within scope, research and propose the missing design choices without presenting them as accepted requirements. Do not add product requirements, acceptance criteria, restrictions, owners, deadlines, or approval gates the user has not established.

A supplied idea, design, or body of research is enough to begin drafting. Do not require an epic, a previous implementation, a specification release, or a new first-principles interview. An existing governing workflow retains its actual source authority and approval rules; read [framework integration](references/framework-integration.md) when working within one or selecting capabilities from it. A request to document a proposal authorizes authoring and appropriate local explanatory artifacts, not implementation, rollout, or external publication.

Reuse the existing proposal when it serves this scope. Give it a descriptive project-and-role title, such as “Invoice exports — Design proposal.” Its opening identifies what it proposes, why it exists, who should review or use it, and its actual status. Include the source revision and responsible person or team when established. State a review question only when a real decision remains. An approved design may still be unimplemented; approval status and implementation status are separate.

The proposal owns the coherent explanation of this design and its rationale. Keep detailed references, operational procedures, delivery records, and research with their existing owners, using only enough context to make this document stand alone. Do not produce a separate executive summary, decision packet, or handoff narrative that repeats the proposal. Preserve an existing implementation overview's identity and purpose.

## Ground the recommendation

Inspect the evidence needed to explain the current problem and judge the proposal. Existing code, configuration, tests, and runtime observations can establish the relevant baseline; a greenfield proposal does not need a fictional baseline. Use bounded research for consequential unknowns, and keep source inventories and investigation notes internal.

Distinguish verified current behavior, proposed behavior, assumptions, and unresolved choices where each appears in prose and media. A plan establishes intent. A diagram establishes a model. A prototype can exercise an interaction or limited mechanism. None alone proves that the proposed system is implemented, deployed, reliable, or performant. Identify expected benefits as expectations unless the evidence supports a measurement, and compare alternatives on compatible scopes.

Explain why the recommendation fits the stated problem and constraints. Compare meaningful alternatives when they affect the decision, including retaining current behavior when relevant. Do not manufacture an alternatives catalog, reverse-engineer historical intent without evidence, or reopen settled choices merely to fill a section. If new evidence materially conflicts with an accepted choice, show the conflict and its consequence before changing the proposal's authority or meaning.

## Explain how the design would work

Describe the proposal directly in complete sentences, from the initiating actor or event through the intended outcome. Introduce actors and terms where the reader needs them. Weave in the interfaces, responsibility boundaries, state and data changes, integrations, concurrency, failures, and recovery that materially affect understanding. Explain what users and other systems would experience, rather than cataloging components or prescribing a file-by-file implementation plan.

Include compatibility, transition, operational, security, cost, or rollback consequences when they affect the choice. Identify important feasibility questions and the evidence needed to resolve them. Reuse agreed verification expectations; do not invent passing thresholds or turn suggested investigative work into adopted acceptance gates. Keep unresolved alternatives visibly open without duplicating the whole design for each possible answer.

Use headings that help the reader navigate the actual proposal and omit empty categories. Comprehensiveness means the reader can evaluate the recommendation and its material consequences. Length follows that explanation, without word, page, diagram, or question quotas. The document describes the current proposal coherently; revision history and the list of edits belong in the accompanying review message when useful.

## Produce purposeful media autonomously

Default to a compact visual document. Select media while shaping the explanation, before expanding it into prose. Use diagrams for relationships and behavior, prototypes or annotated screens for user experience, rrweb for recorded interactions, asciinema for actual terminal or library execution, and compact comparisons for tradeoffs. Combine media when they answer distinct questions. Respect explicit text-only or other format requests; use text alone when visuals add no explanatory value.

Read [proposal media and prototypes](references/proposal-media-and-prototypes.md) when preparing visual or interactive content. Independently select representative scenarios, inspect reusable assets, create or capture useful demonstrations, assemble the viewing experience, and verify it within scope. Do not wait for a separate media request or ask the user to make recordings that can be produced within the permitted scope. A model or prototype must remain visibly distinguishable from implemented product behavior.

When no destination format is specified and replay or interaction helps, prefer a portable HTML document with embedded media and meaningful static alternatives. Place each asset beside the question it answers. Keep prose for context, rationale, consequences, and uncertainty; remove narration that merely repeats visible clicks, output, or diagram structure. Each asset needs a distinct explanatory purpose.

## Keep the user engaged in consequential decisions

Explain material findings and their implications as the proposal takes shape. Resolve accessible facts and routine editorial, layout, and media choices autonomously. Ask when an unresolved question about intended behavior, scope, a material tradeoff, or missing authority needs this user's judgment and prevents a coherent recommendation or next step.

Before asking, check the existing decisions and investigate the relevant facts. State the recommendation when supported, the meaningful alternatives or uncertainty, what the answer changes, and why it matters now. Ask the smallest useful question rather than exposing a speculative tree of dependent questions. Accept a clear answer and continue without another confirmation. If uncertainty can be bounded honestly, finish independent work and identify it in the proposal.

Present a concrete proposal before requesting an existing final approval. Keep design and visual review in the same reading surface. On revision, direct attention to the affected choice and sections; request renewed approval only as required by the actual workflow and changed scope. Do not demand another review of unchanged supporting material or create additional review gates for the writing process.

## Deliver a document the team can use

Read the whole result as a teammate arriving without context. They should understand what is proposed, why, how it would behave, what is uncertain, and what action is expected. Challenge the proposal against its sources and inspect the visuals for contradictions. Correct editorial errors directly; surface a substantive conflict with the governing design instead of silently redrawing it as resolved.

State document-wide status and evidence limits once where the reader first needs them. Repeat a qualification locally only when a specific claim or separately viewed asset could otherwise imply stronger evidence. Do not append another inventory of every unimplemented behavior or unspecified detail. Keep one full explanation of each idea: examples, prose, and media should contribute different information rather than retelling the same flow.

Use available, permitted tools to inspect rendering, exercise meaningful controls, and verify media. If no suitable viewer is available, complete the authoring and available static checks, keep a readable fallback, and deliver with a concise statement of the unverified rendering, interactions, or playback. Static checks do not establish those outcomes. Follow the [viewing and verification guidance](references/proposal-media-and-prototypes.md#finish-and-inspect-the-viewing-experience) for tool alternatives and genuinely required verification gates.

Keep the main explanation complete without opening another document. Use descriptive, durable shared references for optional evidence and depth. Team-facing content must not depend on local filesystem paths, localhost, session handles, unexplained artifact names, or invented URLs.

Prepare the document and assets before requesting a genuinely missing destination or publication authority. An unpublished local result remains an explicitly identified draft, not a claim of team access. After an authorized publication, fetch and compare the provider's content, source association, media, and intended audience access with the prepared result as far as tools allow. Honor existing revision and approval bindings without creating a second approval process. Sending messages to others requires explicit authorization.

Return the proposal or its verified shared link and material verification limits. Keep manifests, receipts, and editorial bookkeeping internal. An accurate proposal, a tested prototype, and an approved design are distinct from implementation and release authority.
