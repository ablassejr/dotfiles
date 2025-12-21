-- Plugin: olimorris/codecompanion.nvim
-- AI-powered coding assistant with multiple LLM provider support

return {
  "olimorris/codecompanion.nvim",
  dependencies = {
    "nvim-lua/plenary.nvim",
    "nvim-treesitter/nvim-treesitter",
    "ravitemer/mcphub.nvim",
    "Davidyz/VectorCode",
  },
  opts = function(_, opts)
    require("codecompanion").setup({
      adapters = {
        acp = {
          claude_code = function()
            return require("codecompanion.adapters").extend("claude_code", {
              env = {
                CLAUDE_CODE_OAUTH_TOKEN = "${CLAUDE_CODE_OAUTH_TOKEN}",
              },
            })
          end,
        },
      },
    })
  end,
}
