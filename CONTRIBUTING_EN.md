# Contributing

[简体中文](CONTRIBUTING.md)

This repository publishes versioned BurpSuite MCP Bridge artifacts, the Python
MCP adapter, client configuration examples, and operating documentation. It
does not contain the complete Burp extension build project.

## Documentation and configuration changes

Documentation corrections and deployment examples are accepted through pull
requests. Keep `README.md` and `README_EN.md` aligned, use generic paths and
hosts, and do not include captured traffic, credentials, tokens, or local
environment details.

Run at least:

```bash
python3 -m py_compile wsl-mcp/server.py
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .mcp.json >/dev/null
sha256sum -c SHA256SUMS-2.1.0.txt
```

## Runtime changes

Runtime changes must be implemented, tested, and versioned in the build project
before they are synchronized to this release repository. Each release must
provide:

- a versioned extension JAR and a content-identical `latest` JAR;
- an updated Python MCP adapter when the tool schema changes;
- SHA-256 checksums and a CycloneDX SBOM;
- compatibility verification against the documented baseline;
- capacity limits, timeout recovery, and unload release behavior for every
  Proxy-blocking path.

Do not add a new MCP tool when an existing flow, rule, intercept, or evidence
abstraction already represents the operation.

## Pull request requirements

- State the purpose, affected components, and verification steps.
- Keep commands, paths, and tool names reproducible.
- Update English and Simplified Chinese documents in the same change.
- Do not replace versioned release artifacts in a documentation-only change.
