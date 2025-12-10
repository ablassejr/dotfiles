-- Add a small VectorCode status component to lualine.
return {
  "nvim-lualine/lualine.nvim",
  optional = true,
  event = "VeryLazy",
  opts = function(_, opts)
    local ok, vc_lualine = pcall(require, "vectorcode.integrations.lualine")
    if not ok then
      return opts
    end

    opts.sections = opts.sections or {}
    opts.sections.lualine_x = opts.sections.lualine_x or {}

    -- Shows number of cached results for the current buffer and async job count.
    table.insert(opts.sections.lualine_x, vc_lualine({ show_job_count = true }))
    return opts
  end,
}
