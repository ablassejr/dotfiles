---
name: memory-recall
description: "Search and recall relevant memories from past sessions via Claude Mem. Use when the user's question could benefit from historical context, past decisions, debugging notes, previous conversations, or project knowledge -- especially questions like 'what did I decide about X', 'why did we do Y', or 'have I seen this before'. Also use when a `<claude-mem-context>` block says more detail is available through memory search. Skip when the question is purely about current code state, ephemeral, or the user explicitly asks to ignore memory."
---

# Memory Recall with Claude Mem

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


Search Claude Mem's persistent cross-session observation database and return
only context that materially helps with the current request.

Do not use MemSearch or Milvus for this skill.

## Preferred Tool Flow

Use tool discovery for `Claude Mem search observations timeline
get_observations`, then follow Claude Mem's three-layer workflow:

1. **Search**: Call Claude Mem's `search` tool with a focused query, normally
   `limit=20`, and a project filter when the current project is known.
2. **Filter and orient**: Review the compact result titles. Use `timeline` for
   the most relevant result when surrounding chronology would change the
   interpretation.
3. **Fetch**: Call `get_observations` only for the relevant IDs. Batch all
   selected IDs into one call.

Never fetch full observations before filtering the search index.

## Local Worker Fallback

If Claude Mem's MCP tools are not exposed, use the installed local worker rather
than falling back to another memory backend.

When plugin registration is needed, run the bundled `bash scripts/install-claude-mem.sh` installer. It registers the plugin and worker with the host provider, without opting into hosted memory sign-in. Restart the host and confirm its native memory tools before use.

Use the plugin root reported by the installer or the host’s plugin inventory. The standard Claude marketplace location is:

```bash
CLAUDE_MEM_PLUGIN="${CLAUDE_MEM_PLUGIN:-$HOME/.claude/plugins/marketplaces/thedotmack/plugin}"
```

Start or reuse the worker:

```bash
node "$CLAUDE_MEM_PLUGIN/scripts/bun-runner.js" \
  "$CLAUDE_MEM_PLUGIN/scripts/worker-service.cjs" start
```

Resolve its port from `~/.claude-mem/settings.json` when present; otherwise use
Claude Mem's per-user default:

```bash
PORT="$(jq -r '.CLAUDE_MEM_WORKER_PORT // empty' \
  "$HOME/.claude-mem/settings.json" 2>/dev/null)"
: "${PORT:=$((37700 + $(id -u) % 100))}"
```

Use the worker endpoints in the same search-filter-fetch order:

```bash
curl -fsSG "http://127.0.0.1:$PORT/api/search" \
  --data-urlencode "query=<focused query>" \
  --data-urlencode "limit=20"

curl -fsSG "http://127.0.0.1:$PORT/api/timeline" \
  --data-urlencode "anchor=<observation id>" \
  --data-urlencode "depth_before=3" \
  --data-urlencode "depth_after=3"

curl -fsS -X POST "http://127.0.0.1:$PORT/api/observations/batch" \
  -H 'content-type: application/json' \
  --data '{"ids":[<filtered observation ids>]}'
```

If the worker cannot start or the Claude Mem database is empty, say so briefly
and continue from direct source-of-truth files instead of substituting Milvus.

## Output

Summarize only the retrieved decisions, patterns, fixes, or constraints that are
useful now. Include observation IDs and dates for traceability. Clearly label
anything that may be stale, and verify drift-prone facts against current source
state when that is cheap.
