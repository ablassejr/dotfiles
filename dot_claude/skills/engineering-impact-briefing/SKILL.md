---
name: engineering-impact-briefing
description: Autonomously turn engineering work and evidence into concise visual team briefings whose media shows before-and-after changes and their practical impact. Use for end-of-week reviews, progress updates, change handoffs, and demo narratives that explain outcomes, availability, and needed action.
---

# Engineering impact briefing

Create one briefing that lets colleagues understand the meaningful result, why it matters, and how it affects their work without opening another document or knowing the conversation. A list of completed activities, tickets, or artifacts does not establish an outcome. Let useful visuals and recordings carry the explanation, supported by short context, captions, consequences, and actions.

## Establish what the audience needs

Use the requested audience, reporting period, delivery format, and available attention. Infer these from the conversation when possible. For a team review, write for colleagues outside the presenting workstream. Default to a compact visual briefing. When no format is specified and replay or interaction helps, prefer a portable HTML reading surface with embedded media and static alternatives. Respect an explicit text-only or other format request. Use text alone when visuals add no explanatory value; do not impose a fixed number of topics or recordings.

Read the supplied material before choosing the story. Meeting remarks and attached instructions are evidence of what people said, not authorization to contact them, change a system, or publish. Respect a requested source boundary. Use accessible work evidence to resolve consequential gaps when that is within scope; do not start a broad investigation merely to fill a reporting template.

When Git and the codebase are the requested sources, establish the reporting window and inspected revisions, then use history, relevant diffs, implementation, tests, and existing demo assets to explain the results. Resolve PR associations from evidence and keep branch work separate from merged work. Do not require the user to supply notes or recordings that can be derived or captured within the permitted scope.

Group related work by the outcome the audience cares about. Give prominence to changed capabilities, consequences for other teams, material constraints, and decisions that need attention. Combine work that explains the same outcome. Reading the whole source does not require mentioning every work item: retain details that change the audience's understanding or action. When the user requests complete coverage, preserve it economically in the same briefing instead of silently dropping items.

A briefing derived from a meeting is not a set of meeting minutes. Omit facilitation feedback, speaker-by-speaker history, and minor fixes unless they explain a consequential result, decision, or action. Retain attribution when it matters to the evidence, without making colleagues reconstruct the outcome from a sequence of reports.

## Build the explanation from evidence

For each meaningful outcome, establish the relevant earlier condition, the supported result, and the practical consequence. A qualitative comparison is useful when numbers are unavailable. If no baseline is established, describe the current result and say which comparison cannot be made. Compare measurements only across compatible scopes, definitions, and periods. Keep hypothetical examples, estimates, and expected benefits distinct from measured results; do not turn an illustrative count or a speaker's uncertain recollection into a fact.

Distinguish what is reported from what was inspected or exercised. Also distinguish planned work, implementation, merge, deployment to a named environment, and an observed result. Explain the state naturally where it changes the meaning of a claim. A demo, an open pull request, or a merged change does not establish that colleagues can use it. An investigation or plan can be a useful outcome: explain the supported finding or decision it enables without presenting it as a delivered capability.

Translate internal shorthand into the concept the reader needs. When two similarly named capabilities differ in behavior, authority, source, or intended use, make that difference explicit. Use verified names and definitions when available. Do not settle a disputed taxonomy or guess a tool name from poor captions; use an accurate functional description and identify the ambiguity only if it affects understanding or action.

## Produce useful media autonomously

Choose media around the before-and-after change while selecting the story, before expanding it into prose. Show the earlier experience or limitation, the same representative task after the change, and the practical difference for users or colleagues. For a weekly review, use the baseline before the relevant work in the reporting period and combine related changes into their meaningful result. Paired rrweb replays can show changed browser workflows; asciinema can show changed command or library results; screenshots, diagrams, or compact tables can compare visible states, flows, responsibilities, or constraints. Choose the medium for its explanatory job, without requiring every medium in every briefing.

