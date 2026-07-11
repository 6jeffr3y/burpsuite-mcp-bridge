# BurpSuite MCP Bridge v2.1.0 Release Notes

[简体中文](RELEASE_NOTES_v2.1.0.md)

Version 2.1.0 adds bounded request/response interception and consolidates the extension interface. The release was validated with Burp Suite Professional `2026.4.2` and retains Montoya API `2025.10` as its compile baseline.

## Key advantages and new capabilities

### Request and response interception

A rewrite rule with `action="intercept"` can now hold a matching Proxy request or response.

- `intercept_mode="burp"` routes the message to Burp Proxy Intercept for manual review and editing.
- `intercept_mode="mcp"` routes the message to a bounded pending queue for disposition through `burp_intercept_poll` and `burp_intercept_decide`.
- Supported decisions are `forward`, `replace`, and `drop`.

### Target overview focus

`burp_target_overview` now accepts:

```text
focus=default|auth|logic|upload|data
```

The focus value changes candidate ranking and annotations; it does not make a vulnerability determination.

## Reliability and control boundaries

- Pending queue capacity is bounded.
- Messages without a decision before the configured timeout are forwarded unchanged.
- Unloading the extension releases all pending messages.
- Temporary rules support `ttl_seconds`, `max_matches`, and `auto_disable`.
- Match counters are applied in memory before debounced persistence to avoid exceeding a rule limit during concurrent traffic.

For one-off validation, use an exact host/path match with `max_matches=1` and `auto_disable=true`.

## Interface changes

The Burp extension interface now exposes three primary views:

- **Overview:** runtime status, configuration summary, and buffer state.
- **Intercept:** pending-message and intercept configuration status.
- **Rules:** rewrite and intercept rule management.

Low-frequency diagnostic details and internal rule identifiers were removed from the primary view. They remain available through status and rule APIs where required.

## Compatibility

| Component | Baseline |
| --- | --- |
| Burp Suite | Professional `2026.4.2` |
| Java | 21 |
| Montoya compile API | `2025.10` |
| Python | `3.11+` |
| MCP transport | stdio; optional Streamable HTTP |

Optional APIs introduced after the compile baseline are enabled only after runtime capability checks.

## Upgrade procedure

1. Replace the loaded extension with `burp-plugin/burpsuite-mcp-bridge-2.1.0-all.jar`.
2. Restart the Python MCP adapter so that the client receives the updated tool schema.
3. Start a new MCP client session.
4. Call `burp_bridge_status` and verify the reported version, queue limits, and last error.
5. Confirm that existing rewrite rules are expected before enabling traffic processing.

## Verification sequence

A minimal intercept verification uses a non-destructive, one-match rule:

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

After the test, confirm that the rule is disabled and the pending queue is empty.

## Release artifacts

- Versioned and `latest` extension JARs
- Python MCP adapter
- Codex/MCP client configuration examples
- MCP operation skill and references
- SHA-256 checksum manifest
- CycloneDX SBOM

## Documentation

- Installation and tool reference: `README.md`, `README_EN.md`
- Intercept procedure: `docs/intercept-workflow_EN.md`
- Compatibility matrix: `docs/compatibility_EN.md`
- Change history: `CHANGELOG.md`, `CHANGELOG_EN.md`
- Artifact integrity: `SHA256SUMS-2.1.0.txt`, `bom.json`
