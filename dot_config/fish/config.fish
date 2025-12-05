source ~/.config/fish/conf.d/_tide_init.fish
tide configure --auto --style=Rainbow --prompt_colors='True color' --show_time='12-hour format' --rainbow_prompt_separators=Angled --powerline_prompt_heads=Round --powerline_prompt_tails=Sharp --powerline_prompt_style='Two lines, character and frame' --prompt_connection=Solid --powerline_right_prompt_frame=No --prompt_connection_andor_frame_color=Lightest --prompt_spacing=Sparse --icons='Many icons' --transient=Yes
zoxide init fish | source
mise activate fish | source

export SUDO_PASS="lpass show --password 1279211307193658237OD"
export NVIM_APPNAME="craftzdog/dotfiles-public/.config/nvim nvim"
abbr -a -g la "exa --long --sort modified --tree --level 3 | most"
abbr -a -g bashconfig "micro ~/.bashrc"
abbr -a -g zshconfig "micro ~/.zshrc"
abbr -a -g lmost "ls -la | most"
abbr -a -g mkexec "sudo -S chmod +x"
abbr -a -g jupyter-tui "source ~/.local/share/jupyter-tui/.venv/bin/activate && python ~/.local/share/jupyter-tui/main.py"
abbr -a -g savesession "hyprsession --mode save-and-exit && shutdown now"
