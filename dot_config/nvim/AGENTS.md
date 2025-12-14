# Repository Guidelines

Use this guide to keep contributions consistent with the existing LazyVim-based Neovim setup.

## Project Structure & Module Organization
- Entry point `init.lua` loads `lua/config/lazy.lua`, which bootstraps LazyVim and all plugin specs.
- Core settings live in `lua/config/`: `options.lua` (editor defaults), `keymaps.lua`, and `autocmds.lua`.
- Plugin specs sit in `lua/plugins/*.lua`; each file returns a Lazy plugin table and is auto-discovered.
- Version and extras metadata are in `lazy-lock.json` (pinned plugin commits) and `lazyvim.json`; keep them in sync with plugin changes.
- Formatting rules are configured in `stylua.toml`; reference snippets and tips in `neovim_tips/`.

## Build, Test, and Development Commands
- Launch locally with `nvim` (uses this config in `~/.config/nvim`).
- Install/update plugins: inside Neovim run `:Lazy sync`; check for updates with `:Lazy check`; remove orphans with `:Lazy clean`.
- Ensure external tooling via `:Mason` and install required tools (e.g., `stylua`, `shellcheck`) from the UI.
- Format Lua before committing: `stylua .`.
- Quick headless sanity check (respects lockfile): `nvim --headless "+Lazy! sync" +qa`.

## Coding Style & Naming Conventions
- Lua: 2-space indentation, 120-column soft limit, spaces not tabs (enforced by `stylua`).
- Keep plugin spec files kebab-cased and descriptive, e.g., `nvim-dap-view.lua` or `vectorcode-lualine.lua`.
- Prefer `local` bindings, minimal globals, and small composable `opts` functions for overrides.
- Keymaps and autocmds belong in `lua/config/`; avoid defining them inside multiple plugin specs unless scoped to that plugin.

## Testing Guidelines
- No automated test suite; validate changes by launching Neovim and exercising affected plugins or keymaps.
- For plugin additions, run the headless `Lazy! sync` above, then open Neovim and verify `:checkhealth` for relevant providers.
- When modifying defaults, document a minimal reproduction note in the PR to explain how to observe the change.

## Commit & Pull Request Guidelines
- Follow the existing log style: short, imperative messages with optional prefix, e.g., `fix: disable lazy checker notify`.
- Commit related files together; include `lazy-lock.json` when plugin versions change.
- PRs should explain the intent, list manual checks performed (`stylua`, `Lazy sync`, `checkhealth`), and note any user-facing keymap or option changes.
- Add screenshots or short notes when altering UI-facing plugins (statusline, incline, hover, etc.).

## Security & Configuration Tips
- Do not commit personal tokens or machine-specific paths; prefer env-driven settings when configuring tools.
- When experimenting, keep local-only tweaks in a separate plugin spec excluded from commits or guarded by `if vim.env.USER == ...` checks.
