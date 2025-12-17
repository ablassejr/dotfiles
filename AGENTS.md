# Repository Guidelines

This repository contains personal dotfiles managed with `chezmoi`. Source files live here and are rendered into your home directory (e.g., `dot_zshrc` → `~/.zshrc`, `dot_config/nvim/` → `~/.config/nvim/`).

## Project Structure & Module Organization

- Shell: `dot_zshrc`, `dot_bashrc`, `dot_profile` (login/interactive configuration).
- Terminal tools: `dot_tmux.conf`.
- App configs: `dot_config/**` (e.g., `dot_config/ghostty/`, `dot_config/kitty/`, `dot_config/nvim/`).
- Repo-specific guidance: deeper trees may include their own `AGENTS.md` (for Neovim see `dot_config/nvim/AGENTS.md`).

## Build, Test, and Development Commands

Run these from the repo root (`~/.local/share/chezmoi`):

- Preview changes: `chezmoi -S . diff`
- Apply changes: `chezmoi -S . apply`
- One-file edit flow: `chezmoi edit ~/.zshrc` (then `chezmoi apply`)
- Check what’s managed: `chezmoi managed`

## Coding Style & Naming Conventions

- Keep configs OS-appropriate (avoid hardcoded Linux paths in macOS-targeted files).
- Prefer guarded/conditional logic in shell configs (e.g., `command -v brew >/dev/null && …`).
- Indentation: 2 spaces for shell/Lua configs unless the file’s existing style differs.
- Naming: use chezmoi conventions (`dot_*`, `dot_config/<app>/…`) and keep new app configs grouped under `dot_config/<app>/`.

## Testing Guidelines

No automated suite; do quick smoke checks after applying:

- Zsh parse: `zsh -n ~/.zshrc`
- Tmux config: `tmux -f ~/.tmux.conf -L test new -d \; kill-server`
- Neovim config: follow `dot_config/nvim/AGENTS.md`

## Commit & Pull Request Guidelines

- Commit messages in history are short and imperative (commonly `Add …` / `Update …`, occasionally `fix:`). Follow that style and keep messages focused on the primary change.
- Don’t commit machine-local artifacts (e.g., `.DS_Store`, caches, history files).
- PRs: describe intent, list the smoke checks run, and call out any user-visible behavior changes (prompt, keybindings, themes).

## Security & Configuration Tips

- Never commit secrets; prefer `~/.env` (ignored/unmanaged) or environment variables.
- Avoid network actions during shell startup (no `git clone`/auto-install in `dot_zshrc`).
