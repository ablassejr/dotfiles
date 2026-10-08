# Three-person delivery planning

This reference describes the explicitly selected Linear/Notion/Camunda automation profile. Apply its provider-specific schemas, fixed staffing policy, and runtime gates only when that setup governs the current project. It does not select a destination for another workspace. See [workspace and destinations](../../epic-spec-workflow/references/workspace-and-destinations.md) for the portable workflow and actual adapter limits.

The implementation program contains exactly three milestone workstreams inside one carrier project. Each workstream belongs to a different person. Every issue belongs to one workstream and uses that person's consistent owner identity. Resolve those identities to three distinct Linear users before publication.

When the compiler receives the approved specification, it grounds the required outcomes in the repository and separates the surviving work into independently ownable responsibilities. It splits each responsibility into the smallest useful outcome that one person can implement, verify, and submit in one reviewable pull request. It records why the issue is small enough and how its outcome can be observed. It keeps semantic scope and existing code-mass obligations attached to every resulting issue.

An issue's `work_unit` has this consumer-facing shape:

```json
{
  "outcome": "A customer can see the current invoice total.",
  "verification": "Open an invoice with known line items and observe its expected total.",
  "size": {
    "assessment": "bite_sized",
    "rationale": "This issue covers one existing invoice view and one observable total; it can be reviewed in one PR."
  }
}
```

Sizing uses one independently reviewable outcome. No fixed duration, equal issue count, or prescribed frontend/backend/testing division is assumed. Apply a human-supplied effort limit when one exists. A draft can record `needs_split` or `unknown`; a publishable plan requires `bite_sized` with a rationale. Uncertain SLOC estimates remain `UNKNOWN` under the separate code-mass contract and do not establish issue size.

When an issue contains unrelated outcomes, the compiler splits them and reconnects their semantic references, native dependencies, and ledger entries. When uncertainty prevents a responsible split, it gathers the missing evidence. It uses the existing open-ended decision loop only for a material choice or an unavoidable constraint. It does not invent additional requirements, filler work, a third owner, or an approval for each split.

The compiler then checks the native `blocks` graph, including declared external issue references. A cycle blocks validation. It identifies one issue from each workstream that can be ready together after their prerequisites finish. If no such group exists, the plan needs a different partition or an explicit discussion of the dependency constraint. Shared prerequisites and later cross-stream handoffs are allowed; they are shown to the supervisor. Related, similar, and duplicate relations do not schedule work.

`specflow validate-linear-plan` returns a `workstreams` report with the three `lanes`, each lane's `milestone`, `owner`, `issues`, and `ready_issues`, a `parallel_frontier` containing one issue per person, and its `prerequisites` and `external_blockers`. This is a structural analysis of the planned graph. A ready issue has no declared blocker; the report does not read live completion state or claim equal workload, simultaneous starts, or freedom from shared-file conflicts. The compiler reviews shared write surfaces and handoff contracts against repository evidence and explains material risks in the proposal.

At final program planning, the supervisor sees a three-lane visual with each person's bounded issues, shared prerequisites, and cross-stream handoffs. Figma Design, LikeC4, or Archify renders that graph under the existing visual policy. The visual carries the ownership and dependency explanation; prose supplies only missing context, uncertainty, or the decision requested.

After the existing program approval, the publisher creates or resolves the carrier and uploads the complete deliberately prepared team artifact set under [project artifact publication](../../epic-spec-workflow/references/project-resources.md). Once project Resources and member access are verified, it creates the three milestones and all issues before creating their native relations. It persists each issue's outcome and verification in readable issue content and its full `work_unit` alongside the structured contract. It fetches the milestone membership, three distinct resolved owners, work units, PR boundaries, and relation graph and compares them with the approved plan. Partial publication remains incomplete and retries reconcile existing provider identities. Dispatch follows live readiness; completion of a prerequisite automatically makes its authorized successors eligible without requesting permission to move within the stage.

## Camunda completion contract

Program compilation returns `linearPlan` using schema version 4, the approved `semanticManifest`, and `programBinding` with a stable `ref` and a `hash` of the exact plan. The hash is SHA-256 of UTF-8 JSON with sorted keys, compact separators, escaped non-ASCII characters, and no NaN values. The existing `visuals` inventory accompanies the result.

The `three-person-workstreams-v1` job policy invokes the public plan validator over that snapshot before completing compilation. It verifies the same snapshot at supervisor proposal publication, Linear program publication, and ticket dispatch. Publication and dispatch cannot replace the plan, manifest, or binding. Invalid input returns `invalid_program_plan`; a configured worker exposes an incident that can be repaired and retried. A corrected compilation continues to proposal publication automatically and reaches the existing final human review.

Schema version 4 is required by `validate-linear-plan` and `code-mass-policy`. Recompile older plan documents against the approved manifest and real team identities; changing only the version number cannot satisfy the ownership, sizing, and graph contracts. Draft initialization leaves identities and work empty until grounded. Already-running Camunda instances retain their deployed definition; deploying the policy does not migrate them or change existing Linear issues.

## Assignment timing

Issue owners describe intended ownership in the plan. Provider issue creation leaves assignees empty. The [individual issue review gate](../../epic-spec-workflow/references/issue-review-before-assignment.md) completes every created issue’s own HITL loop before assigning any issue to its approved owner. Execution still respects native blockers and the three distinct workstreams.
