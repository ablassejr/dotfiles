---
name: issue-writing
description: Write self-explanatory issues and work items in the selected tracker or portable task list. Include minimal behavioral acceptance criteria, keep required context in the issue, use only its design proposal as a document reference, and keep detailed implementation design in that proposal.
---

# Issue writing: describe the problem and required outcome

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

**When writing or editing any issue or work item** (create, save, comment, or when a user asks to "clean up", "polish", or "strip implementation details from" an issue), the description **must explain the problem, the required outcome, and minimal observable acceptance criteria grounded in the stated intent.** Keep implementation design in the optional design proposal.

The issue is a contract about **what state of the world must exist afterward**. Leave internal design choices to the assignee while preserving the user's stated constraints and established public contracts.

## Trigger

Use when preparing or saving an issue description, comment, or work-item draft in the selected destination. Also fires when the user asks to "remove implementation details", "clean up", or "polish" an existing issue or work item.

## Issue destination

Use the organization, tracker, project or queue, status, labels, and owner established by the current request or verified project conventions. Reuse an existing issue's associations. Do not assume any team's inbox or label, and do not create a container just to satisfy a template. Prepare a portable draft when no destination is selected; ask only when an actual publication needs missing destination information. Follow [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md).

## Treat these as implementation (remove)

- **Code-level details:** file paths, directory structures, framework / library choices, class or function names, module layouts, test-file locations, mocking strategies, "wire it into X" plumbing prose.
- **Unrequired interface design:** proposed command syntax, new flags, routes, signatures, or output formats that the request does not require. Preserve an existing or explicitly required public interface when it is necessary to identify the problem or acceptance outcome; do not strip the user-visible behavior from the contract.
- **Naming choices for internal resources:** specific IAM role names, exact database / schema names, exact secret names, exact S3 bucket / prefix strings, environment variable names — even if they exist today. Current names are the current *implementation*; a redesign can rename them and still satisfy the contract.
- **Structural suggestions:** "new subpackage", "mirroring the structure of X", "extends class Y", "under `apps/foo/…`".
- **Test-tooling prose:** "unit tests using vitest", "mocked Snowflake client", "pytest fixture" — replace with the observable behavior that must work. Test frameworks, fixtures, and execution commands belong in the implementation or verification plan.

## Keep (the actual contract)

- **The problem** — what's broken, what's painful, what today's workaround looks like and why it hurts.
- **The motivation** — why fixing it is worth doing now.
- **The outcome** — the state of the world after the operation, described in domain terms ("a developer with an open PR can, in one step, return the DB to a pristine baseline"), not interface terms.
- **Required behavioral properties** — only those established by the request or affected contract, such as idempotence, error semantics ("fails loudly with actionable errors when …"), safety requirements ("destructive, requires explicit confirmation"), performance envelopes when actually required. These are examples, not default requirements.
- **Constraints on what must NOT change** — expressed as domain properties ("no S3 mutation", "no preview task recycling"), not as specific paths.
- **Non-goals / out-of-scope** — the contract's boundary.
- **The optional design proposal reference** — the only document reference permitted on the issue. Native issue relations and PR associations retain their operational purpose.

## The single sentence-level test

Before saving, re-read every sentence and ask:

> Does this sentence establish the problem, required observable behavior, or a stated constraint, or does it choose an internal solution?

Keep the necessary behavioral contract and constraints. Rewrite an unrequired solution as an observable outcome, or remove it. An acceptance criterion may constrain public behavior without prescribing its internal implementation.

## Common failure mode

The most tempting thing to leave in is the command syntax box:

```
just foo bar <arg> [--flag ...]
```

It feels harmless — "just describing the shape". It isn't. It commits the assignee to a CLI, a verb, a flag set, and a placement in the CLI tree. If the request leaves these choices open, omit the invented syntax. Retain an exact interface only when it is an established or explicitly required contract needed to understand the work.

## Minimal behavioral acceptance criteria

Derive the smallest useful set of acceptance criteria from the user's stated goal, the problem's first principles, and established behavior that the change must preserve. Explain what the actor or caller can do and what observable result establishes success. Use concise domain-language bullets, with context and an initiating action when they matter; Given/When/Then syntax is optional. The issue explains why the work matters; the criteria make completion reviewable without repeating that explanation.

