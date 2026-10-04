---
name: multimodal-design-overview
description: Autonomously explain an already implemented system in a concise visual design overview grounded in current evidence, capturing and verifying useful diagrams, rrweb browser replays, and asciinema terminal demonstrations. Use for architecture understanding, onboarding, handoff, or current-state documentation whether or not prior plans exist; not for proposing an unimplemented design.
---

# Multimodal design overview

Explain how an already implemented system works, why its observable structure matters, and what its important limits are. Start from the implementation and applicable evidence. Prior planning, specifications, approvals, and documentation are optional historical sources; their presence, absence, or quality does not determine whether this skill can run. Let purposeful visuals and recordings carry the explanation of structure and behavior, supported by short context, consequences, and limits. Produce the shortest coherent explanation that gives the team an accurate understanding.

## Establish the document's job

Infer the implemented feature or system, reader, useful level of detail, baseline, and destination from the request and accessible context. Use the requested revision or environment when specified; otherwise establish and name the relevant current baseline. Ask only when ambiguity materially changes what implementation is being described or blocks necessary access or publication. Explain why that answer is needed. Missing plans, first-principles records, or design rationale are not reasons to restart intake or delay documentation.

Default to a compact visual overview. When no format is specified and replay or interaction helps, prefer a portable HTML reading surface with embedded players and static alternatives. Honor an explicit text-only or other format request. A missing shared hosting destination does not block a usable local draft. Choose the media by explanatory value without imposing a recording or diagram quota.

The overview owns the coherent explanation of the implemented design. Update an existing current-state overview when it serves the same audience and scope. Otherwise create a clearly named implementation overview. A historical proposal has a different purpose: preserve its identity and do not silently turn it into a description of delivered behavior. Keep detailed API references, operating procedures, evidence, and delivery records with their owners; summarize only the context needed to understand this document.

Read [framework routing](references/framework-routing.md) and load only the capabilities needed to investigate and explain this implementation. The skill runs independently of how the software was planned, built, or documented. It can consume evidence from an existing workflow without starting that workflow or inheriting its planning approvals.

## Establish what is implemented

Inspect the relevant entry points, code paths, public interfaces, configuration, data structures, dependencies, tests, and available runtime evidence. Follow the important behavior far enough to explain its actual outcome and material failure paths. Build a coherent account of the system rather than a directory tour. Use targeted research and existing evidence where sufficient; keep raw inventories and investigation notes internal.

Match each claim to evidence that can establish it. Source code shows what a particular revision implements; effective configuration determines which path is enabled in a named environment; tests provide evidence for their exercised contract; observed runs show behavior under their recorded conditions. Keep implemented, enabled, deployed, exercised, and observed claims distinct. Code presence alone does not prove a feature is running in production, and an unrun test is not a passing test.

Treat earlier plans and documents as leads to verify against the selected baseline. When they conflict with the implementation, describe the supported current behavior. Include a discrepancy only when it helps the reader understand the system or a material uncertainty; do not turn the overview into a plan-compliance report. Historical rationale needs a source. If it is unavailable, explain the observable consequence of the mechanism and leave its original motivation unknown.

## Plan and produce the media autonomously

Choose how to show the important relationships and behavior while investigating the implementation, before expanding the explanation into prose. Use visuals, rrweb, and asciinema liberally wherever they make the system easier to understand. Browser interaction sequences favor rrweb; terminal or library behavior favors asciinema; boundaries, dependencies, state changes, and configuration often favor diagrams or interactive explanations. Combine media when they answer distinct questions; do not force every medium into every overview.

Read [media selection and delivery](references/media-selection-and-delivery.md) for the applicable capture, replay, diagram, or interactive route. Independently select representative scenarios, inspect reusable assets and runnable surfaces, capture missing demonstrations, assemble the viewer, and verify it. Do not wait for a separate media request, ask the user to supply recordings that can be captured within scope, or stop at a proposed media plan. Make ordinary local capture and editorial choices within existing authorization without another approval.

