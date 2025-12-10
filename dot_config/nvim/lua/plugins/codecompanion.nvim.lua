-- Plugin: olimorris/codecompanion.nvim
-- Installed via store.nvim

return {
  "olimorris/codecompanion.nvim",
  -- VectorCode tools are added in opts below.
  dependencies = { "ravitemer/mcphub.nvim", "Davidyz/VectorCode" },
  opts = function(_, opts)
    local has_vc, vc = pcall(require, "vectorcode.integrations.codecompanion")
    if not has_vc then
      return opts
    end

    local has_cli = function()
      local ok, cfg = pcall(require, "vectorcode.config")
      return ok and cfg.has_cli({ notify = false })
    end

    opts.strategies = opts.strategies or {}
    opts.strategies.chat = opts.strategies.chat or {}
    opts.strategies.chat.tools = opts.strategies.chat.tools or {}
    opts.strategies.chat.tools.groups = opts.strategies.chat.tools.groups or {}

    local tools = opts.strategies.chat.tools

    tools.vectorcode_ls = tools.vectorcode_ls
      or {
        description = "List VectorCode projects on disk",
        enabled = has_cli,
        callback = function()
          return vc.chat.make_tool("ls")
        end,
      }

    tools.vectorcode_files_ls = tools.vectorcode_files_ls
      or {
        description = "List files indexed for a project",
        enabled = has_cli,
        callback = function()
          return vc.chat.make_tool("files_ls")
        end,
      }

    tools.vectorcode_query = tools.vectorcode_query
      or {
        description = "Search the VectorCode index for relevant chunks/files",
        enabled = has_cli,
        callback = function()
          return vc.chat.make_tool("query", {
            include_in_toolbox = true,
            summarise = { enabled = false },
          })
        end,
      }

    tools.vectorcode_vectorise = tools.vectorcode_vectorise
      or {
        description = "Add files to the VectorCode database",
        enabled = has_cli,
        callback = function()
          return vc.chat.make_tool("vectorise", {
            include_in_toolbox = true,
            requires_approval = true,
          })
        end,
      }

    tools.vectorcode_files_rm = tools.vectorcode_files_rm
      or {
        description = "Remove files from the VectorCode database",
        enabled = has_cli,
        callback = function()
          return vc.chat.make_tool("files_rm", { requires_approval = true })
        end,
      }

    tools.groups.vectorcode_toolbox = tools.groups.vectorcode_toolbox
      or {
        description = "VectorCode retrieval/indexing tools",
        prompt = "You can inspect indexed projects with ${tools}.",
        tools = {
          "vectorcode_ls",
          "vectorcode_files_ls",
          "vectorcode_query",
          "vectorcode_vectorise",
          "vectorcode_files_rm",
        },
        opts = { collapse_tools = true },
      }

    return opts
  end,
}
