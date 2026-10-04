# Media selection and delivery

Plan the media with the explanation and produce it as part of the overview. Select the medium for the understanding it provides about the inspected implementation and the destination's actual support. Use rrweb, asciinema, and other visuals liberally for relevant behavior and relationships, combining focused assets when they answer distinct questions, such as a boundary diagram and a demonstration of implemented recovery. Verify existing media against the selected baseline; prior design assets are not automatically accurate. Do not illustrate every paragraph or expand prose merely to narrate what the media shows.

| What the reader needs to understand | Useful medium | When a simpler form is clearer |
|---|---|---|
| Relationships, ownership, boundaries, or movement | Architecture, sequence, state, data-flow, process, or annotated spatial diagram | A sentence for one relationship; a table for independent mappings |
| Terminal interaction, progress, or recovery | asciinema recording with a player and meaningful preview | A command/result excerpt when time and interaction add nothing |
| A browser journey, validation, or state transition | rrweb replay of a controlled session | Annotated screenshots for a static state or a short sequence |
| Native UI, motion, or visual behavior a DOM replay cannot reproduce | Short screen video or animation | A still image when motion is incidental |
| How implemented behavior changes with inputs or configuration | Small interactive explanatory model, explorable diagram, or chart | A static comparison when there are few meaningful cases |
| Measurements, distributions, or quantitative tradeoffs | Chart with labeled units, data source, and assumptions | A table for exact lookup; prose for a single quantity |
| Sound or timing that is itself part of the implemented behavior | Audio example or captioned audiovisual clip | Text when narration merely repeats the document |

## Prepare the demonstration autonomously

Identify a representative starting state, action, and observable result for each useful demonstration. Include the failure, recovery, concurrency, or configuration branch that materially changes how the reader understands the design. Inspect existing assets and accessible runnable surfaces. Reuse a recording only when its revision and demonstrated behavior support the selected claim; otherwise prepare a focused capture. Missing supplied recordings are a reason to investigate capture options, not to hand that work back to the user.

Prefer an authorized application environment when it is available. If the full application cannot run locally, use an isolated harness that loads actual components or calls actual libraries from the inspected revision. Keep capture code separate from product code. Supply controlled inputs or fixture services and persistence where needed, and identify those substitutions beside the media. The resulting recording establishes only the behavior exercised by the real code; fixture responses cannot prove backend execution, persistence, integrations, or deployment. A reimplementation of the behavior remains an explanatory illustration.

Use available capture and rendering capabilities with their current documentation. Resolve routine scenario and layout choices yourself within existing authorization. If one capture route is unavailable or cannot represent the behavior faithfully, use a supported alternative or clearly labeled source-derived view, bound the claim, and continue the other media. Keep an explicitly requested but unmet medium visible as a limitation. Do not manufacture execution evidence or require live credentials merely to demonstrate source behavior that can be shown locally.

## Diagrams and static media

Choose a renderer suited to the content, editing needs, and destination. Simple supported Mermaid, D2, Graphviz, or ASCII diagrams can be sufficient; use LikeC4 for modeled architecture, draw.io/Excalidraw/tldraw for appropriate visual composition, or Figma/Archify for richer governed or interactive views. Check current available capabilities rather than treating this list as exhaustive. An active caller's renderer contract still applies.

Show only the implemented relationships needed for the current question. Label actors and boundaries with names the team recognizes, explain unfamiliar notation, and make the reading direction clear. Distinguish source-derived structure, configured behavior, and observed execution when that affects interpretation; mark unknown relationships instead of filling them with an ideal architecture. Color alone is insufficient. Keep readable text at the document's normal viewing size. Split an overloaded view by distinct questions rather than shrinking it.

For screenshots, use the actual relevant implementation state and focused annotations. For generated imagery, label illustrative content and avoid giving it the appearance of a captured implementation. Inspect the rendered export, including font size, contrast, clipping, connector direction, and caption accuracy. Retain editable sources with the owning asset when useful without creating another required reading surface.

## Terminal demonstrations with asciinema

Use a controlled terminal session of the implemented software to show the specific interaction and its outcome. Check the installed CLI, recording format, and intended player's compatibility against current [recording documentation](https://docs.asciinema.org/manual/cli/quick-start/) and [player documentation](https://docs.asciinema.org/manual/player/quick-start/). Build commands from the retrieved version's documentation; do not embed guessed universal flags in the workflow.

Record the actual command or a small driver invoking the real library through its observable boundary. Show the relevant inputs, output or error, and recovery when it explains the design. Explanatory labels may orient the viewer, but printing expected answers does not demonstrate execution. Retain the exit result and final observable state. Use suitable sample data and inspect prompts, commands, output, and recording metadata for material that should not be shared. Stop the recorder when the scenario ends. Preserve the actual sequence and result; shortening idle periods or adding a chapter marker must not imply faster execution or a different outcome.

Embed the cast with a compatible player in the local draft or authorized shared destination. Label the implementation revision, environment or fixture conditions, scenario, observed outcome, and any timing edits when they matter. A useful still frame and short result excerpt let the reader understand the point without playing the clip. A controlled local run establishes that scenario, not production deployment. Avoid dumping the whole transcript into the overview.

