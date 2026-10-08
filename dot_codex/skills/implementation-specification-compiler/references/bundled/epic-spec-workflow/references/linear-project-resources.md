# Planning artifacts in Linear project Resources

This reference describes the explicitly selected Linear/Notion/Camunda adapter profile. Apply its provider-specific schemas and operations only in that configured workflow. For other projects use [workspace and destinations](workspace-and-destinations.md) and the provider-neutral scope contracts.

Immediately before creating the approved Linear issues, the implementation program uploads the complete prepared team artifact set to the carrier project’s Resources section. Apply [review and artifact design](review-and-artifact-design.md) when selecting and explaining that set. Camunda exposes this automatic stage as **Project resources**, between supervisor approval and issue distillation. The existing program approval authorizes this publication within its approved carrier. No separate per-file approval is introduced.

When preparing the program, use a dedicated publication directory outside the product checkout. Include only documents, media, and evidence with a distinct team purpose: the shared semantic handoff, applicable delivery records, necessary design views or demonstrations, and evidence the team needs to inspect. Refer to existing shared authoritative records instead of publishing duplicate narratives. When a portable snapshot is needed for exact-revision recovery, label it as archival evidence and identify its governing source. The published proposal remains the reading entry point. Notion keeps semantic authority.

Keep working manifests, raw research, temporary packets, alternate drafts, prepared-versus-fetched comparisons, render receipts, and execution logs in separate internal storage. Retain required verification and recovery records there; do not delete them to simplify the published set. Earlier stages and delegated work follow the same selection rule. The author prepares this directory deliberately; the inventory command scans it exhaustively and does not judge relevance or readability.

Before the final supervisor review, verify that the proposal and its review-critical evidence are already accessible through authorized shared references. Inventory the prepared directory against `programBinding` and return the inventory as `projectArtifactInventory`. The later project upload is not a substitute for access during review. Keep the inventory JSON, operation store, upload receipts, and running logs outside the directory to avoid recursively uploading publication bookkeeping. The command reads every regular file, including nested and hidden files, without an extension allowlist. An empty directory, unreadable file, or symbolic link blocks inventory creation rather than silently dropping content; materialize linked artifacts first.

```text
specflow inventory-project-artifacts /absolute/planning-artifacts --source program-binding.json --json
```

The command's `result` is the inventory, containing `schema_version: 1`, the exact `source`, an absolute `root`, and an `artifacts` list of relative `key`, `sha256`, byte `size`, and `content_type`, plus an `inventory_hash`. It is local and does not contact Linear or change files. See the [inventory and publication schema](../../../../scripts/specflow_runtime/project-resources.schema.json).

After supervisor approval, `specflow.publish-project-resources` refreshes the inventory from the same prepared directory, including the final document representation and deliberately selected supporting artifacts. Check late-arriving material against the approved scope and artifact purpose before placing it there. Evidence that changes the design follows the existing revision path; a directory refresh cannot approve it. It binds the full set to the current plan and sends it through the configured Linear adapter. The adapter resolves the existing carrier or creates only the carrier authorized by the plan's creation record. It uploads the exact file bytes to Linear storage and creates a discoverable project resource for every file. A local path, a signed URL that expires, or an issue-only attachment does not satisfy this step.

The adapter can use native project documents containing uploaded files or project resource links to the durable Linear asset URLs. Preserve existing project resources. Use descriptive project-and-purpose resource titles. Each document explains its purpose, audience, status, responsible owner, and source relationship in its opening; a media caption or resource description supplies this context for non-document files. Retain original relative keys, revisions, and hashes as provenance metadata without requiring readers to interpret filenames or internal IDs. Link the supervisor proposal as the reading entry point and place optional evidence beside the claim it supports. Remove local references from exported reader-facing content and verify the shared replacements. Graph artifacts continue to require Figma Design, LikeC4, or Archify under the existing visual policy.

