# BurpSuite MCP Bridge v2.1.0 发布说明

v2.1.0 面向 Burp Suite 与 Codex/Agent 的协同测试场景，重点补齐请求与响应的双向拦截、可控修改和恢复执行能力。本版本兼容性验证基线为 **Burp Suite Professional 2026.4.2**。

## 核心优势

### 1. 请求与响应双向拦截

同一套规则模型可作用于 Proxy request 和 response，并提供两种执行路径：

- **Burp Native Intercept**：命中后进入 Burp Proxy Intercept，由测试人员使用原生编辑器检查、修改并放行；
- **MCP-controlled Intercept**：命中后进入有界 pending queue，Agent 可读取原始消息并执行 `forward`、`replace` 或 `drop` 决策。

该设计既保留 Burp 原生交互体验，又支持 Agent 自动完成响应字段替换、请求参数调整和状态迁移验证，尤其适合客户端信任、前端鉴权、支付状态和业务流程控制等逻辑缺陷测试。

### 2. 可控且可恢复的自动化

- pending queue 设有容量边界，避免无限堆积造成 Proxy 链路阻塞；
- 超时未决消息自动按原文放行；
- 插件卸载时统一释放等待消息；
- 临时规则支持 `ttl_seconds`、`max_matches` 和 `auto_disable`，可限定生效窗口与命中次数。

相比无边界的自动改包脚本，该机制更适合持续运行的 Burp 工作区，也便于复现单次业务状态变更。

### 3. 目标中心的低噪声分析

`burp_target_overview` 将 Proxy History、Logger-like 流量、Selection、人工注释和高亮标记统一到目标视角；`focus="logic"` 会给出可解释的响应控制信号与 mutation ideas。Agent 可先定位高价值业务请求，再拉取完整报文或建立一次性拦截规则，减少无关静态资源和重复请求带来的上下文消耗。

### 4. Burp 原生能力兼容

插件继续以 Montoya API 为集成边界，并在运行时检测可用能力。v2.1.0 不重复实现 Repeater、Proxy Intercept 等成熟功能，而是通过统一 MCP 接口完成检索、定位和调度，具体编辑与人工确认仍可回到 Burp 原生工作流。

### 5. 可审计的交付物

发布包提供版本化 JAR、`latest` JAR、SHA-256 校验清单、CycloneDX SBOM、兼容性说明和专业 Codex Skill。关键操作可以通过 flow ID、规则 ID、intercept ID 与原始证据导出结果进行关联，便于复测和团队协作。

## 快速使用

### 1. 加载插件

在 Burp Suite 中进入 `Extensions -> Installed -> Add`，选择：

```text
burp-plugin/burpsuite-mcp-bridge-2.1.0-all.jar
```

插件加载后，在 `Burp MCP` 页签确认 Bridge 状态为运行中。默认 HTTP Bridge 地址为 `http://127.0.0.1:9639`。

### 2. 配置 MCP Server

安装依赖：

```bash
python3 -m pip install -r requirements-wsl.txt
```

将 `config-examples/` 中与运行环境对应的配置复制到 Codex/MCP 客户端配置文件，并把 `wsl-mcp/server.py` 路径替换为实际发布仓库路径。

### 3. 建立目标概览

```python
burp_health()
burp_target_overview(host="example.com", focus="logic")
```

先根据 overview 返回的候选 flow ID 拉取完整请求/响应，确认目标、路径及响应字段，再创建拦截规则。

### 4. MCP 控制的响应修改

```python
burp_rule_upsert(
    direction="response",
    action="intercept",
    intercept_mode="mcp",
    match_host_contains="example.com",
    match_path_contains="/api/order/confirm",
    max_matches=1,
    auto_disable=True,
)

pending = burp_intercept_poll(direction="response", include_bodies=True)

burp_intercept_decide(
    intercept_id="<interceptId>",
    action="replace",
    body_replace_from='"success":false',
    body_replace_to='"success":true',
)
```

不修改时使用 `action="forward"`；需要终止该消息时使用 `action="drop"`。建议逻辑漏洞验证默认采用 `max_matches=1`，避免页面并发资源被连续拦截。

### 5. 使用 Burp 原生编辑器

将规则的 `intercept_mode` 设为 `burp`。匹配的 request/response 将进入 Burp Proxy Intercept，可使用原生消息编辑器修改后点击 Forward。

### 6. 验证与清理

完成测试后检查规则命中计数及 pending 状态，禁用或删除不再使用的临时规则，并导出关键 flow 的原始请求/响应作为复测证据。

## 完整文档

- 安装、工具分组与工作流：`README.md`
- 双向拦截操作手册：`docs/intercept-workflow.md`
- 兼容性矩阵：`docs/compatibility.md`
- Codex 专业使用 Skill：`skills/use-burpsuite-mcp-bridge/SKILL.md`
- 文件完整性：`SHA256SUMS-2.1.0.txt`
- 软件物料清单：`bom.json`
