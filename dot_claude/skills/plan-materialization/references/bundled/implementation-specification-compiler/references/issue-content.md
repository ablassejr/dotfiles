# Self-contained issue content

Every workflow uses [the shared writing skill](../../issue-writing/SKILL.md). Issues explain their approved work or decision without external context. The design proposal is their sole optional document reference. Supporting documents remain accessible inside that proposal and through project resources.

## Public validation contract

Run `specflow validate-issue-content issue-content.json --json` before an issue write and against fetched content afterward. This local command makes no provider calls. Supply the issue-facing content, not the complete provider API request:

```json
{
  "title": "Make interrupted billing exports recoverable",
  "body": "## Problem\nBilling operators must restart an export after an interruption and cannot tell whether it finished.\n\n## Required outcome\nOperators can recover an interrupted export and see whether it completed, without duplicating the exported records.\n\n[Design proposal](https://linear.app/acme/document/billing-export-design)",
  "design_proposal_url": "https://linear.app/acme/document/billing-export-design",
  "comments": [],
  "document_attachments": []
}
```

`title` and `body` are required nonempty strings. `design_proposal_url` is an optional HTTPS URL or null. `comments` contains workflow-authored comment strings; `document_attachments` contains document objects with `title` and `url`. Omitted arrays mean empty arrays. The same proposal's section fragments are allowed. Direct issue and GitHub PR links retain their operational purpose. Relative document links, other web references, Markdown reference links, HTML links, and document attachments to any other document fail with `invalid_issue_content` and field-specific details. An unlinked document mention still violates the writing rule and is checked by the editorial pass.

A successful response reports `policy: "self-contained-issue-design-proposal-only-v1"`, `reference_check: "passed"`, and `editorial_review: "required"`. This last field states the local check's limit; it is not a new approval task. The command exits 2 on a contract error.

## Program integration

Schema-v4 plans retain semantic IDs, basis and release bindings, and structured Code Mass Contracts as machine records. Their issue bodies contain the problem and approved outcome rather than mandatory source-authority or orchestration headings. Each issue may declare `design_proposal_url`; the shared content check runs inside `validate-linear-plan` and before the configured program publication handler runs. A plan with disallowed issue content returns `invalid_issue_content` in its validation errors, and Camunda program completion returns `invalid_program_plan`.

The issue-creation handler returns every `createdIssues` entry with a `content` object containing the fetched `title`, `body`, optional `design_proposal_url`, `comments`, and `document_attachments`. Explicit empty arrays establish that no workflow-authored comment or document attachment was published. Completion validates this object and compares it with the exact approved plan projection before individual issue review starts. Changed content returns `invalid_issue_review`; a disallowed reference returns `invalid_issue_content`. Reconcile partial writes and repair the existing issues before retrying. Content intentionally changed after approval returns through the existing planning review path.

The handler resolves the designated proposal against the actual scope and provider readback. The local runtime validates the supplied evidence; it does not authenticate arbitrary provider commands or police writes made outside these workflows. Supporting resources are published at project scope and are not issue document attachments. Ticket HITL records and technical evidence live in the proposal and internal workflow records; the issue receives only any approved behavioral consequences it needs to remain self-contained.

## Native associations on the selected provider

The optional `native_associations` field identifies actual native issue, pull-request, commit, diff, and CI associations on any HTTPS provider. Populate it from inspected provider records, not from guesses about a URL or an attempt to relabel a supporting document. For example:

```json
"native_associations": [
  {"kind": "issue", "url": "https://gitlab.example.org/library/catalog/-/issues/42"},
  {"kind": "pull_request", "url": "https://gitlab.example.org/library/catalog/-/merge_requests/51"}
]
```

The validator permits these exact association URLs in authored prose and comments. Document attachments still accept only the actual design proposal. Existing recognized Linear issue and GitHub operational links remain compatible without the extra field. Read back saved content and its actual associations through the selected provider before reporting publication complete. This local check cannot prove provider identity, access, publication, or the truth of the association's declared kind; editorial review remains required.
