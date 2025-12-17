-- Plugin: ahmedkhalf/project.nvim
-- Installed via store.nvim

return {
    "ahmedkhalf/project.nvim",
    config = function()
        require(
            "project_nvim"
        ).setup {}
    end,
    event = "VeryLazy"
}