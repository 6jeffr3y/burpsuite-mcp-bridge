param(
  [string]$BridgeUrl = $env:BURP_MCP_BRIDGE_URL,
  [string]$BridgeHost = $env:BURP_MCP_BRIDGE_HOST,
  [string]$BridgePort = $env:BURP_MCP_BRIDGE_PORT
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:BURP_MCP_PLUGIN_ROOT = $root
if ($BridgeUrl) { $env:BURP_MCP_BRIDGE_URL = $BridgeUrl }
if ($BridgeHost) { $env:BURP_MCP_BRIDGE_HOST = $BridgeHost }
if ($BridgePort) { $env:BURP_MCP_BRIDGE_PORT = $BridgePort }
$python = if ($env:PYTHON_EXE) { $env:PYTHON_EXE } else { 'python' }
& $python "$root\wsl-mcp\server.py"
