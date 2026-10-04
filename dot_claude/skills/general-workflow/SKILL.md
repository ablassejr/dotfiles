---
name: general-workflow
description: Use when starting non-trivial agent work that needs codebase context, external documentation, first-principles alignment, visual artifacts, ambiguous requirements, or a durable workflow before implementation.
---

# General Workflow

Use this as the outer workflow for substantial Codex or Claude Code tasks. It
coordinates local documentation context, direct codebase retrieval, external
documentation, visual review, and first-principles alignment before
implementation.

## Start Here

1. Interpret the user's request in operational terms: desired outcome, target
   repo or files, constraints, success criteria, side effects, and whether edits
   are expected.
2. Clarify only blocking ambiguities. If the ambiguity is non-blocking, state the
   assumption and proceed.

## Visual Work

If the request involves UI, layout, images, diagrams, charts, slides, design
systems, visual polish, or any artifact whose quality depends on appearance:

- Keep a browser view open for the work.
- Show the user the visual state at every meaningful step: initial context,
  alternatives, implementation progress, corrections, and final verification.
- Prefer a local URL with screenshots or live browser interaction over text-only
  descriptions.
- Do not claim a visual result is correct until it has been viewed in the
  browser.

## Start Local Documentation Context

Start or reuse the local documentation service early when external documentation
may affect the work. Do not spawn duplicates; inspect first. Record the port and
log so later corrections can reuse the same context.

```bash
WORKFLOW_RUN_DIR="${TMPDIR:-/tmp}/claude-general-workflow"
mkdir -p "$WORKFLOW_RUN_DIR"

pick_port() {
  local port="$1"
  while lsof -nP -iTCP:"$port" -sTCP:LISTEN >/dev/null 2>&1; do
    port=$((port + 1))
  done
  printf '%s\n' "$port"
}

if ! pgrep -f '[d]ocs-mcp-server.*(server|--protocol|--port|--resume)' >/dev/null 2>&1; then
  DOCS_MCP_PORT="$(pick_port "${DOCS_MCP_PORT:-6280}")"
  nohup docs-mcp-server server --protocol http --host 127.0.0.1 --port "$DOCS_MCP_PORT" --resume \
    >"$WORKFLOW_RUN_DIR/docs-mcp-server.log" 2>&1 &
  printf '%s\n' "$DOCS_MCP_PORT" >"$WORKFLOW_RUN_DIR/docs-mcp-server.port"
fi

```

After startup, inspect the log or process table. If the service fails, show the
exact failure and use the best available fallback; do not silently continue as
if local documentation context is live.

For `docs-mcp-server`, also check `docs-mcp-server config get app.storePath`
when corpus contents matter. The active database path can vary by process and
configuration.

## Gather Codebase Context

Inspect the repository directly first. Find the repository root, relevant files,
checked-in documentation, tests, symbols, callers, and current Git state using
the repository's native tools.

Suggested starting sequence:

```bash
ROOT="$(git rev-parse --show-toplevel 2>/dev/null || pwd)"
git -C "$ROOT" status --short
rg --files "$ROOT"
rg -n "<task keywords or symbol>" "$ROOT"
git -C "$ROOT" log -n 10 --oneline -- "<relevant path>"
```

Use `claude-context` for complementary semantic search when it is available and
likely to reveal implementation details that direct inspection did not answer.
Treat indexing commands as side effects; explain their effect before running
them when they could surprise the user.

## Gather External Context

Use `docs-mcp-server` for library, framework, API, CLI, cloud, and standards
documentation whenever current external facts could affect the answer. Prefer
already indexed docs, then index or fetch primary docs when needed.

Use Exa MCP when:

- The needed source is not in `docs-mcp-server`.
- The task needs broader web discovery.
- The information is recent, niche, or not cleanly tied to one documentation
  corpus.

Prefer primary sources. Capture enough source detail to defend the decision, but
do not turn context gathering into a literature review unless the task requires
it.

## Enter Brainstorming

After the initial context-gathering pass, invoke `brainstorming`.

- In Claude Code, prefer the Skill tool: `Skill("brainstorming")`.
- If slash commands are the active interface, use `/brainstorming`.
- In Codex, load the `brainstorming` skill through the available skill mechanism
  and follow it directly.
- Ground the task in first principles before design or implementation:
  invariants, domain rules, user goals, system boundaries, failure modes,
  tradeoffs, and what "done" actually means.
- Align those first principles with the user. Ask one question at a time when
  alignment is unclear.

## Recheck Loop

At every step, clarification, correction, and new learning, ask:

- Would `docs-mcp-server` improve the external facts, API semantics, or
  compatibility assumptions?
- Would direct repository inspection or `claude-context` reveal codebase
  structure, side effects, ownership boundaries, hidden callers, or better
  implementation options?
- For visual work, should the browser view be updated before the next decision?

Use the relevant context tool when the answer could change the decision. If the
answer is clearly no, proceed and keep momentum.

## Failure Handling

- If a local service is missing, blocked, or unhealthy, report the exact command
  and log path, then use the best available fallback.
- If docs are missing from the local corpus, start the server, index or fetch the
  necessary documentation when feasible, and tell the user when indexing may
  take time.
- If `claude-context` disagrees with direct file inspection, inspect the files
  directly and treat search indexes as context, not authority.
- Never skip visual browser verification for visual claims.

## Issue writing

Whenever this workflow creates or edits issue prose, apply [the shared issue-writing contract](../issue-writing/SKILL.md). Each issue must stand on its own; its only optional document reference is its actual design proposal. Put supporting source documents and technical records in the proposal or internal workflow evidence. Validate the prepared content and provider readback, and repeat the automatic readability review after material edits. This rule creates no new issue, publication authority, or human approval.

## Pull request writing

When this workflow authors PR content, apply [the shared PR-writing contract](../pull-request-writing/SKILL.md). The description explains the change and verification on its own, and its sole optional document reference is the design proposal. Validate prepared content and provider readback automatically within existing publication authority.
