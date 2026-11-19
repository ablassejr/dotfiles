# Tool routing

Resolve tools by capability and obey explicit host, session, or repository instructions when they require a stricter order or more frequent documentation checks.

## Repository context

For an integrated semantic, program, or ticket workflow, open implementation context only after approval of its exact First-Principles Basis. Standalone Ground Me uses its own entry contract and does not require creating an epic.

After the basis gate, establish repository identity, exact baseline commit, target branch, worktree state, and available structural indexes. Git and inventory establish identity, history, and changed surfaces. CodeGraph or the configured structural adapter locates symbols, callers, dependencies, ownership, and blast radius; use it before direct search when the repository already owns a `.codegraph` index. `claude-context` retrieves semantically relevant code, tests, conventions, and documentation. Treat both indexes as navigation and verify decisive claims in current source. Do not initialize CodeGraph without the user's choice.

The current repository host and selected tracker reconstruct pull-request, review, issue, and decision lineage. Approved specification revisions in the selected documentation home and ADRs establish recorded intent; architecture views are projections. Preserve source revisions and freshness assessments in the workflow manifest.

## Documentation and commands

Before the first nontrivial or version-sensitive CLI operation in a session, record the installed version and retrieve applicable authoritative documentation through `docs-mcp-server` for the command, arguments, flags, and side effects. If documentation is missing or stale, index or refresh official documentation and wait for completion. Do not guess syntax. Record the verified command family, applicable version, environment, documentation source, and retrieval time as a reusable capability record.

Reuse that record for the same documented operations until the version, environment, or intended operation changes. Ordinary Git inspection and already verified commands do not require repeated documentation retrieval under this skill. Explicit session instructions requiring lookup before every CLI still apply.

`specflow` uses this bundle's versioned documentation. Before its first use, index the bundle as `epic-spec-system` at `VERSION`, wait for completion, and query the intended command. Re-index when the installed version changes. Its local validation does not establish external authorization, live revision freshness, exclusive worker execution, accepted Camunda completion, or human approval.

## Ground Me and external research

Ground Me traverses current source, introducing and modifying Git history, repository-host reviews and superseding work, the selected tracker's parent and related work, approved specification records and ADRs, architecture artifacts, and historical external constraints. Apply the same capability-record policy to lineage helpers and Git. Their output provides correlations and source evidence, not proof of intent.

Prefer Exa search and fetch when available, or the host's current web research capability when absent. Use primary sources, record retrieval dates and applicable versions, and resolve only gaps selected by the research loop. Do not start an overlapping research loop with independent stopping rules.

## Orchestration access

Resolve the Camunda 8.9 cluster and tenant, selected deployed process definition/version, root business identity, and live instance key through an authorized API/client capability. Apply [the runtime contract](camunda-orchestration.md). The bundled CLI supplies local validation and the [Camunda commands](camunda-runtime.md), including `start`, `status`, `inspect`, `resume`, `correlate`, and `validate`. Research reads need no operation token. Persistent index/cache updates use maintenance-operation tokens in the runtime integration.

## External writes

Resolve the authenticated identity, exact destination, current source revisions, and authorized scope. Respect existing authorization; request only missing permission. Route mutations through [operation-token-aware adapters](operation-adapters.md). Keep a durable effect plan, stable operation identity, actual destination guarantee, revisions, receipts, and readback. Use the strongest supported combination of idempotency, guarded publication, conditional writing, or reconciliation. Record materially harmful best-effort risk explicitly. A revision conflict or uncertain outcome invokes the declared recovery path; it does not justify a global writer lease.

For specification delivery, follow [the publication transaction](specification-publication.md), using the selected destination and reporting partial writes and exact-revision readback. For visuals, inspect structure and a rendered view and classify feedback through [the visual review contract](visual-language.md). The semantic skill can carry authorized human decisions through the scope's selected interaction surface; it cannot create an implementation program. In a separately invoked implementation compiler, create objects before native relations, then fetch membership and relations to verify the approved program.

## Missing capability

A missing tool, documentation, Camunda runtime access, required adapter capability, or authorization blocks only its dependent stage. Record the boundary and continue independent read-only work. Never paste credentials into specifications, logs, issues, command arguments, or memory.
