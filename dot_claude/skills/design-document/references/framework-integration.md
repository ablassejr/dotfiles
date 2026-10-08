# Framework integration

Select capabilities for the proposal's actual needs. Discover the installed skill or tool and read its applicable instructions. These routes are optional capabilities, not stages that every document must pass through.

| Need | Applicable capabilities | Result used in the proposal |
|---|---|---|
| Understand the relevant existing system | Claude Context, source inspection, project exploration, architecture analysis, domain modeling | A verified baseline and the boundaries affected by the recommendation |
| Resolve a consequential factual or feasibility question | Documentation lookup, research skills, applicable modules of `multimodal-research-compiler` or grounding tools | Supported facts, uncertainty, and useful evidence; no mandatory new research dossier |
| Explain an existing specification or design | The supplied first-principles basis, semantic records, implementation design, or existing proposal | Its actual intent, constraints, decisions, and open choices, with source authority preserved |
| Clarify architecture, interactions, or behavior visually | Available diagram, Figma, tldraw, Draw.io, Excalidraw, Archify, or other suitable rendering tools | Readable views of the proposal; honor a caller's real renderer contract |
| Make a proposed mechanism or interaction understandable | Prototype, playground, visualization, browser, or terminal capabilities | A bounded explanatory model, with actual rrweb or asciinema capture when useful |
| Challenge a recommendation or inconsistent explanation | Relevant bounded design-review or adversarial-review capabilities | Material findings and corrections, without an automatic additional human review round |
| Deliver in the requested medium | Document, presentation, PDF, web, Linear, Notion, or other destination tools | One usable proposal with compatible media, appropriate access, and publication readback |

Use only the modules needed for the authoring task. Reusing a research, rendering, or review capability does not automatically invoke that skill's planning, implementation, or publication workflow. Missing planning history does not block a standalone proposal. When the user asks only to document a supplied design, do not compile a delivery program, create issues, or implement it.

For repository investigation, invoke Claude Context first and verify its context in underlying sources. Retrieve applicable CLI documentation through Docs MCP before using commands; refresh missing or stale documentation before constructing invocations. If documentation access blocks a command, continue independent authoring and identify that specific limit instead of guessing syntax.

## Work within an existing planning workflow

When an epic, program, or ticket workflow explicitly calls this skill, identify the governing design source, its revision, the current scope, and the existing review action. This document explains that source; it does not become a competing semantic authority. Route material source conflicts back to the owning decision rather than silently resolving them during writing.

The epic framework's supervisor-design-document contract owns the proposal's purpose, selected destination, applicable visual policy, publication readback, and exact-revision approval binding. Honor the current project's configured rules; its [destination contract](bundled/epic-spec-workflow/references/workspace-and-destinations.md) does not choose a provider merely because a connector is installed. The authoring skill does not itself complete a `publish_design_proposal` job, create a binding receipt, grant publication authority, or advance a Camunda task. An actual authorized adapter and verified provider result are needed for those operations. A standalone invocation does not inherit those workflow gates or require Linear.

Use the existing approval and repair path when one applies. Editorial improvements retain the governing source; a changed design returns to the appropriate decision. Reuse accepted answers and direct attention to what materially changed. Keep machine receipts and source inventories outside the reader's narrative.

`design-document` explains what is proposed and why. `multimodal-design-overview` explains how an already implemented system works. An approved proposal remains a proposal until implementation is established; an implementation overview can serve as optional baseline evidence without duplicating its full contents here.
