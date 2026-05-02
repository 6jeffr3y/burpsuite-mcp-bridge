@echo off
setlocal
set ROOT=%~dp0..
set BURP_MCP_PLUGIN_ROOT=%ROOT%
if not "%~1"=="" set BURP_MCP_BRIDGE_URL=%~1
if not "%~2"=="" set BURP_MCP_BRIDGE_PORT=%~2
if defined PYTHON_EXE (
  "%PYTHON_EXE%" "%ROOT%\wsl-mcp\server.py"
) else (
  python "%ROOT%\wsl-mcp\server.py"
)
