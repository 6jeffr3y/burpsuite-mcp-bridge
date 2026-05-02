#!/usr/bin/env bash
set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
export BURP_MCP_PLUGIN_ROOT="$ROOT_DIR"
python3 "$ROOT_DIR/wsl-mcp/server.py"