Each content-hashed inventory is an immutable publication set with its own operation target. Resources carry their artifact version; older attempts cannot overwrite a newer artifact version. This organizes retry identity without claiming a project-wide write lock.

When a write is interrupted, the adapter reconciles the project and existing resource identities before retrying. It reuses completed matching uploads and finishes missing ones. Changed content receives a matching version or updated resource; an old upload cannot stand in for new bytes. Prepare, upload, and finalize one file at a time when signed URLs have a short lifetime. Incomplete publication remains a retry or incident, never a completed workflow stage.

After publication, fetch the project's Resources section, verify that every artifact appears there, download the uploaded bytes and compare their hashes, and verify project-member access. Check access as the intended project audience, not merely as the uploader. Do not make the artifacts public on the internet to bypass an access problem. Repair project or resource access within existing authorization, or surface the missing access decision through the existing open-ended loop.

The worker returns `projectResourcesBinding` and the refreshed `projectArtifactInventory`. Camunda advances automatically to `specflow.publish-linear-program`, displayed as **Distill Approved Linear Issues**, only after the receipt passes validation. Issue creation and dispatch retain that receipt, reject changed artifacts or missing resources, and reach supporting project resources through the issue’s actual design proposal. Issue prose retains only that optional document reference. A provider change after publication still requires live verification by the publishing or dispatching handler; a static receipt is not continuous access monitoring.

## Worker and adapter contract

Configure the installed worker with an authenticated Linear command adapter:

```json
{
  "operation_store": "/absolute/specflow-operation-store",
  "handlers": {
    "specflow.publish-project-resources": {
      "builtin": "project-resources",
      "command": ["/absolute/linear-project-resource-adapter"],
      "guarantee": "RECONCILED",
      "timeout_seconds": 120
    }
  }
}
```

Use `specflow worker --config worker.json --once --json` to process available work. The command path is deployment-specific; the package does not invent credentials or configure an unattended worker. A missing publisher leaves an explicit service job waiting.

The adapter receives the existing stdin/stdout [operation envelope](operation-adapters.md), with `request.kind: "linear-project-resources-v1"`, the approved `carrier`, program `source`, `inventory_hash`, `artifacts`, a `files` map from artifact keys to local paths, and `audience: "project_members"`. It supports `reconcile`, `apply`, and a read-only `verify` phase. Reconciliation returns `found` for a complete matching publication or `absent` when the full intended set is not yet present; `apply` reconciles any partial set before filling it. `verify` returns `found` only after current resource membership, bytes, and access are checked. Classified temporary failures use the existing `transient` result and retry budget.

A successful adapter result contains the following binding fields:

- `schema_version`, `source`, `inventory_hash`, the approved `carrier`, and resolved `project_id`;
- one `resources` entry per artifact with `artifact_key`, `resource_id`, `project_id`, durable `asset_url`, expected `sha256`, and downloaded `readback_sha256`;
- `readback` with `project_id`, the fetched `resource_ids`, `verified_at`, and `access: {"scope":"project_members","verified":true,"evidence":"provider access evidence reference"}`.

The worker validates adapter results before caching them and performs live `verify` even when reusing a cached operation receipt. Manual `complete-job` calls use the same binding contract. Invalid inventory, incomplete coverage, hash mismatch, wrong project, missing resource membership, or unverified access returns `invalid_project_resources`. The client validates declared evidence; the authenticated provider adapter performs uploads, downloads, and audience checks. Neither the directory scan nor a receipt can establish that an author placed every artifact produced outside that directory into it.

## Provider references

Linear documents and links appear in [project Resources](https://linear.app/docs/project-overview). Direct [file uploads](https://linear.app/developers/how-to-upload-a-file-to-linear) use a prepared upload URL and raw-byte PUT with the returned headers. Uploaded files use Linear's [authenticated private storage](https://linear.app/developers/file-storage-authentication). The issue attachment connector requires an existing issue; it is not the project-resource publication path.
