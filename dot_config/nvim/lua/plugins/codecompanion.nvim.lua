-- Plugin: olimorris/codecompanion.nvim
-- AI-powered coding assistant with multiple LLM provider support

return {
  "olimorris/codecompanion.nvim",
  dependencies = { "ravitemer/mcphub.nvim", "Davidyz/VectorCode" },
  opts = function(_, opts)
    local auth = require("config.auth")

    -- Configure adapters with environment-based authentication
    -- ACP adapters (Agent Control Protocol) - for Claude Code
    opts.adapters = opts.adapters or {}
    opts.adapters.acp = opts.adapters.acp or {}

    -- Claude Code adapter (uses subscription via OAuth token - RECOMMENDED)
    if auth.has_credential("CLAUDE_CODE_OAUTH_TOKEN") then
      opts.adapters.acp.claude_code = function()
        return require("codecompanion.adapters").extend("claude_code", {
          env = { CLAUDE_CODE_OAUTH_TOKEN = "CLAUDE_CODE_OAUTH_TOKEN" },
        })
      end
      -- Set as default strategy adapter
      opts.strategies = opts.strategies or {}
      opts.strategies.chat = opts.strategies.chat or {}
      opts.strategies.chat.adapter = "claude_code"
      opts.strategies.inline = opts.strategies.inline or {}
      opts.strategies.inline.adapter = "claude_code"
    end

    -- HTTP adapters - for direct API calls
    opts.adapters.http = opts.adapters.http or {}

    -- Anthropic API (fallback if no OAuth token)
    if auth.has_credential("ANTHROPIC_API_KEY") then
      opts.adapters.http.anthropic = function()
        return require("codecompanion.adapters").extend("anthropic", {
          env = { api_key = "ANTHROPIC_API_KEY" },
        })
      end
    end

    -- OpenAI adapter
    if auth.has_credential("OPENAI_API_KEY") then
      opts.adapters.http.openai = function()
        return require("codecompanion.adapters").extend("openai", {
          env = { api_key = "OPENAI_API_KEY" },
        })
      end
    end

    -- OpenRouter adapter (provides access to multiple models)
    if auth.has_credential("OPENROUTER_API_KEY") then
      opts.adapters.http.openrouter = function()
        return require("codecompanion.adapters").extend("openrouter", {
          env = { api_key = "OPENROUTER_API_KEY" },
        })
      end
    end

    -- VectorCode tools integration
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
