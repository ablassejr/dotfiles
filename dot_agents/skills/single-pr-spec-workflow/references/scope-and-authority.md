# Scope and authority

## The unit of work

The unit is one issue, fix, or feature with one coherent observable outcome that can be delivered in one independently useful, reviewable PR. Multiple files, layers, migrations, and tests can belong to that outcome. A file count, duration, point estimate, or arbitrary SLOC threshold cannot establish or disprove this boundary.

Ask whether the PR can fulfill the agreed outcome against a known baseline, whether its changes and tests explain one causal story, and whether dependencies and deployment consequences fit that story. Record why the answer is credible. Unknowns that could change feasibility remain visible.

A safe backward-compatible migration, a feature flag, or coordination with an existing release process can fit one PR. Describe its actual prerequisites and operational steps. Do not equate a deployment step with an additional PR. Conversely, a required separately merged code change is a real dependency even if both PRs are called one feature. A follow-up promised to repair an incomplete contract does not make the first PR independently complete.

When the original outcome requires multiple PRs, explain the blocking dependency or coupled outcomes. Offer a narrower complete outcome, a justified alternative that fits, or a move to epic/program planning. The human chooses a changed scope. Continue independent research that informs that choice, but do not create the program or implement a partial outcome without instruction.

Implementation may eventually expose a material mismatch. The handoff tells the executor to return the evidence for a targeted specification revision instead of silently expanding the PR. Ordinary file-level adjustments that preserve the approved behavior can remain implementation judgment; distinguish them from a scope or contract change.

## Standalone authority

A standalone run uses the user's request and accepted decisions as its initial authority. Its artifact records a stable work identifier, revision, source/baseline references, decision history, and approval evidence. A local identifier need not be a provider issue ID.

The initial basis is implementation-context-free. Capture the intended outcome before inspecting implementation. A clear request or prior exact approval can supply the basis; missing fields do not justify inventing constraints. Ask only for a material missing choice. Supporting assumptions may remain explicit proposals while authorized investigation continues.

The specification holds the behavioral contract and rationale; its evidence references support factual claims. The handoff explains an implementation proposal and planned verification. When the two disagree, resolve the conflict in the specification rather than allowing a more detailed handoff to silently change intent.

Use the user's selected artifact destination or a writable local workspace. A standalone request does not require creating the selected issue tracker, the selected documentation home, Figma, or Camunda objects. Missing optional integrations do not block local specification work. A specifically required unavailable tool, required external evidence, or required publication destination is a real dependency; prepare unaffected work and report precisely what it prevents.

## Managed authority

When the work is already bound to an epic framework process or an approved managed ticket, inspect that binding and load the currently installed owning skills. Preserve the separation between approved semantic authority, issue contract and native relations, implementation design, workflow state, and source code.

Use the existing process instance, tenant, business identity, deployed definition, active work items, source revisions, and approval receipts. Do not initialize a substitute process, migrate a running process, replay historical approvals, or infer authority from a local manifest. Read the live state at resume and after accepted transitions. A reachable endpoint or successful local helper does not establish the required historical process identity.

This companion is a specification and handoff entrypoint, not a registered runtime operation. If the existing process has a design-only or review route, use its verified supported route. If the next modeled step is implementation, stop before it and retain the correct active wait or job; do not claim that this local handoff completed the runtime job. An unavailable or incompatible runtime path is reported to the owning workflow.

Reuse an inherited basis only when the current authoritative approval is valid and the exact unchanged basis covers the contribution. Read back the source approval and binding using the owning framework's rules. Record the actual approval lineage. A new outcome, constraint, forbidden tradeoff, destination, or authority scope requires the appropriate successor or authorization; reference equality alone cannot prove semantic coverage.

Keep native dependency truth and approved accounting contracts in their existing homes. Detailed implementation proposals belong in the existing linked design record when required. Do not promote a standalone Markdown artifact to the selected documentation home semantic authority or write managed manifest/schema fields this skill does not own.

Apply the current managed graph, supervisor-proposal, operation-adapter, and approval policies. The active epic framework uses Figma Design, LikeC4, and Archify for governed graph outputs and records their actual render evidence. Load that policy before governed visual work rather than inferring compatibility from a file extension. Keep three-person programs, project artifact uploads, milestone compilation, and issue fan-out in their owning program scope.

## Approval economy and binding

Separate four facts: the user approved the intent; the agent gathered evidence; a review evaluated the proposal; the human approved a particular final specification and handoff. Evidence for one does not prove the others.

Maintain a binding that identifies the work and current revision, the exact specification and handoff content, relevant visual artifacts, the source baseline including relevant dirty changes, and the evidence/decision revisions that support it. A content hash or immutable revision can identify content; it does not prove quality or approval. Do not invent timestamps, actor names, task IDs, or receipt values.

For local artifacts, record the actual response reference and actor together with the exact revision approved. If the platform cannot give a durable message reference, quote the actual response and identify the conversation and available timing honestly. For provider artifacts, retain their current provider revision or timestamp and fetched content binding under the owning adapter's contract.

Keep approval-status bookkeeping in a separate receipt or binding when editing it would change the reviewed content. A current approval receipt can bind unchanged proposal artifacts whose historical status was pending. Identify that current receipt clearly in the handoff response so an executor can distinguish the approved proposal from its earlier approval state. This does not prescribe a new file format or permit a receipt to approve changed content.

Reusing already granted authority avoids redundant permission questions. Continue fact-finding, in-scope repairs, formatting, and preparation covered by the request. When a semantic change requires a real choice, obtain that choice. Final design approval remains one decision over the complete current proposal, including its visuals. Do not split it into ceremonial approvals for every section.

Presentation-only repairs preserve the behavioral source and unaffected review evidence, but the revised presentation has a new binding for final review. A semantic change, changed baseline relevant to the proposal, stale evidence, or changed question invalidates dependent approvals. Preserve the history and reopen only the affected work.

## Resume and interruption

On resume, load the current artifact and actual decision history, then verify the authoritative source and relevant repository state. Identify which work is complete, which evidence is still applicable, the current unresolved question, and the next authorized action. Never use a remembered approval or old checkpoint as proof of current approval.

If work was interrupted during an external write, reconcile the existing operation and destination before retrying. If a human answered a question whose premise changed, preserve the answer as historical evidence and present the current choice rather than applying it to a different question.

Keep useful partial work when a capability or decision blocks completion. State what is missing, why it matters, what evidence would clear the dependency, and what can continue. Do not describe an unverified hypothesis as a completed investigation.

## Report labels

Use a label when its stated boundary applies. Ordinary research, drafting, and human understanding or decision waits use a plain-language progress report naming the current stage and pending question. They need no invented final enum. Reserve `BLOCKED` for an unavailable required dependency; distinguish that dependency from a normal human checkpoint when both are present.

| Label | Meaning |
|---|---|
| `AWAITING_SPEC_APPROVAL` | The current reviewable specification and handoff are prepared; the actual final human approval is pending. |
| `HANDOFF_READY` | The current single-PR specification and handoff have completed applicable review and exact final approval; remaining execution prerequisites are explicitly recorded. |
| `SCOPE_DECISION_REQUIRED` | Evidence shows that the agreed outcome does not fit the single-PR boundary without a human scope choice. |
| `BLOCKED` | Required evidence, authority, or a capability is unavailable and prevents the next necessary work. |

These labels report local specification work. They are not commands, runtime enums, provider status updates, or claims of implementation completion. A proposed feature can be fully specified while execution waits on a declared environment or release prerequisite. A material unresolved design choice cannot be hidden in that prerequisite list.
