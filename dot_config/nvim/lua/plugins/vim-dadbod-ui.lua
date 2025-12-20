-- Plugin: kristijanhusak/vim-dadbod-ui
-- Database UI with environment-based connection configuration

return {
  "kristijanhusak/vim-dadbod-ui",
  dependencies = {
    { "tpope/vim-dadbod", lazy = true },
    { "kristijanhusak/vim-dadbod-completion", ft = { "sql", "mysql", "plsql" }, lazy = true },
  },
  cmd = { "DBUI", "DBUIToggle", "DBUIAddConnection", "DBUIFindBuffer" },
  init = function()
    vim.g.db_ui_use_nerd_fonts = 1

    -- Save connections to a local (gitignored) location
    vim.g.db_ui_save_location = vim.fn.stdpath("data") .. "/dadbod"

    -- Environment variable support:
    -- - Set DBUI_URL and DBUI_NAME for a single default connection
    -- - Or use DB_UI_* prefix for multiple connections:
    --     DB_UI_DEV=postgresql://user:pass@localhost/dev
    --     DB_UI_PROD=postgresql://user:pass@prod.example.com/prod
  end,
}
