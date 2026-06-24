#!/usr/bin/env bash
set -euo pipefail

script_dir="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
eval "$("${script_dir}/veee-proxy-env.sh")"

if (( $# == 0 )); then
  env | grep -Ei '^(HTTP|HTTPS|ALL|NO)_PROXY=|^(http|https|all|no)_proxy=' | sort
  exit 0
fi

exec "$@"
