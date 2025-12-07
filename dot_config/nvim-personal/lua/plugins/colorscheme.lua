-- Colorscheme plugins
return {
  -- Cyberdream - Primary theme
  {
    "scottmckendry/cyberdream.nvim",
    lazy = false,
    priority = 1000,
    config = function()
      require("cyberdream").setup({
        variant = "default",
        transparent = false,
        saturation = 1,
        italic_comments = true,
        hide_fillchars = false,
        borderless_pickers = true,
        terminal_colors = true,
        cache = false,
        extensions = {
          telescope = true,
          notify = true,
          mini = true,
          treesitter = true,
          treesittercontext = true,
          whichkey = true,
          gitsigns = true,
          cmp = true,
          trouble = true,
          noice = true,
          rainbow_delimiters = true,
          indent_blankline = true,
          hop = true,
          lazy = true,
          dashboard = true,
          render_markdown = true,
        },
      })
      vim.cmd("colorscheme cyberdream")
    end,
  },

  -- VSCode theme - Alternative
  {
    "Mofiqul/vscode.nvim",
    lazy = true,
    config = function()
      local c = require("vscode.colors").get_colors()
      require("vscode").setup({
        transparent = false,
        italic_comments = true,
        underline_links = true,
        disable_nvimtree_bg = true,
        terminal_colors = true,
        color_overrides = {},
        group_overrides = {
          Cursor = { fg = c.vscDarkBlue, bg = c.vscLightGreen, bold = true },
        },
      })
    end,
  },
}
