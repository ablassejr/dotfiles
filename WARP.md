# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Repository Overview

This is a **chezmoi dotfiles repository** that manages configuration files across machines. The repository uses chezmoi's naming conventions where files prefixed with `dot_` represent dotfiles in the home directory (e.g., `dot_bashrc` → `~/.bashrc`).

## Key Concepts

### Chezmoi Architecture
- **Source state**: Files in this repo (`~/.local/share/chezmoi`)
- **Target state**: What chezmoi wants your home directory to look like
- **Destination state**: Current state of your home directory
- Chezmoi transforms source → target using special prefixes and templates

### File Naming Conventions
- `dot_` prefix → `.` (dotfile)
- `dot_config/nvim/` → `~/.config/nvim/`
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

# Add a new file to chezmoi management
chezmoi add ~/.config/newfile.conf

# Check what chezmoi would do
chezmoi status
```

### Advanced Operations
```bash
# Re-add a file (updates source with destination changes)
chezmoi re-add ~/.bashrc

# Open a shell in the source directory
chezmoi cd

# Run git commands in the source directory
chezmoi git -- log
chezmoi git -- status

# Remove a file from chezmoi management
chezmoi forget ~/.unwanted_config

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
gmp # git magic -apm (custom git alias)
```

## Configuration Structure

### Shell Configurations
- **Bash**: `dot_bashrc`, `dot_bash_profile`
  - Uses oh-my-bash framework
  - Integrates ble.sh for enhanced line editing
  - Skips fancy shell features when running in Warp (via `SKIP_OMB_BLESH`)
- **Zsh**: `dot_zshrc`
  - Uses zinit plugin manager
  - Powerlevel10k theme
  - Auto-installs oh-my-zsh if missing
- **Common**: `dot_profile` (sourced by both shells)
  - Contains zoxide configuration
  - Shared environment setup

### Terminal Emulators
- **Ghostty**: `dot_config/ghostty/config`
- **Kitty**: `dot_config/kitty/kitty.conf`

### Window Manager
- **Hyprland**: `dot_config/hypr/bindings.conf`
  - Uses Omarchy framework bindings
  - Machine-specific configs (monitors, nvidia, startup) are in `.chezmoiignore`

### Editors
- **Neovim**: `dot_config/nvim/`
  - LazyVim-based configuration
  - Plugins in `lua/plugins/`
  - Config in `lua/config/`
- **Micro**: `dot_config/micro/`
  - Lightweight text editor

### Version Control
- **Git**: `dot_config/git/config`
  - GitHub CLI credential helper configured
  - Default branch: `main`
  - Pull strategy: rebase

### Development Tools
- **Mise**: Configured for version management (shims in PATH)
- **Zoxide**: Smart directory jumping (initialized in `.profile`)
- **Tmux**: `dot_tmux.conf`
  - Prefix: `Ctrl-a`
  - Mouse support enabled
  - Vim-style navigation

## Machine-Specific Exclusions

The following are excluded via `.chezmoiignore` (won't be applied):
- Hyprland system-specific configs (monitors.conf, nvidia.conf, etc.)
- SSH keys and known_hosts
- Local environment files (.env, .env.local)
- Editor runtime files (micro buffers/backups)
- Cache and temporary files

## Workflow Patterns

### Making Changes
1. Edit files directly: `chezmoi edit <file>` or edit in `~/.local/share/chezmoi`
2. Preview changes: `chezmoi diff`
3. Apply changes: `chezmoi apply`
4. Commit to git: `chezmoi git -- add . && chezmoi git -- commit -m "message"`

### Pulling Updates from Another Machine
```bash
chezmoi update  # Pulls from git and applies
```

### Adding New Configs
```bash
# Add existing file from home directory
chezmoi add ~/.config/newapp/config

# Edit the newly added file
chezmoi edit ~/.config/newapp/config
```

## Important Notes

### Warp Terminal Integration
Both shell configs detect Warp via `$TERM_PROGRAM` and disable oh-my-bash/ble.sh features that conflict with Warp's native features.

### Path Management
Multiple tools add to PATH:
- mise shims for version management
- JetBrains Toolbox scripts
- Local bin directories (~/.local/bin)
- cargo/rust binaries

### Font Preferences
- Primary: Iosevka (user prefers this)
- Alternative: JetBrains Mono Nerd Font
- Neovide as preferred editor

### Git Workflow
The repository uses automatic commits via `chezmoi update` or manual commits through:
```bash
chezmoi git -- add -A
chezmoi git -- commit -m "Update configs"
chezmoi git -- push
```

The `gmp` alias exists for "git magic" operations (custom tool).

## Testing Changes

Before applying system-wide:
```bash
# See what would change
chezmoi diff

# Dry run to check for errors
chezmoi apply --dry-run --verbose

# Verify everything is correct
chezmoi verify
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