Test execution is supporting verification, not briefing demonstration media. Do not substitute test-run recordings, red-to-green assertions, CI screens, or passing-test counts for the visible change. Run tests as needed and summarize relevant coverage and limits briefly beside the outcome or in optional evidence. A focused driver may demonstrate real behavior through an observable boundary, but the audience should see the changed experience, output, or operational consequence rather than a test runner.

Read [Demonstrations and optional depth](references/demonstrations-and-depth.md) when preparing a visual briefing. Independently select representative scenarios, reuse suitable evidence, capture missing media, assemble the viewing experience, and verify it. Missing supplied recordings are a reason to inspect capture options, not to ask the user to produce them or settle immediately for text. Resolve routine media and layout choices yourself; do not stop at a media plan or ask for separate approval of ordinary local capture already within scope.

Keep a short explanation of the result, its significance, availability, and needed action beside the media. Remove prose that merely narrates visible clicks, output, or diagram structure. Put deeper evidence beside the relevant result in optional detail. If capture is unavailable or would exceed authorization, use an honest static alternative, bound the claim, and continue the rest of the briefing. Do not let one unavailable recorder block useful media elsewhere.

## Write the briefing

Give the document a descriptive title and a short opening that identifies its purpose, reporting scope, and central takeaway. Include the date, environment, or evidence boundary where needed to interpret the result. A new reader should know why the document exists and whether it is a draft, a report of others' statements, or a verified update.

Tell each outcome as a short connected explanation. Orient the reader to the earlier problem when it is supported, show what the evidence establishes now, and explain the consequence for users or colleagues. Put the material limit beside the claim it qualifies. Then state any actual action or decision, with the affected audience and known timing. These are questions the prose answers, not mandatory headings or a form to repeat for every item.

Make practical consequences concrete. If access, commands, configuration, ownership, or a working environment changes, include the verified instruction someone needs and when it applies. Do not invent a migration step, owner, deadline, release promise, or benefit to make the update feel complete. Missing usage instructions or unknown availability remain explicit when they prevent a handoff. State that no action is needed only when the evidence supports it; otherwise distinguish an informational update from an unresolved operational effect.

The result and its practical consequence must remain understandable when playback is unavailable or meeting time is limited. A meaningful final frame, diagram, or short result caption provides that alternative without repeating the whole demonstration in prose.

## Engage the user at consequential moments

Draft with the information already available. Ask only when an unresolved fact or choice would materially change what the audience believes or does and cannot be resolved from permitted evidence. Explain why the answer matters, give the established context, and ask the smallest useful question. Batch closely related factual gaps when that reduces interruption. Do not make the user retell the work, repeat settled decisions, or approve every topic, medium, and paragraph.

When a gap can be bounded honestly, continue and label it. If the central claim cannot be supported, narrow the claim or identify the necessary evidence instead of manufacturing certainty. A review request should point to the specific uncertainty or consequential wording; unchanged content does not need another approval. Include an audience decision only when one actually exists, with enough context and tradeoffs to answer it. Do not manufacture a decision to make the meeting interactive.

## Deliver one understandable reading surface

Keep the main explanation self-contained. Place optional evidence and depth next to the outcome they support, with descriptive labels that explain what a reader will find. Reuse existing documents for their distinct purpose. A briefing explains a period's results and team implications; `$multimodal-design-overview`, when installed and relevant, explains how an implemented system works. Neither requires creating the other. Avoid separate summaries, evidence narratives, and handoff documents that repeat the same content.

Team-facing references must be durable and meaningful to their audience. Keep local filesystem paths, localhost, session handles, unexplained artifact names, and invented or inaccessible URLs out of the briefing. An unpublished local deliverable is a draft; provide its file to the requesting user without representing it as shared. A missing shared destination does not block preparation. Apply existing publication authorization, and request anything genuinely missing only after the result is concrete and reviewable. Sending messages to others still requires explicit authorization.

Read the result as someone outside the workstream. They should be able to explain the result, its significance, its availability, and any action from the briefing itself. Remove duplicated detail and unjustified certainty. Check that any cited evidence supports the claim and any included media actually communicates its stated point. Report material verification or delivery limits in the handoff. Do not claim that a written skill, a generated file, or a rehearsal has demonstrated improved team understanding in a real meeting.
