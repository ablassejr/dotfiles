return {
  "folke/snacks.nvim",
  opts = {
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
    scroll = {
      enabled = false, -- Disable scrolling animations
    },
    animations = {
      enabled = false, -- Disable all animations
    },
    dashboard = { enabled = true },
    picker = { enabled = true },
    scratch = { enabled = true },
  },
}
