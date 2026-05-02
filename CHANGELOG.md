# Changelog

## 1.0.0

### Highlights
- Simple configuration for **Windows Burp ↔ WSL Codex / Agent AI / MCP CLI / IDE** communication.
- Reads both **Burp Proxy traffic** and **Burp internal HTTP tool / extension / fuzz traffic**.
- Supports **request replay with mutation**, **request/response rewrite rules**, **Repeater handoff**, and **safe evidence export**.
- Supports both **stdio MCP** and **Streamable HTTP MCP** transports.

### Stability / Performance
- loopback-only bridge by default
- bounded worker pool and bounded queued clients
- bounded live/logger ring buffers
- preview-only body extraction for detail responses
- temp-file backed copies for captured live/logger request/response objects
- large-body-safe search path using Burp/Montoya `contains()`
- request/response body mutation size guards
- logger buffer clear support
- raw request/response bundle export for oversized flows

### Tested Baseline
- Burp Suite Professional 2025.10.3
