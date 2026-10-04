---
name: implementation-specification-compiler
description: Compile an approved specification into a reviewable delivery plan with clear ownership, independently useful single-PR work, and explicit dependencies for the project's chosen tracker or portable work list.
---

# Implementation specification compiler

Consume an approved specification on explicit invocation and prepare the delivery plan before any external issue creation. The semantic workflow stops at its handoff boundary. Read [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md), [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md), and [delivery planning](references/delivery-planning.md).

## Verify the source and scope

Resolve the exact approved specification, its content revision or snapshot, approval evidence, basis lineage, and relevant repository baseline. The source may live in repository documentation, a shared document, a wiki, or a portable package. Verify its content and authority; do not require a Notion page, Linear project, or a second copy in another service. A stale baseline, unresolved semantic blocker, missing source, unverified claimed publication, or material mismatch returns to its owning decision.

Reuse an unchanged approved basis that covers this program. New intent requires its own approved basis before implementation context. Invoke `$post-basis-context-loader` and `$basis-context-reconciler`, then resolve material program choices through `$decision-frontier-manager` and `$human-decision-loop`. Keep program approval separate from semantic approval while reusing settled decisions.

Use `$framed-engineering-sequence` and `$subtractive-design-analyzer` before partitioning work. Ground uncertain removal candidates, remove work without a distinct observable contribution, simplify ownership and dependency boundaries, and form the smallest independently useful and verifiable batches. Preserve applicable code-mass accounting, review, exception, and behavioral testing obligations without inventing new product requirements.

## Compile the actual team's work

Use the people, team size, effort limits, ownership boundaries, and project containers established for this scope. Do not infer three people, a particular inbox, or a mandatory project solely from a historical example. If an approved three-person program applies, retain it and use [its profile](references/three-person-workstreams.md). Otherwise group work according to actual responsibilities and dependency overlap, without adding filler work or invented owners.

Each issue or portable task owns one coherent outcome, one integration owner when established, one reviewable PR boundary, source semantics, observable verification, and material dependencies. Record uncertain ownership explicitly. Keep estimates and structured contracts in their owning plan or proposal sections. Identify shared prerequisites, conflicting write surfaces, contract handoffs, rollout, and rollback when they affect execution. Check cycles, unresolved references, and actual readiness; do not claim parallel progress merely because lanes have different names.

Write self-contained issue prose through `$issue-writing`. Keep implementation design, source inventories, and detailed evidence in the proposal or internal records. Use native relationships when the chosen tracker supports them; otherwise preserve the dependency graph in the selected planning record and explain the limitation. A tracker without milestones or native blocking edges can still hold the work without fabricated provider fields.

Bind the plan to its actual source and baseline. Read the complete plan as a reviewer and verify scope coverage, ownership, PR boundaries, dependency meaning, and existing obligations. The portable plan is usable without a provider-specific schema. A validator can establish only the contract it actually implements.

## Review and publication

Prepare one `$design-document` explaining the program under the [supervisor proposal contract](../epic-spec-workflow/references/supervisor-design-document.md). Use a visual ownership/dependency view when it helps, with the actual people and groups. Keep supporting evidence optional and purpose-labeled. Readback and rendered verification retain their distinct limits, including the unavailable-viewer fallback.

Use the existing final approval for the concrete plan and proposal; do not create another approval per issue, split, or file. Prepare the deliberate team artifact set under [shared resources](../epic-spec-workflow/references/project-resources.md). Existing shared references may satisfy access without uploading duplicate files to the tracker. A local draft remains explicitly unpublished.

When external creation is requested and authorized, invoke `$tasks-to-issues` for the chosen tracker. Resolve its actual parent/container, workflow, and people. Create only needed authorized containers, create issues, retain returned identities, apply supported relationships, and read back content and associations. Preserve partial results for reconciliation. Do not report a graph published from local validation alone.

Follow [issue review and assignment](../epic-spec-workflow/references/issue-review-before-assignment.md) when the governed program requires it. Review-only work does not implement issues; execution still observes live blockers. After the required design decisions and review pass, a separately authorized `$issue-implementation` invocation may execute the approved PR boundary.

## Optional packaged automation

The packaged `specflow` runtime, [manifest](references/manifest-and-cleanup.md), [Linear plan](references/linear-plan.md), and [three-person policy](references/three-person-workstreams.md) implement the explicitly selected Linear/Notion/Camunda profile. Preserve their real field names and validation requirements when using that profile. They do not validate arbitrary providers or generic portable plans. Do not initialize that runtime, require its accounts, or manufacture its receipts for other projects. Reuse independent content and code-mass utilities only when their input contract fits, following current CLI documentation.

Cleanup preserves the selected canonical documents, approved plan, recovery evidence, and unrelated work. A compatibility cleanup check cannot justify deleting a repository's chosen documentation home. Use the reconciliation and provenance-based cleanup skills only within their authorized scope.
