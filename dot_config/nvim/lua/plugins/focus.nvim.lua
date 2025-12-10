-- Plugin: nvim-focus/focus.nvim
-- Installed via store.nvim

return { "nvim-focus/focus.nvim", version = "*", opts = {
  config = function()
    require("focus").setup()
  end,
} }
