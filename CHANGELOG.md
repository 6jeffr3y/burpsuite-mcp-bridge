# 更新日志

本文档记录 BurpSuite MCP Bridge 的用户可见变更。

## 未发布

### 仓库结构

- 将跨平台 Python Adapter 从 `wsl-mcp/` 更名为 `mcp-server/`，并采用常规的 `requirements.txt`。
- 将 JAR、校验清单与 CycloneDX SBOM 收敛到 `dist/`；删除与版本化 JAR 字节相同的 `latest` 副本。
- 将英文参考文档集中到 `docs/en/`，版本说明集中到 `docs/releases/`，并合并双语 NOTICE。

### 文档

- 按设计范围、运行边界、安装、证据处理和发布完整性重写英文与简体中文 README。
- 将拦截和兼容性说明拆分为英文、简体中文文档。
- 把客户端配置示例中的开发机路径替换为通用安装路径。
- 明确本仓库用于分发发布文件，不包含 Burp 扩展构建工程。
- 默认文档统一使用简体中文，英文版本统一使用 `_EN` 后缀。
- 删除旧版本 JAR、冗余历史发布说明和空 `artifacts` 占位目录；历史变更继续由本文件记录。

## 2.1.0

### 新增

- 新增 request/response 双向拦截规则，支持 `intercept_mode="mcp|burp"`。
- 新增有界 pending queue、超时自动原样放行和卸载清理。
- 新增 `burp_intercept_poll`、`burp_intercept_decide`，支持 `forward`、`replace`、`drop`。
- `burp_target_overview` 新增 `focus=default|auth|logic|upload|data`。

### 变更

- 扩展界面收敛为 Overview、Intercept、Rules。
- 发布流程增加 Java 和 Python 校验。
- 兼容性验证基线设为 Burp Suite Professional `2026.4.2`。

## 2.0.1

### 修复

- `burp_replay_flow`、`burp_rule_upsert` 的 `body` 参数兼容 JSON object/list；MCP adapter 会在转发给 Bridge 前序列化可兼容的 JSON 值。

### 新增

- history、live、logger、selection、target overview 和 marked flows 支持时间窗口过滤。
- `burp_history_search` 新增 `time_from`、`time_to`、`sort=newest|oldest`。
- live、logger、selection poll 工具新增 `created_from`、`created_to` 和排序参数。

## 2.0

### 变更

- **Ignore asset responses** 调整为过滤低价值静态响应，同时保留请求以及 JavaScript、SourceMap、WebAssembly 响应。
- live、logger、selection、history 列表接口改为 compact-first，完整报文按 flow ID 获取。
- Selection 支持通过右键菜单、HotKey、command palette 捕获，并可选择是否消费已读取记录。
- Rewrite Rule 新增 `ttl_seconds`、`max_matches`、`auto_disable` 和命中计数 debounce 持久化。
- `burp_mcp_list` 支持按 section/topic 获取工具文档。

### 新增

- 新增 `burp_marked_flows(host=...)`，按 host 读取带 comment 或 highlight 的 flow。
- 增加架构、操作流程和证据处理文档。

### 兼容性

- Montoya 编译基线：`2025.10`。
- Burp Suite 验证基线：Professional `2026.4.2`。

## 1.1.0

### 新增

- 新增按 host 聚合流量的 `burp_target_overview`。
- 新增分级工具说明 `burp_mcp_list`。
- Rewrite Rule 支持可执行的 `modify`、`drop`、`spoof` 动作。
- Rule scope 支持 `proxy`、`tool`、`all`。
- 在运行时能力可用时接入 Selection 捕获、内部 HTTP 工具 drop/spoof、BCheck 导入和 Bambda 导入。

### 变更

- MCP 配置简化为直接启动 `wsl-mcp/server.py` 并设置 `BURP_MCP_BRIDGE_URL`。

## 1.0.0

### 新增

- 首个 Windows Burp 到 WSL/本地 MCP Bridge 发布版本。
- 支持 Proxy 与 logger-like 流量读取。
- 支持重放、Rewrite Rule、Repeater 联动和原始证据导出。
