# Technical debt and code mass

Classify each debt observation by its relationship to the change. INTRODUCED means the change creates it; WORSENED means the change increases it; EXPOSED means existing debt makes the changed behavior unsafe or unverifiable; UNLOCKED means the change makes an older mechanism potentially removable; TOUCHED_PREEXISTING means nearby relevant debt is present without being worsened. Discard unrelated discoveries from the review.

Focus on responsibility duplication, multiple sources of truth, repeated transformations or validation, parallel mechanisms with the same contract, unnecessary dependency surface, and behaviorally redundant tests. A single implementation can still justify an abstraction, and an old compatibility branch can still serve an external consumer. Explain the maintenance cost or behavioral consequence, rather than declaring a pattern bad in isolation.

## Deletion safety

When proposing deletion, establish what replaces the behavior and who consumes it. Inspect local static and dynamic/configured entry points, public exports, persisted representations, migrations, rollout/version skew, parallel implementations, and behavior tests as relevant. Record positive evidence for preserved behavior and any consumers that local evidence cannot rule out. If external consumers or runtime discovery remain unknown, recommend investigating or deprecating the mechanism; do not present deletion as safe.

Every deletion recommendation carries evidence for replacement behavior, consumer analysis, and compatibility, plus unresolved risks. The helper rejects a deletion finding without these records. These are evidence requirements for a deletion claim in the supplied design, not new acceptance criteria for the application. A suggested smaller implementation remains a proposal until separately authorized and implemented.

## Accounting

`code-mass.json` separates raw added/removed text lines from maintained source lines. Git's line statistics include comments, blanks, tests, data, and generated material; they are not SLOC. Pure renames contribute zero additions/removals. Binary changes have unknown textual size. Working-tree mode recognizes exact-content moves and labels its rename method; edited moves may be counted as deletion/addition until a better local analyzer is used.

The built-in helper reports maintained SLOC as unknown. When an installed counter is available, measure both pinned snapshots with the same tool/version and classification. Separate production code, tests, configuration/IaC, documentation, and generated/vendor/lockfile material. Report added and removed maintained lines with the method and exclusions, not just a total-size difference or an invented estimate. A new small wrapper plus a large copied implementation is not a reduction. Formatting and code motion do not establish simplification.

The supplied modifications mention a 6:5 principle without defining its direction. The request/assessment permits an advisory `removed_per_added` ratio with an explicit basis; without a supplied interpretation its target remains unset. When the target is 6 removed for 5 added, evaluate removed × 5 against added × 6. With no additions, a removal-only change is reported as such, without division by zero. Missing maintained-line measurement yields UNKNOWN, not failure or fabricated zero. The ratio never overrides correctness, security, behavioral coverage, or compatibility and never appears as a merge blocker by itself.

For each debt observation, explain the relationship to the PR, local evidence, suggested treatment in this PR or a separate change, expected maintenance benefit, and uncertainty. Keep `technical-debt.md` short and separate from blocking defects. Do not create follow-up tickets.
