# Review and artifact design

Use this contract whenever a framework skill prepares a human interaction or a team-facing artifact. It owns presentation, question selection, and the division of information between artifacts. [Approval economy](approval-economy.md) owns approval reuse and repair routes; [open-ended decisions](open-decisions.md) owns answer assessment and response bindings. These writing rules introduce no additional approval task or runtime schema.

## Keep the user engaged in the work

When a scope begins, explain the outcome being designed, where the work is, and the next meaningful contribution the user may need to make. Derive stage information from [stage visibility](stage-visibility.md). As work advances, explain a material finding, its implication, and what the next activity will resolve. A stage change informs the user; it is not a request to authorize another routine step. Keep updates brief enough that the user can follow the design without reading an activity log.

During first-principles intake, resolve only missing fundamentals and present the resulting basis for its existing approval. Once that basis is approved, research facts and develop the design autonomously within the authorized scope. Use accepted decisions, stated preferences, and verified basis inheritance before creating a question. Do not restart a broad interview at research, architecture, visual, program, or ticket boundaries.

Prompt when an unresolved choice needs this person's judgment about intended behavior, scope, priorities, a material tradeoff or risk, or when required information or authority is unavailable. Explain what their answer changes and why it is needed now. A required final approval reviews a concrete, verified proposal and its exact scope. Do not solicit preferences about routine implementation details already determined by approved intent and evidence.

Before presenting a decision, investigate accessible facts, remove hypothetical branches without a material consequence, and check whether a recorded answer already settles it. Ask the smallest question that unblocks the design. Keep dependent questions in the internal frontier until their prerequisites settle; do not expose the entire tree or create a sequence of questions just to fill it. When several concerns are consequences of one choice, explain that choice together instead of asking the user to approve each consequence separately. Independent decisions keep their own bindings and are not bundled into ambiguous approval.

Each prompt contains the current recommendation when evidence supports one, the decisive evidence or uncertainty, meaningful alternatives and their consequences when useful, the specific answer needed, and why this user needs to decide now. Use natural language rather than a field checklist. Leave the answer open and make Ground Me available as optional depth. Do not require a grounding exercise, a code-mass table, or a full alternatives catalog in every prompt.

After an answer, state the understood choice and its practical consequence, record and assess it through the existing loop, then continue. Do not ask for confirmation of clear intent. Raise a material conflict with evidence and a concrete suggested adjustment. Reopen only the affected choice when new evidence, changed intent, or a different consequence warrants it; do not repeatedly challenge an acknowledged answer. If no question remains, say what is ready and continue to the existing review or handoff boundary. Do not invent a question to demonstrate engagement.

## Give each artifact one job

Before creating a separate artifact, identify its reader, the decision or task it supports, the information it uniquely owns, and its durable home. If an existing artifact already serves that purpose, update its owning section or record. A skill boundary, tool call, review pass, or generated filename is not a reason for another document. Do not create a new index or catalog solely to explain an unnecessary collection of files.

| Artifact or record | Information it owns | Reader's use |
|---|---|---|
| First-Principles Basis | Originating outcome, problem, invariants, boundaries, and success evidence approved for the scope | Approve intent once and reuse it while unchanged |
| Approved specification snapshot | Versioned requirements, constraints, decisions, and other normalized semantic records | Resolve the exact approved behavioral contract and its sources |
| Scope's design proposal | The coherent explanation of the recommendation, consequential tradeoffs, and how the design works | Understand and review that scope without prior conversation |
| Evidence or grounding record | The source-supported answer to a specific factual or provenance question | Inspect a disputed claim or decision-changing uncertainty |
| Review findings | Unresolved defects, their consequences, and disposition | Assess remaining concerns without rereading the specification |
| Delivery program and issues | Delivery ownership, scoped outcomes, observable verification, and native dependencies | Plan and perform each person's work |
| Visual or formal model | A relationship, behavior, or architecture view best understood in that form | Understand the distinct question named in its caption |
| Handoff and recovery records | Exact identities, revisions, approvals, verification, and resumption bindings | Verify or resume the authorized scope |

