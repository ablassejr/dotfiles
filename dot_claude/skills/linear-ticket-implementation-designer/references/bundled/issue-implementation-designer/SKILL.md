---
name: issue-implementation-designer
description: Produce a concrete repository-grounded implementation proposal for one issue or work item and store it in the issue's linked design record rather than its description or comments.
---

# Issue implementation designer

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Resume `$issue-implementation` after the ticket-level basis is approved, `$post-basis-context-loader` returns evidence sufficient for the design decisions, and `$basis-context-reconciler` classifies its relationship to the basis. Apply `$framed-engineering-sequence` at ticket scope before choosing code shape.

Invoke `$subtractive-design-analyzer` against the ticket's responsibility domain and use `$ground-me` for uncertain or unknown deletion safety before proposing code. Describe the entry point, exact behavior introduced and removed, affected public contracts, files and symbols added and removed, production and test SLOC estimates, conceptual-complexity delta, public-API delta, dependency delta, data and state changes, concurrency, failure and recovery behavior, security boundaries, migrations and rollback, observability, and behavior-focused verification. Explain why deletion-only and existing-mechanism reuse are insufficient and why the selected mechanism is the minimum correct and comprehensible design.

Keep the proposal to one issue, one owner, and one pull request. Fill the issue's structured Code Mass Contract and explain its implications in the design proposal. If the issue cannot remain independently useful and reviewable, return `ISSUE_SPLIT_REQUIRED` rather than hiding a second change inside it.

During [program issue review](../epic-spec-workflow/references/issue-review-before-assignment.md), unresolved execution blockers do not by themselves prevent design. Ground the proposal in approved predecessor contracts, resolve material design dependencies, and leave implementation blocked until its native prerequisites are satisfied. Return prepared design evidence to the modeled ticket decision loop; finalize alignment and review in the governing records after that loop resolves; use `specflow.finalize-ticket-design` only for its configured runtime profile.

Use `$decision-frontier-manager` and `$human-decision-loop` to resolve material choices one question at a time. Keep required estimates and accounting in the structured Code Mass Contract. Surface only the grounded consequences that materially help the current choice, such as reversibility, operational risk, migration cost, or code-mass impact; do not require the supervisor to parse a full accounting table for every question. When the human selects `Ground me`, suspend the choice, invoke `$ground-me`, align understanding, and accept an explicit combined answer through [approval economy](../epic-spec-workflow/references/approval-economy.md) when the evidence and question still match. Without that answer, return to the current question; an invalid premise requires recomputation.

Run `$first-principles-implementation-alignment`, the planning pass of `$code-mass-auditor`, and `$adversarial-implementation-review` in that order before presenting the concise final decision frontier. The planning audit returns `CODE_MASS_TARGETED`; it does not claim committed measurements or approve a Net Addition Gate. At the end of planning, publish the resulting proposal as the linked [supervisor design document](../epic-spec-workflow/references/supervisor-design-document.md), using the existing record when available. Its main narrative explains and proposes the design to a human with no starting context, prefers visuals over equivalent text, and retains only sentences that add necessary understanding. Keep detailed engineering evidence behind precise links unless the decision needs it. Fetch and inspect the document before the existing final design approval in the selected review surface, then bind approval to its exact source, revision, and content hash. The issue body retains the approved behavioral contract and only its optional design proposal reference; code-mass details remain in the proposal and structured records.

## Graph visual gate

Apply the shared [graph visual policy](../epic-spec-workflow/references/graph-visual-policy.md) to every graph-like output. Use Figma Design, LikeC4, or Archify and retain matching render-operation and artifact evidence. Include all produced or published visuals in the current step’s inventory and run `specflow validate-visuals <manifest.json> --json` before presentation. A missing renderer or invalid receipt blocks the visual output. Non-graph media keep their own communication purpose.

Follow [approval economy](../epic-spec-workflow/references/approval-economy.md) for the scope’s evidence-bound automatic routes, combined final visual/design review, targeted revision, and existing authorization. Automatic review records remain distinct from human approval.
