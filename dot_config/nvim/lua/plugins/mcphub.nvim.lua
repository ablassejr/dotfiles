-- Plugin: ravitemer/mcphub.nvim
-- MCP (Model Context Protocol) hub for AI integrations

return {
  "ravitemer/mcphub.nvim",
  event = "VeryLazy",
  dependencies = {
    "nvim-lua/plenary.nvim",
  },
  opts = {
    port = 37373,
    config = vim.fn.expand("~/.config/mcphub/servers.json"),
    log_level = vim.log.levels.WARN,
  },
}
