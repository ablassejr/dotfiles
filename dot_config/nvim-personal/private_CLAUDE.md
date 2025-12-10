# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Personal Neovim configuration using lazy.nvim as the plugin manager. Plugins are organized as one file per plugin in `lua/plugins/`.

## Architecture

### Directory Structure

```
init.lua                    # Entry point - loads config modules
lua/config/
  ├── options.lua           # Vim options (line numbers, leader key)
  ├── lazy.lua              # lazy.nvim bootstrap and setup
  ├── keymaps.lua           # Key mappings (currently minimal)
  └── autocmds.lua          # Autocommands (yank highlight, last location, etc.)
lua/plugins/
  └── *.lua                 # One file per plugin (auto-imported by lazy.nvim)
.claude/
  ├── agents/               # Specialized Claude Code agents
  └── commands/             # Custom slash commands
```

### Loading Order

1. `config/options` - Sets vim options and leader key (Space)
2. `config/lazy` - Bootstraps lazy.nvim, imports all `plugins/*.lua`
3. `config/keymaps` - Key mappings
4. `config/autocmds` - Autocommands

### Plugin File Pattern

Each plugin is a separate file returning a single spec table:

```lua
-- lua/plugins/example.nvim.lua
return {
    "author/plugin-name",
    dependencies = { "dep/plugin" },
    event = "VeryLazy",  -- or "BufReadPost", etc.
    opts = { ... }
}
```

## Key Plugins

| Plugin | Purpose |
|--------|---------|
| snacks.nvim | Dashboard, explorer, picker, notifications, scroll, indent |
| telescope.nvim | Fuzzy finder |
| flash.nvim | Motion/navigation |
| treesitter | Syntax highlighting |
| mason.nvim | LSP server management |
| conform.nvim | Formatting |
| trouble.nvim | Diagnostics list |
| nvim-dap | Debugging |
| gitsigns, diffview, vgit | Git integration |
| claude-code.nvim, VectorCode | AI integration |

## Adding a Plugin

1. Create `lua/plugins/<plugin-name>.lua`
2. Return a lazy.nvim spec table
3. Use lazy loading (`event`, `cmd`, `ft`) when possible

## Claude Code Integration

- `/ultra-think` - Deep analysis slash command for complex problems
- `.claude/agents/` - backend-architect, python-pro, search-specialist agents
- `.mcp.json` - MCP servers (context7, memory, playwright, etc.)
