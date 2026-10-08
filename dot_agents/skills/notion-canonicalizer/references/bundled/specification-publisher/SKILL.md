---
name: specification-publisher
description: Prepare or publish a canonical specification in the project's chosen documentation home, preserving exact content, approval, source relationships, and honest readback and access status.
---

# Specification publisher

Use [workspace and destinations](../epic-spec-workflow/references/workspace-and-destinations.md), [specification publication](../epic-spec-workflow/references/specification-publication.md), and [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Publish only the requested specification scope; publication does not start implementation or authorize unrelated cleanup.

Resolve the actual governing source, revision, destination, audience, existing record, and authorization. A repository revision, shared document, wiki, or portable package can hold the specification. Reuse the chosen home rather than requiring a second service. When only a draft is requested or no target is established, finish a useful portable result and identify its unpublished status.

Prepare exact semantic records and their readable explanation with distinct ownership of information. Preserve stable identities, source references, supersession, and content-bound approval where required. Check references and media within available capabilities. Do not create another narrative, approval gate, or document merely to satisfy a publishing tool.

For authorized publication, use supported writes and concurrency controls, then fetch and compare the saved content, relationships, source revision, media, and audience access. Keep preparation, readback, rendering, and access evidence distinct. Reconcile partial or mismatched writes before retrying and report the remaining limitation accurately.

When the workflow requires an immutable approved release, retain a reconstructable snapshot of the exact approved content with its source and approval evidence. A mutable title alone is insufficient. New content follows the existing successor and review path; unchanged content does not require another interview. Return verified references and status to the owning workflow.

Use [the Notion adapter transaction](../epic-spec-workflow/references/notion-publication.md) only when that provider and its governed runtime profile are selected. Do not invent a Notion page, Linear proposal, or Camunda task for another destination.
