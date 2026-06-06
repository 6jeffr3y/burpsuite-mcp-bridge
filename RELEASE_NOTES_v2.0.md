# BurpSuite MCP Bridge v2.0

## 重点更新

- `Ignore asset responses / 忽略低价值静态响应` 已升级为只过滤低价值静态响应：请求保留，JS/SourceMap/WASM 保留。
- 新增/完善按 host 读取 Burp 注释和高亮颜色的高价值索引：`burp_marked_flows(host=...)`。
- live/logger/selection/history 列表类接口默认 compact-first，减少 MCP 上下文压力；完整包通过 flow detail 或 raw bundle 获取。
- Selection/HotKey/右键捕获支持一次性交给 AI，并可自动消费 selection buffer。
- Rewrite Rule 增强 `ttl_seconds`、`max_matches`、`auto_disable` 与命中计数 debounce 持久化。
- `burp_mcp_list` 覆盖全部工具，支持按 section/topic 分级查看使用方法。
- README 改为中文优先正式说明，补充架构流程图和推荐 AI 工作流。

## 发布资产

- `burp-plugin/burpsuite-mcp-bridge-2.0-all.jar`
- `burp-plugin/burpsuite-mcp-bridge-latest.jar`
- `wsl-mcp/server.py`
- `config-examples/` 下四类 Codex 配置示例：WSL mirrored、WSL NAT、Windows、macOS

## 测试基线

- Burp Suite Professional `2026.4.2`
- 编译基线：`montoya-api 2025.10`

## 升级建议

1. 用 `burp-plugin/burpsuite-mcp-bridge-latest.jar` 替换 Burp 中已加载的旧 JAR。
2. Codex/MCP 配置继续直接启动 `wsl-mcp/server.py`，通过 `BURP_MCP_BRIDGE_URL` 指定完整 bridge URL。
3. 若 AI 工具列表未刷新，重启 MCP 客户端或 Codex 会话。
