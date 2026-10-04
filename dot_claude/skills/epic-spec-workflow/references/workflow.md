# Workflow and scope contract

The semantic scope establishes the problem, desired behavior, constraints, rationale, and approved basis. It ends with the approved specification and verified handoff, or an explicitly identified prepared draft when delivery conditions remain unmet. `$epic-spec-workflow` does not start delivery execution implicitly.

An explicit `$implementation-specification-compiler` invocation turns that source into an ownership and dependency plan for the actual team. It reuses approved intent, reconciles current repository evidence, resolves material program choices, and prepares reviewable work. `$tasks-to-issues` publishes that work only to a selected, authorized tracker; a portable plan remains useful without one.

`$issue-implementation` owns one issue or task and one PR boundary. It checks approved intent, context, dependencies, design decisions, alignment, and applicable review before execution. `$single-pr-executor` owns implementation and observable verification. Reconciliation compares the integrated behavior with approved semantics and updates the chosen documentation home. Cleanup removes only provenance-owned temporary work.

At each scope, record what is prepared, what has been approved, what has been externally published and read back, what is implemented, and what remains uncertain. Store each fact and decision once in an existing governing record. Use [workspace and destinations](workspace-and-destinations.md), [workflow records](workflow-records.md), and [review and artifact design](review-and-artifact-design.md) to preserve authority and legibility.

Resolve only material human choices. A stage transition is a progress update, not another interview or permission prompt. Accepted answers remain settled until changed evidence or scope materially affects them. A grounding request informs the current choice; it does not silently answer it. Repair the earliest affected decision and dependent artifacts without restarting unrelated work.

When a configured orchestrator governs this scope, its accepted work-item completion is the execution authority. Follow that process's current position, identity, version, and bindings. The [packaged Camunda mapping](camunda-workflow.md) describes its existing Linear/Notion profile; it is not a prerequisite or provider-neutral state machine. Without that engine, record actual progress and explicit decisions in the current scope's evidence without inventing process keys or engine completion.
