-- Git plugins
return {
  -- Gitsigns
  {
    "lewis6991/gitsigns.nvim",
    event = { "BufReadPre", "BufNewFile" },
    opts = {
      signs = {
        add = { text = "┃" },
        change = { text = "┃" },
        delete = { text = "_" },
        topdelete = { text = "‾" },
        changedelete = { text = "~" },
        untracked = { text = "┆" },
      },
      signcolumn = true,
      numhl = false,
      linehl = false,
      word_diff = false,
      watch_gitdir = { follow_files = true },
      auto_attach = true,
      attach_to_untracked = false,
      current_line_blame = false,
      current_line_blame_opts = {
        virt_text = true,
        virt_text_pos = "eol",
        delay = 1000,
        ignore_whitespace = false,
      },
      current_line_blame_formatter = "<author>, <author_time:%R> - <summary>",
      sign_priority = 6,
      update_debounce = 100,
      max_file_length = 40000,
      preview_config = {
        style = "minimal",
        relative = "cursor",
        row = 0,
        col = 1,
      },
      on_attach = function(bufnr)
        local gs = package.loaded.gitsigns
        local function map(mode, l, r, opts)
          opts = opts or {}
          opts.buffer = bufnr
          vim.keymap.set(mode, l, r, opts)
        end

        -- Navigation
        map("n", "]h", function()
          if vim.wo.diff then return "]c" end
          vim.schedule(function() gs.next_hunk() end)
          return "<Ignore>"
        end, { expr = true, desc = "Next Hunk" })

        map("n", "[h", function()
          if vim.wo.diff then return "[c" end
          vim.schedule(function() gs.prev_hunk() end)
          return "<Ignore>"
        end, { expr = true, desc = "Prev Hunk" })

        -- Actions
        map("n", "<leader>ghs", gs.stage_hunk, { desc = "Stage Hunk" })
        map("n", "<leader>ghr", gs.reset_hunk, { desc = "Reset Hunk" })
        map("v", "<leader>ghs", function() gs.stage_hunk({ vim.fn.line("."), vim.fn.line("v") }) end, { desc = "Stage Hunk" })
        map("v", "<leader>ghr", function() gs.reset_hunk({ vim.fn.line("."), vim.fn.line("v") }) end, { desc = "Reset Hunk" })
        map("n", "<leader>ghS", gs.stage_buffer, { desc = "Stage Buffer" })
        map("n", "<leader>ghu", gs.undo_stage_hunk, { desc = "Undo Stage Hunk" })
        map("n", "<leader>ghR", gs.reset_buffer, { desc = "Reset Buffer" })
        map("n", "<leader>ghp", gs.preview_hunk, { desc = "Preview Hunk" })
        map("n", "<leader>ghb", function() gs.blame_line({ full = true }) end, { desc = "Blame Line" })
        map("n", "<leader>ghd", gs.diffthis, { desc = "Diff This" })
        map("n", "<leader>ghD", function() gs.diffthis("~") end, { desc = "Diff This ~" })
        map("n", "<leader>gtb", gs.toggle_current_line_blame, { desc = "Toggle Blame" })
        map("n", "<leader>gtd", gs.toggle_deleted, { desc = "Toggle Deleted" })

        -- Text object
        map({ "o", "x" }, "ih", ":<C-U>Gitsigns select_hunk<CR>", { desc = "Select Hunk" })
      end,
    },
  },

  -- Diffview
  {
    "sindrets/diffview.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    cmd = { "DiffviewOpen", "DiffviewClose", "DiffviewFileHistory" },
    keys = {
      { "<leader>gd", "<cmd>DiffviewOpen<cr>", desc = "Diffview Open" },
      { "<leader>gD", "<cmd>DiffviewClose<cr>", desc = "Diffview Close" },
      { "<leader>gH", "<cmd>DiffviewFileHistory %<cr>", desc = "File History" },
    },
    opts = {
      diff_binaries = false,
      enhanced_diff_hl = true,
      use_icons = true,
      show_help_hints = true,
      watch_index = true,
      view = {
        default = { layout = "diff2_horizontal" },
        merge_tool = { layout = "diff3_horizontal", disable_diagnostics = true },
        file_history = { layout = "diff2_horizontal" },
      },
      file_panel = {
        listing_style = "tree",
        tree_options = { flatten_dirs = true, folder_statuses = "only_folded" },
        win_config = { position = "left", width = 35 },
      },
      file_history_panel = {
        log_options = {
          git = {
            single_file = { diff_merges = "first-parent", follow = true },
            multi_file = { diff_merges = "first-parent" },
          },
        },
        win_config = { position = "bottom", height = 16 },
      },
    },
  },

  -- LazyGit
  {
    "kdheepak/lazygit.nvim",
    lazy = true,
    cmd = {
      "LazyGit",
      "LazyGitConfig",
      "LazyGitCurrentFile",
      "LazyGitFilter",
      "LazyGitFilterCurrentFile",
    },
    dependencies = { "nvim-lua/plenary.nvim" },
    keys = {
      { "<leader>gg", "<cmd>LazyGit<cr>", desc = "LazyGit" },
      { "<leader>gG", "<cmd>LazyGitCurrentFile<cr>", desc = "LazyGit Current File" },
    },
    config = function()
      vim.g.lazygit_floating_window_winblend = 0
      vim.g.lazygit_floating_window_scaling_factor = 0.9
      vim.g.lazygit_floating_window_border_chars = { "╭", "─", "╮", "│", "╯", "─", "╰", "│" }
      vim.g.lazygit_use_neovim_remote = 1
    end,
  },

  -- Neogit
  {
    "NeogitOrg/neogit",
    dependencies = {
      "nvim-lua/plenary.nvim",
      "sindrets/diffview.nvim",
      "nvim-telescope/telescope.nvim",
    },
    cmd = "Neogit",
    keys = {
      { "<leader>gn", "<cmd>Neogit<cr>", desc = "Neogit" },
    },
    opts = {
      disable_hint = false,
      disable_context_highlighting = false,
      disable_signs = false,
      graph_style = "ascii",
      kind = "tab",
      commit_editor = { kind = "tab", show_staged_diff = true },
      integrations = { telescope = true, diffview = true },
      sections = {
        untracked = { folded = false },
        unstaged = { folded = false },
        staged = { folded = false },
        stashes = { folded = true },
        recent = { folded = true },
      },
    },
  },

  -- VGit (alternative to gitsigns with more features)
  {
    "tanvirtin/vgit.nvim",
    enabled = false, -- Disabled in favor of gitsigns
    dependencies = { "nvim-lua/plenary.nvim" },
    opts = {},
  },

  -- Octohub - GitHub integration
  {
    "2kabhishek/octohub.nvim",
    cmd = { "Octohub" },
    dependencies = {
      "2kabhishek/utils.nvim",
      "nvim-telescope/telescope.nvim",
    },
    opts = {
      repos = {
        per_user_dir = true,
        projects_dir = "~/Projects/",
      },
    },
    keys = {
      { "<leader>goo", "<cmd>Octohub<cr>", desc = "Octohub" },
    },
  },

  -- Chezmoi integration
  {
    "xvzc/chezmoi.nvim",
    dependencies = { "nvim-lua/plenary.nvim" },
    config = function()
      require("chezmoi").setup({
        edit = {
          watch = false,
          force = false,
        },
        events = {
          on_open = { notification = { enable = true, msg = "Opened a chezmoi-managed file" } },
          on_apply = { notification = { enable = true, msg = "Successfully applied" } },
        },
      })
    end,
  },
}
