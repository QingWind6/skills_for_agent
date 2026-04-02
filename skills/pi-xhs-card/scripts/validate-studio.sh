#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <studio-dir>" >&2
  exit 1
fi

studio_dir="$1"

required_files=(
  "${studio_dir}/server.mjs"
  "${studio_dir}/export.mjs"
  "${studio_dir}/public/app.js"
)

for file in "${required_files[@]}"; do
  if [[ ! -f "${file}" ]]; then
    echo "Missing required file: ${file}" >&2
    exit 1
  fi
done

node --check "${studio_dir}/server.mjs"
node --check "${studio_dir}/export.mjs"
node --check "${studio_dir}/public/app.js"

echo "Studio validation passed for ${studio_dir}"
