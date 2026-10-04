---
name: local-simplification
description: Analyze a bounded local responsibility for removable or duplicate mechanisms, ground candidates in source and Git history, compile local consolidation plans, and verify user-created implementations with maintained-code accounting and behavioral evidence.
metadata:
  version: "1.0.1"
---

# Local simplification

Answer which implementation surface can disappear while required behavior remains. Start with a local diff, commit, module, symbol, or named responsibility. Keep the investigation centered on that responsibility and expand only to its consumers, dependencies, tests, configuration, parallel implementations, and relevant local history.

The repository is input. Reports and disposable execution workspaces are outputs. Never alter source, Git refs, or the index, install packages, or publish a finding during an analysis run. This package's creation and maintenance are separate from running its analysis. The reviewing agent may use hosted or local models and configured context, documentation, and research services according to the user's authorization and host instructions. The helper invokes no model.

Read [the command contract](references/command-contract.md) before executing helpers, and [accounting and evidence](references/accounting-and-evidence.md) when evaluating reduction or deletion safety. Follow the host's CLI documentation and repository-context requirements using its configured tools.

## Capture and investigate

Run `scripts/simplify.py audit` with an explicit repository, local scope or change, and a new output directory. Python 3.11+ and local Git are required. The helper captures source bytes without archive substitution, classifies supported code, extracts Python declarations and call expressions, and proposes structural duplicate or forwarding candidates. Structural similarity and absent text matches never establish deletion safety.

Read the generated candidate and responsibility artifacts. Use `candidate` to record other evidence-supported hypotheses, `evidence` for exact source excerpts, and `ground` for bounded local history. Use `structure` when a locally installed ast-grep can supply Tree-sitter outlines. An existing external index may be imported through the documented normalized graph schema. The helper does not run or download SCIP or CodeQL indexers. Imported provider precision is a claim whose coverage still needs review.

Explain the current responsibility in ordinary sentences: what enters, which mechanism owns each decision, what state it reads or writes, what consumers observe, and how failure and recovery behave. Search for counterevidence, legitimate isolation boundaries, independent variation, dynamic registration, persisted compatibility, and historical constraints before proposing consolidation. A wrapper may preserve a useful public contract even if its body is small.

## Plan the transition

Complete the run's `assessment.json`. Name the canonical target and each obsolete symbol or file. Map observable behavior contracts to end-to-end checks and declared component/service seams to integration checks. Assertions belong at stable public or system boundaries. A private helper's call count is not a behavioral contract.

For each preservation obligation, record supporting local evidence, conflicts, or unknowns. Record actual conceptual entities before and after rather than inventing aggregate complexity scores. Keep code estimates null when no grounded estimate exists. Compile a local plan with `plan`; this creates proposed PR partitions and does not publish or implement them.

The completed responsibility transition must preserve required behavior, reduce maintained code, and reduce at least one conceptual dimension. The default removal/addition target is 1.2 for that completed transition. A documented, evidence-bound ratio exception can justify a lower ratio while retaining all other success conditions. Intermediate preparation work receives no completed savings credit. These metrics never override behavior, compatibility, or unresolved consumer evidence.

## Verify the user's implementation

Use `verify` after the user supplies a local implementation commit or working tree. It keeps the plan's captured head as the baseline, captures the implementation, checks scope and named mechanism changes, and runs the same declared commands on disposable copies. Native checks require a passing macOS sandbox capability probe. When isolation, dependencies, submodule content, or a necessary language adapter is unavailable, record the gap and continue permitted evidence work. Never execute checks without the required containment.

Review the exact implementation using the generated `target-review.json` and pinned source evidence. The review must cover consumer migration, dynamic uses, contracts, required behavior, replacement completeness, failures, state ownership, historical constraints, and test preservation. Preserve contradictions and unknowns. `finalize` binds this review to the executed check results and computes the final local verdict. Check success cannot stand in for semantic review; review assertions cannot turn failed or unavailable execution into a pass.

Run `report` before presenting a saved result so changed source or artifacts cannot leave a current-looking pass. Explain what responsibility became simpler, actual measured changes, which checks ran, the review's evidence limits, and the rollback path. Link the local Markdown/HTML and JSON artifacts. A local pass is advisory evidence within the declared contract, not CI, merge, deployment, external-consumer proof, or a command to delete code.

Read [validation and support](references/validation.md) for the supported adapters, host limitations, behavioral tests, and package verification.
