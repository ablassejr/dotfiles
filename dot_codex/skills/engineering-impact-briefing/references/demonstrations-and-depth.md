# Demonstrations and optional depth

Plan the media with the story and produce it as part of the briefing. Use several focused visuals or recordings when they explain distinct outcomes. Choose by the audience's question and the destination's capabilities, rather than adding decoration to an already complete prose report. A supplied recording is useful evidence, but it is not a prerequisite for preparing a visual review.

## Choose what the audience should see

For each outcome that benefits from a visual, choose a representative task that makes the change apparent. Show how that task behaved before the work and how it behaves after, retaining enough context and final state for the viewer to understand the consequence. Compare like inputs and conditions; identify changes in scope, environment, data, or timing that affect the comparison. Include a consequential failure or recovery path when it changes how colleagues interpret or use the capability. Do not impose universal slide, word, duration, or topic quotas.

| What needs explaining | Useful medium |
| --- | --- |
| A browser task becomes possible, clearer, or easier | Paired rrweb replays showing the earlier workflow and the changed result |
| A command, converter, library, or recovery path changes its result | An asciinema comparison of actual inputs, outputs, errors, or recovery |
| A visible state changes, or a recording needs a fallback | Annotated before-and-after screenshots or meaningful frames |
| A boundary, dependency, data flow, or availability changes | A comparison diagram, compact table, or interactive explanation |

Use rrweb and asciinema proactively when the sequence explains the difference; use static comparisons when sequence adds little. For example, show the earlier manual recovery steps beside the recovery behavior after the change, or show the same input producing an unusable result before and a useful result after. State measured savings only when comparable evidence supports them. An interactive illustration can explain a change, but label it as an explanation rather than a recording of the system.

Inspect both sides of the comparison. If the earlier version cannot run, use suitable historical footage, screenshots, or a clearly labeled source-derived illustration with its evidence limit. Do not fabricate a broken earlier experience or present a reconstruction as a recorded run. If no baseline is supported, show the current result with that limit or keep the point in text. An investigation may compare the earlier uncertainty with the supported finding without pretending that system behavior changed.

Test runs, CI screens, assertion results, and pass counts do not show the team's before-and-after experience. Keep them in concise verification notes or optional supporting evidence. If a harness is needed to expose a component's real behavior, demonstrate its relevant input and output; do not present the harness's checks as the outcome.

## Capture the evidence within scope

First inspect existing media and the runnable surfaces available from the permitted evidence. Reuse material when its revision, environment, and demonstrated behavior fit the claim. When it does not, prepare a focused local capture instead of handing the capture work back to the user. Reuse installed capture, browser, diagram, and document capabilities, and consult the chosen tool's current documentation before invoking it. Keep recorder and player formats compatible.

When an authorized application environment is available, record the relevant interaction and retain enough starting context for a new viewer. When the full system cannot run locally, an isolated harness can exercise the actual component or library from the inspected revision with synthetic inputs and fixture services or persistence. Keep the harness separate from product code. State those substitutions beside the replay, and limit the claim to the behavior exercised. A component replay cannot prove backend persistence or cloud execution supplied by a fixture. If actual execution cannot be captured, use a clearly labeled source-derived illustration or existing evidence.

For a browser demonstration, capture the representative task on the relevant earlier and current versions when available. Begin rrweb capture before the meaningful interaction, perform it through the supported browser controls, wait for the relevant completion or failure state, and retain that final state before stopping. For an asynchronous action, show submission, work in progress, persistence, and refreshed display when they explain the difference. Each event file must come from its labeled recorded interaction.

For a terminal demonstration, run the actual command or a small driver that invokes the real library through its observable boundary while asciinema records the session. Use comparable inputs on the earlier and current versions when available, and show the changed result, error, or recovery. Explanatory labels may orient the viewer, but printed expected answers are not execution evidence. Preserve exit results and enough context to distinguish a useful outcome from a command merely starting or a test passing.

Use non-sensitive inputs within existing authorization. Inspect the recording for credentials, private session data, and irrelevant local details before including it. Prepare safe data and capture boundaries first; recapture or redact exposed material without concealing behavior relevant to the claim. Shorten idle gaps when helpful, while retaining the meaningful transitions. Label synthetic data, edited time, historical footage, and sampled scope where they affect interpretation. Capturing media does not authorize deployment, external publication, or new access.

## Assemble and verify the viewing experience

Label the earlier and current states clearly. Give each medium a concise caption stating what changed, why it matters, the relevant revision or environment, and the material evidence limit. Keep prose about the consequence and colleague action; remove duplicate narration of the visible sequence. Provide meaningful static frames or a brief comparison so unavailable playback does not erase the difference.

Embed working players next to the claims they explain. For a portable HTML briefing, embed player assets, recordings, and fallback images when feasible so the user receives one usable file. Respect the requested destination: where playback cannot be embedded, use its supported preview or an accessible, durable player link with a readable static alternative. A local draft can be complete without a shared hosting destination. Do not claim that local assets are already available to the team.

Open the assembled briefing in its intended viewer. Play every included recording through to its outcome, inspect the rendered framing and captions, and exercise meaningful tabs, branches, or layout controls. Check that someone outside the workstream can see what changed and why it matters without interpreting a test log. Check that recordings remain understandable at the displayed size and that static alternatives preserve the comparison. A raw cast, an rrweb event file, or a player container without verified playback is not a completed demonstration. Repair broken capture or rendering, or replace it with an honest usable fallback and state the limit. Retain the source association and capture scope needed to reproduce or assess each demonstration.

## Use depth without creating another presentation

Keep the main briefing coherent without opening tickets, an audit, a design overview, or a code diff. Put optional detail at the point where a reader might want it, explaining its purpose rather than saying "see artifacts." A live presenter can answer a specific question with that detail after stating the result; traversing a tracker is not itself an explanation of the work.

For a supplied time budget, fit the narrative and representative demonstrations to it, reserving room for consequential questions as appropriate. Without a budget, choose a compact treatment rather than interrupting for a number. If preparation cannot support the intended presentation, provide the strongest honest explanation available and identify the remaining preparation clearly.

Keep slide content, spoken explanation, and captions complementary if those forms are requested. The slide carries the point and evidence, the presenter explains the consequence, and optional sources answer deeper questions. Do not generate all three as separate deliverables by default.
