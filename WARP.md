# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a **chezmoi dotfiles repository** targeting macOS on Apple Silicon and Intel. It keeps
a MacBook and a Mac mini on the same development environment. Files prefixed with `dot_`
represent dotfiles in the home directory (`dot_bashrc` → `~/.bashrc`).

`AGENTS.md`, `WARP.md`, `README.md`, and `Brewfile` are repository tooling. `.chezmoiignore`
excludes them, so they are never rendered into the home directory.

## Key Concepts

### Chezmoi Architecture
- **Source state**: Files in this repo (`~/.local/share/chezmoi`)
- **Target state**: What chezmoi wants your home directory to look like
- **Destination state**: Current state of your home directory
- Chezmoi transforms source → target using special prefixes and templates

### File Naming Conventions
- `dot_` prefix → `.` (dotfile)
- `dot_config/nvim/` → `~/.config/nvim/`
- `.tmpl` suffix → rendered as a Go template
- `encrypted_` → age-encrypted at rest in the repository
- `private_` → target file gets mode `0600`
- Prefix order for a regular file: `encrypted_`, `private_`, `readonly_`, `empty_`,
  `executable_`, `dot_`
- Files listed in `.chezmoiignore` are not applied to the destination

## Essential Commands

### Daily Workflow
```bash
# Edit a managed file (opens in source directory)
chezmoi edit ~/.bashrc
# Shorthand alias
ce ~/.bashrc

# View differences before applying
chezmoi diff

# Apply changes to home directory
chezmoi apply
# Shorthand alias
ca

# Edit and apply in one step
chezmoi edit --apply ~/.zshrc

# Edit the encrypted secrets file (decrypts, opens editor, re-encrypts)
chezmoi edit ~/.zshenv

# Add a new file to chezmoi management
chezmoi add ~/.config/newfile.conf

# Check what chezmoi would do
chezmoi status
```

## Post-Edit Memory and Signature Reporting

After completing any request that edits files:

- Persist a concise memory of the completed changes and verification in `claude-mem` when available; otherwise use the agent platform's native memory. Never store secrets, credentials, tokens, or other sensitive data in memory.
- In the final user-facing response, include a `Signature changes` section listing every function, method, named object, class, type, interface, and enum added, removed, or modified by that request. Include each file path and the declaration signature; for changed declarations, show `before -> after` when both are available. Include entities whose bodies changed even if their declaration signature did not.
- If no such code signatures changed, explicitly write `Signature changes: none`.


## Human-Readable Pseudocode for Ideas

When proposing, comparing, or explaining an idea, design, workflow, algorithm, architecture, or behavioral change, present it using human-readable, comprehensive, maximally descriptive pseudocode to improve shared understanding and alignment.

- Write for people first: use plain language, descriptive names, and explicit steps instead of language-specific syntax, abbreviations, or clever shorthand.
- Make the pseudocode complete enough to expose the relevant actors, prerequisites, inputs, outputs, state changes, decision branches, loops or concurrency, side effects, integrations, failure paths, recovery behavior, invariants, and success criteria.
- Clearly distinguish current verified behavior, proposed behavior, assumptions, and unresolved choices. Never present pseudocode as implemented or verified code.
- Scale the pseudocode to the idea, but do not omit material branches, edge cases, or tradeoffs merely for brevity.

## Behavior-Only Testing

Test observable behavior and declared contracts only. Never test implementation details, including in regression tests. This applies to unit, regression, integration, contract, end-to-end, and every other kind of test.

- Assert positive outcomes at the closest stable public or user-visible boundary, such as returned values, emitted events, rendered output, persisted state, external protocol behavior, or documented errors.
- Do not assert private helpers or state, internal call order or counts, specific internal collaborators, incidental data structures, source text or code patterns, or any other mechanism that can change without changing behavior.
- Mock or fake only true external boundaries and nondeterministic dependencies. Do not mock the internal worker, helper, or unit whose behavior the test is meant to prove.
- Whenever a request touches code or tests, inspect all request-relevant existing tests for violations of this rule. Refactor violating tests in place as part of the same request, preserving or strengthening their intended behavioral coverage without expanding into unrelated tests.
- For regressions, reproduce the externally observable failure and assert the intended positive contract. Use negative assertions only when absence is itself an externally observable requirement.
- If behavior cannot be observed at a stable boundary, improve the production seam or test harness rather than coupling the test to implementation.

### Advanced Operations
```bash
# Re-add a file (updates source with destination changes)
chezmoi re-add ~/.bashrc

# Open a shell in the source directory
chezmoi cd

# Run git commands in the source directory
chezmoi git -- status

# Remove a file from chezmoi management
chezmoi forget ~/.config/oldfile

# See what's managed
chezmoi managed

# See what's not managed
chezmoi unmanaged

# Verify destination matches target state
chezmoi verify

# Update from remote and apply
chezmoi update

# Check for common issues
chezmoi doctor
```

