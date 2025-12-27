return {
  "saghen/blink.cmp",
  -- optional: provides snippets for the snippet source
  dependencies = {
    "rafamadriz/friendly-snippets",
    -- blink.cmp extension plugins
    "fang2hou/blink-copilot", -- Copilot integration
    "mikavilpas/blink-ripgrep.nvim", -- Ripgrep search integration
    -- Database completion (loaded for SQL filetypes)
    { "kristijanhusak/vim-dadbod-completion", ft = { "sql", "mysql", "plsql" } },
    { "olimorris/codecompanion.nvim" },
  },

  -- use a release tag to download pre-built binaries
  version = "1.*",
  -- AND/OR build from source, requires nightly: https://rust-lang.github.io/rustup/concepts/channels.html#working-with-nightly-rust
  -- build = 'cargo build --release',
  -- If you use nix, you can build from source using latest nightly rust with:
  -- build = 'nix run .#build-plugin',

  ---@module 'blink.cmp'
  ---@type blink.cmp.Config
  opts = {
    -- 'default' (recommended) for mappings similar to built-in completions (C-y to accept)
    -- 'super-tab' for mappings similar to vscode (tab to accept)
    -- 'enter' for enter to accept
    -- 'none' for no mappings
    --
    -- All presets have the following mappings:
    -- C-space: Open menu or open docs if already open
    -- C-n/C-p or Up/Down: Select next/previous item
    -- C-e: Hide menu
    -- C-k: Toggle signature help (if signature.enabled = true)
    --
    -- See :h blink-cmp-config-keymap for defining your own keymap
    keymap = { preset = "default" },

    appearance = {
      -- 'mono' (default) for 'Nerd Font Mono' or 'normal' for 'Nerd Font'
      -- Adjusts spacing to ensure icons are aligned
      nerd_font_variant = "mono",
    },

    -- (Default) Only show the documentation popup when manually triggered
    completion = { documentation = { auto_show = true } },

    -- Default list of enabled providers defined so that you can extend it
    -- elsewhere in your config, without redefining it, due to `opts_extend`
    sources = {
      default = { "lsp", "path", "snippets", "copilot", "ripgrep", "dadbod", "codecompanion" },
      providers = {
        lsp = {
          name = "LSP",
          module = "blink.cmp.sources.lsp",
          enabled = true,
          kind = "LSP",
          score_offset = 1000,
        },

        -- Copilot source configuration
        copilot = {
          name = "copilot",
          module = "blink-copilot",
          score_offset = 100, -- Prioritize copilot suggestions
          async = true,
        },
        -- Ripgrep source configuration
        ripgrep = {
          module = "blink-ripgrep",
          name = "Ripgrep",
          enabled = true,
          -- Options documented at: https://github.com/mikavilpas/blink-ripgrep.nvim
        },
        -- Database completion source
        dadbod = {
          name = "Dadbod",
          module = "vim_dadbod_completion.blink",
          enabled = true,
          score_offset = 500,
        },
        snippets = {
          name = "Snippets",
          module = "blink.cmp.sources.snippets",
          kind = "Snippet",
          enabled = true,
          score_offset = 750,
        },
      },

      -- (Default) Rust fuzzy matcher for typo resistance and significantly better performance
      -- You may use a lua implementation instead by using `implementation = "lua"` or fallback to the lua implementation,
      -- when the Rust fuzzy matcher is not available, by using `implementation = "prefer_rust"`
      --
      -- See the fuzzy documentation for more information
      fuzzy = { implementation = "prefer_rust_with_warning" },
    },
    opts_extend = { "sources.default" },
  },
}
