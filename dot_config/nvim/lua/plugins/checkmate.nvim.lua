-- Plugin: bngarren/checkmate.nvim
-- Installed via store.nvim

return {
  "bngarren/checkmate.nvim",
  ft = "markdown", -- Lazy loads for Markdown files matching patterns in 'files'
  opts = { files = { "*.md" } }, -- Plugin options
}

