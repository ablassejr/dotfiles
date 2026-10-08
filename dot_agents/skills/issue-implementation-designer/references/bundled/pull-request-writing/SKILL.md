---
name: pull-request-writing
description: Write or update a self-explanatory pull request in any workflow. Explain the change and its verification directly, and use only its design proposal as a document reference.
---

# Pull request writing

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Apply this skill whenever a workflow prepares, creates, or updates a PR description or authors a PR comment or document attachment. It governs presentation within the task's existing authorization; it does not authorize pushing, publication, review submission, or merge.

A reviewer with no starting context must understand the problem, why the change is needed, the resulting behavior, the implementation choices needed to assess the diff, and what verification actually established. Explain material compatibility, migration, rollout, recovery, or remaining limitations when the change has them. Keep the title and description aligned with the current diff and scope. A linked issue, diff, test log, or prior conversation cannot carry essential explanation on its own. State approved requirements and observed results; do not invent acceptance criteria, claim unrun checks, or use a pending check as evidence of success.

The actual design proposal is the PR's sole optional document reference. Put links to specifications, ADRs, runbooks, research, grounding records, implementation handoffs, audit reports, and session transcripts inside the proposal or internal workflow records. A document ID, relative path, attachment, embed, or instruction to read another document is still a document reference without a hyperlink. Do not relabel another document as a proposal. Include the decision-relevant facts in the PR itself; the proposal provides optional depth. Preserve the existing prohibition on Claude session links.

Native issue, PR, commit, diff, and CI associations retain their operational purpose. Concise file or symbol names, public-interface examples, and verification commands may explain the implemented change. The issue-writing skill's restrictions on implementation detail apply to issue prose, not PR explanations.

Follow the repository's required PR sections and applicable checklists. Write their useful context and actual task or verification status inline. When a template requires a documentation reference, link the appropriate section of the design proposal. Supporting reference documentation remains reachable inside that proposal. If applicable instructions require a document and none exists, prepare the actual design proposal for the PR's scope through the authorized documentation workflow; do not fabricate a URL or silently ignore the requirement.

Before an authorized PR write, read the description as an unfamiliar reviewer and repair missing context, unsupported claims, and unnecessary prose. Run [the PR content validator](../implementation-specification-compiler/references/pr-content.md) on the exact title, body, authored comments, and document attachments. Publish through the configured provider path with the task's existing authorization. Fetch the saved content, compare it with the prepared version, run the same validator, and inspect the rendered description. Reconcile partial or concurrent writes before retrying. A material change to the diff, design, or verification updates the explanation and repeats these checks.

These are automatic authoring and readback steps within the current stage. They add no human approval. Missing publication authority or a required provider leaves only its dependent work pending; the policy does not turn preparation into permission to publish. A passing validator checks common references and nonempty text, not human comprehension, all unlinked document mentions, or whether the designated URL is truly a proposal. The authoring and readback review establishes those facts.
