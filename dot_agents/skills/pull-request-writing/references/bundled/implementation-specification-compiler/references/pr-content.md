# Self-contained pull request content

Every workflow uses [pull-request-writing](../../../../SKILL.md). A PR explains its problem, resulting behavior, review-relevant implementation, and actual verification in its own description. The design proposal is its sole optional document reference. The issue-content command retains its separate contract.

## Validation

Run `specflow validate-pr-content pr-content.json --json` before an authorized PR write and on fetched content afterward. This command is local: it performs no publication, push, or merge. The content envelope uses the title and body from the PR, workflow-authored comments, and document attachments. It is not the complete GitHub API request.

```json
{
  "title": "Recover interrupted billing exports without duplicate records",
  "body": "Billing operators currently restart an export after an interruption and cannot tell whether it finished. This change preserves completed export progress and reports the outcome when the operator retries, so completed records are not exported twice. The recovery and repeated-retry behavior passed the export integration suite.\n\n[Design proposal](https://linear.app/acme/document/billing-export-design)",
  "design_proposal_url": "https://linear.app/acme/document/billing-export-design",
  "comments": [],
  "document_attachments": []
}
```

This is an illustrative description; a real PR reports only its implemented behavior and checks actually run. The [JSON schema](../scripts/specflow_runtime/pr-content.schema.json) defines the envelope. `title` and `body` are required nonempty strings. `design_proposal_url` is an optional HTTPS URL or null. Omitted comment and document-attachment arrays mean empty arrays; attachments contain `title` and `url`. The proposal's section fragments are valid references.

Common Markdown links, reference links, HTML links, bare document URLs, and document attachments are checked against the designated proposal. Direct issue and GitHub PR links retain their operational purpose. PR validation also accepts native GitHub issue, commit, and Actions run/job links. Other document references return `invalid_pr_content` with the affected field and exit code 2. Literal code examples remain implementation evidence and are reviewed by the author rather than treated as prose hyperlinks. Unlinked document mentions, document pointers hidden in code examples, and unfamiliar non-document link formats require the agent's editorial review; the validator does not infer provider state or document meaning.

A successful command returns:

```json
{
  "command": "validate-pr-content",
  "status": "ok",
  "result": {
    "policy": "self-contained-pr-design-proposal-only-v1",
    "reference_check": "passed",
    "editorial_review": "required"
  }
}
```

The editorial field describes the local validator's limit and is not a human approval. The workflow author reviews standalone meaning and the actual proposal destination, validates the prepared content, publishes within existing authority, then validates and compares provider readback. It repairs an invalid or mismatched result before reporting successful publication. The CLI does not intercept arbitrary GitHub tool calls or fence external writers.

## Required templates

Keep required sections, including a supported task checklist, verification, and material release or compatibility fields. Fill them directly. A required documentation field points only to the relevant design-proposal section, with supporting sources inside that proposal. Follow any applicable requirement to prepare missing reference documentation through the authorized proposal workflow. An unavailable required proposal or publication capability remains explicit; no placeholder link counts as completion.

## Native associations on the selected provider

The optional `native_associations` field identifies actual native issue, pull-request, commit, diff, and CI associations on any HTTPS provider. Populate it from inspected provider records, not from guesses about a URL or an attempt to relabel a supporting document. For example:

```json
"native_associations": [
  {"kind": "issue", "url": "https://gitlab.example.org/library/catalog/-/issues/42"},
  {"kind": "pull_request", "url": "https://gitlab.example.org/library/catalog/-/merge_requests/51"}
]
```

The validator permits these exact association URLs in authored prose and comments. Document attachments still accept only the actual design proposal. Existing recognized Linear issue and GitHub operational links remain compatible without the extra field. Read back saved content and its actual associations through the selected provider before reporting publication complete. This local check cannot prove provider identity, access, publication, or the truth of the association's declared kind; editorial review remains required.
