# Milestone-first Linear plan contract

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](bundled/epic-spec-workflow/references/workspace-and-destinations.md) for the portable workflow and actual adapter limits.

## Semantic release binding

A schema-version 4 plan names the approved manifest's slug, repository baseline, Notion page, approved and read-back-verified revision, content hash, First-Principles Basis ID, and basis version. Every milestone and issue carries at least one semantic ID from that manifest.

Run `specflow validate-linear-plan <plan> --manifest <manifest> --json`. Local validation proves structure, release binding, Code Mass Contract arithmetic, milestone-ledger reconciliation, bounded escrow locality, and controlled exception evidence. It does not prove that a live Linear object exists or remains unchanged. Resolve and read back live identities and relations through the authenticated integration.

## Carrier project

The plan contains one existing or explicitly approved minimal carrier project. Milestones and issues inherit that project and cannot carry their own project fields. Additional projects require a separate user-approved reason and plan.

## Milestone workstreams

The plan has exactly three milestone workstreams for three distinct people under [three-person delivery planning](three-person-workstreams.md). Every milestone has a local key, name, one owner, one responsibility domain, semantic IDs, and a Code Mass Ledger. Each issue uses its milestone owner; all three milestones contain independently useful work. The ledger baseline equals the approved repository baseline. Its issue rows record additions, removals, ratio, 6:5 deficit or surplus, and its totals record additions, removals, ratio, net delta, `PASS`, `DEFICIT`, or `UNKNOWN`, and any approved project-level exception.

The ledger contains every issue in that milestone exactly once. Each row uses the issue's reported measurements when present and its estimates otherwise. UNKNOWN operands propagate to dependent totals; an UNKNOWN milestone cannot claim a ratio pass or closure. Credit cannot move between milestones. Deletions merged before the baseline and reverted deletions are removed from the ledger.

## Single-pull-request issues

Every issue has a local key, title, Markdown body, one milestone, one owner, semantic IDs, exactly one pull request, a `work_unit` describing its outcome, verification, and sizing rationale, and one structured Code Mass Contract. The issue remains independently useful and owns one coherent behavioral outcome and one replacement or deletion strategy.

The issue uses [the shared content contract](issue-content.md). Explain the problem, required outcome, and approved behavioral scope in the issue itself. Its only optional document reference is `design_proposal_url`, identifying the relevant design proposal. The body has no mandatory orchestration headings; detailed source authority, basis, grounding, decisions, and code-mass records are retained in the proposal and structured workflow artifacts. Native Linear relations remain the dependency and escrow graph.

## Code Mass Contract

The structured contract is attached to this issue.
```

The body does not contain dependency sections, source code shapes, or command syntax. Detailed code design lives in the linked implementation-design record. Native Linear relations remain the dependency and escrow graph.

## Code Mass Contract

The structured contract records:

- irreducible new behavior;
- current mechanisms that are removed or replaced, why they become unnecessary, their confirmed Ground Me record, and deletion safety;
- estimated and reported production, test, and combined normalized maintained SLOC;
- removal locality within one responsibility domain;
- delete/configuration, reuse, and additive alternatives;
- Net Addition Gate state and evidence;
- bounded milestone escrow; and
- one structured lifecycle state.

Combined additions and removals equal the production and test values. Net equals additions minus removals. Ratio equals removed divided by added when additions are positive and is null otherwise. Credited removals require `SAFE` or `SAFE_WITH_REPLACEMENT` plus a confirmed Ground Me record.

Unavailable estimate fields use the literal `UNKNOWN`; derived values remain UNKNOWN whenever an operand is unavailable. Reported measurements require numeric SLOC. Historical estimates remain intact after measurement. The gate follows reported measurements when present and estimates otherwise. An unknown delta keeps the gate `REQUIRED` without approval evidence; it cannot establish a numeric target, deficit, pass, or approved exception. Its lifecycle remains unassessed, review-required, or deletion-grounding-required.

A positive estimate enters `REQUIRED` gate state with lifecycle `net-addition:review-required`. That is a valid planning contract and is not permission to merge. After a committed result is measured, the gate becomes `APPROVED` with lifecycle `net-addition:approved-exception` only when it contains first-principles validation evidence, the complete verification matrix, `ALIGNED` and `NO_BLOCKERS` independent reviews, a verified auditor, named task and code owners, applicable security or platform approval, the human minimum-responsible-addition confirmation, and a controlled `NET_ADDITION_EXCEPTION`.

## Bounded escrow

Every issue targets `5R >= 6A`. An issue below target uses active milestone escrow, an approved milestone-level project exception, or—when its net delta is positive—the controlled Net Addition Exception. Escrow names a compensating issue, milestone, and responsibility domain. Both issues belong to that milestone and are explicitly linked in the top-level native relations. The deletion issue is identified before the enabling issue is approved and merges first whenever technically possible. A project-level ratio exception never substitutes for the Net Addition Gate.

## Native relations

The top-level `relations` list supports `blocks`, `duplicate`, `related`, and `similar`. Each endpoint names either a planned issue or a declared `existing_issue_refs` entry. An existing entry supplies `key`, provider `id`, and `operation: "reference_only"`. It is not created, reassigned, included in milestone totals, or usable as compensating work for milestone escrow. Keys and provider identities must be unique; undeclared endpoints are rejected. For `blocks`, the source blocks the target. Create all issues, resolve their returned identifiers, create relations, and read them back. Never repair a failed relation by copying dependency prose into an issue.

## Measurement check

Before merge, update the selected issue's `reported` measurements and run:

```text
specflow code-mass-policy <repository> --base <base> --head <head> --plan <linear-plan.json> --issue <issue-key> --format-command-json '<json-array>' --json
```

The command requires a clean tracked checkout at the exact committed head. It runs the repository-selected formatting verification, counts committed base and head source, separates production and tests, cancels pure movement, reports exclusions and renames, compares every reported value, evaluates 6:5, and invokes the Net Addition Gate for a positive measured delta. The Code Mass Auditor separately determines whether measured removals are semantically legitimate.

## Human presentation

The validated plan is the source for the [supervisor design document](bundled/epic-spec-workflow/references/supervisor-design-document.md). Publish that visual-first, self-contained Linear proposal before requesting final program approval. Its reference is carried by the runtime review binding; the schema-v4 delivery-plan payload remains the source of the carrier, milestones, issue contracts, and native relations.
