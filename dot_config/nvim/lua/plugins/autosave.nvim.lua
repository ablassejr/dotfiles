-- Plugin: 0x00-ketsu/autosave.nvim
-- Installed via store.nvim

return {
  "0x00-ketsu/autosave.nvim",
  config = function()
    require("autosave").setup({
      event = {
        "BufLeave",
        "BufEnter",
      },
      debounce_delay = 10000, -- milliseconds
    })
  end,
}
