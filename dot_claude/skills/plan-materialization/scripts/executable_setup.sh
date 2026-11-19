#!/bin/bash
set -euo pipefail
skill_dir=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
if [[ "${1:-}" == "--help" ]]; then
  printf '%s\n' 'Usage: bash scripts/setup.sh [--check | --plan | --install] [--tool NAME ...] [--prefix PATH] [--application PATH.app] [--env]' 'Default: check required utilities. Optional utilities require --tool. Installs npm/Python dependencies in an isolated prefix.'
  exit 0
fi
python_bin=$(command -v python3 || true)
if [[ -z "$python_bin" && -x /opt/homebrew/bin/python3 ]]; then python_bin=/opt/homebrew/bin/python3; fi
if [[ -z "$python_bin" && -x /usr/local/bin/python3 ]]; then python_bin=/usr/local/bin/python3; fi
if [[ -z "$python_bin" ]]; then
  if [[ " ${*} " != *' --install '* ]]; then
    printf '%s\n' 'Python 3 is missing. Use --install to provision it, or read references/setup.md.' >&2
    exit 2
  fi
  brew_bin=$(command -v brew || true)
  if [[ -z "$brew_bin" && -x /opt/homebrew/bin/brew ]]; then brew_bin=/opt/homebrew/bin/brew; fi
  if [[ -z "$brew_bin" && -x /usr/local/bin/brew ]]; then brew_bin=/usr/local/bin/brew; fi
  if [[ -z "$brew_bin" ]]; then
    printf '%s\n' 'Homebrew is missing. Run bash scripts/bootstrap.sh --install-homebrew, then retry.' >&2
    exit 2
  fi
  "$brew_bin" install python
  python_bin="$("$brew_bin" --prefix)/bin/python3"
fi
exec "$python_bin" -B "$skill_dir/scripts/setup.py" "$@"
