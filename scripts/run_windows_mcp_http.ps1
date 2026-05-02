param(
  [string]$BridgeUrl = $env:BURP_MCP_BRIDGE_URL,
  [string]$BridgeHost = $env:BURP_MCP_BRIDGE_HOST,
  [string]$BridgePort = $env:BURP_MCP_BRIDGE_PORT,
  [string]$McpHost = $env:BURP_MCP_SERVER_HOST,
  [string]$McpPort = $env:BURP_MCP_SERVER_PORT,
  [string]$McpPath = $env:BURP_MCP_SERVER_PATH
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$env:BURP_MCP_PLUGIN_ROOT = $root
$env:BURP_MCP_TRANSPORT = 'streamable-http'
if ($BridgeUrl) { $env:BURP_MCP_BRIDGE_URL = $BridgeUrl }
if ($BridgeHost) { $env:BURP_MCP_BRIDGE_HOST = $BridgeHost }
if ($BridgePort) { $env:BURP_MCP_BRIDGE_PORT = $BridgePort }
if (-not $McpHost) { $McpHost = '127.0.0.1' }
if (-not $McpPort) { $McpPort = '9640' }
if (-not $McpPath) { $McpPath = '/mcp' }
$env:BURP_MCP_SERVER_HOST = $McpHost
$env:BURP_MCP_SERVER_PORT = $McpPort
$env:BURP_MCP_SERVER_PATH = $McpPath
$python = if ($env:PYTHON_EXE) { $env:PYTHON_EXE } else { 'python' }
& $python "$root\wsl-mcp\server.py" --transport streamable-http --host $McpHost --port $McpPort --path $McpPath
