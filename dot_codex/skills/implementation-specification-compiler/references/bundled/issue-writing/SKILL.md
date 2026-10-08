---
name: issue-writing
description: Write self-explanatory issues and work items in the selected tracker or portable task list. Keep required context in the issue, use only its design proposal as a document reference, and keep detailed implementation design in that proposal.
---

# Issue writing: describe the problem and required outcome

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

**When writing or editing any issue or work item** (create, save, comment, or when a user asks to "clean up", "polish", or "strip implementation details from" an issue), the description **must describe *the problem* and *the required outcome* — nothing about *how* the assignee will build it, and nothing about *what the finished thing will look like from the outside*.**

The issue is a contract about **what state of the world must exist afterward**. Everything else — code, structure, interface — is the assignee's call.

## Trigger

Use when preparing or saving an issue description, comment, or work-item draft in the selected destination. Also fires when the user asks to "remove implementation details", "clean up", or "polish" an existing issue or work item.

## Issue destination

Use the organization, tracker, project or queue, status, labels, and owner established by the current request or verified project conventions. Reuse an existing issue's associations. Do not assume any team's inbox or label, and do not create a container just to satisfy a template. Prepare a portable draft when no destination is selected; ask only when an actual publication needs missing destination information. Follow [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md).

## Treat these as implementation (remove)

- **Code-level details:** file paths, directory structures, framework / library choices, class or function names, module layouts, test-file locations, mocking strategies, "wire it into X" plumbing prose.
- **Interface-level details:** command syntax, flag names, subcommand placement in a CLI tree, exact HTTP paths, route names, function signatures, exact CLI/API/UI names, endpoint verbs, output formats. **The user-facing contract is still implementation** — the assignee chooses it.
- **Naming choices for internal resources:** specific IAM role names, exact database / schema names, exact secret names, exact S3 bucket / prefix strings, environment variable names — even if they exist today. Current names are the current *implementation*; a redesign can rename them and still satisfy the contract.
- **Structural suggestions:** "new subpackage", "mirroring the structure of X", "extends class Y", "under `apps/foo/…`".
- **Test-tooling prose:** "unit tests using vitest", "mocked Snowflake client", "pytest fixture" — replace with an outcome ("test coverage at parity with sibling operations").

## Keep (the actual contract)

- **The problem** — what's broken, what's painful, what today's workaround looks like and why it hurts.
- **The motivation** — why fixing it is worth doing now.
- **The outcome** — the state of the world after the operation, described in domain terms ("a developer with an open PR can, in one step, return the DB to a pristine baseline"), not interface terms.
- **Behavioral properties** — idempotence, error semantics ("fails loudly with actionable errors when …"), safety requirements ("destructive, requires explicit confirmation"), performance envelopes ("seconds, not minutes"). None of these prescribe an interface.
- **Constraints on what must NOT change** — expressed as domain properties ("no S3 mutation", "no preview task recycling"), not as specific paths.
- **Non-goals / out-of-scope** — the contract's boundary.
- **The optional design proposal reference** — the only document reference permitted on the issue. Native issue relations and PR associations retain their operational purpose.

## The single sentence-level test

Before saving, re-read every sentence and ask:

> Could a reasonable assignee choose a completely different design — different command name, different flag set, different interface, different resource names — and still satisfy this sentence?

If **no**, that sentence is the *solution*, not the *problem*. Rewrite it as a property of the outcome, or delete it.

## Common failure mode

The most tempting thing to leave in is the command syntax box:

```
just foo bar <arg> [--flag ...]
```

It feels harmless — "just describing the shape". It isn't. It commits the assignee to a CLI, a verb, a flag set, and a placement in the CLI tree. All of those are implementation. Cut it.

## Scope

Applies to issue descriptions and comments in the selected tracker. Does **not** apply to:

- Operator runbooks (by design pin exact commands/paths — that's their job).
- ADRs (by design record a specific decision + its concrete rationale).
- PR implementation explanations, including relevant paths and command names. PRs follow the separate [PR-writing contract](../pull-request-writing/SKILL.md) for standalone readability and proposal-only document references.

## Shared rule for every workflow

Apply this rule whenever any workflow creates an issue or work item, including implementation programs, standalone work, decision tickets, follow-up work, and imports. Apply it to workflow-authored issue descriptions, comments, and document attachments so later review steps preserve the issue's readability. An explicit user instruction controls any exception.

The reader must understand the issue without conversation history, another ticket, or an open document. Explain who faces the problem or question, the relevant current situation, why it matters, the required outcome or decision, and the approved scope and constraints. Include the observable completion evidence already supported by the request. Define unfamiliar terms where needed. Do not invent acceptance criteria to fill a template. Use only sections that help this particular issue; keep the title in the title field.

The design proposal is the only document the issue may reference, and linking it is optional. Use the actual proposal for the issue's scope, or the relevant section of its program proposal. Do not disguise a specification, handoff, research packet, ADR, grounding record, runbook, resource index, or code-mass attachment as a design proposal. Put source links and detailed records inside the proposal or internal workflow artifacts. Summarize any approved consequence needed to understand the issue directly in its prose. A document name, record ID, relative path, embed, attachment, or instruction to read another document is still a document reference even without a hyperlink.

Native parent, child, dependency, duplicate, milestone, owner, and PR relationships remain operational metadata. They cannot substitute for necessary issue context. The chosen shared document or artifact home retains the accessible supporting material; do not copy their document links onto individual issues.

## Automatic authoring and readback

When a workflow prepares an issue, write the complete problem or question and its required outcome from the approved scope. Read it as an assignee with no starting context and repair gaps, undefined terms, unsupported requirements, and references that carry essential meaning. Keep detailed source authority, basis lineage, grounding evidence, code-mass records, and implementation rationale in the design proposal and structured workflow records.

Before an authorized write, identify the actual design proposal URL if one exists and validate the exact issue-facing content with [the shared content validator](../../issue-content.md). If there is no proposal, omit the reference and keep the issue self-contained; do not create an unrelated document solely to satisfy the validator.

After publication, fetch the title, description, workflow-authored comments, and document attachments. Validate that readback and compare it with the prepared content. If publication is partial or adds a disallowed reference, reconcile and repair through the existing authorized write path before reporting success or advancing the workflow. Repeat the standalone reading pass after a material HITL edit. These are agent tasks within the stage, not new human approvals. An unavailable provider or validator leaves its verification explicitly pending.

The validator checks conventional links, designated document attachments, and nonempty title and body. It does not prove comprehension, classify every unlinked document mention, or verify that a URL is truly a design proposal. The authoring and readback review must establish those facts. A passing check cannot substitute for that review.
