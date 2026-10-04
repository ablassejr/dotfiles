# Validation and practical limits

Run the public behavior suite from the package root:

```sh
python3 -B -m unittest discover -s tests -v
```

The tests create disposable local Git repositories and exercise the CLI as a consumer. They do not import private production helpers or assert internal call order. Git setup mutates only synthetic fixtures; reviewed fixtures are compared at their observable filesystem boundary. The runtime does not depend on unittest or any third-party package during a real review.

## Behavior matrix

| Observable contract | Validation boundary |
| --- | --- |
| Correct local range and tree identity | Real commits, divergent branches, direct comparison, and evidence content |
| Staged contents remain distinct from unstaged/untracked contents | Index and working-tree modes return different pinned evidence |
| Dirty/untracked/ignored input and Git data remain unchanged | Filesystem bytes, symlink targets, permission bits, and Git files before/after |
| Renames, binary files, unusual paths, symlinks, root commits, unborn index | Public change inventory and captured source content |
| Merge parent and multiple merge-base ambiguity | Explicit incomplete errors or selected parent identity |
| Missing local refs or promised objects | Explicit failure, preserved source/Git files, configured lazy-fetch transport remains unexecuted |
| Linked worktrees and shared Git state | Actual worktree fixture and stale result after shared-ref mutation |
| Dirty nested Git dependencies | Visible gitlink surface, conservative dirty state, explicit separate-review limitation |
| Scoped output writes | Fresh explicit in-repository output allowed; existing input, Git storage, and symlink destinations rejected |
| Prepared source/evidence binding | Rejected changed packet, artifact bytes, missing records, or mismatched identity |
| Evidence coordinates and input shape | Invalid coordinates, partial coordinates, malformed JSON envelopes/entries, invalid numeric fields, and unknown properties fail visibly |
| Preparation and missing verification cannot imply PASS | Public completeness and verdict values |
| Supported findings and deterministic failures remain visible with gaps | HOLD and incomplete status coexist |
| Debt remains nonblocking and separate | Dedicated debt report, root-problem deduplication, unrelated candidate removal |
| Deletion claims need safety evidence | Invalid deletion assessment rejected |
| Code-mass ratio is advisory and unknowns remain explicit | Below-target fixture does not block; unknown maintained SLOC remains null |
| Current human reports agree after errors/staleness | JSON, Markdown, and HTML no longer display the earlier recommendation |
| Repository executable integrations are not run | Configured fsmonitor/pager/diff/textconv/clean/smudge traps do not execute |
| HTML treats evidence as text | Parsed rendered output contains literal evidence text without executable script elements |

The synthetic native-check, model-host, and fresh-context receipts test the import and validation contract. They do not constitute execution of a real local model, proof of operating-system isolation, or a real project's test suite. No actual user repository was reviewed as part of framework validation.

An independent forward-testing pass uses only additional synthetic repositories. Its findings informed the contract coverage for immutable prepared inputs, coherent invalidation across all reports, malformed evidence, and nested dirty gitlinks. This is framework validation under the authoring request, not a claimed offline semantic review by a cloud model.

## Capability limits

The helper does not implement inference, a sandbox, a language-server/graph service, a native-command runner, or a maintained-SLOC analyzer. The skill describes the local host and evidence contracts for these capabilities. Native commands may run only in a host enforcing the specified boundary, and their results are labeled as imported evidence.

Python changed-symbol overlap is automated; other language symbols and dependency relationships require local tools or direct source inspection. Working-tree rename recognition is exact-content only. Edited moves require additional interpretation. Changed gitlinks and dirty nested repositories are surfaced, but nested source needs a separate pinned review; the outer helper retains an explicit incomplete gap. The helper does not infer external consumers, remote CI, deployment state, or provider-ref freshness.

Fingerprinting all source and Git storage includes ignored dependencies and object stores, so large repositories may take substantial local I/O. Fingerprints detect lasting byte/mode/kind changes, not a modification that another actor made and reverted between snapshots. There is no signed evidence journal or defense against a writer deliberately replacing both local artifacts and their digests. Host isolation prevents source/network effects, and the local reviewer still evaluates semantic truth.

The [validation receipt](validation-receipt.json) records the actual suite result and package checks, with the captured test output distributed beside it. Repeat tests when code changes or an uncovered public contract is identified; do not expand testing merely to increase test counts.
