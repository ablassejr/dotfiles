# Research and design decisions

Research date: 2026-09-09. The two supplied documents define the requested behavior. The document beginning “Locked” defines the runtime boundary where the documents differ. The older document's opaque citation handles were not treated as independently verified sources; the research below uses current primary documentation.

## A skill plus local artifacts

Agent Skills defines a skill as a directory with YAML-frontmatter `SKILL.md`, with optional scripts and supporting resources loaded when needed. Its experimental allowed-tools field is not a portable sandbox contract. The package uses a short entry point, focused references, public schemas, and a single cohesive deterministic helper. It does not assume a particular cloud agent or hosted MCP service. [Agent Skills specification](https://agentskills.io/specification)

When a user starts a review, local Git identifies the change and the helper captures evidence. The agent reviews that evidence inside the enforcing local host and records its reasoning and command receipts. A validator computes the local result and writes reports. Each new revision can be reconstructed from its local objects and artifacts, so the framework uses ordinary files rather than a service, workflow engine, or SQLite journal. This is a design decision for the supplied single-user/local-effects scope, not a claim that SQLite or durable orchestration is generally unsuitable.

## Exact local identity

Git's documented merge-base operation can return multiple best common ancestors. A PR-style range therefore pins the supplied base tip, head, and actual unique merge base separately. An ambiguous baseline is reported, and an explicit direct comparison remains available. Root commits use an in-memory empty file map; staged/working modes use content identities rather than pretending HEAD identifies dirty data. [Git merge-base](https://git-scm.com/docs/git-merge-base)

Git exposes NUL-delimited machine-readable file records, rename detection, and explicit suppression of external diff/text-conversion drivers. The helper uses those where the comparison is between Git objects or index state, and preserves unusual paths and binary changes. It computes raw line deltas independently from maintained SLOC. Working-tree bytes are read directly, with exact-content rename recognition and disclosed limits for edited moves. [Git diff](https://git-scm.com/docs/git-diff), [Git cat-file](https://git-scm.com/docs/git-cat-file)

Git documents optional-lock and lazy-fetch controls; a nominal read can otherwise acquire optional locks or retrieve missing promised objects. The helper disables both, blocks transport protocols, disables executable integrations, and fails on missing local inputs. This protects the intended local behavior without mutating global configuration. [Git environment and options](https://git-scm.com/docs/git), [Git configuration](https://git-scm.com/docs/git-config)

## Immutability is not just a status check

Git status describes changes between HEAD, the index, and working files. It does not provide a byte-for-byte fingerprint of every untracked/ignored file or prove the absence of transient changes. The helper hashes file contents, file kinds, symlink text, and modes across the source and Git storage. External metadata for worktrees and nested repositories is included. Native tools additionally need host-enforced write/network denial; comparison detects drift but is not a sandbox. [Git status](https://git-scm.com/docs/git-status), [Git worktree](https://git-scm.com/docs/git-worktree)

The package deliberately supplies no unsafe fallback runner. OS isolation and local model execution are host responsibilities. This limits automatic execution while preserving the requested no-side-effects boundary. A cloud model cannot become offline through a Markdown instruction. A runtime capable only of cloud inference can use the public framework documentation, but cannot satisfy the locked review by sending private code to its provider.

## Existing utilities are conditional capabilities

Installed static analyzers and graph tools can provide useful evidence, but their names do not establish offline behavior. For example, Semgrep documents metric behavior that depends on configuration and authentication, and an explicit metrics-off mode. Disabling a telemetry flag is useful configuration, not proof that all network traffic is impossible. Use installed local rule/data files and host denial; do not automatically contact registries or install analyzers. [Semgrep metrics](https://docs.semgrep.dev/metrics)

Google's review guidance emphasizes design, functionality, complexity, and meaningful tests, including whether tests fail for broken behavior and remain valid when implementations change. The framework uses these as review lenses while retaining the user's approved contracts and behavior-only testing instructions. It does not adopt another organization's policies as new application requirements. [Google: what to look for in a code review](https://google.github.io/eng-practices/review/reviewer/looking-for.html)

## Finding discipline

When a candidate appears, the reviewer searches for evidence that would disprove it, explains the reachable consequence, and classifies its relationship to the PR. A fresh local context challenges serious findings and the overall conclusion. Parallel lenses may help a capable host, but they share one pinned packet and one final adjudication phase. Repeated opinions do not increase confidence on their own. Semantic evidence, check outcomes, missing context, and advisory code mass remain distinct.

The documents name a 6:5 measure but do not define which term is additions. The package makes the direction and basis explicit and leaves the default target unset. No independent research established this ratio as a correctness law, and the supplied design explicitly says it cannot override correctness.

## Traceability to the requested modifications

| Requested behavior | Package mechanism | Practical limit |
| --- | --- | --- |
| Local inputs, no remote integration | Fixed local helper operations and locked skill boundary | Host must keep semantic model and all optional tools local |
| Source/Git immutability | Comprehensive fingerprints, disabled Git integrations, host isolation requirements | Fingerprints detect lasting drift; native isolation is supplied by the host |
| Base/head, commit, staged, working modes | `prepare` and pinned snapshot contract | Missing objects and ambiguous input are explicit incomplete results |
| Bounded responsibility context and local Ground Me | Source evidence command and context/history protocol | Language graphs and causal rationale need local evidence and agent judgment |
| Deterministic checks | Repository discovery protocol and bound local receipts | Helper validates receipts; it does not execute native commands |
| Review lenses and fresh challenge | Explicit assessment fields and completion validation | The host establishes actual independent local contexts |
| Debt, deletion safety, advisory 6:5 | Separate debt records, deletion evidence, optional maintained-line input | Absence of local references cannot prove absence of outside consumers |
| Local Markdown/JSON/optional HTML | Local rendering with escaped text and no external assets | Verdict is advisory and makes no remote CI or merge claim |

Python's documented script execution, bytecode suppression, and unittest interface support running the dependency-free helpers and behavioral suite without installing packages. [Python command line](https://docs.python.org/3/using/cmdline.html), [Python unittest](https://docs.python.org/3/library/unittest.html)
