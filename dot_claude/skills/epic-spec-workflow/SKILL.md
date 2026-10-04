---
name: epic-spec-workflow
description: Design or resume a large epic before implementation. Establish approved first principles, reconcile evidence, resolve material human decisions, and produce a legible specification and handoff in the project's chosen destinations.
---

# Epic specification workflow

Design the required behavior and its rationale, then deliver a verified semantic handoff. Stop at the specification boundary; this request does not implicitly start implementation, create delivery issues, or publish to an external service.

Read [workspace and destinations](references/workspace-and-destinations.md) and [review and artifact design](references/review-and-artifact-design.md). Use the current project's organization, repositories, audience, conventions, and chosen document and issue homes. No organization, tracker, wiki, project container, or process engine is required merely to use this skill.

## Establish authority and resume accurately

The approved specification owns required behavior, constraints, decisions, and their sources. Its exact reviewed revision and First-Principles Basis lineage preserve intent. The design proposal explains that source coherently to a teammate. A visual is a projection with a distinct communication purpose. A delivery plan owns work allocation and dependencies. Merged code, tests, contracts, and migrations establish implementation; ADRs preserve durable rationale. Assign these roles to existing records or purposeful sections without duplicating narratives.

On resume, read the actual governing records, source revisions, approvals, repository baseline, pending decisions, and incomplete writes. Reuse settled choices and unchanged approvals. If a configured orchestrator governs this scope, read its current process position and follow its versioned contract. The packaged [Camunda integration](references/camunda-orchestration.md) and [runtime](references/camunda-runtime.md) apply only to that selected profile. A local manifest or provider status cannot impersonate engine completion.

Read [the workflow contract](references/workflow.md) for scope boundaries and [workflow records](references/workflow-records.md) for evidence and handoff. Keep preparation, approval, external publication, and implementation distinct. A local draft can be useful without being a team-ready published handoff.

## Establish first principles before implementation context

For a new scope, invoke `$first-principles-intake` with only the raw request, directly applicable approved product goals, stated outcomes, and explicit constraints. Resolve missing fundamentals about the problem, desired observable state, irreducible behavior, invariants, minimum sufficient change, and evidence of success. Obtain the existing exact-basis approval before implementation context can anchor the design. Do not repeat intake when an unchanged approved basis already covers the scope under [approval economy](references/approval-economy.md).

After approval, invoke `$post-basis-context-loader` and `$basis-context-reconciler`. Resolve repository identity, baseline, worktree state, relevant organizational evidence, and current source revisions. Use the configured structural and semantic tools, verify indexed leads in source, inspect the current project's issue and review history where relevant, and use primary research for unresolved external facts. Follow [tool routing](references/tool-routing.md) and applicable host or repository documentation requirements. Missing access to one source remains an explicit evidence gap, not an assumption that the project must adopt that source's provider.

Initialize a specification workspace only when useful and authorized. Inspect proposed paths and preserve existing files and conventions. Spec Kit and `specflow` are optional integrations with their own actual compatibility limits, not prerequisites for reasoning or drafting.

## Develop the semantic design

Invoke `$subtractive-design-analyzer`, `$first-principles-specification`, and `$framed-engineering-sequence` at the appropriate scope. Start with the smallest mechanism that satisfies approved intent. Challenge requirements, remove unjustified work, simplify the surviving system, improve trustworthy feedback, and automate stable execution. Preserve applicable behavioral verification and code-mass obligations; unknown estimates remain unknown. Removal credit requires grounded purpose, consumers, current necessity, and the approvals and replacement evidence that the governing policy actually requires.

Give each semantic record a stable identity, authoritative source, rationale, and established steward. Distinguish facts, interpretations, proposals, decisions, and unknowns. Maintain each claim and decision once. Generate a graph, ledger, matrix, or separate document only when it answers a distinct question. Apply [research and review](references/research-and-review.md) and [subtractive code mass](references/subtractive-code-mass.md) when relevant.

