@echo off
setlocal
set ROOT=%~dp0..
set BURP_MCP_PLUGIN_ROOT=%ROOT%
set BURP_MCP_TRANSPORT=streamable-http
if "%BURP_MCP_SERVER_HOST%"=="" set BURP_MCP_SERVER_HOST=127.0.0.1
if "%BURP_MCP_SERVER_PORT%"=="" set BURP_MCP_SERVER_PORT=9640
if "%BURP_MCP_SERVER_PATH%"=="" set BURP_MCP_SERVER_PATH=/mcp
if defined PYTHON_EXE (
  "%PYTHON_EXE%" "%ROOT%\wsl-mcp\server.py" --transport streamable-http --host "%BURP_MCP_SERVER_HOST%" --port "%BURP_MCP_SERVER_PORT%" --path "%BURP_MCP_SERVER_PATH%"
) else (
  python "%ROOT%\wsl-mcp\server.py" --transport streamable-http --host "%BURP_MCP_SERVER_HOST%" --port "%BURP_MCP_SERVER_PORT%" --path "%BURP_MCP_SERVER_PATH%"
)
