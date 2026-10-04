# Subtractive code mass policy

Use the project's selected source and work records under [workspace and destinations](workspace-and-destinations.md). The code-mass and behavioral obligations apply to the approved scope. Commands that require a Linear/Notion manifest or fixed three-person plan apply only to that compatible profile. For other projects, perform and record the same independent normalized measurements, removal-credit checks, budgets, approved exceptions, and behavior verification against the actual source and dependency records using compatible repository tools. Do not fabricate provider fields, require three owners, or claim a packaged CLI result that was not obtained.


## Constitutional invariant

Maintained code is a liability. The implementation strategy replaces, consolidates, simplifies, reuses, or removes current mechanisms before it adds code. New maintained code represents irreducible new behavior. Correctness and comprehensibility remain hard invariants.

The repository-local Spec Kit constitution contains the packaged [Subtractive Code Mass principle](../assets/spec-kit-constitution-subtractive-code-mass.md). The framework implementation policy, First-Principles Basis, Code Mass Opportunity Map, decision records, issue Code Mass Contract, milestone ledger, implementation reviews, `code-mass-policy` report, and as-built reconciliation all enforce the same invariant.

## Measurement contract

Normalized maintained SLOC counts first-party production and test source, build and deployment scripts, migrations, repository-owned generators, executable infrastructure, and repository-owned development tooling. Generator source counts; generated output does not receive credit.

Blank and comment-only lines, vendored or generated material, compiled and distribution output, lockfiles, third-party snapshots, binary assets, non-executable data fixtures, pure renames, pure movement, and formatter-only changes are excluded. A repository-selected formatting verification runs before measurement. The auditor reviews semantic structure because a physical-line counter cannot detect code golf or hidden complexity by itself.

For each pull request, `A` is validated maintained SLOC added, `R` is validated maintained SLOC removed, and `delta` is head maintained SLOC minus base maintained SLOC. The removal ratio is `R / A` when `A` is positive. Production, tests, and their combined result are reported. The target is `5R >= 6A`; a positive delta independently invokes the Net Addition Gate.

Automated measurement provides evidence. A Code Mass Auditor establishes which measured removals are semantically valid. Only `VALID_REMOVAL` and verified `REMOVAL_REQUIRES_REPLACEMENT` findings receive credit.

## Anti-gaming invariants

Removal credit stays in the same responsibility domain and has one of these relationships to the added behavior: it replaces, supersedes, consolidates, makes unnecessary, removes a prerequisite, removes duplicate verification, or retires migration behavior. A change cannot claim credit by compressing code, moving behavior, deleting valuable tests, shifting machinery into configuration or generated output, adopting a dependency, weakening safeguards, or deleting unrelated code.

Dependency replacement is evaluated through API and configuration surface, transitive dependencies, upgrade and supply-chain burden, runtime behavior, wrapper code, failure modes, and operational complexity. Test consolidation proves equal or stronger observable behavior rather than relying on coverage percentage. A reduction succeeds only when both maintained code mass and conceptual state space become smaller.

## First-principles and context sequence

Before implementation context is visible, the intake asks what behavior must remain after the change and cannot be removed from the problem. It then asks which current responsibility, process, concept, or behavior should disappear or become simpler. The answer remains conceptual and contains no file or symbol guesses. The basis records `irreducible_new_behavior`, `expected_simplification`, and `forbidden_tradeoffs`.

After basis approval and context reconciliation, `$subtractive-design-analyzer` searches the in-scope responsibility domain and produces a Code Mass Opportunity Map. Every candidate carries current symbols or paths, estimated SLOC, evidence, affected behavior and tests, provenance, confidence, and deletion safety. `REQUIRES_GROUNDING` and `UNKNOWN` candidates enter `$ground-me`. Confirmed deletion grounding determines whether code is a current invariant, an obsolete constraint, temporary machinery, accidental complexity, or still-required behavior.

## Decision and program contracts

