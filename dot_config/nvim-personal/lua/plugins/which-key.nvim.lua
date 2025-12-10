-- Plugin: folke/which-key.nvim
-- Provides visual keymap hints and organizes keymaps into groups

return {
  "folke/which-key.nvim",
  event = "VeryLazy",
  opts = {
    -- Modern preset with better defaults
    preset = "modern",
    -- Delay before showing the popup (ms)
    delay = 300,
    -- Icons configuration
    icons = {
      breadcrumb = "»",
      separator = "➜",
      group = "+",
    },
    -- Window layout
    win = {
      border = "rounded",
      padding = { 1, 2 },
    },
    -- Layout options
    layout = {
      width = { min = 20 },
      spacing = 3,
    },
    -- Sorting
    sort = { "local", "order", "group", "alphanum", "mod" },
  },
  config = function(_, opts)
    local wk = require("which-key")
    wk.setup(opts)

    -- Register group labels for better organization
    wk.add({
      -- Top level groups
      { "<leader>b", group = "Buffer" },
      { "<leader>c", group = "Code" },
      { "<leader>d", group = "Debug" },
      { "<leader>f", group = "Find/Search" },
      { "<leader>g", group = "Git" },
      { "<leader>gh", group = "Hunks" },
      { "<leader>ght", group = "Toggle" },
      { "<leader>l", group = "LSP" },
      { "<leader>n", group = "Notifications" },
      { "<leader>o", group = "Obsidian/Notes" },
      { "<leader>s", group = "Symbols" },
      { "<leader>S", group = "Snippets" },
      { "<leader>t", group = "Terminal" },
      { "<leader>u", group = "UI/Toggle" },
      { "<leader>U", group = "Undo/History" },
      { "<leader>x", group = "Diagnostics" },
      { "<leader>a", group = "AI/Claude" },

      -- Navigation hints
      { "[", group = "Previous" },
      { "]", group = "Next" },
      { "g", group = "Go to" },
      { "z", group = "Fold/Scroll" },

      -- Quick descriptions for common actions
      { "<leader><leader>", desc = "Smart Open" },
      { "<leader>,", desc = "Switch Buffer" },
      { "<leader>-", desc = "Horizontal Split" },
      { "<leader>|", desc = "Vertical Split" },
      { "<leader>.", desc = "Scratch Buffer" },
      { "<leader>w", desc = "Save" },
      { "<leader>W", desc = "Save All" },
      { "<leader>q", desc = "Quit" },
      { "<leader>Q", desc = "Quit All" },
      { "<leader>e", desc = "Explorer" },
      { "<leader>E", desc = "Explorer (reveal)" },
      { "<leader>?", desc = "Buffer Keymaps" },
    })
  end,
}