An asciicast is terminal event data, not a universal video attachment. A self-hosted player needs its player assets and recording available to the reader. For destinations that do not execute scripts, use a preview linked to a verified shared player, or an appropriate video/static export with its limitations stated. [Embedding guidance](https://docs.asciinema.org/manual/server/embedding/) explains the player and preview alternatives. Do not upload to a public recording service merely to obtain an embed when that disclosure was not authorized.

## Browser interaction replay with rrweb

Use rrweb when replayable DOM changes and user interaction explain the implemented behavior. It records browser state and events; it does not rerun the product backend or establish backend correctness. Capture the actual application where available, or actual components in the isolated harness described above with their fixture boundaries labeled. A reconstructed interface remains an illustration and cannot establish what the application implements. Consult the current [rrweb guide](https://rrweb.com/docs/guide) and the [upstream guide](https://github.com/rrweb-io/rrweb/blob/main/guide.md) for the selected recorder, replay package, privacy options, and compatible versions.

Reuse an authorized existing recording from an applicable revision or instrument a controlled application session within the requested scope. Authoring a design document is not permission to add production session tracking. Before capture, choose sample data and appropriate input/text masking or element blocking. Inspect the resulting events as well as the visible replay: masking inputs alone does not remove sensitive DOM text, URLs, or metadata. Keep raw event data and assets within the intended audience's access boundary.

Begin capture before the meaningful interaction, perform the scenario through supported browser controls, wait for the relevant completion or failure state, and retain the final state before stopping. Show submission, work in progress, and the observable result when those distinctions matter. The event file must come from that recorded interaction. Keep the initial state and event sequence needed for a valid replay; do not truncate an event array as though it were a video clip. Shortened idle pauses must preserve meaningful transitions and be identified when they affect interpretation.

Verify playback using the actual selected player, viewport, styles, fonts, images, and other required assets. Check the behavior being explained, including the relevant failure/recovery state if it is part of the scenario. Report what the replay actually shows rather than claiming general product verification.

Canvas and cross-origin frames need specific support; check the official [canvas](https://github.com/rrweb-io/rrweb/blob/main/docs/recipes/canvas.md) and [iframe](https://github.com/rrweb-io/rrweb/blob/main/docs/recipes/cross-origin-iframes.md) recipes when the scenario includes them. Preserve the replay sandbox; do not casually enable unsafe replay options to make a demo render. If a required surface cannot be captured faithfully, a scoped video or annotated sequence may explain it better. State the limitation and preserve any explicitly requested replay as an outstanding deliverable.

Deliver the compatible replay viewer, events, and required assets together in the local draft or authorized shared destination. Provide a meaningful preview and a concise explanation of the significant state change. A usable local draft does not require publication; a local JSON path, localhost player, or untested event file must not be presented as a team-accessible replay.

## Other interactive, video, and audio media

Use interaction when changing an input reveals how the implemented system behaves. Start with a meaningful default, make controls self-explanatory, show units and assumptions, and provide a reset or clear route back. An explanatory model must identify its simplifications and derive its behavior from inspected implementation; unsupported cases remain unknown. Do not turn documentation into a separate product build or require the reader to discover the explanation through trial and error.

Use video for important behavior that a static view or DOM replay loses. Crop and annotate the relevant area, make text readable, and make playback controllable. Use audio when hearing it matters to the implemented behavior, with a transcript or equivalent description; spoken explanation alone is not a reason to add audio. Label synthetic media. Do not autoplay sound or force a linear viewing sequence just to understand the system.

## Deliver and inspect in context

Place each asset beside the claim it explains. Its caption says what to notice and whether it is observed, derived from inspected source, or an illustration. Include the implementation revision, environment, or scenario where that affects trust, and a duration or useful starting point when that helps the reader choose to play. Keep asset identities and technical provenance in the owning records rather than a large media inventory in the document.

Verify the actual destination supports the chosen embed or attachment. Use durable shared URLs and descriptive link text, with a static preview and accessible explanation when interaction is unavailable. Exported documents must remain understandable when scripts and embeds do not survive the export. Do not invent a shared URL or claim access based only on the author's authenticated session.

For a portable HTML overview, embed player assets, recordings, and fallback images when feasible so the reader receives one usable file. Keep the main explanation self-contained and optional evidence beside the relevant passage. A diagram or replay should replace duplicated narration while leaving the system's purpose, practical consequences, and material limits clear. Do not make a local deliverable depend on a temporary capture server.

Open the assembled overview in its intended viewer. Play every included recording through to its outcome, exercise meaningful controls, and inspect the fallback. Check legibility at the displayed size, final-state framing, caption accuracy, and required assets. A raw cast, event file, or visible player container without verified playback is not a completed demonstration. Repair broken capture or rendering, or replace it with a usable supported alternative and state the limitation. When publishing, check that a teammate can reach the required media as far as available tools establish.

If hosting, access, or a requested capture is unavailable, complete the usable draft and explain the specific remaining delivery work outside the design narrative. An optional unavailable asset can be omitted when the explanation remains complete; a requested or understanding-critical missing asset remains an explicit limitation. Never label an untested recording, inaccessible link, or fabricated capture as a verified publication.
