-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

-- Python provider for remote plugins (molten.nvim)
vim.g.python3_host_prog = "/home/draogo/.local/share/mise/shims/python3"

-- Line numbers
vim.opt.relativenumber = true
vim.opt.number = true

-- Performance
vim.opt.updatetime = 10000 -- 10 seconds for autosave
vim.opt.timeoutlen = 300
vim.opt.lazyredraw = false

-- Better editing experience
vim.opt.expandtab = true
vim.opt.shiftwidth = 2
vim.opt.tabstop = 2
vim.opt.softtabstop = 2
vim.opt.smartindent = true
vim.opt.wrap = false

-- Search
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- UI
vim.opt.cursorline = true
vim.opt.scrolloff = 8
vim.opt.sidescrolloff = 8
vim.opt.signcolumn = "yes"

-- Font and ligatures
vim.opt.guifont = "JetBrainsMono Nerd Font:h12"

-- Performance: reduce redraws
vim.opt.redrawtime = 300

-- Command-line completion
vim.opt.wildmenu = true
vim.opt.wildmode = "longest:full,full"
vim.opt.wildoptions = "pum" -- Show completion menu as popup
