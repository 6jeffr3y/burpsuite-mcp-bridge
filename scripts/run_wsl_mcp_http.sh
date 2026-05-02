#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export BURP_MCP_PLUGIN_ROOT="$ROOT_DIR"
export BURP_MCP_TRANSPORT="streamable-http"
export BURP_MCP_SERVER_HOST="${BURP_MCP_SERVER_HOST:-127.0.0.1}"
export BURP_MCP_SERVER_PORT="${BURP_MCP_SERVER_PORT:-9640}"
export BURP_MCP_SERVER_PATH="${BURP_MCP_SERVER_PATH:-/mcp}"
python3 "$ROOT_DIR/wsl-mcp/server.py" --transport streamable-http --host "$BURP_MCP_SERVER_HOST" --port "$BURP_MCP_SERVER_PORT" --path "$BURP_MCP_SERVER_PATH"
