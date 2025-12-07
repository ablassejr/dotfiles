-- Navigation plugins
return {
  -- Plenary - Required by many plugins
  {
    "nvim-lua/plenary.nvim",
    lazy = true,
  },

  -- Telescope
  {
    "nvim-telescope/telescope.nvim",
    cmd = "Telescope",
    version = false,
    dependencies = {
      "nvim-lua/plenary.nvim",
      {
        "nvim-telescope/telescope-fzf-native.nvim",
        build = "make",
        cond = function()
          return vim.fn.executable("make") == 1
        end,
      },
    },
    keys = {
      { "<leader>ff", "<cmd>Telescope find_files<cr>", desc = "Find Files" },
      { "<leader>fg", "<cmd>Telescope live_grep<cr>", desc = "Live Grep" },
      { "<leader>fb", "<cmd>Telescope buffers<cr>", desc = "Buffers" },
      { "<leader>fh", "<cmd>Telescope help_tags<cr>", desc = "Help Tags" },
      { "<leader>fr", "<cmd>Telescope oldfiles<cr>", desc = "Recent Files" },
      { "<leader>fc", "<cmd>Telescope commands<cr>", desc = "Commands" },
      { "<leader>fk", "<cmd>Telescope keymaps<cr>", desc = "Keymaps" },
      { "<leader>fd", "<cmd>Telescope diagnostics<cr>", desc = "Diagnostics" },
      { "<leader>fs", "<cmd>Telescope lsp_document_symbols<cr>", desc = "Document Symbols" },
      { "<leader>fw", "<cmd>Telescope lsp_workspace_symbols<cr>", desc = "Workspace Symbols" },
      { "<leader>gc", "<cmd>Telescope git_commits<cr>", desc = "Git Commits" },
      { "<leader>gs", "<cmd>Telescope git_status<cr>", desc = "Git Status" },
      { "<leader><space>", "<cmd>Telescope find_files<cr>", desc = "Find Files" },
      { "<leader>/", "<cmd>Telescope live_grep<cr>", desc = "Grep" },
      { "<leader>:", "<cmd>Telescope command_history<cr>", desc = "Command History" },
    },
    opts = function()
      local actions = require("telescope.actions")
      return {
        defaults = {
          prompt_prefix = " ",
          selection_caret = " ",
          path_display = { "truncate" },
          sorting_strategy = "ascending",
          layout_config = {
            horizontal = {
              prompt_position = "top",
              preview_width = 0.55,
            },
            width = 0.87,
            height = 0.80,
          },
          mappings = {
            i = {
              ["<C-n>"] = actions.cycle_history_next,
              ["<C-p>"] = actions.cycle_history_prev,
              ["<C-j>"] = actions.move_selection_next,
              ["<C-k>"] = actions.move_selection_previous,
              ["<C-c>"] = actions.close,
              ["<C-u>"] = actions.preview_scrolling_up,
              ["<C-d>"] = actions.preview_scrolling_down,
            },
            n = {
              ["q"] = actions.close,
            },
          },
        },
        pickers = {
          find_files = {
            hidden = true,
            find_command = { "rg", "--files", "--hidden", "--glob", "!**/.git/*" },
          },
        },
        extensions = {
          fzf = {
            fuzzy = true,
            override_generic_sorter = true,
            override_file_sorter = true,
            case_mode = "smart_case",
          },
        },
      }
    end,
    config = function(_, opts)
      local telescope = require("telescope")
      telescope.setup(opts)
      pcall(telescope.load_extension, "fzf")
    end,
  },

  -- Telescope extensions
  {
    "cljoly/telescope-repo.nvim",
    dependencies = { "nvim-telescope/telescope.nvim" },
    keys = {
      { "<leader>fR", "<cmd>Telescope repo list<cr>", desc = "Find Repos" },
    },
    config = function()
      require("telescope").load_extension("repo")
    end,
  },

  {
    "piersolenski/telescope-import.nvim",
    dependencies = { "nvim-telescope/telescope.nvim" },
    keys = {
      { "<leader>fi", function() require("telescope").extensions.import.import() end, desc = "Import" },
    },
    config = function()
      require("telescope").load_extension("import")
    end,
  },

  {
    "kiyoon/telescope-insert-path.nvim",
    dependencies = { "nvim-telescope/telescope.nvim" },
  },

  {
    "danielfalk/smart-open.nvim",
    branch = "0.2.x",
    dependencies = {
      "kkharji/sqlite.lua",
      "nvim-telescope/telescope.nvim",
      { "nvim-telescope/telescope-fzf-native.nvim", build = "make" },
    },
    keys = {
      { "<leader><leader>", function() require("telescope").extensions.smart_open.smart_open() end, desc = "Smart Open" },
    },
    config = function()
      require("telescope").load_extension("smart_open")
    end,
  },

  -- Flash - Quick navigation
  {
    "folke/flash.nvim",
    event = "VeryLazy",
    opts = {},
    keys = {
      { "s", mode = { "n", "x", "o" }, function() require("flash").jump() end, desc = "Flash" },
      { "S", mode = { "n", "x", "o" }, function() require("flash").treesitter() end, desc = "Flash Treesitter" },
      { "r", mode = "o", function() require("flash").remote() end, desc = "Remote Flash" },
      { "R", mode = { "o", "x" }, function() require("flash").treesitter_search() end, desc = "Treesitter Search" },
      { "<c-s>", mode = "c", function() require("flash").toggle() end, desc = "Toggle Flash Search" },
    },
  },

  -- Leap - Quick navigation (alternative to flash)
  {
    "ggandor/leap.nvim",
    enabled = false, -- Disabled in favor of flash.nvim
    dependencies = { "tpope/vim-repeat" },
    keys = {
      { "s", mode = { "n", "x", "o" }, desc = "Leap forward to" },
      { "S", mode = { "n", "x", "o" }, desc = "Leap backward to" },
      { "gs", mode = { "n", "x", "o" }, desc = "Leap from windows" },
    },
    config = function()
      require("leap").add_default_mappings()
    end,
  },

  -- Smart splits
  {
    "mrjones2014/smart-splits.nvim",
    keys = {
      { "<A-h>", function() require("smart-splits").resize_left() end, desc = "Resize left" },
      { "<A-j>", function() require("smart-splits").resize_down() end, desc = "Resize down" },
      { "<A-k>", function() require("smart-splits").resize_up() end, desc = "Resize up" },
      { "<A-l>", function() require("smart-splits").resize_right() end, desc = "Resize right" },
      { "<C-h>", function() require("smart-splits").move_cursor_left() end, desc = "Move to left split" },
      { "<C-j>", function() require("smart-splits").move_cursor_down() end, desc = "Move to below split" },
      { "<C-k>", function() require("smart-splits").move_cursor_up() end, desc = "Move to above split" },
      { "<C-l>", function() require("smart-splits").move_cursor_right() end, desc = "Move to right split" },
      { "<leader><leader>h", function() require("smart-splits").swap_buf_left() end, desc = "Swap buffer left" },
      { "<leader><leader>j", function() require("smart-splits").swap_buf_down() end, desc = "Swap buffer down" },
      { "<leader><leader>k", function() require("smart-splits").swap_buf_up() end, desc = "Swap buffer up" },
      { "<leader><leader>l", function() require("smart-splits").swap_buf_right() end, desc = "Swap buffer right" },
    },
    opts = {
      ignored_buftypes = { "nofile", "quickfix", "prompt" },
      ignored_filetypes = { "NvimTree" },
      default_amount = 3,
      at_edge = "wrap",
    },
  },

  -- Namu - Symbol navigation
  {
    "bassamsdata/namu.nvim",
    config = function()
      require("namu").setup({
        namu_symbols = {
          enable = true,
          options = {
            AllowKinds = {
              default = { "Function", "Method", "Class", "Module", "Property", "Variable" },
            },
            display = { mode = "icon", padding = 2 },
            window = {
              auto_size = true,
              border = "rounded",
              title_prefix = "󱠦 ",
            },
          },
        },
        ui_select = { enable = false },
      })
    end,
    keys = {
      { "<leader>ss", "<cmd>Namu symbols<cr>", desc = "Jump to LSP symbol" },
      { "<leader>sw", "<cmd>Namu workspace<cr>", desc = "Workspace symbols" },
    },
  },

  -- Yanky - Better yank/paste
  -- NOTE: Must learn to use - cycle through yank history with <p> and <P> after paste
  {
    "gbprod/yanky.nvim",
    dependencies = { "kkharji/sqlite.lua" },
    opts = {
      ring = {
        history_length = 100,
        storage = "shada",
        sync_with_numbered_registers = true,
        cancel_event = "update",
      },
      picker = {
        select = { action = nil },
        telescope = { use_default_mappings = true },
      },
      system_clipboard = { sync_with_ring = true },
      highlight = { on_put = true, on_yank = true, timer = 500 },
      preserve_cursor_position = { enabled = true },
    },
    keys = {
      { "<leader>p", function() require("telescope").extensions.yank_history.yank_history({}) end, desc = "Yank History" },
      { "y", "<Plug>(YankyYank)", mode = { "n", "x" }, desc = "Yank text" },
      { "p", "<Plug>(YankyPutAfter)", mode = { "n", "x" }, desc = "Put after" },
      { "P", "<Plug>(YankyPutBefore)", mode = { "n", "x" }, desc = "Put before" },
      { "gp", "<Plug>(YankyGPutAfter)", mode = { "n", "x" }, desc = "Put after (leave cursor)" },
      { "gP", "<Plug>(YankyGPutBefore)", mode = { "n", "x" }, desc = "Put before (leave cursor)" },
      { "<c-p>", "<Plug>(YankyPreviousEntry)", desc = "Previous yank" },
      { "<c-n>", "<Plug>(YankyNextEntry)", desc = "Next yank" },
      { "]p", "<Plug>(YankyPutIndentAfterLinewise)", desc = "Put indented after" },
      { "[p", "<Plug>(YankyPutIndentBeforeLinewise)", desc = "Put indented before" },
    },
  },
}
