#!/bin/bash
set -euo pipefail

if [[ "${1:-}" != "--install-homebrew" ]]; then
  printf '%s\n' 'Usage: bash scripts/bootstrap.sh --install-homebrew' 'Installs Homebrew using its official installer; may request macOS administrator access.'
  exit 2
fi
if [[ "$(uname -s)" != Darwin ]]; then
  printf '%s\n' 'This bootstrap targets macOS. See https://docs.brew.sh/Installation for other platforms.' >&2
  exit 1
fi
if command -v brew >/dev/null 2>&1 || [[ -x /opt/homebrew/bin/brew ]] || [[ -x /usr/local/bin/brew ]]; then
  printf '%s\n' 'Homebrew is already installed.'
  exit 0
fi
installer=$(mktemp -t skill-homebrew.XXXXXX)
trap 'rm -f "$installer"' EXIT
curl --fail --silent --show-error --location https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh --output "$installer"
/bin/bash "$installer"
