# BurpSuite MCP Bridge v2.1.0 发布说明

[English](RELEASE_NOTES_v2.1.0_EN.md)

v2.1.0 增加有边界的 request/response 双向拦截，并收敛扩展界面。本版本以 Burp Suite Professional `2026.4.2` 为验证基线，Montoya API 编译基线保持 `2025.10`。

## 核心优势与新增能力

### 请求与响应双向拦截

设置 `action="intercept"` 的 Rewrite Rule 可以暂停匹配的 Proxy request 或 response。

- `intercept_mode="burp"`：消息进入 Burp Proxy Intercept，由测试人员使用原生界面检查和编辑。
- `intercept_mode="mcp"`：消息进入有界 pending queue，通过 `burp_intercept_poll` 和 `burp_intercept_decide` 处理。
- 支持的决策为 `forward`、`replace`、`drop`。

### 目标概览聚焦策略

`burp_target_overview` 新增：

```text
focus=default|auth|logic|upload|data
```

`focus` 只影响候选 flow 的排序和注释，不直接给出漏洞结论。

## 可靠性与操作边界

- pending queue 设置容量上限；
- 超过决策超时的消息按原文放行；
- 卸载扩展时释放全部 pending 消息；
- 临时规则支持 `ttl_seconds`、`max_matches`、`auto_disable`；
- 命中计数先在内存中生效，再执行 debounce 持久化，避免并发流量超过规则限制。

一次性验证应使用精确的 host/path 条件，并设置 `max_matches=1`、`auto_disable=true`。

## 界面变更

Burp 扩展界面收敛为三个主要视图：

- **Overview：** 运行状态、配置摘要和缓冲区状态；
- **Intercept：** pending message 和拦截配置状态；
- **Rules：** Rewrite Rule 与 Intercept Rule 管理。

低频诊断信息和内部 rule ID 不再占用主界面，需要时仍可通过状态和规则接口获取。

## 兼容性

| 组件 | 基线 |
| --- | --- |
| Burp Suite | Professional `2026.4.2` |
| Java | 21 |
| Montoya 编译 API | `2025.10` |
| Python | `3.11+` |
| MCP transport | stdio；可选 Streamable HTTP |

编译基线之后增加的可选 API 仅在运行时能力检测通过后启用。

## 升级步骤

1. 使用 `burp-plugin/burpsuite-mcp-bridge-2.1.0-all.jar` 替换已加载扩展。
2. 重启 Python MCP adapter，使客户端获取新的工具 schema。
3. 新建 MCP 客户端会话。
4. 调用 `burp_bridge_status`，核对版本、queue 限制和最近错误。
5. 在启用流量处理前确认已有 Rewrite Rule 符合预期。

## 最小验证

使用一条非破坏、单次命中的规则验证拦截路径：

```python
burp_rule_upsert(
    direction="response",
    action="intercept",
    intercept_mode="mcp",
    match_host_contains="example.com",
    match_path_contains="/api/test",
    max_matches=1,
    auto_disable=True,
)

pending = burp_intercept_poll(direction="response", include_bodies=True)

burp_intercept_decide(
    intercept_id="<interceptId>",
    action="forward",
)
```

验证后确认规则已经禁用，pending queue 数量为零。

## 发布文件

- 版本化扩展 JAR 与 `latest` JAR；
- Python MCP adapter；
- Codex/MCP 客户端配置示例；
- MCP 操作 Skill 与 references；
- SHA-256 校验清单；
- CycloneDX SBOM。

## 文档

- 安装和工具说明：`README.md`、`README_EN.md`
- 拦截流程：`docs/intercept-workflow.md`、`docs/intercept-workflow_EN.md`
- 兼容性：`docs/compatibility.md`、`docs/compatibility_EN.md`
- 变更历史：`CHANGELOG.md`、`CHANGELOG_EN.md`
- 发布完整性：`SHA256SUMS-2.1.0.txt`、`bom.json`
