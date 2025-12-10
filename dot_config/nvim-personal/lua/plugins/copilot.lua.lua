-- Plugin: zbirenbaum/copilot.lua
-- Installed via store.nvim

return {
    "zbirenbaum/copilot.lua",
    dependencies = {
        "copilotlsp-nvim/copilot-lsp" -- (optional) for NES functionality
    },
    cmd = "Copilot",
    event = "InsertEnter",
    config = function()
        require("copilot").setup(
            {}
        )
    end
}