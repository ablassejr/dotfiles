-- Plugin: ggandor/leap.nvim
-- Installed via store.nvim

return {
  "ggandor/leap.nvim",
  event = "VeryLazy",
  config = function()
    -- Return an argument table for `leap()`, tailored for f/t motions.
    local function as_ft(key_specific_args)
      local common_args = {
        inputlen = 1,
        inclusive = true,
        -- To limit search scope to the current line:
        -- pattern = function(pat) return '\\%.l' .. pat end,
        opts = {
          labels = "a,s,d,f,j,k,l,z,x,c,n,m,A,S,D,F,J,K,L",                                -- force autojump
          safe_labels = vim.fn.mode(1):match("[no]") and "" or nil, -- normal/operator
        },
      }
      return vim.tbl_deep_extend("keep", common_args, key_specific_args)
    end

    local clever = require("leap.user").with_traversal_keys
    local clever_f = clever("f", "F")
    local clever_t = clever("t", "T")

    for key, key_specific_args in pairs({
      f = { opts = clever_f },
      F = { backward = true, opts = clever_f },
      t = { offset = -1, opts = clever_t },
      T = { backward = true, offset = 1, opts = clever_t },
    }) do
      vim.keymap.set({ "n", "x", "o" }, key, function()
        require("leap").leap(as_ft(key_specific_args))
      end)
    end
  end,
}
