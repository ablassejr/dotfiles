-- Centralized authentication helper for Neovim plugins
-- Provides secure access to credentials via environment variables

local M = {}

--- Get an environment variable with optional fallback
---@param key string The environment variable name
---@param fallback? string Optional fallback value
---@return string|nil
function M.get_env(key, fallback)
  local value = vim.env[key]
  if value and value ~= "" then
    return value
  end
  return fallback
end

--- Check if a credential is available
---@param key string The environment variable name
---@return boolean
function M.has_credential(key)
  local value = vim.env[key]
  return value ~= nil and value ~= ""
end

--- Notify if a credential is missing (for graceful degradation)
---@param service string The service name for the notification
---@param env_var string The missing environment variable
function M.notify_missing(service, env_var)
  vim.schedule(function()
    vim.notify(
      string.format("[Auth] %s: Missing %s", service, env_var),
      vim.log.levels.WARN,
      { title = "Authentication" }
    )
  end)
end

--- Check multiple credentials and return status table
---@param keys table List of environment variable names
---@return table<string, boolean>
function M.check_credentials(keys)
  local status = {}
  for _, key in ipairs(keys) do
    status[key] = M.has_credential(key)
  end
  return status
end

-- Credential definitions for documentation
M.credentials = {
  -- AI/LLM Providers (subscription-based - RECOMMENDED)
  CLAUDE_CODE_OAUTH_TOKEN = { service = "Claude Subscription", required_for = { "codecompanion" } },

  -- AI/LLM Providers (API key-based)
  ANTHROPIC_API_KEY = { service = "Anthropic/Claude API", required_for = { "codecompanion" } },
  OPENAI_API_KEY = { service = "OpenAI", required_for = { "codecompanion" } },
  OPENROUTER_API_KEY = { service = "OpenRouter", required_for = { "codecompanion" } },

  -- GitHub
  GITHUB_PERSONAL_ACCESS_TOKEN = { service = "GitHub", required_for = { "neogit", "mcphub" } },

  -- Database
  DATABASE_URL = { service = "Default Database", required_for = { "dadbod" } },
  DBUI_URL = { service = "DadbodUI Database", required_for = { "dadbod-ui" } },
}

return M
