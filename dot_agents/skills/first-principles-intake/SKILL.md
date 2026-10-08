---
name: first-principles-intake
description: Establish and obtain human approval for a versioned First-Principles Basis before an epic or implementation ticket can load repository, history, or implementation context.
---

# First-principles intake

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Run this gate before any repository, Git, pull-request, implementation-oriented issue history, or existing architecture is exposed to the intake reasoning. Its job is to establish what should be true, why that matters, and what must remain true without allowing the current implementation to define the problem.

For a program or ticket wholly covered by an existing approved basis, retain that exact record and validate its explicit, content-bound human approval; include the accepted user-task completion when an existing Camunda process governs this scope through [approval economy](references/bundled/epic-spec-workflow/references/approval-economy.md). Do not draft a duplicate basis or ask for duplicate approval. New intent or constraints require the restricted intake and approval below.

Prefer a fresh agent invocation with no inherited turns. Give it only the raw user request, the ticket title and stated outcome when a ticket exists, directly applicable approved product goals, and explicit constraints supplied by an authoritative source. If a genuinely context-isolated invocation is unavailable, state that limitation and keep the intake deliberately restricted; do not claim a fresh-context result.

Read [the question sequence](references/question-sequence.md), [the completeness gate](references/completeness-gate.md), and [the anti-anchoring rules](references/anti-anchoring-rules.md). Reuse answers already stated by the user. The following sequence guides coverage; it is not a questionnaire to administer in full. Ask only a missing fundamental that changes the basis, one material question at a time:

1. What observable condition should be true when the work is complete that is not true now?
2. What underlying failure, unmet need, cost, or risk makes that outcome necessary?
3. What behavior must exist after this change that cannot be removed from the problem?
4. If this change succeeds, what existing responsibility, process, concept, or behavior should become unnecessary or simpler?
5. What must remain true, or must not be compromised, while producing that outcome?
6. When scope is ambiguous or broader than necessary, what is the narrowest acceptable change that satisfies the outcome?
7. When proof is not already implied by the desired state, what evidence would demonstrate that the outcome is correct?

Do not propose a library, service, class, schema, architecture, or implementation option during intake. Do not use terminology learned from the repository or turn a requested mechanism into the underlying goal. Do not invent a constraint because the present system might contain it.

Create a First-Principles Basis that conforms to [the packaged schema](schemas/first-principles-basis.schema.json). Record the allowed input sources, fresh or restricted isolation, how each required or conditional question was resolved, that implementation context was not exposed, and that the agent introduced neither a solution proposal nor new implementation terminology. Keep the full schema record for validation. Present its outcome, problem, necessary behavior, boundaries, and success evidence as a concise connected explanation, including only applicable constraints, assumptions, and unresolved points. Explain that this basis preserves originating intent and that approval opens contextual design. Retain exact version binding without making the user review the machine envelope. Do not ask for exact files or symbols during intake. The named human must approve or correct that exact version. Validate it with:

```text
python3 scripts/validate_basis.py <basis.json> --require-approved --json
```

No implementation-context loader may run until validation succeeds. A later discovery never overwrites an approved basis. Create the next version with a new `basis_id`, incremented `version`, and `supersedes_basis_id` pointing to the prior record, then validate the lineage with `--previous <prior-basis.json>`. Preserve both versions so the original intent, contextual discovery, and reason for revision remain distinguishable.
