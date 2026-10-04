# Validation and support

Version 1.0.1 is a skill with a standard-library Python CLI that runs locally. It provides the complete audit, evidence, grounding, proposed-plan, implementation-check, semantic-finalization, and reporting lifecycle for its supported adapters. The analytical interpretation remains the responsibility of the reviewing agent or analyst, using a hosted or local model as appropriate.

## Supported capabilities

| Capability | Current behavior |
|---|---|
| Local source snapshots | Exact Git object bytes, index bytes, or tracked/nonignored working files; content-addressed storage; source and shared Git-storage fingerprints |
| Scope | Explicit paths, qualified Python symbol, exact endpoint range, commit with explicit merge parent, staged change, or working change |
| Maintained-code accounting | Built-in Python AST/tokenizer and JSON adapters; component totals, token-difference credit, matching-line movement reconciliation, and unknown totals when needed |
| Structural discovery | Built-in Python duplicate-declaration and returned-call hypotheses; optional executed ast-grep/Tree-sitter outlines for locally supported languages |
| Other candidate categories | Explicit analyst registration using the supported taxonomy; no claim of automatic semantic detection |
| Local history | Bounded rename-following Git log and optional literal pickaxe; no inferred historical rationale |
| Precise code intelligence | Source-bound normalized graph import; no bundled raw SCIP/LSIF parser, indexer, or CodeQL database runner |
| Planning | Evidence-bound assessment, explicit target/removal identities, conceptual vectors, behavior/check mapping, prerequisite validation, local proposed PR partitions, computed or unknown estimates |
| Verification | Same declared commands on isolated baseline/target copies; optional identical captured harness; real exit codes, logs, timeouts, and source integrity |
| Finalization | Exact target review binding, preserved unknowns/conflicts, no override of failed/unavailable execution, measured removal credit only after completion |
| Reports | JSON, Markdown, self-contained HTML, and SVG; stale reports retain verified historical context without current credit |

Python 3.11 or newer and a local Git executable are required. Native check execution and the optional structural adapter require a working macOS `sandbox-exec`. The capability probe must prove outside writes and network operations are denied before either runs. The runner permits file reads needed by the local toolchain, so this containment does not provide filesystem-read confidentiality. An outer application sandbox may prevent applying Seatbelt; that environment returns `UNAVAILABLE`. The helper never falls back to unconfined checks.

The runtime does not install packages, contact providers, or invoke a model. The reviewing agent may use hosted models and configured context, documentation, and research services under the user's authorization and host instructions. The native check runner's filesystem and network containment applies to executed checks, not to the reviewing agent's tools.

## Behavioral verification

The public CLI suite contains **36 end-to-end tests**. The completed native run passed all 36 in 31.740 seconds on the current macOS host, using Python 3.12.14 and Git 2.54.0. Earlier runs also exercised the explicit unavailable-isolation path under the outer Codex sandbox. Tests use temporary real Git repositories and observe command results, source bytes, persisted artifacts, public behavior, and documented errors. They do not import or assert production private helpers.

| Contract family | Exercised observable behavior |
|---|---|
| Capture and scope | Source/Git byte preservation; archive attribute fidelity; root commit; staged versus working bytes; qualified and ambiguous symbols; new output requirement |
| Accounting | Comments and docstrings; exact moves; scope escape; generated paths; Python/JSON formatting mixed with real changes; unsupported formats; computed totals; finite JSON inputs; explicit ratio exception |
| Evidence and planning | Exact source coordinates; missing evidence; self-dependency; normalized graph identities/endpoints; unknown estimates; incomplete seals and corrupted blobs |
| Behavioral preservation | Public return values and documented errors; same baseline/target checks; failed behavior cannot be overridden by review; named obsolete owner must disappear |
| Component and external seams | Shared harness; provider output persisted and read through a filesystem contract; native runner write/network confinement; ast-grep declaration/source binding |
| Completion and recovery | Review identity rejection; checks alone remain incomplete; missing integration evidence; successful review; invalid finalization; current-credit clearing; stale historical results; timeout failure |
| Presentation | Derived reports rebuilt from evidence; untrusted labels escaped as text; parsed SVG showing declared before/after values |

The supplied skill-creator validator reports `Skill is valid!`. It used an existing cached PyYAML module for that development-time check; the delivered CLI does not depend on PyYAML. The package includes public JSON schemas for assessment, imported graph, target review, candidate artifacts, consolidation plans, and verification reports. Output schemas permit additive fields; input schemas reject unsupported fields.

An independent agent exercised a separate, explicitly synthetic public API fixture without reading the implementation or the author's tests. It observed hypothesis/plan/check/review distinctions, unavailable containment, a completed preserved consolidation, rejection of a Unicode behavior change despite favorable code metrics, and invalidation after source drift. Its evidence and scope are provided separately with the delivered package.

## Reproduce the public test suite

Run this from the package directory with an existing Python interpreter:

```text
python3 -B -m unittest discover -s tests -v
```

The suite adapts to unavailable native containment and validates its explicit incomplete result. A native run is needed to exercise actual command success/failure, timeouts, and confinement. Test success under an unavailable-isolation host does not prove those native paths ran.

## Limits and uncovered behavior

Other maintained language formats remain unknown for code-mass credit. ast-grep outlines extend structural evidence, not measured SLOC or resolved-consumer proof. scc/Tokei execution, raw SCIP/LSIF decoding, CodeQL queries, automated churn/blame ranking, arbitrary-language semantic duplicate detection, and cross-run trend aggregation are not implemented in this version. These integrations require adapter-specific source and behavior contracts before they can contribute verified credit.

The suite does not establish production-scale performance, arbitrary language/parser versions, Windows/Linux containment, real external-consumer completeness, reflection/plugin closure, distributed failures, or concurrent adversarial artifact rewriting. Merge-parent resolution, linked-worktree metadata traversal, submodule/LFS gaps, and unusual symlink layouts have implementation support but are not exhaustively exercised by the public test matrix. Full-tree fingerprints and source capture may be expensive for large repositories. Missing local objects or required dependencies remain explicit gaps; they are never fetched.

Local seals detect inconsistency and ordinary corruption. They are not signatures, independent attestations, or a defense against coordinated rewriting of artifacts and hashes. A reviewer declaration remains a declaration. A passing local contract does not establish CI, merge, deployment, live access, or production behavior.

## Primary implementation references

- [Git object inspection with ls-tree](https://git-scm.com/docs/git-ls-tree) and [cat-file](https://git-scm.com/docs/git-cat-file).
- [Git revision resolution](https://git-scm.com/docs/git-rev-parse), [index/working-file enumeration](https://git-scm.com/docs/git-ls-files), and [local history/pickaxe options](https://git-scm.com/docs/git-log).
- [Python AST](https://docs.python.org/3/library/ast.html), [tokenize](https://docs.python.org/3/library/tokenize.html), and [subprocess execution](https://docs.python.org/3/library/subprocess.html).
- [ast-grep outline command and output contract](https://ast-grep.github.io/reference/cli/outline.html) and [private configuration format](https://ast-grep.github.io/reference/sgconfig.html).
- Apple's locally installed `sandbox-exec(1)` manual supplies the `-f PROFILE COMMAND ARGUMENTS` contract and marks the executable deprecated. Runtime capability checks determine whether the host can use it.
