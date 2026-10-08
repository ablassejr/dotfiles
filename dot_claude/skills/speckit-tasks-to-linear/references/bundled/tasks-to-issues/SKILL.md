---
name: tasks-to-issues
description: Publish an approved task graph to the selected issue tracker, or prepare a portable issue set, preserving self-contained outcomes, ownership, dependencies, and verified write results.
---

# Tasks to issues

Turn an approved task graph into usable work items in the destination selected for this project. Read [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md), [delivery planning](../implementation-specification-compiler/references/delivery-planning.md), and `$issue-writing` before drafting or publishing.

Resolve the source revision, authorized scope, actual project or queue, established status and labels, people, and destination capabilities. Reuse existing associations; do not invent a team, Triage inbox, three-person structure, or new container. Without a chosen tracker, prepare self-contained issue drafts and their dependency graph as a portable result. Ask for a destination only when publication is required next and the target cannot be inferred responsibly.

Each issue describes one independently useful outcome, its approved constraints, and observable completion evidence already supported by the request. Keep its design proposal as the only optional document reference. Source inventories, implementation rationale, and supporting assets belong in that proposal or the governing plan. Use [shared resources](../epic-spec-workflow/references/project-resources.md) to ensure necessary team access without forcing another upload location.

Validate the actual plan's scope, ownership, PR boundaries, and dependency meaning before writing. Preserve cycles or unresolved references as visible problems to resolve, not silently removed edges. When authorized, create only needed approved containers, publish issues, retain their returned identifiers, and then establish supported native relations. If the provider cannot express a relation, retain it in the owning plan with stable references and disclose that execution dependency.

Read back the saved issue content, membership, owners, status, and relations and compare them with the prepared plan. Reconcile uncertain or partial writes before retrying to avoid duplicate work. Apply the scope's existing [review and assignment policy](../epic-spec-workflow/references/issue-review-before-assignment.md), reusing completed reviews. Issue creation does not authorize code implementation, changes to unrelated projects, or a new approval process.

For the explicitly selected Linear/Notion/Camunda profile, use [the Linear plan adapter](../implementation-specification-compiler/references/linear-plan.md), [three-person policy](../implementation-specification-compiler/references/three-person-workstreams.md), and its real publication and review receipts. These helpers are provider-specific. Other destinations use their own supported operations; portable drafts do not require those accounts or fabricated completion receipts.