These are roles, not a required document count. Keep evidence, findings, and decisions in existing records or purpose-specific sections unless a separate resource materially helps their reader. Maintain one source for each fact or decision. Ledgers, matrices, timelines, and summaries are generated views of that source, not independently authored accounts. A handoff references approved content; it does not retell the design. An immutable snapshot preserves a revision and is identified as an archive, not another current document.

The design proposal translates normalized semantics into a readable explanation; do not publish a second full narrative in another documentation store or a separate executive summary with the same content. Include the context needed to understand each artifact independently, but do not copy whole rationales, research histories, requirement inventories, or decisions between artifacts. A self-contained issue states its own scoped behavioral contract, not the epic's design narrative. Apply [issue writing](../../issue-writing/SKILL.md) and [PR writing](../../pull-request-writing/SKILL.md); their sole optional document reference is the actual design proposal, which carries supporting links.

## Make the document explain itself

Use a descriptive title that names the project or behavior and the document's role. In the opening, explain what the document is for, who should use it, whether it is a draft, approved source, explanatory view, or archived evidence, and what action is expected now. Identify the responsible person or team and the governing source or version when relevant; mark an unresolved owner honestly. Put this context in the document itself, not only in a chat message or filename. Internal terms such as “kernel,” “packet,” “frontier,” and bare IDs are not sufficient reader-facing titles or link labels.

For example, “Invoice exports — Design proposal” can open with: “This proposal explains recoverable invoice exports for the delivery team. It is a draft for the product owner's design review. Review the proposed recovery behavior and the retention tradeoff below; the linked approved specification records the exact requirements.” This is an illustrative form, not text to copy when its claims are unverified.

Lead with the conclusion or proposed outcome, why it matters, and the decision needed. Explain behavior in complete sentences from the initiating actor through the outcome, weaving in material failures, recovery, and alternatives. Distinguish verified behavior, proposed behavior, assumptions, and unresolved choices where they occur. Use direct headings and short connected paragraphs. Use tables for genuine comparisons and visuals for relationships; do not restate a diagram in a parallel prose section. Keep necessary technical detail beside the claim it explains and supporting depth in precise, optional links or later sections. Avoid transcript-like histories, empty template sections, decorative subtitles, fixed length quotas, and exhaustive checklists unrelated to the decision.

At a later review, identify the changed decision, affected sections, and approval impact in the review message. Keep the document itself a coherent description of its current state. Direct attention to unresolved concerns and meaningful changes; do not demand another full review of unchanged material. Existing exact-revision final approvals remain required.

## Make references usable by the team

Every reference in a team-facing document resolves to an accessible, durable shared source with a descriptive label and enough context to explain why it is linked. Use verified records in the selected shared destination, hosted repository permalinks pinned to a revision, or an authorized shared artifact store. A bare ID needs a readable name and resolvable shared reference. A local filesystem path, relative scratch link, localhost page, session-only tool handle, or expiring private download is not a team handoff.

Keep local drafting files, manifests, operation receipts, raw extracts, and rendering bookkeeping in the agent's work area. Their internal tool inputs may retain local paths. Publish only the evidence or exported content needed by the team, with its purpose and source version; never copy local reference fields into reader-facing prose. Shared archival copies remain clearly labeled and outside the required reading path. Any review-critical material must be accessible when its review is requested, not promised for a later upload.

Before publication or handoff, inspect the rendered document, verify its links and media, and check access for the intended team audience. Confirm that another team member can tell what each document is, why it exists, which source governs, and what they need to do without asking the author. Fix overlapping content at its owner and repair ambiguous labels or inaccessible references within existing authority. If a destination or access decision is missing, complete the reviewable draft, retain it as unpublished, and ask only for that missing decision. Do not claim a team-ready publication from a successful local write or content hash.

Apply these checks during the existing editorial, publication, and handoff work. Report actual verification and any unresolved access limitation; do not add a separate human sign-off for the writing checklist.
