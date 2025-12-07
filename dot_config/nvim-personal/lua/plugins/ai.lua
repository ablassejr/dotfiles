-- AI and Copilot plugins
return {
  -- Copilot
  {
    "zbirenbaum/copilot.lua",
    cmd = "Copilot",
    event = "InsertEnter",
    config = function()
      require("copilot").setup({
        panel = {
          enabled = false, -- Disabled for blink-copilot
          auto_refresh = false,
        },
        suggestion = {
          enabled = false, -- Disabled for blink-copilot
          auto_trigger = false,
        },
        filetypes = {
          yaml = false,
          markdown = false,
          help = false,
          gitcommit = false,
          gitrebase = false,
          hgcommit = false,
          svn = false,
          cvs = false,
          ["."] = false,
        },
        copilot_node_command = "node",
      })
    end,
  },

  -- Claude Code
  {
    "greggh/claude-code.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("claude-code").setup({
        window = {
          split_ratio = 0.3,
          position = "botright",
          enter_insert = true,
          hide_numbers = true,
          hide_signcolumn = true,
          float = {
            width = "80%",
            height = "80%",
            row = "center",
            col = "center",
            relative = "editor",
            border = "rounded",
          },
        },
        refresh = {
          enable = true,
          updatetime = 100,
          timer_interval = 1000,
          show_notifications = true,
        },
        git = { use_git_root = true },
        command = "claude",
        command_variants = {
          continue = "--continue",
          resume = "--resume",
          verbose = "--verbose",
        },
        keymaps = {
          toggle = {
            normal = "<C-,>",
            terminal = "<C-,>",
            variants = {
              continue = "<leader>cC",
              verbose = "<leader>cV",
            },
          },
          window_navigation = true,
          scrolling = true,
        },
      })
    end,
    keys = {
      { "<C-,>", desc = "Toggle Claude Code" },
      { "<leader>cC", desc = "Claude Continue" },
      { "<leader>cV", desc = "Claude Verbose" },
    },
  },

  -- VectorCode - AI-powered code search
  -- NOTE: Must learn to use - requires vectorcode CLI installation
  -- Install with: pip install vectorcode or uv tool install vectorcode
  {
    "Davidyz/VectorCode",
    version = "*",
    dependencies = { "nvim-lua/plenary.nvim" },
    build = "uv tool upgrade vectorcode",
    cmd = "VectorCode",
    opts = {
      async_opts = {
        debounce = 10,
        events = { "BufWritePost", "InsertEnter", "BufReadPost" },
        exclude_this = true,
        n_query = 1,
        notify = false,
      },
      exclude_this = true,
      n_query = 1,
      notify = true,
      timeout_ms = 5000,
    },
    keys = {
      { "<leader>vc", "<cmd>VectorCode<cr>", desc = "VectorCode Search" },
    },
  },
}
