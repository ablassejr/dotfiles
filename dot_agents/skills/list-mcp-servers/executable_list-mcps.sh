#!/usr/bin/env bash
set -euo pipefail

desktop_config() {
  case "$(uname -s)" in
    Darwin) printf '%s\n' "$HOME/Library/Application Support/Claude/claude_desktop_config.json" ;;
    Linux)  printf '%s\n' "${XDG_CONFIG_HOME:-$HOME/.config}/Claude/claude_desktop_config.json" ;;
    *)      printf '%s\n' "${APPDATA:-$HOME/AppData/Roaming}/Claude/claude_desktop_config.json" ;;
  esac
}

echo "=== Claude Code MCP servers (claude mcp list) ==="
if command -v claude >/dev/null 2>&1; then
  claude mcp list
else
  echo "claude CLI not found on PATH; falling back to config files"
  for f in "$HOME/.claude.json" "$HOME/.mcp.json" "$PWD/.mcp.json"; do
    [ -f "$f" ] || continue
    echo "--- $f ---"
    python3 -c "import json,sys; d=json.load(open(sys.argv[1])); print('\n'.join(sorted(d.get('mcpServers',{}))) or '(none)')" "$f"
  done
fi

echo ""
cfg="$(desktop_config)"
echo "=== Claude Desktop MCP servers ($cfg) ==="
if [ -f "$cfg" ]; then
  python3 -c "
import json,sys
d=json.load(open(sys.argv[1]))
servers=d.get('mcpServers',{})
if not servers:
    print('(none configured)')
for name in sorted(servers):
    s=servers[name]
    cmd=s.get('command') or s.get('url') or '?'
    args=' '.join(s.get('args',[]))
    print(f'{name}: {cmd} {args}'.rstrip())
" "$cfg"
else
  echo "(no Claude Desktop config found at this path)"
fi
