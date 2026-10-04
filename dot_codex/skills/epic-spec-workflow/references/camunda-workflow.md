# Workflow and state contract

This reference describes the explicitly selected Linear/Notion/Camunda adapter profile. Apply its provider-specific schemas and operations only in that configured workflow. For other projects use [workspace and destinations](workspace-and-destinations.md) and the provider-neutral scope contracts.

## Three nested scopes

Semantic specification establishes the problem, desired observable state, principles, invariants, required behavior, and user-approved constraints and acceptance conditions. Its output is the immutable approved Notion Spec Release and verified handoff. `$epic-spec-workflow` owns this scope and stops at `HANDOFF_READY`.

An explicitly invoked `$implementation-specification-compiler` consumes that handoff. It verifies unchanged approved basis inheritance or obtains approval of new program intent before implementation context, reconciles the current repository, and resolves program decisions. Spec Kit plan, tasks, and cross-artifact analysis produce a dependency graph. Ownership, write surfaces, contract seams, independent tests and merge units, rollout, and rollback determine milestone partitions. Exactly three milestones form parallel workstreams for three distinct people under [three-person delivery planning](../../implementation-specification-compiler/references/three-person-workstreams.md). Each issue contributes one independently reviewable outcome and records its sizing rationale and observable verification. The native dependency graph must permit one issue per person to be ready together after stated prerequisites. One approved carrier project is the default, with additional projects or an Initiative only for a distinct approved reason. Native Linear relations carry dependency truth. Before creating the approved issues, an automatic Project resources stage uploads the complete deliberately prepared team artifact set to the carrier project and verifies project-member access under [project artifact publication](project-resources.md). The approved output is a Linear implementation program.

Each issue enters an approved basis and ticket decision loop through `$issue-implementation`. Its planning record names that PR's exact contribution, preserved behavior, minimum independently correct delta, and proof. An unchanged governing basis may be inherited; new intent requires approval. Ticket context, implementation design, first-principles alignment, planning code-mass audit, and adversarial review precede human approval of unresolved choices and `READY_FOR_IMPLEMENTATION`. One owner integrates one worktree and one PR. Independent behavioral verification and differential review precede merge; integrated conformance and `$specification-reconciliation` check the combined system, retain qualifying ADRs, and clean provenance-owned artifacts. None of these later stages runs implicitly from the semantic skill.

Human interactions and team artifacts follow [review and artifact design](review-and-artifact-design.md). Keep one owning record for each decision or fact, one coherent proposal per scope, and shared references with explicit purpose. After approved first principles, ask only for remaining consequential human choices; stage transitions provide progress without another grilling round.

## Authority and persistent records

The immutable approved Notion release owns semantics and basis lineage. LikeC4, Archify, and Figma project approved meaning; FigJam remains exploratory. Camunda 8.9 owns durable execution position and accepted work-item completion. Linear owns the approved program's implementation contracts, ownership, sequencing, status, and native relations. Semantic HITL discussion in Linear needs normalized Notion ratification before it can change semantics. Code, tests, contracts, schemas, migrations, and operational documentation describe the implemented system. ADRs preserve durable implementation rationale.

Keep the external evidence manifest described in [workflow records](workflow-records.md) outside the product repository. Its execution snapshot is derived from Camunda and is not a second process authority. Staging JSON and Markdown remain provisional even when a validator accepts their shape. The manifest references sources and approval evidence; it never grants itself semantic authority. Code-mass opportunity maps are semantic-stage hypotheses and evidence; actual milestone ledgers begin in the implementation program.

## BPMN stage vocabulary

The [Camunda process contract](camunda-orchestration.md) governs runtime progression. This table maps existing semantic gate names to modeled paths and required evidence; it is not a custom state machine enforced by manifest writes. Basis, decision, understanding, visual, specification, review-disposition, and exception approvals use native user tasks where the owning workflow requires human action. Service tasks return gate results to BPMN.

### Semantic stage mapping

