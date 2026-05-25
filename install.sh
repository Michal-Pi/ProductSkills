#!/usr/bin/env sh
set -eu

ROOT_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
CLI="$ROOT_DIR/bin/product-skills.mjs"

usage() {
  cat <<'USAGE'
Usage: ./install.sh [product-skills install options]
       ./install.sh <install|update|validate|status|uninstall|checksum|dist-check> [options]

This bootstrap script only checks local prerequisites and delegates to
bin/product-skills.mjs. It does not install dependencies or edit shell profiles.
USAGE
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || {
    printf '%s\n' "Missing required command: $1" >&2
    exit 1
  }
}

if [ "${1:-}" = "--help" ] || [ "${1:-}" = "-h" ]; then
  usage
  exit 0
fi

require_command node

if [ ! -f "$CLI" ]; then
  printf '%s\n' "Missing installer CLI: $CLI" >&2
  exit 1
fi

case "${1:-}" in
  dist-check)
    require_command npm
    exec node "$CLI" "$@"
    ;;
  checksum|validate|status|help)
    exec node "$CLI" "$@"
    ;;
  install|update|validate|status|uninstall|checksum|dist-check|help)
    require_command git
    exec node "$CLI" "$@"
    ;;
  *)
    require_command git
    exec node "$CLI" install "$@"
    ;;
esac
