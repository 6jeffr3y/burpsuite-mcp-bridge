# 请求与响应双向拦截

[English](en/intercept-workflow.md)

本文档描述 Proxy request/response 的两种拦截路径、最小操作顺序和恢复边界。拦截规则只作用于 Proxy 流量；工具调用成功不代表业务状态或安全影响已经成立。

## 模式选择

| 模式 | 适用场景 | 操作边界 |
| --- | --- | --- |
| `intercept_mode="mcp"` | 需要通过 MCP 接口读取并处理匹配消息 | MCP 客户端读取 pending 消息并执行 `forward`、`replace` 或 `drop` |
| `intercept_mode="burp"` | 人工检查复杂报文、使用 Burp 原生编辑器精细修改 | 消息进入 Proxy Intercept，由测试人员编辑和 Forward |

两种模式共用 Rewrite Rule 的 host、path、method、content-type 等匹配条件，以及 `ttl_seconds`、`max_matches`、`auto_disable` 生命周期约束。

## MCP 控制的响应修改

```python
burp_rule_upsert(
    direction="response",
    action="intercept",
    intercept_mode="mcp",
    match_host_contains="example.com",
    match_path_contains="/api/login",
    max_matches=1,
    auto_disable=True,
)

pending = burp_intercept_poll(direction="response", include_bodies=True)

burp_intercept_decide(
    intercept_id="<pending interceptId>",
    action="replace",
    body_replace_from='"success":false',
    body_replace_to='"success":true',
)
```

使用 `action="forward"` 原样放行，使用 `action="drop"` 丢弃当前消息。pending 消息超过等待时间后自动原样放行；插件卸载时也会释放全部等待消息。

## MCP 控制的请求修改

请求方向的使用方式相同。可通过 `headers_set` 修改或增加请求头，也可以使用 `body_replace_from`/`body_replace_to` 定点替换请求体：

```python
burp_rule_upsert(
    direction="request",
    action="intercept",
    intercept_mode="mcp",
    match_host_contains="example.com",
    match_path_contains="/api/profile",
    max_matches=1,
    auto_disable=True,
)

pending = burp_intercept_poll(direction="request", include_bodies=True)

burp_intercept_decide(
    intercept_id="<pending interceptId>",
    action="replace",
    headers_set={"X-Test-Case": "logic-001"},
    body_replace_from='"role":"user"',
    body_replace_to='"role":"admin"',
)
```

## Burp 原生编辑

将 `intercept_mode` 设置为 `burp`。匹配的 request 或 response 会进入 Burp Proxy Intercept，使用 Burp 原生控件检查、编辑并放行。

## 最小操作顺序

1. 使用 `burp_target_overview(host="...", focus="logic")` 收敛候选业务流量；
2. 拉取候选 flow 的完整报文，精确确定 host、path、direction 和待修改字段；
3. 创建 `max_matches=1`、`auto_disable=True` 的一次性规则；
4. 触发且仅触发一次目标业务请求；
5. 轮询 pending 队列并核对 `interceptId`、URL、原始 body；
6. 执行 `replace`、`forward` 或 `drop`；
7. 观察浏览器后续请求与服务端状态，而不仅是当前页面展示；
8. 删除临时规则并确认 pending 数量归零。

## 运行约束

- 匹配条件应至少约束 host 和 path，避免拦截整站静态资源；
- 首次验证优先使用一次性规则，确认行为后再扩大 `max_matches`；
- 大报文先通过 overview/flow detail 确认目标字段，再决定是否包含 body 轮询；
- 自动超时放行属于故障恢复机制，不应作为正常决策路径；
- 修改响应只能证明客户端行为受到影响时，应继续检查后续请求或服务端状态，避免把纯前端显示变化误判为服务端权限变化。
