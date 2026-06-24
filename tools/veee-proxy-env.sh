#!/usr/bin/env bash
set -euo pipefail

die() {
  echo "veee-proxy-env: $*" >&2
  exit 1
}

command -v lsof >/dev/null 2>&1 || die "lsof is required"

ports=()
while IFS= read -r port; do
  ports+=("$port")
done < <(
  lsof -nP -iTCP -sTCP:LISTEN 2>/dev/null \
    | awk '$1 == "Veee" && $9 ~ /^127\.0\.0\.1:/ { sub(/^127\.0\.0\.1:/, "", $9); print $9 }' \
    | sort -n \
    | uniq
)

if (( ${#ports[@]} == 0 )); then
  die "Veee is not listening on 127.0.0.1. Open Veee or switch it on first."
fi

port_is_veee() {
  local candidate="$1"
  local port
  for port in "${ports[@]}"; do
    [[ "$port" == "$candidate" ]] && return 0
  done
  return 1
}

port_from_proxy_url() {
  local value="${1:-}"
  [[ "$value" =~ ^https?://127\.0\.0\.1:([0-9]+) ]] && {
    echo "${BASH_REMATCH[1]}"
    return 0
  }
  [[ "$value" =~ ^socks5h?://127\.0\.0\.1:([0-9]+) ]] && {
    echo "${BASH_REMATCH[1]}"
    return 0
  }
  return 1
}

http_port=""
socks_port=""

for env_name in HTTPS_PROXY HTTP_PROXY https_proxy http_proxy; do
  value="${!env_name:-}"
  if port="$(port_from_proxy_url "$value" 2>/dev/null)" && port_is_veee "$port"; then
    http_port="$port"
    break
  fi
done

for env_name in ALL_PROXY all_proxy; do
  value="${!env_name:-}"
  if port="$(port_from_proxy_url "$value" 2>/dev/null)" && port_is_veee "$port"; then
    socks_port="$port"
    break
  fi
done

if [[ -z "$http_port" ]]; then
  http_port="${ports[$((${#ports[@]} - 1))]}"
fi

if [[ -z "$socks_port" ]]; then
  socks_port="${ports[0]}"
fi

cat <<EOF
export HTTP_PROXY=http://127.0.0.1:${http_port}
export HTTPS_PROXY=http://127.0.0.1:${http_port}
export http_proxy=http://127.0.0.1:${http_port}
export https_proxy=http://127.0.0.1:${http_port}
export ALL_PROXY=socks5://127.0.0.1:${socks_port}
export all_proxy=socks5://127.0.0.1:${socks_port}
export NO_PROXY=localhost,127.0.0.1,::1
export no_proxy=localhost,127.0.0.1,::1
EOF

echo "veee-proxy-env: HTTP=${http_port} SOCKS=${socks_port}" >&2
