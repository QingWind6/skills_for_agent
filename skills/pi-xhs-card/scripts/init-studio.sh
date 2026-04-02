#!/usr/bin/env bash
set -euo pipefail

if [[ $# -ne 1 ]]; then
  echo "Usage: $0 <target-dir>" >&2
  exit 1
fi

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
template_dir="${script_dir}/../assets/studio-template"
target_dir="$1"

if [[ ! -d "${template_dir}" ]]; then
  echo "Template directory not found: ${template_dir}" >&2
  exit 1
fi

if [[ -e "${target_dir}" ]] && find "${target_dir}" -mindepth 1 -maxdepth 1 | read -r _; then
  echo "Target directory exists and is not empty: ${target_dir}" >&2
  exit 1
fi

mkdir -p "${target_dir}"
cp -a "${template_dir}/." "${target_dir}/"

echo "Initialized PI XHS Card studio at ${target_dir}"
