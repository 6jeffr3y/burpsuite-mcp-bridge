# 更新日志

## 1.0.0

### 核心特性
- 支持 **Windows Burp ↔ WSL Codex / Agent AI / MCP CLI / IDE** 的简单通信。
- 同时读取：
  - **Burp Proxy 流量**
  - **Burp 内部 HTTP 工具 / 扩展 / fuzz 流量**
- 支持：
  - 请求重放与改包
  - 请求 / 响应自动改写规则
  - Repeater 联动
  - 安全证据导出
- 同时支持：
  - **stdio MCP**
  - **Streamable HTTP MCP**

### 稳定性 / 性能
- 默认 loopback-only bridge
- 有界 worker pool 与队列上限
- 有界 live/logger ring buffer
- detail 返回采用 preview-only body 提取策略
- live/logger 捕获对象优先转为 temp-file backed copy
- 大包搜索优先使用 Burp/Montoya 原生 `contains()`
- request/response body 改写增加大小保护
- 支持清空 logger buffer
- 支持在超大 flow 场景下导出完整 request/response bundle

### 已验证基线
- Burp Suite Professional 2025.10.3
