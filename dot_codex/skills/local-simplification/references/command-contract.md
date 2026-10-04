# Local command and artifact contract

The executable is `scripts/simplify.py`, run with Python 3.11 or newer. The core uses the standard library and an existing Git executable. Commands do not install packages, contact providers, change refs, or execute a model. The reviewing agent may use hosted or local models and configured services under the user's authorization and host instructions. `--offline` remains accepted as a legacy no-op flag; it does not restrict the reviewing agent's tools.

## Inspect capabilities

`python3 -B scripts/simplify.py doctor` reports installed optional tools and runs a disposable macOS isolation probe. The probe tests an allowed write, a denied write outside the workspace, and denied network binding. Missing or unusable isolation is reported as `UNAVAILABLE`; native checks have no unconfined fallback.

## Capture a responsibility

`python3 -B scripts/simplify.py audit --repo /path/to/repo --scope src/provider --scope tests/provider --responsibility 'Resolve provider identity' --output /path/to/new-run`

Scope paths may name files, directories, or an explicitly selected whole repository (`--scope .`). Repeating `--scope` includes related tests and configuration. A scope-only audit captures HEAD on both sides and discovers candidates in that snapshot. An audit must select a scope, symbol, or change.

`python3 -B scripts/simplify.py audit --repo /path/to/repo --base main --head HEAD --output /path/to/new-run`

Base and head compare exact endpoints. The helper does not silently substitute a merge base. Without `--scope`, changed paths seed the responsibility. `--symbol module.py::Class.method`, `--symbol Class.method`, or an unambiguous short name selects Python declarations. `--staged` captures index bytes; `--working-tree` captures tracked working contents and nonignored untracked files. Both use HEAD as the baseline. `--commit REV` captures a commit against its parent; merge commits require `--parent NUMBER`, starting at one. Root commits use an empty in-memory baseline. These mode selectors are mutually exclusive. `--head` belongs to endpoint comparison and `--parent` belongs to commit mode.

`--policy /path/to/policy.json` accepts the maintained-path classification fields and minimum ratio described in [accounting and evidence](accounting-and-evidence.md). The output must be a new directory. Explicit output directories inside the repository are excluded from integrity fingerprints; Git storage and repository-root overlap are refused. Artifact paths cannot traverse symlinks. Use canonical paths such as `/private/tmp` instead of a symlink alias where needed.

The run stores `manifest.json`, immutable content-addressed `blobs`, `seal.json`, `inventory.json`, `candidates.json`, `responsibility-current.json`, `code-mass.json`, an editable `assessment.json`, and local reports. A source fingerprint covers file bytes, kinds, modes, link text, Git storage, and linked worktree Git metadata. Source content is read with `ls-tree`/`cat-file`, so archive export attributes do not remove or substitute files. Submodule pointers and LFS pointers remain explicit coverage gaps. No symlink target is read as source content.

## Collect evidence

`python3 -B scripts/simplify.py structure --run /path/to/run --side head --path src/provider.py`

This optional adapter executes an already installed `ast-grep outline` with its bundled Tree-sitter parsers, against disposable pinned files under the same tested native containment. Repeat `--path` to choose files; omitted paths use the selected scope. `--lang LANGUAGE` selects an installed parser when file extension inference is unsuitable. A private empty configuration prevents repository-specific parser or outline configuration from executing. The receipt records tool binary identity, actual exit/log evidence, snapshot hashes, source coordinates, declarations/imports/exports, and direct member relationships. It does not resolve call targets or prove that no consumers exist. Missing tooling, unsupported versions/languages, and unavailable containment produce an explicit incomplete receipt. Nothing is installed.

`python3 -B scripts/simplify.py evidence --run /path/to/run --side head --path src/provider.py --start 10 --end 25 --relation consumer --reason 'This caller consumes the selected provider identity'`

Evidence coordinates are one-based and inclusive. The source hash, snapshot digest, exact excerpt, relationship, and explanation are captured. Allowed relationships are `selected`, `consumer`, `dependency`, `test`, `contract`, `history`, `configuration`, and `parallel`. Consumer, dependency, test, configuration, and parallel evidence extends the plan's responsibility scope to those exact paths.

`python3 -B scripts/simplify.py ground --run /path/to/run --candidate CON-identifier --limit 50 --pickaxe lookup_provider`

Grounding records bounded local Git history for the candidate paths at the captured revision, following file renames. `--pickaxe` is optional and uses literal occurrence-count history. Grounding supplies chronology; the reviewing agent or analyst establishes rationale and current constraint validity from source, tests, checked-in documents, and history.

`python3 -B scripts/simplify.py candidate --run /path/to/run --path src/provider.py --owner src/provider.py::Resolver --classification REDUNDANT_STATE --statement 'The cache may repeat persisted provider identity'`

An analyst may add a candidate for any supported taxonomy category. At least one path must intersect the selected scope. Candidates begin with unknown deletion safety. Adding one extends the editable assessment without discarding existing cards.

`python3 -B scripts/simplify.py import-graph --run /path/to/run --side head --file /path/to/local-graph.json`

The [graph schema](../schemas/graph.schema.json) describes a normalized local graph exported by an existing SCIP, LSIF, language-server, Tree-sitter, or CodeQL integration. Every node carries the exact source hash and coordinates, and every edge has resolved endpoints. The helper validates source binding and imports provider claims; it does not parse raw SCIP protobufs or CodeQL databases or attest that an indexer ran. A complete consumer graph is never inferred from an imported provider name.

## Compile a plan

`python3 -B scripts/simplify.py plan --run /path/to/run --assessment /path/to/completed-assessment.json`

