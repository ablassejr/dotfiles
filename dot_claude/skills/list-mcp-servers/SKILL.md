---
name: list-mcp-servers
description: Use when the user asks which MCP servers are available, configured, or connected — across Claude Code and Claude Desktop — or wants to see MCP connection health, scopes, or where a given server is defined.
---

# List MCP Servers

## Self-contained utility setup

Use [the bundled setup instructions](references/setup.md) and [dependency manifest](dependencies.json) when this workflow needs a utility. Check availability first; the skill’s scripts install selected missing tools without relying on another skill’s setup files. Optional media, engine operations, and repository-specific toolchains are selected for the actual task. Existing session permissions and account configuration still apply.


## Overview

Claude Code and Claude Desktop maintain **separate** MCP configurations. This skill produces one consolidated listing of both, including connection health for Claude Code.

Core fact: the two apps do not share config. A server present in one may be absent in the other.

## Quick Reference

| Source | Where it lives | How to read it |
|--------|----------------|----------------|
| Claude Code (canonical) | merged from all scopes | `claude mcp list` |
| Claude Code user scope | `~/.claude.json` → `mcpServers` | JSON |
| Claude Code project (shared) | `<project>/.mcp.json` | JSON |
| Claude Code project (local) | `~/.claude.json` → `projects.<path>.mcpServers` | JSON |
| Claude Desktop (macOS) | `~/Library/Application Support/Claude/claude_desktop_config.json` | JSON |
| Claude Desktop (Linux) | `~/.config/Claude/claude_desktop_config.json` | JSON |
| Claude Desktop (Windows) | `%APPDATA%\Claude\claude_desktop_config.json` | JSON |

`claude mcp list` is the source of truth for Claude Code: it merges user/project/local scopes **and** plugin-provided and remote claude.ai connector MCPs, and reports per-server health (`✓ Connected`, `✗ Failed to connect`, `! Needs authentication`). The raw JSON files do NOT include plugin or connector MCPs.

## Usage

Run the bundled script — it handles both apps and all platforms:

```bash
bash list-mcps.sh
```

It prints Claude Code servers (via `claude mcp list`, with health) then Claude Desktop servers (parsed from the platform-correct JSON path). If the `claude` CLI is missing, it falls back to parsing the Claude Code JSON config files directly.

## Reading the Output

- **Connection status** comes only from `claude mcp list`. The JSON files show what is *configured*, not what is *reachable*.
- **Conflicting scopes**: `claude mcp list` warns when a server name is defined in multiple scopes with different endpoints — OAuth tokens are stored per endpoint, so auth in one scope does not carry to the other.
- A Desktop-only server (e.g. `Kafka UI`) will not appear in `claude mcp list`, and vice versa.

## Common Mistakes

- **Assuming the configs are shared.** They are not — always read both sources.
- **Trusting JSON as the full list for Claude Code.** Plugin and remote connector MCPs only surface via `claude mcp list`.
- **Hardcoding the macOS Desktop path.** Use the platform branch in the script for Linux/Windows.
