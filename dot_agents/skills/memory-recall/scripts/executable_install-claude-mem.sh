#!/bin/bash
set -euo pipefail
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bash "$script_dir/setup.sh" --install --tool claude-mem
eval "$(bash "$script_dir/setup.sh" --check --tool claude-mem --env)"
CLAUDE_MEM_ONLINE_OPTIN=false claude-mem install --provider host
