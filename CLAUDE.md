# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This is a **chezmoi-managed dotfiles repository** for managing shell configuration files across systems. The repository contains configuration for multiple shells (Bash and Zsh) and terminal tools.

## Chezmoi Naming Convention

Files in this repository use chezmoi's naming convention:
- `dot_` prefix → becomes `.` (hidden file)
- Examples:
  - `dot_bashrc` → `~/.bashrc`
  - `dot_zshrc` → `~/.zshrc`
  - `dot_tmux.conf` → `~/.tmux.conf`

## Key Commands

### Testing Changes
```bash
# Preview what chezmoi would do (dry-run)
chezmoi diff

# Apply changes to home directory
chezmoi apply

# Apply specific file
chezmoi apply ~/.zshrc
```

### Managing Dotfiles
```bash
# Add a new file to chezmoi
chezmoi add ~/.config/newfile

# Edit a file (opens in editor, then prompts to apply)
chezmoi edit ~/.bashrc

# Re-add an existing file (after manual edits)
chezmoi re-add ~/.zshrc
```

### Repository Operations
```bash
# Check chezmoi status
chezmoi status

# Pull and apply latest changes
chezmoi update

# Initialize chezmoi on a new system
chezmoi init --apply https://github.com/ablassejr/dotfiles.git
```

## Architecture

### Shell Configuration Files

**Bash Setup:**
- `dot_bash_profile` - Bash login shell configuration, sources .bashrc
- `dot_bashrc` - Main Bash configuration with:
  - oh-my-bash framework (theme: "developer")
  - blesh (Bash Line Editor)
  - zoxide integration (smart directory jumping)
  - Completions: git, chezmoi, gh, npm, pip, maven, ssh
  - Plugins: git, bashmarks
- `dot_profile` - Generic shell profile with PATH and aliases
  - JetBrains Toolbox scripts in PATH
  - Custom aliases: `bashconfig`, `lmost`, `la`, `cmx`

**Zsh Setup:**
- `dot_zshrc` - Main Zsh configuration with:
  - zinit plugin manager
  - powerlevel10k theme
  - Plugins: syntax-highlighting, autosuggestions, completions, fzf-tab, z (directory jumper), git helpers, colored-man-pages, autopair
  - Editor: nvim
  - fzf integration
  - Git aliases: `gs`, `ga`, `gc`, `gp`
  - ls aliases: `ll`, `la`

**Tmux:**
- `dot_tmux.conf` - Tmux configuration with custom key bindings:
  - `|` for horizontal split
  - `-` for vertical split

### Tool Dependencies

The configurations depend on these tools being installed:
- **zinit** (Zsh plugin manager) - auto-installed if missing
- **oh-my-bash** - expected at `~/.oh-my-bash`
- **blesh** - expected at `~/.local/share/blesh/ble.sh`
- **zoxide** - directory jumping tool
- **fzf** - fuzzy finder
- **nvim** - default editor
- **mise** - version manager (shims in PATH)
- **powerlevel10k** - Zsh theme config at `~/.p10k.zsh`

## Important Workflows

### Adding New Configuration Files
When adding new dotfiles to this repository:
1. Place the actual file in your home directory first
2. Use `chezmoi add <filepath>` to import it
3. The file will appear with chezmoi naming (e.g., `dot_filename`)
4. Commit and push the changes to this repository

### Modifying Existing Files
**Option 1 (Recommended):**
```bash
# Edit through chezmoi (maintains consistency)
chezmoi edit ~/.bashrc
# Review changes
chezmoi diff
# Apply changes
chezmoi apply
```

**Option 2:**
1. Edit files directly in this repository
2. Test with `chezmoi diff`
3. Apply with `chezmoi apply`

**Option 3:**
1. Edit the actual dotfile in home directory
2. Use `chezmoi re-add ~/.filename` to sync back to repository
3. Commit changes

### Deploying to New System
```bash
# One-command setup
chezmoi init --apply https://github.com/ablassejr/dotfiles.git

# This will:
# 1. Clone the repo to ~/.local/share/chezmoi
# 2. Apply all dotfiles to home directory
# 3. Note: External dependencies (zinit, oh-my-bash, etc.) may need manual installation
```