Use `$decision-frontier-manager` to filter out settled choices, accessible facts, and routine details covered by approved intent. Route only a material unresolved human choice to `$human-decision-loop`. Explain what the answer changes and why it is needed now. After first principles, stage boundaries do not trigger another grilling round. Assess an open-ended answer against the approved basis, evidence, and accepted decisions; raise a consequential conflict with reasons, respect a clear final choice, and record it before recomputing affected decisions.

Offer `$ground-me` for deeper understanding of the pending choice. It reconstructs current behavior, history, decision lineage, and still-valid forces using sources the project actually has. Its evidence packet does not itself answer or remove the parent's decision. A matching explicit combined alignment-and-answer can settle both without another confirmation. An invalid premise returns evidence for the parent to preserve the old question and recompute its dependents. See [open-ended decisions](references/open-decisions.md) and [approval economy](references/approval-economy.md).

## Review the design and its explanation

`$specification-research-loop` and `$speckit-autonomous-research-gate` return `CONTINUE_RESEARCH`, `REQUEST_HITL`, `REVISE_FIRST_PRINCIPLES`, or `PROCEED`. `PROCEED` requires traceable goals and requirements, sufficient applicable evidence for blocking facts, no unexplained invariant conflict, and human ownership of remaining material judgments. It ends factual research, not unresolved decisions or required approval.

Use independent, bounded review contexts at the owning scopes. `$adversarial-specification-review` receives the basis, current semantic records, evidence, accepted decisions, models, and relevant sources without the author's hidden reasoning or favored conclusion. Classify findings by consequence and repair authority. Recheck repaired findings and affected downstream artifacts rather than restarting unrelated stages.

Before context-sensitive review or handoff, compare the baseline with current relevant changes. Refresh affected evidence and bindings without silently rewriting prior approval. Apply the project's actual visual policy, using each medium for a different explanatory purpose. Inspect available rendered views and report verification limits honestly. Preserve explicitly required renderer and review gates.

Prepare one concise, self-contained `$design-document` under the [supervisor proposal contract](references/supervisor-design-document.md). It explains the recommendation, behavior, consequential tradeoffs, and actual open decisions in the selected document home. Combine visual and design review where the workflow already permits it. The proposal remains comprehensible without opening supporting records.

## Publish or deliver according to the request

Use `$specification-publisher` and [specification publication](references/specification-publication.md) when publication is authorized. Resolve the real destination and existing record, prepare exact content, write within scope, and read back the resulting revision and associations. Reconcile a partial write before retrying. Retain content-bound approval and a reconstructable snapshot. A repository commit or versioned document can carry the semantic release; an editable title alone is not a release identity.

If the task requests a draft or has no chosen shared destination, deliver the prepared portable document with its status and verification limits. Ask for a destination only when publication is the next required action and the answer is genuinely missing. Do not create a tracker project or document account to satisfy a hardcoded layout.

## Handoff and cleanup boundary

The handoff identifies the approved specification revision, basis lineage, repository baseline when applicable, semantic and evidence identities, decisions, non-goals, residual questions, relevant code-mass evidence, approval, and verification. It references the design rather than retelling it. Use descriptive shared links or portable content appropriate to the requested delivery; keep local operational paths internal.

Report `HANDOFF_READY` only when the scope's required approvals, freshness, durable content, and intended team access are actually verified. Otherwise deliver the completed draft or preparation and identify the exact unmet condition. Preserve recovery evidence and selected canonical repository documents. Remove only provenance-owned temporary artifacts after their required durable replacement and authorization are established.

Stop at this boundary. A later explicit `$implementation-specification-compiler` invocation plans delivery for the actual team and chosen tracker or portable work list. `$issue-implementation` and reconciliation skills own execution and integration. Optional provider-specific references describe their supported automation; they do not silently choose those services for a new project.
