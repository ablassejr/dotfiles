-- Plugin: folke/snacks.nvim
-- Installed via store.nvim

return {
  "folke/snacks.nvim",
  priority = 1000,
  lazy = false,
  ---@type snacks.Config
  opts = {
    -- your configuration comes here
    -- or leave it empty to use the default settings
    -- refer to the configuration section below
    keys = {
      {
        "<leader>T.",
        function()
          -- Can implement your own logic for saving files by cwd, project, git branch, etc.
          local data = vim.fn.stdpath("data")
          local root = data .. "/snacks/todo"
          vim.fn.mkdir(root, "p")
          local file = root .. "/todo.md" -- IMPORTANT: must match checkmate `files` pattern

          ---@diagnostic disable-next-line: missing-fields
          Snacks.scratch.open({
            ft = "markdown",
            file = file,
          })
        end,
        desc = "Toggle Scratch Todo",
      },
    },
    bigfile = {
      enabled = true,
    },
    dashboard = {
      enabled = true,
    },
    explorer = {
      enabled = true,
    },
    indent = {
      enabled = true,
    },
    input = {
      enabled = true,
    },
    picker = {
      enabled = true,
    },
    notifier = {
      enabled = true,
    },
    quickfile = {
      enabled = true,
    },
    scope = {
      enabled = true,
    },
    scroll = {
      enabled = true,
    },
    statuscolumn = {
      enabled = true,
    },
    words = {
      enabled = true,
    },
  },
}
