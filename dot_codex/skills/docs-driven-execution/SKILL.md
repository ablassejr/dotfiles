---
name: docs-driven-execution
description: Require a complete, version-aware Grounded Docs MCP (`docs-mcp-server`) documentation inventory before planning or autonomously executing non-trivial technical work. Use for implementation plans, migrations, integrations, architecture changes, debugging plans, infrastructure work, or any task whose correct execution depends on library, framework, platform, CLI, API, protocol, database, build, test, deployment, or operations documentation. Durably repair docs-MCP if it is unhealthy; never bypass, defer, or replace this gate with web search, memory, source inspection, or another documentation tool.
---

# Docs-Driven Execution

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


Treat docs-MCP as a hard prerequisite, not an optional research aid. Inventory every task-relevant technology, index its complete official documentation at the applicable version, query that index, and derive an execution-ready plan from the retrieved evidence. Continue into execution only when the user's request authorizes it.

## Non-negotiable invariants

- Do not write the project plan or begin implementation until the documentation gate passes.
- Do not substitute web browsing, model memory, package source, repository examples, another MCP, or ad hoc notes for docs-MCP retrieval.
- Use repository inspection and official-site discovery before the gate only to identify technologies, versions, and authoritative documentation roots.
- If docs-MCP is broken, pause project work and repair the actual installation durably. Do not use a temporary command, alternate cache, one-off process, direct web reading, or manual copy as a workaround.
- Preserve the persistent documentation store during runtime or native-module repair unless corruption is proven and a recoverable migration is prepared.
- Treat incomplete indexing, unexplained scrape errors, version ambiguity, and unqueryable indexes as failed gates.
- Never claim complete coverage without an explicit inventory and evidence for every included technology.

## Workflow

### 1. Establish the technology inventory

Inspect the task and the relevant repository surface before planning. Read manifests, lockfiles, toolchain files, imports at the affected boundary, build and test configuration, CI workflows, deployment manifests, and runtime configuration.

Classify a technology as relevant when autonomous execution will rely on any of its:

- commands, flags, generators, or authentication setup;
- APIs, SDKs, schemas, protocols, or configuration formats;
- build, lint, typecheck, test, migration, release, deployment, or rollback behavior;
- runtime, hosting, database, queue, observability, security, or infrastructure contracts.

Include directly used transitive dependencies only when the task crosses their public contract. Exclude incidental dependencies, but record the evidence-based reason for each plausible exclusion.

Create an inventory with:

| Field | Required evidence |
|---|---|
| Technology | Canonical product or project name |
| Relevance | The exact task decision or action it constrains |
| Version | Lockfile, manifest, runtime, configuration, or deployed-state evidence |
| Official docs root | Version-appropriate vendor or project documentation URL or local official docs path |
| Required coverage | Documentation areas needed for commands, workflows, contracts, failure handling, and verification |
| Index status | Missing, stale, wrong version, incomplete, or verified |

Re-run the inventory after documentation research. Add newly discovered tools or platforms and repeat the gate for them before planning.

### 2. Prove docs-MCP health

Use the configured Grounded Docs MCP tools when available. Also identify the canonical `docs-mcp-server` launcher and persistent store so failures can be repaired at their source.

Prove all required capabilities:

1. The MCP server initializes and lists its tools.
2. The index can list libraries and versions.
3. A known indexed library can be searched.
4. The server can perform or accept an indexing operation.
5. The same canonical launcher works outside any temporary shell or cache used during diagnosis.

If any check fails:

1. Capture the exact error, launcher resolution, runtime version, package version, configuration, native-module ABI when applicable, and persistent-store location.
2. Identify the root cause before changing state.
3. Repair the canonical installation, wrapper, runtime pin, package installation, native dependency, configuration, permissions, or store migration that caused the failure.
4. Prefer an isolated, version-pinned runtime and package over ambient `PATH`, global packages, or ephemeral `npx` caches when runtime drift caused the failure.
5. Re-run the full health proof from a clean invocation context.
6. If durable repair cannot be completed, stop and report the task as blocked. State the failed proof and the durable repair still required; do not continue project planning.

Diagnostics and repair planning for docs-MCP itself are the only exception to the project-planning gate.

