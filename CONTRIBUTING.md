# Contributing

## Baseline

- Java 21
- `montoya-api 2025.10`
- Compatibility test baseline: Burp Suite Professional `2026.4.2`
- Python 3.11+

## Before submitting a change

```bash
python3 scripts/check_versions.py
python3 -m py_compile wsl-mcp/server.py
python3 -m unittest discover -s tests -v
mvn -f burp-extension/pom.xml verify
```

Keep list/search tools compact by default. Reuse existing mutation, rule, and
flow abstractions rather than adding overlapping MCP tools. New Proxy blocking
paths must be bounded and must automatically release on timeout and unload.
