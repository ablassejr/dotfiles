# Proposal media and prototypes

Use media to help the reviewer understand a proposed mechanism or choice. The most useful medium may be a diagram, an annotated screen, a comparison, a runnable model, or a short recording. A proposed system does not need to exist for the proposal to be explained visually.

## Choose a medium that answers a question

| Reviewer needs to understand | Suitable approach |
|---|---|
| Components, ownership, data flow, trust boundaries, or dependencies | A focused diagram with explicit current and proposed elements |
| State changes, concurrency, failure, or recovery | A sequence or state diagram; an interactive model when branching matters |
| A proposed interaction or user journey | Annotated screens or a small clickable prototype; rrweb when the sequence matters |
| A proposed command or computational mechanism | An illustrative command example, or an asciinema recording of an actual runnable prototype or experiment |
| A consequential choice | A compact comparison of evidence, expected benefits, costs, and uncertainty |
| Current behavior that motivates the proposal | A capture or view of the inspected existing implementation, labeled with its baseline |

Discover the capture and viewing capabilities available in this session before selecting media. Use the available diagram, design, browser, terminal, document, and interactive capabilities that fit the question. Prefer simple readable views over exhaustive architecture maps. Avoid imposing a renderer outside an actual caller's contract. No diagram or recording count is required.

## Show intent without fabricating implementation evidence

Label current, proposed, assumed, and unresolved elements where the viewer encounters them. In a mixed architecture view, use explicit labels and a readable legend; color alone is insufficient. Show undecided branches as alternatives rather than drawing one as selected. A caption should state the takeaway and the model's or recording's scope without repeating the diagram in prose.

For proposed behavior, create the smallest local explanatory prototype that materially helps review and remains within the user's authorized scope. Use fixed or synthetic data when appropriate, keep it separate from product code, and label mocked integrations, persistence, policy, and other substitutions. An illustrative prototype demonstrates the interaction or rule encoded in it; it does not establish backend feasibility, security, durability, performance, or production availability. Reuse an existing prototype when its behavior and revision fit.

If a recording explains the point better, capture real execution of that prototype. Start rrweb before the representative interaction, operate the UI through supported controls, and retain the meaningful final state. Use asciinema to record an actual prototype command, experiment, or driver. Preserve the output, failures, and recovery relevant to the claim. Do not print expected answers and call them a test, fabricate replay events, or present a hypothetical command as available tooling. A static mockup or pseudocode can explain a proposed command honestly without a terminal recording.

When demonstrating the existing baseline, inspect and exercise the actual relevant implementation. Keep current-system evidence distinct from recordings of proposed behavior. If an isolated harness uses existing components with fixture services, explain what is real and what is substituted. A side-by-side comparison must not imply equivalent evidence when one side is an observed system and the other is a simulation. Claim measured improvement only when comparable evidence supports it.

Consult applicable skills and current tool documentation before capture, rendering, embedding, or export. Use permitted environments and non-sensitive data. Inspect captured material for credentials, private session information, and irrelevant local details. Label edited time or sampled scope where it affects interpretation. If actual capture is unavailable, use an honest supported static or interactive explanation and continue useful work elsewhere.

## Finish and inspect the viewing experience

Embed media beside the claim it explains, with a concise caption and a meaningful static alternative. For portable HTML, embed player assets, recordings, and fallback views when feasible. In a shared editor, use its supported embeds or a durable accessible player with the essential explanation available in the document itself. Keep local draft assets portable; do not expose local source paths as team references or invent hosting links.

When a suitable permitted viewer is available, open the assembled document. Read diagrams at their displayed size, play every included recording through its outcome, and exercise meaningful controls and fallback views. Check that the view preserves the proposal's actual states, choices, and evidence limits. A generated asset or visible player frame is not proof of successful playback.

If the preferred viewer is unavailable, use another already available supported viewer that fits the document and existing authorization. Do not require a particular browser or MCP integration. A missing capability is different from a denied action: respect explicit tool restrictions, instructions to stop before alternatives, and security rejections. Do not bypass them through another route. Installing tools, changing authentication, or publishing the draft is not an implied remedy.

If no suitable viewer is available, finish the document and the applicable static checks, such as parsing embedded data, checking navigation targets and asset references, and checking script syntax. Repair defects those checks reveal and preserve or provide a meaningful readable fallback using the document's own content. Keep useful media; lack of a viewer does not by itself require deleting it or making the document text-only. Do not repeatedly retry unavailable tools or make the user repair the toolchain before receiving the result.

Report the checks actually performed and the specific unverified outcomes once, distinguishing document preparation from validation status. For example: “The proposal is prepared and its data, links, and script syntax were checked. Layout, scenario switching, and playback remain unverified because no suitable viewer was available.” Successful static checks or unchanged file hashes do not prove rendering or interaction. An existing document that needs no editorial changes can be delivered as reviewed and unchanged with the same verification limits.

When the user or governing workflow explicitly requires rendered verification before acceptance or publication, leave that specific gate unfinished. Complete independent work, explain which outcome needs verification, and ask only for the missing capability or authorized next step needed to satisfy that requirement. Do not silently waive the gate or claim full verification; ordinary authoring without such a gate can conclude with the disclosed limitation.

Repair failed capture or rendering within scope, or replace it with a usable alternative and disclose the remaining limit. Do not defer a promised explanatory asset as a paragraph describing what will eventually be added. A missing recorder need not make the entire document text-only, and a polished prototype must not hide an unresolved design decision.