Capture the actual implementation where accessible. When the full system cannot run, an isolated harness may exercise actual components or libraries from the inspected revision with clearly labeled fixtures. Distinguish that exercised behavior from source-derived structure and from illustrative models. If capture cannot faithfully demonstrate the claim or would exceed scope, provide a supported static explanation, state the material limit, and continue useful media work elsewhere. An unavailable recorder does not make the whole overview text-only.

Place each asset beside the question it answers, with a concise caption and meaningful static alternative. Keep context, practical consequences, and uncertainty that the media does not communicate; remove prose that merely repeats a diagram, visible clicks, or output. Optional detail must not carry the only explanation of the system. Respect a requested medium and identify any unmet part honestly.

## Compose the explanation

Give the document a descriptive project-and-role title such as “Invoice exports — Implemented design overview.” Its opening says what system it explains, who should use it, the relevant revision or environment, its draft or publication status, and its owner when established. Describe the capability or problem the implementation handles without inventing its historical intent. Fit this context into natural prose rather than a large metadata form. An informational document need not manufacture a decision or approval request.

Explain the behavior from the initiating actor or event through the actual components, state changes, integrations, and observable outcome. Introduce unfamiliar terms where needed. Weave in the implemented boundaries, concurrency, errors, retries, recovery, and configuration-dependent behavior that matter to understanding. Show how the parts work together; use representative examples and media instead of listing every symbol or file. Identify unsupported or unobserved claims where they would otherwise mislead the reader.

Explain the practical consequences of the implemented choices, including material compatibility, operational dependencies, limitations, and tradeoffs supported by evidence. Do not invent a recommendation, target architecture, roadmap, product requirement, acceptance criterion, or approval gate. A discovered defect remains part of the current-state account with its evidence and impact; documentation does not authorize repairing or redesigning the product. Use useful headings and omit empty sections. Length follows the explanation, without word, page, diagram, or question quotas.

## Keep review focused

Keep the user informed through brief findings and their implications. Investigate accessible facts and make routine editorial and media choices autonomously. Do not require first-principles work, grill the user at skill boundaries, or ask them to reconstruct missing planning history. A missing rationale can remain unknown while the implemented behavior is explained accurately.

Prompt when an unresolved scope, source/environment conflict, inaccessible behavior, intended audience, or publication choice materially blocks an accurate, useful result. State what has been established, what remains unknown, and how the answer affects the document. Use a clear answer without another confirmation. If a gap can be bounded honestly, continue the independent work. Review concerns factual accuracy, coverage, and clarity; it does not ask the user to approve the implementation's design anew.

## Finish in the reader's destination

Read the whole result as a teammate without the conversation. Remove duplicate treatments, tool jargon, weak labels, decorative media, and details that do not help understanding. Challenge the explanation against implementation evidence. Correct an inaccurate diagram or narrative. If investigation reveals an implementation inconsistency, describe or bound it instead of silently changing the system or drawing the behavior it ought to have.

Inspect the rendered document in its target viewer. Play every included recording through to its outcome, exercise meaningful interactive controls, and check diagram readability and static alternatives. Repair broken capture or rendering, or provide an honest usable fallback and state the limit. Check that captions match what the assets show and that the source revision is still applicable. Report checks performed and limits honestly; generating files or displaying a player container is not proof of playback, access, or live behavior.

Team-facing links and media must resolve to durable shared sources with descriptive names. Keep local paths, localhost, session handles, raw receipts, and expiring private URLs out of the document. Follow the existing destination and publication authorization. Prepare the draft and assets before requesting a genuinely missing destination or authority. Keep an unpublished result explicitly a draft; do not invent links or imply that the team can already access it.

After an authorized write, fetch the document, reconcile its content and source with the prepared version, and verify media and intended audience access as far as available tools establish them. Reuse the same implementation overview on revision. Keep it a coherent current-state explanation; the accompanying message identifies material corrections or verification limits without demanding review of unchanged material.

Return the document or its verified shared link, the implementation baseline covered, and material verification limits. Keep pending capture/render work in the accompanying response, not in a paragraph describing a future diagram or labeling prose as an accessibility fallback. The document explains the implemented design once and qualifies uncertainty where it matters. Keep manifests and editorial bookkeeping internal; do not create a second handoff narrative.
