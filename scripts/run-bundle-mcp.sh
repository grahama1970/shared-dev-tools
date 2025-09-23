#!/usr/bin/env bash
set -euo pipefail

if [[ $# -lt 2 ]]; then
  echo "usage: $(basename "$0") <node-path> <script-path> [args...]" >&2
  exit 2
fi

NODE_BIN=$1
SCRIPT=$2
shift 2

# Log to STDERR (never stdout)
printf '[bundle-wrapper] node=%s script=%s args=%s cwd=%s\n' \
  "$NODE_BIN" "$SCRIPT" "$*" "$(pwd)" >&2

exec "$NODE_BIN" --enable-source-maps --trace-warnings "$SCRIPT" "$@"
