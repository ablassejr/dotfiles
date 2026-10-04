---
name: decision-frontier-manager
description: Maintain the dependency graph of unresolved implementation decisions and select the single next material question after basis-context reconciliation.
---

# Decision frontier manager

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Build a dependency graph from the approved basis, current-state map, reconciled constraint ledger, Code Mass Opportunity Map, and unresolved implementation choices. A decision is unblocked only when all of its prerequisite decisions and factual questions are resolved.

Bind the selected decision and understanding response to the actual question revision and reviewed content under [workflow records](../epic-spec-workflow/references/workflow-records.md). If an existing engine governs the scope, also use its real user-task identity and accepted completion contract. Otherwise record the assessed explicit answer in the current scope's records without requiring a provider or fabricating process state. Helpers validate evidence; they do not create authority or approve an answer.

Before selecting a question, remove choices already settled by the approved basis or accepted decisions, resolve accessible facts, and handle routine design details within that authority. Keep candidates only when a human answer can materially change intended behavior, scope, priorities, or accepted risk. When none remain, return the completed frontier without prompting. Otherwise select one material question from the unblocked frontier. Prefer a question with greater downstream impact, lower reversibility, higher uncertainty, and more dependent decisions after honoring prerequisite order. Remove branches that cannot change the approved outcome. Do not batch the frontier and do not ask a question whose answer depends on another unresolved question.

Keep each question’s stable ID, basis links, current-state evidence, and response binding in its record. Present a plain-language question with the consequence at stake, why the user must decide now, and the minimum evidence needed to answer. Use descriptive shared references in the prompt; do not display the graph or machine envelope as required reading. Use schema version 3 for open-ended questions. Alternatives and a recommendation are optional context, not an exhaustive answer set. When useful, explain their behavioral consequences, grounded code-mass effects, complexity, reversibility, operational risk, and migration cost without inventing estimates or options. Offer `Ground me` for every material question.

Represent the selected question with [the packaged schema](schemas/decision-question.schema.json) and validate it before presentation:

```text
python3 scripts/validate_decision_question.py <decision-question.json> --json
```

After the named human acts, pass the question and action record through `scripts/advance_decision.py`. An answer first requires assessment. A clean assessment or explicit disposition of its concerns records one decision and requires frontier recomputation. `ground_me` suspends the same decision without resolving it or recomputing the frontier. `question_invalidated` removes the false premise and requires recomputation.

An answer does not enter the graph until `$human-decision-loop` assesses it against the approved basis, evidence, and accepted decisions, and resolves any material follow-up. After a recorded answer, recompute the whole affected frontier. After Ground Me, apply an explicit combined answer only through the verified [approval economy](../epic-spec-workflow/references/approval-economy.md) contract. Without a matching answer, keep the decision unresolved and replace only its evidence, wording, or options. If Ground Me proves the premise invalid, mark `QUESTION_INVALIDATED`, update the context model, remove the invalid node and dependent assumptions, and recompute the graph before choosing a new root question.

The frontier is complete only when every material decision is resolved or explicitly deferred by the named human and no consequential branch remains silently assumed.
