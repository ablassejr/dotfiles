local opt = vim.opt
local env = vim.env
-- Options are automatically loaded before lazy.nvim startup
-- Default options that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/options.lua
-- Add any additional options here

-- Plugin settings
vim.g.snacks_animate = false -- Disable snacks.nvim animations

-- Editor settings
opt.colorcolumn = "80" -- Set color column at 80 characters
opt.termguicolors = true -- Enable 24-bit RGB colors
opt.shiftround = true
opt.smartindent = true -- Insert indents automatically
opt.shortmess:append({ W = true, I = true, c = true, C = true })
opt.showmode = false -- Dont show mode since we have a statusline
opt.ruler = false -- Disable the default ruler
opt.clipboard = env.SSH_CONNECTION and "" or "unnamedplus"
