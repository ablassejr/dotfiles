-- Plugin: Davidyz/VectorCode
-- Source commit requested by user: 171361ea0410e739f9bf2a04c75113cd80d3c0d0

return {
  "Davidyz/VectorCode",
  commit = "171361ea0410e739f9bf2a04c75113cd80d3c0d0",
  event = "VeryLazy",
  config = function()
    -- Use defaults; change here if you want to tune the CLI path or enable
    -- auto-updates/LSP backend.
    require("vectorcode.config").setup()
  end,
}
