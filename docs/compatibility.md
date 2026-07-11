# 兼容性

[English](compatibility_EN.md)

| 组件 | 基线 |
| --- | --- |
| Burp Suite | Professional 2026.4.2 |
| Java | 21 |
| Montoya 编译 API | 2025.10 |
| Python | 3.11+ |
| MCP transport | stdio；可选 Streamable HTTP |

扩展以 Montoya `2025.10` 为编译基线，并通过运行时能力检测启用后续版本中的可选 API。

发布前必须在 Burp Suite Professional `2026.4.2` 上验证以下路径：

- request/response 捕获；
- flow detail 和重放；
- Burp 原生 Intercept；
- MCP pending intercept；
- rule auto-disable；
- timeout 和 unload 清理。
