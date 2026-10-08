#!/bin/bash
set -euo pipefail
if [[ "${1:-}" == "--help" ]]; then printf "%s\n" "Usage: bash scripts/build-analysis-image.sh [IMAGE_TAG]" "Builds and loads a Python/Perl tool image; may download its official base image."; exit 0; fi
script_dir=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
bash "$script_dir/setup.sh" --check --tool docker
eval "$(bash "$script_dir/setup.sh" --check --tool docker --env)"
image_tag=${1:-agent-skill-analysis:python3.12}
docker build --load --tag "$image_tag" "$script_dir/analysis-image"
docker image inspect --format "{{.Id}}" "$image_tag"