| Current state | Normal next state | Evidence required to advance |
|---|---|---|
| `INITIALIZED` | `BASIS_DRAFT` | Raw request and scope are recorded; implementation context remains closed. |
| `BASIS_DRAFT` | `BASIS_APPROVAL_PENDING` | Versioned intake is structurally valid and unresolved fundamentals are explicit. |
| `BASIS_APPROVAL_PENDING` | `BASIS_APPROVED` | Named-human approval binds to the exact basis version. A revision request returns to `BASIS_DRAFT`. |
| `BASIS_APPROVED` | `CONTEXT_GATHERING` | Approval is current; repository and integration context can open. |
| `CONTEXT_GATHERING` | `CONTEXT_RECONCILED` | Snapshot pins identity, baseline, worktree state, source revisions, contradictions, and classified forces. |
| `CONTEXT_RECONCILED` | `SEMANTIC_DESIGN` | Basis/current-state reconciliation is complete; changed intent has an approved successor basis. |
| `SEMANTIC_DESIGN` | `ADVERSARIAL_REVIEW` | Research is `PROCEED`, semantic records are traceable, and blocking decisions are resolved. |
| `ADVERSARIAL_REVIEW` | `VISUAL_REVIEW` | Material semantic findings are repaired or disposed of by their proper owner, with no unresolved blocker. |
| `VISUAL_REVIEW` | `NOTION_PUBLICATION` | Applicable architecture reviews and renderer checks pass, sources are current, and exact visual revisions are included in the pending combined final proposal review. Record why no view is needed when none is applicable. |
| `NOTION_PUBLICATION` | `NOTION_APPROVAL_PENDING` | The complete normalized Notion draft and its Linear supervisor proposal pass readback comparison. Partial writes cannot advance. |
| `NOTION_APPROVAL_PENDING` | `NOTION_APPROVED` | A named human approves the verified content; the immutable release and constituent revisions are created and read back without mismatch. |
| `NOTION_APPROVED` | `HANDOFF_READY` | The immutable handoff is complete, current, read-back verified, and clear of blocking semantic questions. |
| `HANDOFF_READY` | None | Report the package and stop. Further work needs a separate explicit invocation. |

`BLOCKED` reports a modeled wait or incident with the last completed gate and recovery evidence. When the cause is resolved, Camunda resumes the applicable work item with fresh evidence. `SUPERSEDED` reports a retired workflow or artifact and links its successor. A failed gate follows the modeled route to its earliest repair stage with recorded reasons and dependent invalidations. Report every active branch and its permitted action instead of assigning one global next transition. A reopened completed semantic workflow uses a recorded successor rather than mutating the approved release.

## Reusable decision substate

During the owning scope's design stage, the frontier selects one unblocked decision and records `DECISION_PENDING`. An open-ended answer enters `DECISION_VALIDATION` for automatic assessment. Material disagreement, conflict, decision-changing evidence, or consequential ambiguity opens a follow-up with reasons and a suggested change. The human can retain the choice, revise it freely, or request grounding. Changed originating intent uses intake, missing facts use research/context, and a clean or explicitly retained answer becomes `DECISION_RECORDED` before the frontier is recomputed. An empty frontier permits the scope's review only when its other gates pass.

A Ground Me request records `GROUNDING` while keeping that decision unresolved. After investigation and provenance review, `UNDERSTANDING_ALIGNMENT` asks the human to confirm, correct, or request more depth. Deeper work returns to grounding. A correction records `GROUNDING_MODEL_UPDATE`, updates the evidence, and obtains alignment with the corrected model. Confirmed understanding with an explicit, matching combined answer enters automatic decision assessment. Otherwise it returns to the current `DECISION_PENDING`. When the premise is false, record the finding while understanding is pending. After alignment and packet validation, Ground Me returns `QUESTION_INVALIDATED`; the parent decision workflow accepts the modeled grounding result and publishes the frontier evidence through an operation-aware adapter, preserves the evidence and old question, removes it from the active frontier, and rebuilds affected dependencies. Invalidation does not select an option or approve a replacement question.

The parent scope state stays separate from this decision substate. The manifest's response-binding envelope carries the question ID, frontier revision, and packet ID/hash alongside the unchanged packet and human action, as specified in [workflow records](workflow-records.md). Reject a stale binding before invoking a helper so a late answer cannot resolve a different or revised question.

## Camunda resume and external-effect recovery

Follow [the Camunda resume protocol](camunda-orchestration.md). Resolve the root instance, verify its definition and version, read variables and referenced artifacts, and inspect active user tasks, jobs, events, incidents, called subprocesses, and terminal state. Validate source hashes, revisions, approvals, baseline freshness, and configured static gates. Reconstruct the permitted action from that live position. Resume does not acquire a distributed workflow lease or perform process-instance modification.

Persist intended external effects and recoverable receipts through [operation-aware adapters](operation-adapters.md). Repeated attempts use the same intended operation identity. A native destination precondition can protect a conditional write; other destinations may offer idempotency, guarded publication, reconciliation, or explicitly recorded best-effort risk. A lack of universal writer exclusion does not itself block a reconciled destination. Report a missing required adapter capability honestly and preserve dependent work for retry or incident recovery.

Before context-sensitive review, visual or Notion publication, or handoff, compare the current target branch with the recorded baseline. Record intervening changes and their impact on context, grounding, code mass, architecture, and handoff. If irrelevant, retain the evidence attribution and record the assessment. If relevant, mark affected records stale and rerun reconciliation and dependent reviews through the model's repair paths. Preserve prior evidence when the approved baseline changes.

