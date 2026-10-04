# Research the codebase

Establish current behavior, ownership, topology, contracts, and impact at the pinned repository baseline.

Invoke Claude Context before repository investigation. If `.codegraph/` exists at the repository root, use CodeGraph before text search or direct reading for structural questions. Treat both as navigation and verify findings in current source, public contracts, behavioral tests, or runtime evidence.

For each material code claim, capture the repository, commit, file or symbol locator, the observable behavior it establishes, and whether it is explicit, structurally derived, or behaviorally inferred. Trace callers and consumers far enough to identify public boundaries and cross-component seams. Do not infer intended behavior solely from current implementation.

In `IMPLEMENTATION` mode, map approved requirements to public behavior, affected files and symbols, data and control flow, ownership, failure behavior, concurrency or transaction boundaries, migrations, security and observability boundaries, relevant behavioral tests, and safe deletion candidates. Inspect request-relevant tests for implementation coupling and plan coverage at stable boundaries.
