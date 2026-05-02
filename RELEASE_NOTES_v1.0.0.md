# BurpSuite MCP Bridge v1.0.0

## Highlights
- Simple MCP connectivity for **Windows Burp Suite ↔ WSL / Windows Agent-AI / MCP CLI / IDE**.
- Supports both **stdio MCP** and **Streamable HTTP MCP**.
- Reads both **Burp Proxy traffic** and **Burp internal HTTP tool / extension / fuzz traffic**.
- Supports **request replay with mutation**, **temporary request/response rewrite rules**, **Repeater handoff**, and **raw request/response bundle export**.

## Why it is useful
- Works well for **Windows Burp + WSL Codex** workflows.
- Avoids depending on Burp's official stdio proxy-jar workflow for mixed Windows / WSL environments.
- Gives AI clients a lower-noise path into Burp traffic, replay, and verification workflows.

## Included assets
- `burpsuite-mcp-bridge-latest.jar`
- `burpsuite-mcp-bridge-1.0.0-all.jar`

## Tested baseline
- Burp Suite Professional `2025.10.3`
