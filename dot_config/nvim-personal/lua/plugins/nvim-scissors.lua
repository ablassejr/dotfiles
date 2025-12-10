-- Plugin: chrisgrieser/nvim-scissors
-- Installed via store.nvim

return {
    "chrisgrieser/nvim-scissors",
    dependencies = "nvim-telescope/telescope.nvim", -- if using telescope
    opts = {
        snippetDir = "path/to/your/snippetFolder"
    }
}