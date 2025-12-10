-- Plugin: b0o/incline.nvim
-- Installed via store.nvim

return {
    "b0o/incline.nvim",
    config = function()
        require("incline").setup(

        )
    end,
    -- Optional: Lazy load Incline
    event = "VeryLazy"
}