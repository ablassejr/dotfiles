-- Options configuration
local opt = vim.opt

-- Leader keys (must be set before lazy)
vim.g.mapleader = " "
vim.g.maplocalleader = "\\"

-- Line numbers
opt.number = true
opt.relativenumber = true

-- Tabs & Indentation
opt.tabstop = 2
opt.shiftwidth = 2
opt.expandtab = true
opt.autoindent = true
opt.smartindent = true

-- Line wrapping
opt.wrap = false

-- Search settings
opt.ignorecase = true
opt.smartcase = true
opt.hlsearch = true
opt.incsearch = true

-- Cursor line
opt.cursorline = true

-- Appearance
opt.termguicolors = true
opt.background = "dark"
opt.signcolumn = "yes"

-- Backspace
opt.backspace = "indent,eol,start"

-- Clipboard
opt.clipboard:append("unnamedplus")

-- Split windows
opt.splitright = true
opt.splitbelow = true

-- Consider - as part of word
opt.iskeyword:append("-")

-- Disable swapfile
opt.swapfile = false
opt.backup = false

-- Undo
opt.undofile = true
opt.undodir = vim.fn.expand("~/.undodir")

-- Decrease update time
opt.updatetime = 250
opt.timeoutlen = 300

-- Completion
opt.completeopt = "menu,menuone,noselect"

-- Scrolloff
opt.scrolloff = 8
opt.sidescrolloff = 8

-- Enable mouse
opt.mouse = "a"

-- Concealment for markdown etc
opt.conceallevel = 2

-- Better display for messages
opt.cmdheight = 1

-- Don't show mode since we have a statusline
opt.showmode = false

-- Enable 24-bit color
opt.termguicolors = true

-- Fill chars
opt.fillchars = {
  foldopen = "",
  foldclose = "",
  fold = " ",
  foldsep = " ",
  diff = "╱",
  eob = " ",
}

-- Session options
opt.sessionoptions = { "buffers", "curdir", "tabpages", "winsize", "help", "globals", "skiprtp", "folds" }

-- Grep settings
opt.grepformat = "%f:%l:%c:%m"
opt.grepprg = "rg --vimgrep"