The [assessment schema](../schemas/assessment.schema.json) is the public input format. Omit `--assessment` to use the run's editable draft. Each candidate names its responsibility, canonical target owner, obsolete mechanisms to remove, preservation obligations, observable behavior contracts, conceptual entities, rollback, estimates, and prerequisites. Owners use `path.py::Qualified.name` or a complete source path. The compiler rejects unknown evidence, unknown or cyclic prerequisites, duplicate IDs, and inconsistent behavior/check references. Incomplete cards may produce a proposed plan; they cannot produce verified savings. An optional `ratio_exception` object contains a nonempty `reason` and one or more bound `evidence_ids`; it permits an explicitly justified below-target ratio only when all other completion conditions pass.

Each retained candidate produces a proposed responsibility PR with computed prerequisite references. Estimates remain null when unknown. Totals are calculated only when all components are known. One completed responsibility transition is the accounting unit; staging estimates do not receive deletion credit. Plans remain local JSON artifacts, and no PR is created.

## Execute verification

`python3 -B scripts/simplify.py verify --run /path/to/original-run --head IMPLEMENTATION_COMMIT --output /path/to/new-verification`

The latest bound plan is used unless `--plan plans/PLAN-identifier.json` selects another bound plan. `--working-tree` verifies a local dirty implementation instead of a commit. The baseline is always the original plan's captured head; historical source changes after planning are expected and do not invalidate that immutable baseline.

Checks are explicit argv arrays supplied in the assessment. Each has an ID, kind, contract IDs, and timeout. Kinds are `end_to_end`, `integration`, `build`, `typecheck`, `lint`, and `static_analysis`. Every declared behavior maps to an end-to-end check, and a declared component/service seam also maps to an integration check. The helper runs the same arrays on disposable baseline and target snapshots. `{python}` expands to the current interpreter and `{source}` to the disposable source root. With `--harness /path/to/harness`, the same captured harness bytes are supplied to both sides and `{harness}` expands to that copy.

Example check object:

```json
{
  "id": "provider-contract",
  "kind": "end_to_end",
  "argv": ["{python}", "-B", "-m", "unittest", "discover", "-s", "tests"],
  "contract_ids": ["provider-identity"],
  "timeout_seconds": 60
}
```

The macOS runner uses the locally installed `sandbox-exec -f PROFILE COMMAND ARGUMENTS`. The profile denies by default, permits process execution and file reads, confines file writes to the disposable workspace plus `/dev/null`, and denies network operations and unrestricted Mach IPC. It supplies a minimal environment and terminates the process group after completion or timeout. This is filesystem-write and network isolation; it is not filesystem-read confidentiality. The deprecated Apple executable is capability-probed each run. Unsupported hosts produce unavailable checks.

The result records actual exit codes, logs, snapshot digests, sandbox profile hashes, code-mass results, named mechanism removal, and target existence. `execution-report.json` is sealed execution evidence. `target-review.json` is an unfinished semantic review. Even if checks pass, the verification remains incomplete until that review is supplied.

## Finalize and report

`python3 -B scripts/simplify.py finalize --run /path/to/verification --review /path/to/target-review.json`

The [target review schema](../schemas/target-review.schema.json) binds each review to the exact verification run, plan, and target snapshot. It covers all proposed candidates and preservation obligations, including target source coordinates and hashes. Unknowns remain incomplete and contradictions fail. A local `PASS` requires successful executable checks, completed grounded declarations, disappearance of named mechanisms, a surviving canonical owner, net maintained-code reduction, the configured ratio, and a declared conceptual reduction. Source drift remains stale. Local reviewer statements are not cryptographic attestations of semantic truth.

`python3 -B scripts/simplify.py report --run /path/to/run`

Reporting rechecks pinned source and evidence integrity. It rebuilds report projections from bound artifacts and renders Markdown, self-contained HTML, and `responsibility-map.svg`, with escaped content and a restrictive HTML content security policy. Invalid finalization clears the current verdict and credit. Source changes render a stale report. When the sealed snapshot evidence remains intact, the report keeps its historical identity, measurements, and receipts with an explicit historical-only label. Reports make no network requests.

## Exit codes and recovery

All commands print a JSON object to stdout. Exit `0` means successful audit, planning, reporting, evidence collection, capability inspection, or a passing finalized verification. Exit `2` means malformed input, corrupted evidence, unavailable source, or stale source. Exit `3` means verification/finalization returned failed or incomplete. Audit and plan are successful preparation operations even though their advisory verdict is incomplete.

Input validation never authorizes repository changes. Keep an incomplete run for inspection and create a fresh run after source changes, except when a plan is intentionally reused as the immutable baseline of `verify`. No run directory is overwritten by audit or verify.

## Public output formats

| Artifact | Consumer contract |
|---|---|
| `candidates.json` | [Candidate artifact schema](../schemas/candidate.schema.json): run identity and structural hypotheses with unknown safety |
| `plans/PLAN-identifier.json` | [Consolidation plan schema](../schemas/consolidation-plan.schema.json): captured baseline, assessment, proposed PRs, prerequisites, and computed/unknown totals |
| `verification-report.json` | [Verification report schema](../schemas/verification-report.schema.json): verdict, completeness, code-mass credit, and remaining evidence; successful records also retain execution, plan, and review identity |

An executed check succeeds independently of whether the whole simplification is complete. A typical pre-review report includes `"execution_verdict": "PASS"`, `"verdict": "INCOMPLETE"`, and `"validated_removal_credit": null` inside `code_mass`. A finalized preserved transition can expose `"verdict": "PASS"` and a measured removal count. An invalid or stale report clears current credit; historical measurements are labeled with `"historical_only": true` when their seals remain valid. Output schemas permit additive fields for compatible extensions. Input schemas are versioned and reject unsupported fields.
