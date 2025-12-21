-- Plugin: Davidyz/VectorCode
-- Source commit requested by user: 171361ea0410e739f9bf2a04c75113cd80d3c0d0

return {
  "Davidyz/VectorCode",
  version = "*",
  build = "uv tool upgrade vectorcode", -- Keeps CLI updated with plugin
  dependencies = { "nvim-lua/plenary.nvim" },
  cmd = "VectorCode", -- Lazy-load on command
  opts = {
    config = function()
      require("vectorcode").setup({
        -- CLI configuration
        cli_cmds = {
          vectorcode = "vectorcode", -- Path or command name
        },

        -- Synchronous API options (blocking queries)
        n_query = 1, -- Documents to retrieve
        notify = true, -- Show completion notifications
        timeout_ms = 5000, -- Query timeout (sync only)
        exclude_this = true, -- Exclude current file from results

        -- Backend selection
        async_backend = "lsp", -- "default" or "lsp"

        -- Async API options (non-blocking cached queries)
        async_opts = {
          debounce = 10, -- Milliseconds between queries
          events = { "BufWritePost", "InsertEnter", "BufReadPost" },
          exclude_this = true,
          n_query = 1,
          notify = false,
          query_cb = require("vectorcode.utils").make_surrounding_lines_cb(-1),
          run_on_register = false,
          single_job = false, -- Cancel previous job when new starts
        },

        -- Startup behavior
        on_setup = {
          update = true, -- Run vectorcode update on startup
          lsp = true, -- Pre-start LSP server
        },

        sync_log_env_var = false, -- Auto-set VECTORCODE_LOG_LEVEL
      })
    end,
  },
}