Every implementation option reports expected additions, removals, ratio, and net effect. The recommendation weighs first-principles alignment, behavioral correctness, code mass, conceptual complexity, reversibility, operational risk, and migration cost. Fewer lines alone never determine the recommendation.

The program compiler maximizes independent ownership and mergeability, safe deletion, consolidation, and comprehensibility while minimizing maintained code, duplicate behavior, public surface, conceptual authorities, shared writes, and integration uncertainty. Each issue remains one owner, one coherent behavioral outcome, one responsibility domain, one deletion or replacement strategy, and one pull request.

Every issue body is self-contained and may reference only its design proposal. Source authority, basis, grounding, implementation decisions, and code-mass details live in that proposal and structured workflow records. Its structured contract records irreducible behavior, replacement or removal candidates and Ground Me evidence, estimated and reported production/test/combined measurements, removal locality, alternatives, lifecycle state, bounded milestone escrow, and Net Addition Gate state.

The structured lifecycle states are `code-mass:unassessed`, `code-mass:targeted`, `code-mass:pass`, `code-mass:deficit`, `net-addition:review-required`, `net-addition:approved-exception`, and `deletion:grounding-required`.

## Bounded milestone escrow

Every issue independently targets 6:5. When an enabling pull request must precede safe deletion, its contract names the compensating issue before approval. The approved dependency/escrow relation, work grouping, and responsibility domain bind both issues using the chosen tracker's capabilities or the owning plan's graph. The deletion merges first whenever technically possible. The ledger never accepts unrelated offsets or transfers a deficit to a later or unrelated project.

Each milestone ledger begins at the approved repository baseline, records every issue's added and removed SLOC, ratio, deficit or surplus, and aggregates totals. A non-positive pull request that misses 6:5 may carry a visible bounded deficit. The milestone closes only at 6:5 or with an explicit project-level exception. That project exception cannot approve a positive net delta; the Net Addition Gate remains independent. Deletions before the baseline and reverted deletions do not count.

## Net Addition Gate

A positive measured delta proves that the behavior traces to an approved requirement, belongs to the minimum sufficient desired state and selected component, cannot responsibly reuse or replace an existing mechanism, creates no parallel authority, stays within ticket scope, and states its deficit.

Verification records acceptance and regression behavior, failure paths, changed public contracts, state and migration behavior, security, concurrency and retry behavior, performance, observability, critical-logic fault injection, and the measured delta. Checks that are not relevant record `NOT_APPLICABLE` with a rationale; acceptance, regression, failure-path, and SLOC evidence remain verified.

Approval requires `ALIGNED` first-principles review, adversarial review with no blockers, verified Code Mass Auditor measurements, a named task owner, a named code owner, applicable security or platform approval, and the human confirmation that the delta is the minimum responsible maintained-code addition.

A controlled `NET_ADDITION_EXCEPTION` uses only these categories: new externally required behavior, security or compliance, a compatibility shim that cannot yet replace an old path, tests that expose previously unverified behavior, migration scaffolding, a new protocol or platform obligation, or an emergency correctness fix. It records why no safe deletion exists, why the addition is minimal, whether it is temporary, its expiration and compensating work, the human approver, and review date.

## Implementation and reconciliation

Ticket design runs subtractive analysis, grounds uncertain deletions, produces the minimum-code proposal, performs first-principles alignment, runs the Code Mass Auditor planning pass, runs adversarial design review, and resolves the human decision frontier before declaring readiness. Implementation continuously compares the result with the issue budget. A committed candidate receives as-built alignment, the Code Mass Auditor verification pass, adversarial review, any required Net Addition Gate, the repository's behavioral tests, and the final code-mass policy assessment, using `code-mass-policy` only when the selected plan matches its declared adapter contract.

As-built reconciliation records the final production, test, and combined result, removes invalid or reverted credit, updates the milestone ledger, leaves a visible bounded deficit or approved exception when required, updates authoritative artifacts to current state, and deep-cleans provenance-owned temporary work.
