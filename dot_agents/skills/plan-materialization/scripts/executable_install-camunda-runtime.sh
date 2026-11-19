#!/bin/bash
set -euo pipefail
if [[ $# != 1 ]]; then printf "%s\n" "Usage: bash scripts/install-camunda-runtime.sh VERSION" "Downloads the selected c8run version; does not start or deploy it." >&2; exit 2; fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bash "$script_dir/setup.sh" --install --tool c8ctl --tool java
eval "$(bash "$script_dir/setup.sh" --check --tool c8ctl --tool java --env)"
c8ctl cluster install "$1"
