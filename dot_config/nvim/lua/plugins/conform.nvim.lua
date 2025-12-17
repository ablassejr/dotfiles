-- Plugin: stevearc/conform.nvim
-- Installed via store.nvim

return {
  "stevearc/conform.nvim",
  opts = {
    config = {
      require("conform").setup({
        formatters_by_ft = {
          c = { "clang_format" },
          cpp = { "clang_format" },
        },
        formatters = {
          clang_format = {
            prepend_args = { "--style=file", "--fallback-style=LLVM" },
          },
        },
      }),
    },
  },
}

