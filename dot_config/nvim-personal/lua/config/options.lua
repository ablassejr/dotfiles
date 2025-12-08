-- Options configuration
local opt = vim.opt
-- Line numbers
opt.number = true
opt.relativenumber = true
vim.g.mapleader = " "

-- Undo persistence (for time-machine.nvim)
opt.undofile = true

-- Statuscolumn (for snacks.nvim)
opt.statuscolumn = [[%!v:lua.require'snacks.statuscolumn'.get()]]

-- Disable unused providers
vim.g.loaded_node_provider = 0
vim.g.loaded_perl_provider = 0
vim.g.loaded_ruby_provider = 0
