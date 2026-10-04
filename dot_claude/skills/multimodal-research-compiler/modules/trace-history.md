# Trace history

Use local version history for chronology and the collaboration system for rationale that did not survive into the commit.

Before each Git or hosting CLI invocation, retrieve current command documentation and side effects through Docs MCP Server. Pin the repository and baseline before interpreting history. Trace introductions, semantic modifications, moves, removals, reintroductions, reverts, and replacement changes. Follow linked pull requests, review threads, issues, and decisions when available within the source boundary.

A sequence of commits establishes order, not causation. Label a rationale `EXPLICIT` only when a source states it. Otherwise use `CHRONOLOGICALLY_INFERRED` and list plausible alternatives. Compare the original constraint with current code and documentation before calling it expired.

Build timeline events with event time, source reference, change or decision, affected entities, and confidence. Preserve discrepancies between author time, commit time, merge time, and issue updates when they matter.
