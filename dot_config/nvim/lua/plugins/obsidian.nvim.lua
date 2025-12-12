-- Plugin: obsidian-nvim/obsidian.nvim
-- Installed via store.nvim

return {
  "obsidian-nvim/obsidian.nvim",
  version = "*", -- recommended, use latest release instead of latest commit
  ft = "markdown",
  ---@module 'obsidian'
  ---@type obsidian.config
  opts = {
    legacy_commands = false, -- this will be removed in the next major release
    workspaces = {
      {
        name = "Documents",
        path = "~/Documents",
      },
    },
  },
}

