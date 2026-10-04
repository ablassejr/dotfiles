---
name: list-mcp-servers
description: Use when the user asks which MCP servers are available, configured, or connected — across Codex and Codex Desktop — or wants to see MCP connection health, scopes, or where a given server is defined.
---

# List MCP Servers

## Overview

Codex and Codex Desktop maintain **separate** MCP configurations. This skill produces one consolidated listing of both, including connection health for Codex.

Core fact: the two apps do not share config. A server present in one may be absent in the other.

## Quick Reference

| Source | Where it lives | How to read it |
|--------|----------------|----------------|
| Codex (canonical) | merged from all scopes | `Codex mcp list` |
| Codex user scope | `~/.Codex.json` → `mcpServers` | JSON |
| Codex project (shared) | `<project>/.mcp.json` | JSON |
| Codex project (local) | `~/.Codex.json` → `projects.<path>.mcpServers` | JSON |
| Codex Desktop (macOS) | `~/Library/Application Support/Codex/claude_desktop_config.json` | JSON |
| Codex Desktop (Linux) | `~/.config/Codex/claude_desktop_config.json` | JSON |
| Codex Desktop (Windows) | `%APPDATA%\Codex\claude_desktop_config.json` | JSON |

`Codex mcp list` is the source of truth for Codex: it merges user/project/local scopes **and** plugin-provided and remote Codex.ai connector MCPs, and reports per-server health (`✓ Connected`, `✗ Failed to connect`, `! Needs authentication`). The raw JSON files do NOT include plugin or connector MCPs.

## Usage

Run the bundled script — it handles both apps and all platforms:

```bash
bash list-mcps.sh
```

It prints Codex servers (via `Codex mcp list`, with health) then Codex Desktop servers (parsed from the platform-correct JSON path). If the `Codex` CLI is missing, it falls back to parsing the Codex JSON config files directly.

## Reading the Output

- **Connection status** comes only from `Codex mcp list`. The JSON files show what is *configured*, not what is *reachable*.
- **Conflicting scopes**: `Codex mcp list` warns when a server name is defined in multiple scopes with different endpoints — OAuth tokens are stored per endpoint, so auth in one scope does not carry to the other.
- A Desktop-only server (e.g. `Kafka UI`) will not appear in `Codex mcp list`, and vice versa.

## Common Mistakes

- **Assuming the configs are shared.** They are not — always read both sources.
- **Trusting JSON as the full list for Codex.** Plugin and remote connector MCPs only surface via `Codex mcp list`.
- **Hardcoding the macOS Desktop path.** Use the platform branch in the script for Linux/Windows.
