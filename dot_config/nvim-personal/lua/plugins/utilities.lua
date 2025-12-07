-- Utility plugins
return {
  -- Toggleterm
  {
    "akinsho/toggleterm.nvim",
    version = "*",
    cmd = "ToggleTerm",
    keys = {
      { "<C-\\>", "<cmd>ToggleTerm<cr>", desc = "Toggle Terminal" },
      { "<leader>tf", "<cmd>ToggleTerm direction=float<cr>", desc = "Float Terminal" },
      { "<leader>th", "<cmd>ToggleTerm direction=horizontal<cr>", desc = "Horizontal Terminal" },
      { "<leader>tv", "<cmd>ToggleTerm direction=vertical<cr>", desc = "Vertical Terminal" },
    },
    opts = {
      size = function(term)
        if term.direction == "horizontal" then
          return 15
        elseif term.direction == "vertical" then
          return vim.o.columns * 0.4
        end
      end,
      open_mapping = [[<c-\>]],
      hide_numbers = true,
      shade_terminals = true,
      start_in_insert = true,
      insert_mappings = true,
      terminal_mappings = true,
      persist_size = true,
      persist_mode = true,
      direction = "float",
      close_on_exit = true,
      shell = vim.o.shell,
      auto_scroll = true,
      float_opts = {
        border = "curved",
        winblend = 0,
      },
    },
  },

  -- Term-edit
  {
    "chomosuke/term-edit.nvim",
    event = "TermOpen",
    version = "1.*",
    opts = {
      prompt_end = "%$ ",
    },
  },

  -- Obsidian
  {
    "epwalsh/obsidian.nvim",
    version = "*",
    lazy = true,
    ft = "markdown",
    dependencies = { "nvim-lua/plenary.nvim" },
    opts = {
      workspaces = {
        { name = "personal", path = "~/vaults/personal" },
        { name = "work", path = "~/vaults/work" },
      },
      notes_subdir = "notes",
      daily_notes = {
        folder = "notes/dailies",
        date_format = "%Y-%m-%d",
        alias_format = "%B %-d, %Y",
        default_tags = { "daily-notes" },
      },
      completion = { nvim_cmp = false, min_chars = 2 },
      new_notes_location = "notes_subdir",
      preferred_link_style = "wiki",
    },
    keys = {
      { "<leader>on", "<cmd>ObsidianNew<cr>", desc = "New Note" },
      { "<leader>oo", "<cmd>ObsidianOpen<cr>", desc = "Open in Obsidian" },
      { "<leader>os", "<cmd>ObsidianSearch<cr>", desc = "Search Notes" },
      { "<leader>oq", "<cmd>ObsidianQuickSwitch<cr>", desc = "Quick Switch" },
      { "<leader>ob", "<cmd>ObsidianBacklinks<cr>", desc = "Backlinks" },
      { "<leader>ot", "<cmd>ObsidianToday<cr>", desc = "Today's Note" },
    },
  },

  -- Cord - Discord presence
  {
    "vyfor/cord.nvim",
    build = ":Cord update",
    opts = {},
  },

  -- Vuffers - Buffer management
  {
    "Hajime-Suzuki/vuffers.nvim",
    dependencies = { "nvim-tree/nvim-web-devicons" },
    config = function()
      require("vuffers").setup({
        exclude = {
          filenames = { "term://" },
          filetypes = { "lazygit", "NvimTree", "qf" },
        },
        keymaps = { use_default = true },
        sort = { type = "none", direction = "asc" },
        view = {
          modified_icon = "󰛿",
          pinned_icon = "󰐾",
        },
      })
    end,
  },

  -- Fyler - File explorer
  {
    "A7Lavinraj/fyler.nvim",
    dependencies = { "echasnovski/mini.icons" },
    branch = "stable",
    lazy = false,
    opts = {},
    keys = {
      { "<leader>e", "<cmd>Fyler<cr>", desc = "Open Fyler" },
    },
  },

  -- Time Machine - Undo history
  -- NOTE: Must learn to use - visual undo tree
  {
    "y3owk1n/time-machine.nvim",
    version = "*",
    cmd = { "TimeMachineToggle", "TimeMachinePurgeBuffer", "TimeMachinePurgeAll" },
    keys = {
      { "<leader>tt", "<cmd>TimeMachineToggle<cr>", desc = "Toggle Time Machine" },
      { "<leader>tx", "<cmd>TimeMachinePurgeCurrent<cr>", desc = "Purge current" },
    },
    opts = {
      diff_tool = "native",
      keymaps = {
        undo = "u",
        redo = "<C-r>",
        restore_undopoint = "<CR>",
        refresh_timeline = "r",
        close = "q",
        help = "g?",
      },
    },
  },

  -- Checkmate - Todo management in markdown
  -- NOTE: Must learn to use - manage todos in markdown files
  {
    "bngarren/checkmate.nvim",
    ft = "markdown",
    version = "*",
    opts = {
      enabled = true,
      notify = true,
      default_list_marker = "-",
      enter_insert_after_new = true,
      smart_toggle = { enabled = true },
      show_todo_count = true,
    },
    keys = {
      { "<leader>Tt", "<cmd>Checkmate toggle<CR>", desc = "Toggle todo item" },
      { "<leader>Tc", "<cmd>Checkmate check<CR>", desc = "Check todo" },
      { "<leader>Tu", "<cmd>Checkmate uncheck<CR>", desc = "Uncheck todo" },
      { "<leader>Tn", "<cmd>Checkmate create<CR>", desc = "Create todo" },
    },
  },

  -- ATAC - API client
  -- NOTE: Must learn to use - REST API client in Neovim
  {
    "NachoNievaG/atac.nvim",
    dependencies = { "akinsho/toggleterm.nvim" },
    config = function()
      require("atac").setup({
        dir = "~/.config/atac",
      })
    end,
    keys = {
      { "<leader>ra", "<cmd>Atac<cr>", desc = "ATAC API Client" },
    },
  },

  -- ScrollEOF
  {
    "Aasim-A/scrollEOF.nvim",
    event = { "CursorMoved", "WinScrolled" },
    opts = {
      insert_mode = false,
      floating = true,
      disabled_filetypes = { "terminal" },
    },
  },

  -- Smear cursor
  {
    "sphamba/smear-cursor.nvim",
    opts = {
      smear_between_buffers = true,
      smear_between_neighbor_lines = true,
      scroll_buffer_space = true,
      smear_insert_mode = true,
    },
  },

  -- NUI - UI component library
  {
    "MunifTanjim/nui.nvim",
    lazy = true,
  },

  -- Haunt - Floating windows
  {
    "adigitoleo/haunt.nvim",
    config = function()
      require("haunt").setup()
    end,
  },

  -- Store - Session management
  {
    "alex-popov-tech/store.nvim",
    cmd = "Store",
    opts = {},
  },
}
