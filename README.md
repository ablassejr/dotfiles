# dotfiles

Personal macOS dotfiles managed with [chezmoi](https://www.chezmoi.io), shared between a
MacBook and a Mac mini. Apple Silicon and Intel are both supported; there is no Linux
support and none should be added.

> **This repository is public.** Everything committed here is world-readable and remains
> in the git history after deletion. Secrets belong in the age-encrypted
> `encrypted_private_dot_zshenv.age`, never in a plaintext source file.

## Setting up a machine

Copy the age identity across first — it is deliberately not in this repository, and
without it chezmoi cannot decrypt `~/.zshenv`:

```bash
mkdir -p ~/.config/chezmoi
scp <other-mac>:~/.config/chezmoi/key.txt ~/.config/chezmoi/key.txt
chmod 600 ~/.config/chezmoi/key.txt
```

Install chezmoi and pull the dotfiles. `chezmoi init` renders `.chezmoi.toml.tmpl` into
`~/.config/chezmoi/chezmoi.toml`, which wires up age encryption:

```bash
brew install chezmoi
chezmoi init --apply https://github.com/ablassejr/dotfiles.git
```

Install the tools the configs expect:

```bash
brew bundle --file="$(chezmoi source-path)/Brewfile"
```

## Keeping the two machines in sync

```bash
chezmoi update                                        # pull and apply dotfiles
brew bundle check --file="$(chezmoi source-path)/Brewfile"   # report package drift
brew bundle --file="$(chezmoi source-path)/Brewfile"         # install what is missing
```

After changing packages on one machine, refresh the manifest and commit it:

```bash
brew bundle dump --file="$(chezmoi source-path)/Brewfile" --force
```

## Layout

| Path | Target | Notes |
| --- | --- | --- |
| `dot_profile` | `~/.profile` | PATH construction shared by all shells |
| `dot_zprofile` | `~/.zprofile` | Interactive zsh: zinit, Powerlevel10k, aliases |
| `dot_zshrc` | `~/.zshrc` | Sources `~/.zprofile` for non-login shells |
| `dot_bashrc`, `dot_bash_profile` | `~/.bashrc`, `~/.bash_profile` | Minimal bash setup |
| `encrypted_private_dot_zshenv.age` | `~/.zshenv` (mode `0600`) | Environment secrets |
| `dot_tmux.conf` | `~/.tmux.conf` | Prefix `Ctrl-a` |
| `dot_config/ghostty/` | `~/.config/ghostty/` | Terminal |
| `dot_gitconfig` | `~/.gitconfig` | Entire global git config (wins over the XDG file) |
| `dot_config/git/ignore` | `~/.config/git/ignore` | Default `core.excludesFile` |
| `dot_config/mise/config.toml` | `~/.config/mise/config.toml` | Global toolchain pins |
| `encrypted_private_mise.toml.age` | `~/mise.toml` (`0600`) | Home-scoped mise env secrets |
| `dot_p10k.zsh` | `~/.p10k.zsh` | Powerlevel10k prompt |
| `private_dot_ssh/private_config` | `~/.ssh/config` (`0600`) | SSH hosts (keys excluded) |
| `dot_codex/`, `dot_config/opencode/`, `dot_config/zed/` | respective | Agent/editor configs, encrypted where they hold keys |
| `dot_config/nvim/` | `~/.config/nvim/` | Git submodule, LazyVim-based |
| `dot_config/nvim-personal/` | `~/.config/nvim-personal/` | `NVIM_APPNAME=nvim-personal` profile |
| `dot_claude/` | `~/.claude/` | Claude Code settings, agents, skills, hooks, statusline |

`AGENTS.md`, `WARP.md`, `README.md`, and `Brewfile` are repository tooling and are
excluded from the home directory by `.chezmoiignore`.

## Editing

```bash
chezmoi edit ~/.zprofile     # edit a managed file
chezmoi edit ~/.zshenv       # decrypts, opens editor, re-encrypts
chezmoi diff                 # preview
chezmoi apply                # write to the home directory
```

Because `dot_config/nvim` is a submodule, changes there are committed to
[`ablassejr/nvim`](https://github.com/ablassejr/nvim) and the submodule pointer is
updated here.
