---
name: repository-artifact-cleaner
description: Remove only provenance-owned temporary framework artifacts after successful reconciliation and verify the repository against the reviewed final allowlist.
---

# Repository artifact cleaner

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


For human interactions and team outputs, follow [review and artifact design](references/bundled/epic-spec-workflow/references/review-and-artifact-design.md). Read it before preparing a question, review, publication, or handoff.

Resume `$specification-reconciliation` at its cleanup stage only after as-built publication and required approvals succeed. Read the epic provenance manifest, current repository status, shared Spec Kit usage, preserved-artifact decisions, and repository allowlist.

Present the exact removal set and its provenance before deletion. Remove only temporary files owned by the epic or explicitly approved generated copies. Preserve source, tests, contracts, schemas, migrations, build and deployment configuration, current-state operational documentation, runbooks, the selected canonical specification and proposals, approved plans, required recovery evidence, unrelated work, shared Spec Kit infrastructure, and ADRs.

For the compatible specflow profile, run `specflow cleanup-check` after removal. In other projects, verify the exact provenance-owned removal set directly against current file state; preserve the chosen documentation home and do not apply an incompatible cleanup allowlist. Derive any `--allow` path from an approved preserved-artifact entry, resolve it relative to the manifest, and verify that it remains inside the repository. Report every residual path and owner; a residual or unverified external write means cleanup is incomplete.
