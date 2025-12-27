-- Autocmds are automatically loaded on the VeryLazy event
-- Default autocmds that are always set: https://github.com/LazyVim/LazyVim/blob/main/lua/lazyvim/config/autocmds.lua
--
-- Add any additional autocmds here
-- with `vim.api.nvim_create_autocmd`
--
-- Or remove existing autocmds by their group name (which is prefixed with `lazyvim_` for the defaults)
-- e.g. vim.api.nvim_del_augroup_by_name("lazyvim_wrap_spell")
local lopt = vim.opt_local
vim.api.nvim_create_autocmd("FileType", {
  pattern = "*",
  callback = function()
    if vim.bo.filetype == "markdown" or vim.bo.filetype == "python" then
      return
    end
    lopt.tabstop = 2
    lopt.shiftwidth = 2
    lopt.softtabstop = 2
    lopt.expandtab = true
  end,
})
-- Automatic registration via autocmd
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function()
    -- Only proceed if VectorCode is loaded
    local ok, vc_config = pcall(require, "vectorcode.config")
    if not ok then
      return
    end

    local cacher_backend = vc_config.get_cacher_backend()
    if not cacher_backend then
      return
    end

    local bufnr = vim.api.nvim_get_current_buf()

    cacher_backend.async_check("config", function()
      cacher_backend.register_buffer(bufnr, {
        n_query = 10,
        events = { "BufWritePost", "InsertEnter" },
      })
    end, nil)
  end,
  desc = "Register buffer for VectorCode on LSP attach",
})
