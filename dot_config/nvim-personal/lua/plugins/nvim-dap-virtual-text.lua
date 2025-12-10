-- Plugin: theHamsta/nvim-dap-virtual-text
-- Installed via store.nvim

return {
    "theHamsta/nvim-dap-virtual-text",
    dependencies = {
        "mfussenegger/nvim-dap",
        "nvim-treesitter/nvim-treesitter"
    },
    event = "VeryLazy"
}