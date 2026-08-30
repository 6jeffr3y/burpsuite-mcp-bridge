# Request and response interception

[简体中文](../intercept-workflow.md)

This document defines the two interception paths, the minimum operating sequence, and the recovery boundaries for Proxy requests and responses. Intercept rules apply only to Proxy traffic. A completed interception operation does not by itself establish a business-state change or security impact.

## Mode selection

| Mode | Use case | Execution boundary |
| --- | --- | --- |
| `intercept_mode="mcp"` | The MCP client must retrieve and process a matching message | The client reads the pending message and decides `forward`, `replace`, or `drop` |
| `intercept_mode="burp"` | The message requires manual review or precise editing in Burp | The message enters Proxy Intercept and is edited and forwarded by the operator |

Both modes use the Rewrite Rule match fields for host, path, method, content type, and other message attributes. They also share the `ttl_seconds`, `max_matches`, and `auto_disable` lifecycle controls.

## MCP-controlled response handling

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

Use `action="forward"` to release the original message and `action="drop"` to terminate it. A pending message is forwarded unchanged when the decision timeout expires. Unloading the extension also releases all pending messages.

## MCP-controlled request handling

Request handling uses the same rule model. `headers_set` can add or replace headers; `body_replace_from` and `body_replace_to` perform an explicit body substitution.

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

## Burp-native editing

Set `intercept_mode="burp"`. A matching request or response enters Burp Proxy Intercept and can be reviewed, edited, and forwarded with Burp's native controls.

## Minimum operating sequence

1. Use `burp_target_overview(host="...", focus="logic")` to narrow the candidate traffic.
2. Retrieve the complete candidate flow and confirm the host, path, direction, and target field.
3. Create a one-match rule with `max_matches=1` and `auto_disable=True`.
4. Trigger exactly one target operation.
5. Poll the pending queue and verify the intercept ID, URL, and original message.
6. Decide `replace`, `forward`, or `drop`.
7. Compare the next client request and server-side state with the baseline; do not rely only on the current rendered page.
8. Delete the temporary rule and confirm that the pending count is zero.

## Operational constraints

- Match at least the target host and path. Do not intercept all site traffic with a broad `/` match.
- Begin with a one-match rule and increase the limit only after the match behavior is confirmed.
- For large messages, inspect the overview and flow detail before requesting bodies from the pending queue.
- Automatic forward-on-timeout is a recovery mechanism, not a normal decision path.
- A modified response may demonstrate only a client-side behavior change. Verify subsequent requests or server-side state before reporting an authorization or workflow impact.
