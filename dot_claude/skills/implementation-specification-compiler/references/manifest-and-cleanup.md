# Manifest and cleanup contract

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](../../epic-spec-workflow/references/workspace-and-destinations.md) for the portable workflow and actual adapter limits.

## Local workspace

`specflow init <directory> --slug <slug>` creates three files and does not overwrite an existing one:

- `specflow.manifest.json` records the durable epic identity, approved First-Principles Basis lineage, repository and Spec Kit baseline, stable identifier allocation, semantic and evidence state, Notion publication and approval, Linear compilation state, and artifact provenance.
- `semantic-spec.json` is the normalized local semantic staging document.
- `linear-plan.json` is an unpopulated implementation plan. It is invalid until it names a legal carrier project and has milestones and issues.

The command accepts `--json` before or after its subcommand. A successful JSON result has `status: "ok"`, the target directory and slug, the created filenames, and an empty `errors` list. A conflict returns exit code 1 and `path_exists`. A bad invocation or filesystem failure returns exit code 2.

## Semantic manifest

The packaged [manifest schema](../schemas/spec-manifest.schema.json) describes the portable JSON shape. `specflow validate-spec <manifest> --json` returns exit code 0 for a structurally valid draft or approved manifest, exit code 1 for contract violations, and exit code 2 when it cannot read JSON.

The initialized durable state has this shape:

```json
{
  "schema_version": 3,
  "kind": "specflow.semantic-manifest",
  "epic_id": "generated-stable-epic-id",
  "slug": "billing-rebuild",
  "stage": "draft",
  "repository": {
    "baseline": null,
    "spec_kit_feature_directory": null
  },
  "first_principles_basis": {
    "status": "pending",
    "current_basis_id": null,
    "current_version": null,
    "lineage": []
  },
  "stable_id_counters": {},
  "semantic_ids": [],
  "view_registry": [],
  "decision_log": [],
  "evidence_ledger": [],
  "subtractive_code_mass": {
    "policy": "subtractive-code-mass-v1",
    "opportunity_maps": [],
    "net_addition_exceptions": [],
    "milestone_ledgers": []
  },
  "notion": {
    "page_id": null,
    "url": null,
    "published_revision": null,
    "readback_revision": null,
    "readback_content_hash": null,
    "readback_verified": false,
    "readback_verified_at": null
  },
  "approval": {
    "status": "pending",
    "revision": null,
    "approved_by": null,
    "approved_at": null
  },
  "linear_compilation": {
    "status": "not_started",
    "plan_path": "linear-plan.json",
    "carrier_project_id": null,
    "compiled_at": null
  },
  "provenance": {
    "temporary_artifacts": [
      "linear-plan.json",
      "semantic-spec.json",
      "specflow.manifest.json"
    ],
    "preserved_artifacts": []
  }
}
```

`epic_id` remains stable for the epic. `first_principles_basis` retains every approved version, its approval evidence, and the exact current version without rewriting earlier intent. `repository.baseline` identifies the exact source state used for compilation, while `repository.spec_kit_feature_directory` locates the feature workspace. `stable_id_counters` records durable allocation state; `semantic_ids` is the authoritative set that delivery work may reference. `view_registry`, `decision_log`, and `evidence_ledger` hold machine-readable records. `subtractive_code_mass` identifies the constitutional policy and links Code Mass Opportunity Maps, controlled exceptions, and milestone ledgers. The semantic specification holds frames and requirement context, the decision log holds material frame selection, requirement challenge, retention, deletion, restoration, simplification, cycle, and automation decisions, and the evidence ledger links them to current evidence. No separate sequence field is required. `linear_compilation` records compilation progress without asserting live Linear state. `provenance` distinguishes temporary artifacts from preserved artifacts.

Stable semantic identifiers are non-empty and unique. Counter values are non-negative integers. Registry and ledger entries are JSON objects. Artifact paths stay relative to the workspace. A pending draft can validate without a repository baseline or Notion page.

An approved manifest is ready for compilation only when it retains an approved current basis and valid version lineage, has at least one semantic identifier, and records a non-empty repository baseline, Notion page identifier and URL, read-back content hash, read-back verification timestamp, approving identity, and approval timestamp. `notion.readback_verified` must be true, and `notion.published_revision`, `notion.readback_revision`, and `approval.revision` must be identical non-empty values.

The validator reports `ready_for_compilation` separately from structural validity. A valid draft returns false. The compiler does not treat a draft as approved simply because its JSON shape is valid.

## Cleanup check

`specflow cleanup-check <repository> [--allow <relative-path> ...] --json` scans without deleting. It reports exit code 0 and an empty `residual` list when clean. It reports exit code 1 and `status: "incomplete"` when temporary artifacts remain. Repository or argument errors return exit code 2.

The scan reports `.specflow`, `.specify`, the three standard workspace filenames, and existing relative paths listed in a discovered manifest's `provenance.temporary_artifacts`. It collapses a reported temporary directory to one repository-relative path. Paths inside a directory named `adr` or `adrs` are exempt.

An allow path is repository-relative and suppresses that path and its descendants. Manifest provenance entries are workspace-relative: resolve each as `manifest.parent / entry`, verify that the result remains inside the repository, then convert it to a repository-relative path before passing it to `--allow`. The allow records an intentional exception for this run; it does not change or delete the artifact. Reject absolute allow paths and paths that escape through `..`.

When cleanup is approved, resolve every candidate against the repository before deletion. Preserve ADRs and unrelated files. Keep shared `.specify` infrastructure while another active feature uses it. Run the check again after cleanup and report residual paths instead of broadening the deletion target.

## Semantic orchestration and handoff

The epic skill uses this semantic envelope with the Camunda-derived evidence snapshot defined in [workflow records](../../epic-spec-workflow/references/workflow-records.md). Camunda owns durable process position; the manifest retains references and recovery evidence. `validate-spec` validates its published local envelope and does not verify live engine position, adapter guarantees, approval, or freshness. `ready_for_compilation` is a local result and does not replace the compiler's live-source and immutable handoff checks.

Use `specflow init` only for a new workspace. An existing workflow resumes from its Camunda process instance and verifies the referenced manifest and receipts; it does not regenerate files or infer approval from a stage label. The durable manifest stays outside the product repository. Its external orchestration record is retained even when provenance-owned product-repository scratch files are removed.
