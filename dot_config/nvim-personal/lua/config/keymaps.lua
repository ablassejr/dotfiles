-- Keymaps configuration
-- Leader key is Space (set in options.lua)
-- Organized by mnemonic prefixes for intuitive recall

local map = vim.keymap.set
local opts = { silent = true }

-- Helper to merge options
local function with_desc(desc)
  return vim.tbl_extend("force", opts, { desc = desc })
end

--------------------------------------------------------------------------------
-- ESSENTIAL MAPPINGS (No prefix)
--------------------------------------------------------------------------------

-- Better escape
map("i", "jk", "<Esc>", with_desc("Exit insert mode"))
map("i", "jj", "<Esc>", with_desc("Exit insert mode"))

-- Clear search highlight
map("n", "<Esc>", "<cmd>nohlsearch<CR>", with_desc("Clear search highlight"))

-- Quick save/quit
map("n", "<leader>w", "<cmd>w<CR>", with_desc("Save file"))
map("n", "<leader>W", "<cmd>wa<CR>", with_desc("Save all files"))
map("n", "<leader>q", "<cmd>q<CR>", with_desc("Quit"))
map("n", "<leader>Q", "<cmd>qa<CR>", with_desc("Quit all"))

-- Better paste (don't replace clipboard when pasting over selection)
map("x", "<leader>p", '"_dP', with_desc("Paste without yanking"))

-- System clipboard
map({ "n", "v" }, "<leader>y", '"+y', with_desc("Yank to system clipboard"))
map("n", "<leader>Y", '"+Y', with_desc("Yank line to system clipboard"))

--------------------------------------------------------------------------------
-- WINDOW NAVIGATION (Ctrl + hjkl)
--------------------------------------------------------------------------------

map("n", "<C-h>", "<C-w>h", with_desc("Go to left window"))
map("n", "<C-j>", "<C-w>j", with_desc("Go to lower window"))
map("n", "<C-k>", "<C-w>k", with_desc("Go to upper window"))
map("n", "<C-l>", "<C-w>l", with_desc("Go to right window"))

-- Window resize with Ctrl + arrows
map("n", "<C-Up>", "<cmd>resize +2<CR>", with_desc("Increase window height"))
map("n", "<C-Down>", "<cmd>resize -2<CR>", with_desc("Decrease window height"))
map("n", "<C-Left>", "<cmd>vertical resize -2<CR>", with_desc("Decrease window width"))
map("n", "<C-Right>", "<cmd>vertical resize +2<CR>", with_desc("Increase window width"))

-- Window splits
map("n", "<leader>-", "<cmd>split<CR>", with_desc("Horizontal split"))
map("n", "<leader>|", "<cmd>vsplit<CR>", with_desc("Vertical split"))

--------------------------------------------------------------------------------
-- BUFFER NAVIGATION (<leader>b prefix)
--------------------------------------------------------------------------------

map("n", "<S-h>", "<cmd>bprevious<CR>", with_desc("Previous buffer"))
map("n", "<S-l>", "<cmd>bnext<CR>", with_desc("Next buffer"))
map("n", "[b", "<cmd>bprevious<CR>", with_desc("Previous buffer"))
map("n", "]b", "<cmd>bnext<CR>", with_desc("Next buffer"))
map("n", "<leader>bb", "<cmd>e #<CR>", with_desc("Switch to alternate buffer"))
map("n", "<leader>bd", "<cmd>bdelete<CR>", with_desc("Delete buffer"))
map("n", "<leader>bD", "<cmd>bdelete!<CR>", with_desc("Delete buffer (force)"))
map("n", "<leader>bn", "<cmd>enew<CR>", with_desc("New buffer"))

--------------------------------------------------------------------------------
-- BETTER EDITING
--------------------------------------------------------------------------------

-- Stay in visual mode when indenting
map("v", "<", "<gv", with_desc("Indent left"))
map("v", ">", ">gv", with_desc("Indent right"))

-- Move lines up/down in visual mode
map("v", "J", ":m '>+1<CR>gv=gv", with_desc("Move selection down"))
map("v", "K", ":m '<-2<CR>gv=gv", with_desc("Move selection up"))

-- Keep cursor centered when scrolling
map("n", "<C-d>", "<C-d>zz", with_desc("Scroll down (centered)"))
map("n", "<C-u>", "<C-u>zz", with_desc("Scroll up (centered)"))
map("n", "n", "nzzzv", with_desc("Next search result (centered)"))
map("n", "N", "Nzzzv", with_desc("Previous search result (centered)"))

-- Join lines without moving cursor
map("n", "J", "mzJ`z", with_desc("Join lines"))

-- Add undo breakpoints
map("i", ",", ",<C-g>u")
map("i", ".", ".<C-g>u")
map("i", ";", ";<C-g>u")

--------------------------------------------------------------------------------
-- SEARCH/FIND (<leader>f prefix) - Using Snacks Picker
--------------------------------------------------------------------------------

map("n", "<leader>ff", function() Snacks.picker.files() end, with_desc("Find files"))
map("n", "<leader>fg", function() Snacks.picker.grep() end, with_desc("Grep (live)"))
map("n", "<leader>fw", function() Snacks.picker.grep_word() end, with_desc("Grep current word"))
map("n", "<leader>fb", function() Snacks.picker.buffers() end, with_desc("Find buffers"))
map("n", "<leader>fr", function() Snacks.picker.recent() end, with_desc("Recent files"))
map("n", "<leader>fc", function() Snacks.picker.commands() end, with_desc("Commands"))
map("n", "<leader>fh", function() Snacks.picker.help() end, with_desc("Help tags"))
map("n", "<leader>fk", function() Snacks.picker.keymaps() end, with_desc("Keymaps"))
map("n", "<leader>fm", function() Snacks.picker.marks() end, with_desc("Marks"))
map("n", "<leader>fq", function() Snacks.picker.qflist() end, with_desc("Quickfix list"))
map("n", "<leader>f/", function() Snacks.picker.lines() end, with_desc("Search in buffer"))
map("n", "<leader>f:", function() Snacks.picker.command_history() end, with_desc("Command history"))
map("n", "<leader>f'", function() Snacks.picker.registers() end, with_desc("Registers"))

-- Smart open (frecency-based)
map("n", "<leader><leader>", function()
  require("telescope").extensions.smart_open.smart_open()
end, with_desc("Smart open"))

-- Alternative: Snacks picker for quick file access
map("n", "<leader>,", function() Snacks.picker.buffers() end, with_desc("Switch buffer"))

--------------------------------------------------------------------------------
-- GIT (<leader>g prefix)
--------------------------------------------------------------------------------

-- Neogit
map("n", "<leader>gg", "<cmd>Neogit<CR>", with_desc("Neogit status"))
map("n", "<leader>gc", "<cmd>Neogit commit<CR>", with_desc("Neogit commit"))
map("n", "<leader>gp", "<cmd>Neogit push<CR>", with_desc("Neogit push"))
map("n", "<leader>gl", "<cmd>Neogit pull<CR>", with_desc("Neogit pull"))

-- Diffview
map("n", "<leader>gd", "<cmd>DiffviewOpen<CR>", with_desc("Diffview open"))
map("n", "<leader>gD", "<cmd>DiffviewClose<CR>", with_desc("Diffview close"))
map("n", "<leader>gh", "<cmd>DiffviewFileHistory %<CR>", with_desc("File history"))
map("n", "<leader>gH", "<cmd>DiffviewFileHistory<CR>", with_desc("Branch history"))

-- Gitsigns (hunk navigation)
map("n", "]h", function() require("gitsigns").next_hunk() end, with_desc("Next hunk"))
map("n", "[h", function() require("gitsigns").prev_hunk() end, with_desc("Previous hunk"))
map("n", "<leader>ghs", function() require("gitsigns").stage_hunk() end, with_desc("Stage hunk"))
map("n", "<leader>ghr", function() require("gitsigns").reset_hunk() end, with_desc("Reset hunk"))
map("n", "<leader>ghS", function() require("gitsigns").stage_buffer() end, with_desc("Stage buffer"))
map("n", "<leader>ghR", function() require("gitsigns").reset_buffer() end, with_desc("Reset buffer"))
map("n", "<leader>ghp", function() require("gitsigns").preview_hunk() end, with_desc("Preview hunk"))
map("n", "<leader>ghb", function() require("gitsigns").blame_line({ full = true }) end, with_desc("Blame line"))
map("n", "<leader>ghtb", function() require("gitsigns").toggle_current_line_blame() end, with_desc("Toggle line blame"))
map("n", "<leader>ghtd", function() require("gitsigns").toggle_deleted() end, with_desc("Toggle deleted"))

-- Visual mode hunk operations
map("v", "<leader>ghs", function() require("gitsigns").stage_hunk({ vim.fn.line("."), vim.fn.line("v") }) end, with_desc("Stage selection"))
map("v", "<leader>ghr", function() require("gitsigns").reset_hunk({ vim.fn.line("."), vim.fn.line("v") }) end, with_desc("Reset selection"))

--------------------------------------------------------------------------------
-- LSP (<leader>l prefix) + go-to definitions (g prefix)
--------------------------------------------------------------------------------

-- Go-to mappings (standard g prefix)
map("n", "gd", vim.lsp.buf.definition, with_desc("Go to definition"))
map("n", "gD", vim.lsp.buf.declaration, with_desc("Go to declaration"))
map("n", "gi", vim.lsp.buf.implementation, with_desc("Go to implementation"))
map("n", "gr", vim.lsp.buf.references, with_desc("Go to references"))
map("n", "gt", vim.lsp.buf.type_definition, with_desc("Go to type definition"))
map("n", "K", vim.lsp.buf.hover, with_desc("Hover documentation"))
map("n", "gK", vim.lsp.buf.signature_help, with_desc("Signature help"))
map("i", "<C-k>", vim.lsp.buf.signature_help, with_desc("Signature help"))

-- LSP actions
map("n", "<leader>la", vim.lsp.buf.code_action, with_desc("Code action"))
map("n", "<leader>lr", vim.lsp.buf.rename, with_desc("Rename symbol"))
map("n", "<leader>lf", function() vim.lsp.buf.format({ async = true }) end, with_desc("Format buffer"))
map("v", "<leader>lf", function() vim.lsp.buf.format({ async = true }) end, with_desc("Format selection"))
map("n", "<leader>li", "<cmd>LspInfo<CR>", with_desc("LSP info"))
map("n", "<leader>lI", "<cmd>Mason<CR>", with_desc("Mason"))
map("n", "<leader>ll", vim.lsp.codelens.run, with_desc("CodeLens action"))
map("n", "<leader>lL", vim.lsp.codelens.refresh, with_desc("CodeLens refresh"))

-- Diagnostics
map("n", "<leader>ld", vim.diagnostic.open_float, with_desc("Line diagnostics"))
map("n", "[d", vim.diagnostic.goto_prev, with_desc("Previous diagnostic"))
map("n", "]d", vim.diagnostic.goto_next, with_desc("Next diagnostic"))
map("n", "[e", function() vim.diagnostic.goto_prev({ severity = vim.diagnostic.severity.ERROR }) end, with_desc("Previous error"))
map("n", "]e", function() vim.diagnostic.goto_next({ severity = vim.diagnostic.severity.ERROR }) end, with_desc("Next error"))

--------------------------------------------------------------------------------
-- DIAGNOSTICS/TROUBLE (<leader>x prefix)
--------------------------------------------------------------------------------

map("n", "<leader>xx", "<cmd>Trouble diagnostics toggle<CR>", with_desc("Diagnostics (Trouble)"))
map("n", "<leader>xX", "<cmd>Trouble diagnostics toggle filter.buf=0<CR>", with_desc("Buffer diagnostics"))
map("n", "<leader>xs", "<cmd>Trouble symbols toggle focus=false<CR>", with_desc("Symbols (Trouble)"))
map("n", "<leader>xl", "<cmd>Trouble lsp toggle focus=false win.position=right<CR>", with_desc("LSP references"))
map("n", "<leader>xL", "<cmd>Trouble loclist toggle<CR>", with_desc("Location list"))
map("n", "<leader>xQ", "<cmd>Trouble qflist toggle<CR>", with_desc("Quickfix list"))
map("n", "<leader>xt", "<cmd>TodoTrouble<CR>", with_desc("Todo (Trouble)"))
map("n", "<leader>xT", "<cmd>TodoTrouble keywords=TODO,FIX,FIXME<CR>", with_desc("Todo/Fix/Fixme"))

-- Todo navigation
map("n", "]t", function() require("todo-comments").jump_next() end, with_desc("Next todo"))
map("n", "[t", function() require("todo-comments").jump_prev() end, with_desc("Previous todo"))

--------------------------------------------------------------------------------
-- DEBUG (<leader>d prefix)
--------------------------------------------------------------------------------

map("n", "<leader>db", function() require("dap").toggle_breakpoint() end, with_desc("Toggle breakpoint"))
map("n", "<leader>dB", function() require("dap").set_breakpoint(vim.fn.input("Breakpoint condition: ")) end, with_desc("Conditional breakpoint"))
map("n", "<leader>dc", function() require("dap").continue() end, with_desc("Continue"))
map("n", "<leader>dC", function() require("dap").run_to_cursor() end, with_desc("Run to cursor"))
map("n", "<leader>di", function() require("dap").step_into() end, with_desc("Step into"))
map("n", "<leader>do", function() require("dap").step_over() end, with_desc("Step over"))
map("n", "<leader>dO", function() require("dap").step_out() end, with_desc("Step out"))
map("n", "<leader>dp", function() require("dap").pause() end, with_desc("Pause"))
map("n", "<leader>dr", function() require("dap").repl.toggle() end, with_desc("Toggle REPL"))
map("n", "<leader>ds", function() require("dap").session() end, with_desc("Session"))
map("n", "<leader>dt", function() require("dap").terminate() end, with_desc("Terminate"))
map("n", "<leader>dw", function() require("dap.ui.widgets").hover() end, with_desc("Widgets"))

-- Debug step controls (function keys)
map("n", "<F5>", function() require("dap").continue() end, with_desc("Debug: Continue"))
map("n", "<F10>", function() require("dap").step_over() end, with_desc("Debug: Step over"))
map("n", "<F11>", function() require("dap").step_into() end, with_desc("Debug: Step into"))
map("n", "<F12>", function() require("dap").step_out() end, with_desc("Debug: Step out"))

--------------------------------------------------------------------------------
-- EXPLORER/FILE TREE (<leader>e prefix)
--------------------------------------------------------------------------------

map("n", "<leader>e", function() Snacks.explorer() end, with_desc("File explorer"))
map("n", "<leader>E", function() Snacks.explorer.reveal() end, with_desc("Explorer (reveal current)"))

--------------------------------------------------------------------------------
-- UI TOGGLES (<leader>u prefix)
--------------------------------------------------------------------------------

map("n", "<leader>uw", "<cmd>set wrap!<CR>", with_desc("Toggle word wrap"))
map("n", "<leader>ul", "<cmd>set relativenumber!<CR>", with_desc("Toggle relative numbers"))
map("n", "<leader>uL", "<cmd>set number!<CR>", with_desc("Toggle line numbers"))
map("n", "<leader>us", "<cmd>set spell!<CR>", with_desc("Toggle spelling"))
map("n", "<leader>uc", "<cmd>set cursorline!<CR>", with_desc("Toggle cursor line"))
map("n", "<leader>uC", "<cmd>set cursorcolumn!<CR>", with_desc("Toggle cursor column"))
map("n", "<leader>uh", "<cmd>set hlsearch!<CR>", with_desc("Toggle highlight search"))
map("n", "<leader>ui", function() vim.lsp.inlay_hint.enable(not vim.lsp.inlay_hint.is_enabled()) end, with_desc("Toggle inlay hints"))

-- Snacks toggles
map("n", "<leader>un", function() Snacks.notifier.hide() end, with_desc("Dismiss notifications"))
map("n", "<leader>uz", function() Snacks.zen() end, with_desc("Toggle zen mode"))
map("n", "<leader>uZ", function() Snacks.zen.zoom() end, with_desc("Toggle zoom"))
map("n", "<leader>ud", function() Snacks.dim() end, with_desc("Toggle dim mode"))

--------------------------------------------------------------------------------
-- TERMINAL (<leader>t prefix)
--------------------------------------------------------------------------------

map("n", "<leader>tf", function() Snacks.terminal() end, with_desc("Toggle terminal"))
map("n", "<leader>tg", function() Snacks.terminal("lazygit") end, with_desc("Lazygit"))
map("n", "<leader>th", function() Snacks.terminal(nil, { win = { position = "bottom" } }) end, with_desc("Terminal (bottom)"))
map("n", "<leader>tv", function() Snacks.terminal(nil, { win = { position = "right" } }) end, with_desc("Terminal (right)"))

-- Terminal mode mappings
map("t", "<Esc><Esc>", "<C-\\><C-n>", with_desc("Exit terminal mode"))
map("t", "<C-h>", "<cmd>wincmd h<CR>", with_desc("Go to left window"))
map("t", "<C-j>", "<cmd>wincmd j<CR>", with_desc("Go to lower window"))
map("t", "<C-k>", "<cmd>wincmd k<CR>", with_desc("Go to upper window"))
map("t", "<C-l>", "<cmd>wincmd l<CR>", with_desc("Go to right window"))

--------------------------------------------------------------------------------
-- SYMBOLS/CODE NAVIGATION (<leader>s prefix)
--------------------------------------------------------------------------------

map("n", "<leader>ss", "<cmd>Namu symbols<CR>", with_desc("Document symbols"))
map("n", "<leader>sw", "<cmd>Namu workspace<CR>", with_desc("Workspace symbols"))
map("n", "<leader>so", function() Snacks.picker.lsp_symbols() end, with_desc("LSP symbols (outline)"))

--------------------------------------------------------------------------------
-- CODE/REFACTORING (<leader>c prefix)
--------------------------------------------------------------------------------

map("n", "<leader>cs", "<cmd>Trouble symbols toggle focus=false<CR>", with_desc("Symbols sidebar"))
map("n", "<leader>cl", "<cmd>Trouble lsp toggle focus=false win.position=right<CR>", with_desc("LSP sidebar"))

-- Formatting with conform
map("n", "<leader>cf", function()
  require("conform").format({ async = true, lsp_fallback = true })
end, with_desc("Format buffer"))
map("v", "<leader>cf", function()
  require("conform").format({ async = true, lsp_fallback = true })
end, with_desc("Format selection"))

--------------------------------------------------------------------------------
-- SNIPPETS (<leader>S prefix)
--------------------------------------------------------------------------------

map("n", "<leader>Sn", function() require("scissors").addNewSnippet() end, with_desc("New snippet"))
map("x", "<leader>Sn", function() require("scissors").addNewSnippet() end, with_desc("New snippet from selection"))
map("n", "<leader>Se", function() require("scissors").editSnippet() end, with_desc("Edit snippet"))

--------------------------------------------------------------------------------
-- AI/CLAUDE (<leader>a prefix)
--------------------------------------------------------------------------------

map("n", "<leader>ac", "<cmd>ClaudeCode<CR>", with_desc("Claude Code toggle"))
map("n", "<leader>as", "<cmd>ClaudeCodeSend<CR>", with_desc("Send to Claude"))
map("v", "<leader>as", "<cmd>ClaudeCodeSend<CR>", with_desc("Send selection to Claude"))

--------------------------------------------------------------------------------
-- NOTES/OBSIDIAN (<leader>o prefix)
--------------------------------------------------------------------------------

map("n", "<leader>on", "<cmd>ObsidianNew<CR>", with_desc("New note"))
map("n", "<leader>oo", "<cmd>ObsidianOpen<CR>", with_desc("Open in Obsidian"))
map("n", "<leader>os", "<cmd>ObsidianSearch<CR>", with_desc("Search notes"))
map("n", "<leader>oq", "<cmd>ObsidianQuickSwitch<CR>", with_desc("Quick switch"))
map("n", "<leader>ob", "<cmd>ObsidianBacklinks<CR>", with_desc("Backlinks"))
map("n", "<leader>ot", "<cmd>ObsidianTags<CR>", with_desc("Tags"))
map("n", "<leader>od", "<cmd>ObsidianToday<CR>", with_desc("Daily note"))
map("n", "<leader>oy", "<cmd>ObsidianYesterday<CR>", with_desc("Yesterday's note"))
map("n", "<leader>ol", "<cmd>ObsidianLinks<CR>", with_desc("Links"))

--------------------------------------------------------------------------------
-- UNDO/TIME MACHINE (<leader>U prefix)
--------------------------------------------------------------------------------

map("n", "<leader>Ut", "<cmd>TimeMachineToggle<CR>", with_desc("Time machine toggle"))

--------------------------------------------------------------------------------
-- QUICKFIX/LOCATION LIST ([ and ] navigation)
--------------------------------------------------------------------------------

map("n", "[q", "<cmd>cprev<CR>", with_desc("Previous quickfix"))
map("n", "]q", "<cmd>cnext<CR>", with_desc("Next quickfix"))
map("n", "[Q", "<cmd>cfirst<CR>", with_desc("First quickfix"))
map("n", "]Q", "<cmd>clast<CR>", with_desc("Last quickfix"))
map("n", "[l", "<cmd>lprev<CR>", with_desc("Previous loclist"))
map("n", "]l", "<cmd>lnext<CR>", with_desc("Next loclist"))

--------------------------------------------------------------------------------
-- MISC UTILITIES
--------------------------------------------------------------------------------

-- Which-key help
map("n", "<leader>?", function() require("which-key").show({ global = false }) end, with_desc("Buffer keymaps"))

-- Snacks utilities
map("n", "<leader>.", function() Snacks.scratch() end, with_desc("Toggle scratch buffer"))
map("n", "<leader>S", function() Snacks.scratch.select() end, with_desc("Select scratch buffer"))
map("n", "<leader>nh", function() Snacks.notifier.show_history() end, with_desc("Notification history"))
map("n", "<leader>gb", function() Snacks.git.blame_line() end, with_desc("Git blame line"))
map("n", "<leader>gB", function() Snacks.gitbrowse() end, with_desc("Git browse"))
map("n", "<leader>gf", function() Snacks.lazygit.log_file() end, with_desc("Lazygit file history"))
map("n", "<leader>gL", function() Snacks.lazygit.log() end, with_desc("Lazygit log"))

-- Rename file
map("n", "<leader>cR", function() Snacks.rename.rename_file() end, with_desc("Rename file"))

-- Better line operations
map("n", "<leader>j", "mzo<Esc>`z", with_desc("Insert line below"))
map("n", "<leader>k", "mzO<Esc>`z", with_desc("Insert line above"))
