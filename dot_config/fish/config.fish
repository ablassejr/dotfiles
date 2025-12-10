abbr -a -g la "exa --long --tree --level 3"
abbr -a -g bashconfig "micro ~/.bashrc"
abbr -a -g zshconfig "micro ~/.zshrc"
abbr -a -g lmost "ls -la | most"
abbr -a -g mkexec "sudo -S chmod +x"
abbr -a -g jupyter-tui "source ~/.local/share/jupyter-tui/.venv/bin/activate && python ~/.local/share/jupyter-tui/main.py"
abbr -a -g savesession "hyprsession --mode save-and-exit && shutdown now"
abbr -a -g clr clear
abbr -a -g nvimc "NVIM_APPNAME=craftzdog/dotfiles-public/.config/nvim nvim"
abbr -a -g nvidec "NVIM_APPNAME=craftzdog/dotfiles-public/.config/nvim neovide"
abbr -a -g fzfrm "fzf | xargs -I {} rm {}"
abbr -a -g nvimm "NVIM_APPNAME=mimikun/dot_config/nvim nvim"
abbr -a -g nvidem "NVIM_APPNAME=mimikun/dotfiles/dot_config/nvim neovide"
abbr -a -g nvimp "NVIM_APPNAME=nvim-personal nvim"
abbr -a -g nvidep "NVIM_APPNAME=nvim-personal neovide"
abbr -a -g releasesudo "faillock --user $(whoami) --reset"
abbr -a -g nvide neovide

if test -d "~/.config/mimikun"
    gh repo clone mimikun/dotfiles ~/.config/mimikun/dotfiles
end

if test -d "~/.config/craftzdog/dotfiles-public/"
    gh repo clone craftzdog/dotfiles-public ~/.config/craftzdog/dotfiles-public
end

#source ~/.config/fish/conf.d/_tide_init.fish
mise activate fish | source
zoxide init fish | source

command clear