### 3. Index all relevant official documentation

Run `list` first. For every inventory row:

1. Reuse an index only when its identity, version, source, completeness, and freshness are verified.
2. Refresh a complete matching index when content may have changed.
3. Scrape the official version-specific documentation root when the index is missing, mismatched, stale, or incomplete.
4. Index local official documentation with an absolute `file://` URL when that is the authoritative source.
5. Cover the full relevant official documentation set. Do not impose page, depth, path, or concurrency shortcuts that omit required material merely to save time.
6. Review scrape totals, skipped pages, redirects, and errors. Resolve every omission that can affect the task.
7. Record any unavoidable upstream access limitation. Treat it as blocking when it prevents complete required coverage.

Use the durable canonical launcher, not `@latest` or an ephemeral cache, when this machine has a pinned docs-MCP installation. Never include credentials in the index name, logs, plan, or memory.

### 4. Validate retrieval coverage

Query docs-MCP for every technology and every required coverage area. At minimum retrieve evidence for:

- installation and prerequisites;
- required CLIs, MCP servers, SDKs, plugins, services, and credentials;
- the exact APIs, configuration, or commands the task will use;
- the official development, build, test, migration, deployment, and rollback workflows that apply;
- documented failure modes, compatibility constraints, and verification procedures.

Require useful results with authoritative source URLs. A library appearing in `list` is not sufficient. If a query exposes missing coverage, repair or expand the index and query again.

Produce a coverage ledger mapping each technology and required area to its indexed version, successful query, and official source. The gate passes only when every row is covered.

### 5. Derive the autonomous execution plan from docs-MCP

Synthesize the plan from retrieved docs-MCP results and repository facts. Clearly label repository-derived facts, docs-derived requirements, assumptions, and unresolved choices. Attach the relevant indexed source URLs to plan decisions.

The plan must specify:

- objective, observable success criteria, and scope boundaries;
- prerequisites and exact version constraints;
- required CLIs, MCPs, SDKs, plugins, services, credentials, and setup checks;
- ordered commands or tool actions, actors, inputs, outputs, and state changes;
- safe parallel work and dependency ordering;
- build, lint, typecheck, unit, integration, contract, and end-to-end verification that actually applies;
- migrations, deployment, monitoring, rollback, cleanup, and recovery behavior;
- expected failure branches and when autonomous execution must stop for new authority;
- an evidence appendix containing the technology inventory and coverage ledger.

Write the behavioral flow in human-readable pseudocode:

```text
WHEN the authorized task starts:
  VERIFY every prerequisite and required tool from indexed official docs.
  IF any prerequisite is absent or incompatible:
    APPLY the documented setup or repair procedure.
    RE-VERIFY before continuing.

  FOR each dependency-ordered execution stage:
    PERFORM the documented commands and state changes.
    OBSERVE the declared public outcome.
    IF the outcome fails:
      FOLLOW the documented diagnosis and recovery branch.
      STOP if recovery needs destructive scope, credentials, approval, or an unresolved product choice.

  RUN every applicable behavioral verification at stable public boundaries.
  IF deployment is authorized:
    DEPLOY through the documented workflow.
    MONITOR documented health signals.
    ROLL BACK through the documented path when success criteria are not met.

  REPORT artifacts, observable results, remaining risks, and any unverified path.
```

Do not invent commands or workflows when the index is silent. Expand the index or mark the plan blocked.

### 6. Execute only within authorization

If the user requested implementation or repair, execute the validated plan and keep docs-MCP available for questions that arise. When a new technology or undocumented decision appears, return to the inventory and documentation gate before proceeding.

If the user requested only analysis or a plan, stop after delivering the evidence-backed plan. Do not mutate the project or external systems.

## Completion checklist

- Every relevant technology and plausible exclusion is recorded.
- Exact or compatible versions are proven from live project evidence.
- The canonical docs-MCP installation passes initialization, list, search, and indexing checks.
- Complete required official documentation is indexed for every relevant technology.
- Every required coverage area returns useful docs-MCP results with official source URLs.
- The plan names all required tooling and official workflows.
- The plan includes prerequisites, state changes, observable verification, failure recovery, rollback, and stopping conditions.
- No project planning or execution occurred before the documentation gate passed.