### Quick Aliases
```bash
ce  # chezmoi edit
ca  # chezmoi apply
```

## Configuration Structure

### Shell Configurations
- **Zsh**: `dot_zprofile` carries the interactive setup — zinit, Powerlevel10k,
  compinit, fzf key bindings, zsh-autosuggestions, zsh-syntax-highlighting, and the
  alias set. `dot_zshrc` sources `~/.zprofile` for non-login shells.
- **Bash**: `dot_bashrc`, `dot_bash_profile` — a minimal alias set plus zoxide and mise.
- **Common**: `dot_profile` — POSIX PATH construction shared by both shells. Every
  entry is added through `path_prepend`/`path_append`, which skip directories that do
  not exist, so one file serves both Homebrew prefixes.
- **Secrets**: `encrypted_private_dot_zshenv.age` → `~/.zshenv` at mode `0600`.

### Terminal Emulator
- **Ghostty**: `dot_config/ghostty/config`

### Editor
- **Neovim**: `dot_config/nvim/` (git submodule, LazyVim-based) and
  `dot_config/nvim-personal/` for the `NVIM_APPNAME=nvim-personal` profile

### Version Control
- **Git**: `dot_gitconfig` → `~/.gitconfig`, the single global config
  - GitHub CLI credential helper, resolved from `PATH`
  - Default branch: `main`; pull strategy merge (`rebase = false`)
  - `core.pager = bat`, diff/merge tool `differ`, git-lfs filters
  - `.chezmoiremove` retires `~/.config/git/config`, which git would otherwise
    still read at lower precedence
- **Ignore rules**: `dot_config/git/ignore` → `~/.config/git/ignore`

### Development Tools
- **Mise**: version management, shims on PATH
- **Zoxide**: directory jumping, initialized in `.zprofile` and `.bashrc`
- **Tmux**: `dot_tmux.conf` — prefix `Ctrl-a`, mouse support, vi-style navigation

## Machine Portability

- `.chezmoi.toml.tmpl` generates `~/.config/chezmoi/chezmoi.toml` on `chezmoi init`,
  wiring up age encryption. The age identity (`key.txt`) is deliberately not in this
  repository and must be copied to a new machine out of band.
- `.chezmoiversion` pins the minimum chezmoi version so both machines resolve the
  source state identically.
- `dot_claude/settings.json.tmpl` derives absolute paths from `.chezmoi.homeDir`.
- `Brewfile` is the package manifest. `brew bundle --file=Brewfile` brings a machine
  up to the same tool set; `brew bundle check --file=Brewfile` reports drift.

## Machine-Specific Exclusions

Excluded via `.chezmoiignore`:
- Repository tooling (`AGENTS.md`, `WARP.md`, `README.md`, `Brewfile`)
- SSH keys and known_hosts
- Local environment files (`.env`, `.env.local`)
- Claude Code local settings (`.claude/settings.local.json`)
- Reference clones under `.config/craftzdog/` and `.config/mimikun/`
- Cache and temporary files

## Workflow Patterns

### Making Changes
```bash
chezmoi edit ~/.zprofile
chezmoi diff
chezmoi apply
```

### Pulling Updates from Another Machine
```bash
chezmoi update
```

### Adding New Configs
```bash
# Add existing file from home directory
chezmoi add ~/.config/tool/config

# Add a file containing secrets
chezmoi add --encrypt ~/.config/tool/credentials

# Edit the newly added file
chezmoi edit ~/.config/tool/config
```

## Important Notes

### Path Management
`dot_profile` builds PATH. `/usr/local` is prepended before `/opt/homebrew` so the
Apple Silicon prefix wins when both exist. `/opt/local` (MacPorts) is prepended after
Homebrew, so MacPorts binaries shadow Homebrew ones where both provide a command.

### Fonts
Ghostty uses `AdwaitaMono Nerd Font`. Both it and `JetBrainsMono Nerd Font` are
listed in the `Brewfile` as casks.

### Git Workflow
```bash
chezmoi git -- add -A
chezmoi git -- commit -m "Update configs"
chezmoi git -- push
```

## Testing Changes

```bash
# See what would change
chezmoi diff

# Dry run to check for errors
chezmoi apply --dry-run --verbose

# Verify everything is correct
chezmoi verify

# Shell syntax
zsh -n dot_zprofile && zsh -n dot_zshrc && zsh -n dot_profile
bash -n dot_bashrc && bash -n dot_bash_profile

# Terminal and multiplexer configs
ghostty +validate-config --config-file=dot_config/ghostty/config
tmux -f dot_tmux.conf -L test new-session -d && tmux -L test kill-server
```

## Troubleshooting

```bash
# Check for common issues
chezmoi doctor

# Verify git repo state
chezmoi git -- status

# Force re-apply everything
chezmoi apply --force

# Check what chezmoi sees as different
chezmoi status
```
