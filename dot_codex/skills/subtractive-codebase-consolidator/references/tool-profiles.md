# Tool profiles

Reuse repository-native checks and one installed tool per missing capability. `collect.py` accepts explicit argument arrays and retains the real command output; the agent interprets that output with the tool's scope and limitations. It does not treat a scanner finding as deletion authorization, implement a parser, or automatically download analyzers.

For Python, Vulture and deptry can identify unused-code and dependency candidates. Account for dynamic use, the files analyzed, and the distinction between development and runtime dependencies. Use existing boundary tests, and add Hypothesis, branch coverage, or mutation testing only when the preserved behavior needs that evidence.

For TypeScript and JavaScript, inspect Knip's entry files and compare its whole-project and production analyses. Production analysis excludes some development roots and answers a different question. dependency-cruiser can protect a justified import boundary. A small contract is preferable to a new architecture-policy subsystem.

Use jscpd or PMD CPD to find repeated structures, ast-grep for constrained structural rules, LibCST for coordinated Python codemods, and Polyglot Piranha for approved cascading transformations. Test reusable rewrite rules against both matching and nonmatching examples. Syntax matching alone does not establish interchangeable contracts.

For Go, inspect deadcode's selected program roots, public APIs, assembly, and linkname limitations. For Rust, inspect supported features and targets before using cargo-machete or cargo-mutants. For JVM code, preserve reflection, serialization, dependency injection, and public roots. For C and C++, use a matching compilation database and existing compiler, sanitizer, and clang-tidy checks.

Git history can identify churn and coupled changes. Code Maat is optional when its analysis would improve prioritization. Formatting and migration commits can distort co-change signals. CodeQL requires a separate licensing and provisioning decision for private repositories; it is not a dependency of this skill.

The tool configuration records its version command, image ID, arguments, exercised scope, skipped scope, and related contracts. Rules supplied as files belong in the pinned snapshot. Missing tools fail visibly. A tool that exits successfully without covering the declared files is still incomplete evidence.

Primary references for runtime behavior:

- [cloc documentation](https://github.com/AlDanial/cloc#readme) explains per-file counts, diffs, and `--skip-uniqueness`.
- [Docker run reference](https://docs.docker.com/reference/cli/docker/container/run/) defines the network, filesystem, resource, image-pull, and process controls.
- [Pydantic strict mode](https://docs.pydantic.dev/latest/concepts/strict_mode/) explains the validated JSON contract types.

Before using another CLI, retrieve its current official command documentation through the environment's required documentation provider. Provision tools separately from an analysis run. Do not assume a hosted documentation or inference service is compatible with an offline session.
