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
    extensions = {
      copilotchat = {
        enabled = true,
        convert_tools_to_functions = true, -- Convert MCP tools to CopilotChat functions
        convert_resources_to_functions = true, -- Convert MCP resources to CopilotChat functions
        add_mcp_prefix = false, -- Add "mcp_" prefix to function names
      },
    },
  },
}