## Earliest-stage repair routing

| Discovery | Owning repair |
|---|---|
| Desired-state or goal defect | First-principles intake and successor basis |
| Unsupported factual claim | Research loop |
| Human value, risk, or irreversible choice | HITL frontier |
| Unexplained current behavior | Ground Me |
| Conflicting grounding evidence | Deeper grounding or a named human decision |
| Requirement contradiction or new product behavior | Semantic specification/change request |
| Architecture inconsistency | LikeC4 and architecture review |
| Misleading visual | Archify or Figma presentation review, or semantic routing when meaning changes |
| Missed repository impact | Implementation-program compiler |
| Unsafe shared write surfaces | Program repartitioning |
| Multiple merge units in one issue | Issue split |
| Implementation violates approved intent | Ticket design, or semantic change request if intent must change |
| Durable technical rationale | Approved ADR |
| Combined system differs from approved release | Integration and as-built reconciliation |
| Obsolete provisional artifacts | Provenance-bounded repository cleanup |

When one finding affects several stages, start at the earliest defective stage and invalidate only its dependents. Research cannot decide human values; visuals cannot ratify semantics; code cannot silently redefine the approved release.

## Cleanup and completion

Persistent records include approved releases and normalized semantic grounding in Notion; program and ticket decisions, review findings, and verification links in Linear design proposals, with ownership and native relations on the issues; current formal and governed visual projections; and repository artifacts needed to build, test, deploy, operate, or understand the system, including approved ADRs.

Raw history extraction, unapproved reconstructions, research notes, provisional claim and contradiction analysis, temporary Grounding Packets and exports, local indexes, team coordination files, and scratch plans are ephemeral. Their normalized conclusions and source references survive when material. Indexes and shared infrastructure are removed only when owned by this workflow and no other active work needs them.

After a transition's write, readback, validation, applicable approval, and accepted Camunda work-item completion with durable evidence references all succeed, remove only obsolete provenance-owned provisional artifacts. Reuse approvals bound to unchanged content and revisions; recording `HANDOFF_READY` does not require an extra handoff approval. Semantic Markdown can be removed after the approved release and immutable handoff are normalized, reference-validated, visually reviewed, durable, and verified. Product-repository reconciliation removes remaining workflow debris later. Neither cleanup nor local validation substitutes for the `HANDOFF_READY` evidence gate.

## Final planning presentation

Each planning scope publishes the [supervisor design document](supervisor-design-document.md) in Linear before its existing final approval. The semantic path follows verified Notion draft publication; the program path follows validated plan compilation; the ticket path follows design review. The `publish_design_proposal` service task precedes `approve_release`, `approve_program`, or `approve_ticket_design` respectively. The user task reviews the exact `designProposalBinding`; changes return through the existing design repair path and repeat publication. The document is a durable explanatory projection, retained with its source and approval references.

## Graph renderer enforcement

The [graph visual policy](graph-visual-policy.md) requires Figma Design, LikeC4, or Archify for every graph-like output, including provisional, published, and as-built views. Record the content kind, renderer, exact artifact, and completed render receipt; validate them before presentation or gate completion. FigJam remains available for non-graph exploration. Delivery formats and screenshots of diagrams do not bypass the policy.

The [approval economy contract](approval-economy.md) defines exact basis inheritance, structured automatic review, combined final review, presentation repair, combined Ground Me answers, and bounded technical recovery. Human tasks remain for changed intent, unresolved judgment, and the final supervisor proposal.

The [stage visibility contract](stage-visibility.md) presents scope, active branches, revisited stages, latest completed work, and the current waiting state. Its timestamped projection is derived from Camunda and is not a persisted execution authority.

Follow [automatic step continuation](stage-visibility.md#automatic-step-continuation). Accepted completions lead directly to the next authorized work item, including routine checks and bounded retries. Stage headings report progress and introduce no additional approval. A continuous worker services configured handlers; a directly acting agent continues the same execution loop without a user continuation prompt.

[Open-ended human decisions](open-decisions.md) defines free-text answers, automatic assessment, evidence-based suggestions, and human-owned reconsideration. The assessment and any follow-up remain within the owning design-decision stage.

## Individual issue review before assignment

The implementation program creates issues without assignees, then runs each issue’s complete ticket decision and supervisor-review loop. **Individual issue HITL** remains current until the entire created set finishes. Only then does **Team assignment** apply the approved workstream owners. Ticket execution reuses an exact, verified review. Follow [the issue review and assignment contract](issue-review-before-assignment.md) for jobs, publication variables, worker configuration, native approval checks, and provider readback.