Cover the intended success outcome and only the failure, recovery, or compatibility cases that materially distinguish a correct result within the stated scope. For a bug, describe the correct behavior under the triggering conditions, not the internal repair. For research or decision work, describe the answer or decision needed instead of inventing runtime tests. Do not add arbitrary counts, performance thresholds, permissions, new restrictions, or implementation choices to fill a template. Deriving an observable check from an established requirement is allowed; creating a new requirement is not.

For example, if the reported bug is that clearing a search leaves old results visible, a criterion can say: “When a person clears the search, the list shows the same results as an unfiltered list.” If preserving filtered search is part of the affected contract, also state its expected result. Do not prescribe a debounce interval, component name, or test framework.

Reuse clear completion conditions already in the issue instead of adding a duplicate section. Resolve wording and routine verification choices autonomously. Ask one focused question only when competing interpretations would materially change the required behavior or scope; explain the consequence and recommend an interpretation. Do not seek approval for each criterion or test boundary.

## Scope

Applies to issue descriptions and comments in the selected tracker. Does **not** apply to:

- Operator runbooks (by design pin exact commands/paths — that's their job).
- ADRs (by design record a specific decision + its concrete rationale).
- PR implementation explanations, including relevant paths and command names. PRs follow the separate [PR-writing contract](../pull-request-writing/SKILL.md) for standalone readability and proposal-only document references.

## Shared rule for every workflow

Apply this rule whenever any workflow creates an issue or work item, including implementation programs, standalone work, decision tickets, follow-up work, and imports. Apply it to workflow-authored issue descriptions, comments, and document attachments so later review steps preserve the issue's readability. An explicit user instruction controls any exception.

The reader must understand the issue without conversation history, another ticket, or an open document. Explain who faces the problem or question, the relevant current situation, why it matters, the required outcome or decision, and the approved scope and constraints. Include the observable completion evidence already supported by the request. Define unfamiliar terms where needed. Prioritize minimal behavioral acceptance criteria derived from that scope; do not invent additional requirements to fill a template. Use only sections that help this particular issue; keep the title in the title field.

The design proposal is the only document the issue may reference, and linking it is optional. Use the actual proposal for the issue's scope, or the relevant section of its program proposal. Do not disguise a specification, handoff, research packet, ADR, grounding record, runbook, resource index, or code-mass attachment as a design proposal. Put source links and detailed records inside the proposal or internal workflow artifacts. Summarize any approved consequence needed to understand the issue directly in its prose. A document name, record ID, relative path, embed, attachment, or instruction to read another document is still a document reference even without a hyperlink.

Native parent, child, dependency, duplicate, milestone, owner, and PR relationships remain operational metadata. They cannot substitute for necessary issue context. The chosen shared document or artifact home retains the accessible supporting material; do not copy their document links onto individual issues.

## Automatic authoring and readback

When a workflow prepares an issue, write the complete problem or question and its required outcome from the approved scope. Read it as an assignee with no starting context and repair gaps, undefined terms, unsupported requirements, and references that carry essential meaning. Keep detailed source authority, basis lineage, grounding evidence, code-mass records, and implementation rationale in the design proposal and structured workflow records.

Before an authorized write, identify the actual design proposal URL if one exists and validate the exact issue-facing content with [the shared content validator](../../issue-content.md). If there is no proposal, omit the reference and keep the issue self-contained; do not create an unrelated document solely to satisfy the validator.

After publication, fetch the title, description, workflow-authored comments, and document attachments. Validate that readback and compare it with the prepared content. If publication is partial or adds a disallowed reference, reconcile and repair through the existing authorized write path before reporting success or advancing the workflow. Repeat the standalone reading pass after a material HITL edit. These are agent tasks within the stage, not new human approvals. An unavailable provider or validator leaves its verification explicitly pending.

The validator checks conventional links, designated document attachments, and nonempty title and body. It does not prove comprehension, classify every unlinked document mention, or verify that a URL is truly a design proposal. The authoring and readback review must establish those facts. A passing check cannot substitute for that review.
