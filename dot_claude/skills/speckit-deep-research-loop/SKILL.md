---
name: speckit-deep-research-loop
description: Run the deep-research loop for a Spec Kit epic by coordinating CodeGraph, Claude Context, exact-version documentation, Exa, evidence synthesis, contradiction detection, and material-gap routing.
---

# Spec Kit deep research loop

For human interactions and team outputs, follow [review and artifact design](../epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Invoke `$specification-research-loop`. When implementation structure is in scope and the repository owns a CodeGraph index, locate the structural surface there first. Continue with `claude-context`, retrieve exact-version behavior through `docs-mcp-server`, and use Exa for unresolved external facts or alternatives.

Update the owning evidence and contradiction records once. Generate claim, source, gap, or findings views only for a distinct review or verification need, and present decision-changing conclusions through the existing proposal or evidence section. Seek disconfirming evidence and route any changed premise to the earliest affected semantic or engineering step.

Continue until the core research loop reports that no unresolved factual gap could materially change the current specification, or until the next unresolved item is a human-owned value or risk decision. Do not convert lack of evidence into approval.
