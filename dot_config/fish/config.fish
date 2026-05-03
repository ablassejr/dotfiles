abbr -a -g la "eza --long --tree --level 3"
abbr -a -g ll "ls -lh"
abbr -a -g gs "git status"
abbr -a -g ga "git add"
abbr -a -g gc "git commit"
abbr -a -g gp "git push"
abbr -a -g ce "chezmoi edit"
abbr -a -g ca "chezmoi apply"
abbr -a -g clr clear
abbr -a -g nvimp "NVIM_APPNAME=nvim-personal nvim"
abbr -a -g nvidep "NVIM_APPNAME=nvim-personal neovide"
abbr -a -g nvide neovide
abbr -a -g tm task-master
abbr -a -g taskmaster task-master
abbr -a -g oc opencode

fish_add_path --path $HOME/.local/bin
fish_add_path --path $HOME/.cargo/bin
fish_add_path --path $HOME/.bun/bin
fish_add_path --path $HOME/.opencode/bin
fish_add_path --path /opt/homebrew/bin /opt/homebrew/sbin
fish_add_path --append --path /Library/TeX/texbin

if command -q mise
    mise activate fish | source
end

if command -q zoxide
    zoxide init fish | source
end
