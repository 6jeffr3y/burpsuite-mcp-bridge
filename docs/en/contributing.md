# Contributing

[简体中文](../../CONTRIBUTING.md)

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
python3 -m py_compile mcp-server/server.py
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .mcp.json >/dev/null
cd dist && sha256sum -c SHA256SUMS
```

## Runtime changes

Runtime changes must be implemented, tested, and versioned in the build project
before they are synchronized to this release repository. Each release must
provide:

- an immutable, versioned extension JAR;
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

## Dependency locking and plugin scanning

`requirements.txt` declares the supported dependency range; `requirements.lock` pins the complete cross-platform Python 3.12 dependency set and download hashes. To update dependencies, install `uv` in a Python 3.12 virtual environment, then regenerate and verify the lockfile:

```bash
uv pip compile --universal --python-version 3.12 --generate-hashes --output-file requirements.lock requirements.txt
python3 -m pip install --require-hashes -r requirements.lock
python3 -m pip check
python3 -m unittest discover -s tests -v
```

`.github/workflows/hol-plugin-scanner.yml` runs HOL Plugin Scanner on pushes and pull requests targeting `main`, requiring a score of at least 80 and no high or critical findings. All Actions are pinned to full commit SHAs; Dependabot checks Actions and Python dependencies weekly.

The adapter currently uses the MCP SDK 1.x `FastMCP` API, so the dependency range is capped at `mcp<2`. The stdio smoke test verifies initialization and tool discovery without accessing Burp or target networks.
