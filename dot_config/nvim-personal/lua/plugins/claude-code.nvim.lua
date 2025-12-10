-- Plugin: greggh/claude-code.nvim
-- Installed via store.nvim

return {
    "greggh/claude-code.nvim",
    dependencies = {
        "nvim-lua/plenary.nvim" -- Required for git operations
    },
    config = function()
        require("claude-code").setup(

        )
    end
}