# Compatibility

[简体中文](../compatibility.md)

| Component | Baseline |
| --- | --- |
| Burp Suite | Professional 2026.4.2 |
| Java | 21 |
| Montoya compile API | 2025.10 |
| Python | 3.11+ |
| MCP transport | stdio; optional Streamable HTTP |

The extension compiles against Montoya 2025.10 and enables newer optional APIs
through runtime capability checks. A release is not complete until request and
response capture, replay, native Burp intercept, MCP pending intercept, rule
auto-disable, and unload cleanup pass on Burp 2026.4.2.
