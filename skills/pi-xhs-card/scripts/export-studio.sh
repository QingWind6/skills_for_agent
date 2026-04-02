#!/usr/bin/env bash
set -euo pipefail

base_url="${1:-http://127.0.0.1:43210}"

curl -fsS "${base_url}/api/health" >/dev/null
curl -fsS -X POST "${base_url}/api/export"
