# 更新日志

## 2.0

### 重点更新
- UI `Ignore asset responses / 忽略低价值静态响应` 已对应新语义：只过滤 CSS/图片/字体/音视频/ico/PDF/压缩包等低价值响应；请求保留；JavaScript、SourceMap、WASM 保留。
- 新增/完善 `burp_marked_flows(host=...)`，可按指定 host 查看带注释或高亮颜色的关键流量索引。
- live/logger/selection/history 的列表类接口默认 compact-first，先返回关键元数据，完整请求/响应再按 flow id 拉取。
- Selection/HotKey/右键捕获支持一次性交给 AI，`burp_selection_get` 默认消费对应 selection buffer，减少重复分析。
- Rewrite Rule 增强 `ttl_seconds`、`max_matches`、`auto_disable`，命中计数持久化加入 debounce，并发命中时先在内存中原子计数。
- `burp_mcp_list` 覆盖全部 MCP 工具，支持按 section/topic 分级取用帮助。
- README 改为中文优先正式描述，并补充架构流程图与推荐 AI 工作流。

### 稳定性 / 兼容性
- 编译基线保持 `montoya-api 2025.10`。
- 2026.4.x 能力继续运行时检测，兼容旧版本基础能力。
- 列表接口默认避免返回完整 body；大包证据继续通过 raw bundle 导出。

### 测试基线
- Burp Suite Professional 2026.4.2

## 1.1.0

### 重点更新
- 新增目标视角流量画像：`burp_target_overview`。
- 新增分级 MCP 帮助：`burp_mcp_list`。
- 改写规则动作真正落地：`modify`、`drop`、`spoof`。
- 规则作用面支持：`proxy`、`tool`、`all`。
- 接入 Burp 2026.4.x 运行时检测能力：HotKey/command palette selection 捕获、internal-tool drop/spoof、BCheck 导入、Bambda 导入。
- 增强 Burp UI：自检、命令复制、规则 UX。
- 简化配置：示例直接启动 `wsl-mcp/server.py` 并设置 `BURP_MCP_BRIDGE_URL`；release 包移除 wrapper 脚本。

## 1.0.0

### 重点更新
- 初始发布，支持 Windows Burp ↔ WSL Codex / Agent AI / MCP CLI / IDE 通信。
- 支持 Burp Proxy 流量与 logger-like 内部工具流量读取。
- 支持重放、改写规则、Repeater 联动和原始包导出。
