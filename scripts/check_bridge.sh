#!/usr/bin/env bash
set -euo pipefail
HOST="${BURP_MCP_BRIDGE_HOST:-127.0.0.1}"
PORT="${BURP_MCP_BRIDGE_PORT:-9639}"
URL="${BURP_MCP_BRIDGE_URL:-http://${HOST}:${PORT}}"
echo "Checking ${URL}/health ..."
curl --noproxy "*" -fsS --max-time 5 "${URL}/health" | python3 -m json.tool
