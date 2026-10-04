# Command contract

The runtime needs Python 3.9 or newer and an installed Git. It has no Python package dependencies. Invoke `scripts/review.py` with Python; no `review-pr` executable is installed on PATH. All commands use argument arrays internally, and none offers publication, remote retrieval, package installation, or arbitrary command execution.

## Prepare

```sh
python3 -B scripts/review.py prepare --repo /workspace/project --base main --head HEAD --output /workspace/reports/review-418
python3 -B scripts/review.py prepare --repo /workspace/project --base HEAD~5 --head HEAD --comparison direct
python3 -B scripts/review.py prepare --repo /workspace/project --staged
python3 -B scripts/review.py prepare --repo /workspace/project --working-tree
python3 -B scripts/review.py prepare --repo /workspace/project --commit abc123
python3 -B scripts/review.py prepare --repo /workspace/project --commit abc123 --parent 2
```

Choose exactly one of `--base`, `--commit`, `--staged`, or `--working-tree`. `--repo` defaults to the current directory; `--head` defaults to HEAD only for ranges; `--depth` is quick, standard, or deep, defaulting to standard. It records the requested review depth for the agent, not an automated amount of model work.

| Mode | Actual comparison | Identity and limits |
| --- | --- | --- |
| Base/head | Unique merge base of local base and head, compared with head | Full base tip, head, merge bases, comparison baseline, and tree IDs are recorded. No branch name is guessed. |
| Direct range | Explicit base tree compared with head tree | `--comparison direct` requests endpoint differences rather than the PR merge-base view. |
| Commit | Selected commit compared with its parent | Root commits compare with an empty tree without writing an empty Git object. Merge commits require `--parent N`. |
| Staged | HEAD compared with the index | Unstaged and untracked changes are excluded. Unborn HEAD is supported. Unresolved index stages are reported as incomplete. |
| Working tree | HEAD compared with tracked working contents plus nonignored untracked files | Includes staged and unstaged changes as they exist in the working tree. Content digests pin this mutable snapshot. Exact-content moves are recognized. |

Locally available remote-tracking refs are ordinary local inputs. Their freshness at the provider is unknown. Missing history is not fetched. Multiple merge bases require an explicit direct comparison or additional user-supplied context rather than selecting one arbitrarily.

The output defaults to a new `personal-pr-review/<random-run-id>` directory under the system temporary directory. Supply `--output` for durable storage. An explicitly requested fresh subdirectory under the repository is supported as the declared report-write exception. Existing directories are not overwritten. A temporary default output may be removed by the operating system.

The preparation JSON response contains the absolute output directory, `analysis_id`, changed-file count, and INCOMPLETE (or STALE) verdict. A successful prepare exits 0 because preparation succeeded; the review remains unfinished. Working-tree cleanliness is a conservative byte/mode comparison against HEAD/index and nonignored untracked files. It can differ from Git status when clean filters or line-ending normalization are involved; it never executes those filters.

## Capture source evidence

```sh
python3 -B scripts/review.py evidence --output /workspace/reports/review-418 --side head --path src/publisher.py --start 20 --end 48 --relation caller --reason 'This caller can retry the changed write'
```

`--path` is relative to the repository and must exist in the selected captured tree. `--side` is base or head; these name review snapshots, not necessarily working files or branch tips. Coordinates are inclusive and one-based. Supply both `--start` and `--end`, or omit both for a file-level hash record (including binary files and symlink text). Supported relations are changed, caller, callee, interface, implementation, test, configuration, coupled, and history. The reason must explain relevance to the changed responsibility.

The command prints the evidence record and stable EV identifier, verifies the content, and adds it to `context-manifest.json`. It refuses stale inputs. Source evidence is read from commit/index blob IDs or checked working-tree content; file-level records do not imply full semantic inspection.

## Import local host evidence

```sh
python3 -B scripts/review.py receipt --output /workspace/reports/review-418 --kind tool_log --file /workspace/check-logs/typecheck.txt --reason 'Typecheck of the pinned snapshot in the isolated host'
```

Kinds are tool_log, challenge, isolation, spec, history, graph, and code_mass. The helper copies the supplied artifact into its output and records a digest, origin, reason, and analysis binding. The receipt proves which artifact was supplied, not that a command or model actually ran. Preserve actual command, tool version, snapshot identity, host isolation configuration, outcome, and limitations in the artifact; do not manufacture a successful receipt. Repository-native command discovery and execution belong to the agent and its enforcing local host.

## Finalize

```sh
python3 -B scripts/review.py finalize --output /workspace/reports/review-418 --assessment /workspace/reports/review-418/assessment.json
```

Finalization validates the public assessment, evidence, and source identity, adjudicates/deduplicates findings, and writes Markdown, JSON, and a self-contained HTML report. It never silently converts preparation into a full review or interprets missing tool output as passing evidence. Re-finalization may use a corrected assessment for the same unchanged run. A source/ref change requires a new run. If finalization fails, the current report is marked incomplete/stale; earlier finding records remain diagnostic artifacts.

| Exit code | Meaning |
| --- | --- |
| 0 | Preparation/evidence import succeeded, or final verdict PASS/PASS_WITH_DEBT |
| 1 | Final verdict HOLD |
| 2 | Invalid arguments, invalid assessment/evidence, unavailable local input, or operation failure |
| 3 | Final verdict INCOMPLETE |
| 4 | Stale inputs detected during preparation/finalization |

Evidence capture on a stale run returns an operation error (2) and marks the run STALE. Consumers should read `analysis-summary.json` for review status rather than treating any successful helper command as a completed review.
