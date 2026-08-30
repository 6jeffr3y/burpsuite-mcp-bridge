# Changelog

This file records user-visible changes to BurpSuite MCP Bridge.

## Unreleased

### Repository layout

- Renamed the cross-platform Python adapter from `wsl-mcp/` to `mcp-server/` and adopted the conventional `requirements.txt` name.
- Colocated the JAR, checksum manifest, and CycloneDX SBOM under `dist/`; removed the byte-identical `latest` JAR alias.
- Grouped English references under `docs/en/`, release notes under `docs/releases/`, and consolidated NOTICE into one bilingual file.

### Documentation

- Reworked the English and Simplified Chinese READMEs around design scope, operational boundaries, installation, evidence handling, and release integrity.
- Split the intercept and compatibility references into English and Simplified Chinese documents.
- Replaced development-machine paths in client configuration examples with generic installation paths.
- Clarified that this repository distributes release artifacts and does not contain the Burp extension build project.
- Standardized Simplified Chinese as the default documentation language and `_EN` as the English suffix.
- Removed superseded JARs, redundant historical release notes, and the empty `artifacts` placeholder; this changelog remains the historical record.

## 2.1.0

### Added

- Added request and response interception rules with `intercept_mode="mcp|burp"`.
- Added a bounded pending queue with automatic forward-on-timeout and unload cleanup.
- Added `burp_intercept_poll` and `burp_intercept_decide` with `forward`, `replace`, and `drop` decisions.
- Added `focus=default|auth|logic|upload|data` to `burp_target_overview`.

### Changed

- Reduced the extension interface to the Overview, Intercept, and Rules views.
- Added Java and Python verification to the release workflow.
- Set the compatibility validation baseline to Burp Suite Professional `2026.4.2`.

## 2.0.1

### Fixed

- `burp_replay_flow` and `burp_rule_upsert` now accept JSON object or array values for `body`; the MCP adapter serializes JSON-compatible values before forwarding them to the bridge.

### Added

- Added time-window filtering to history, live, logger, selection, target overview, and marked-flow retrieval.
- Added `time_from`, `time_to`, and `sort=newest|oldest` to `burp_history_search`.
- Added `created_from`, `created_to`, and sort options to the live, logger, and selection poll tools.

## 2.0

### Changed

- **Ignore asset responses** now filters low-value static responses while retaining requests and JavaScript, SourceMap, and WebAssembly responses.
- List operations for live, logger, selection, and history now use compact-first responses. Complete messages are retrieved by flow ID.
- Selection capture now supports context-menu, hotkey, and command-palette handoff with optional consumption of the selected entry.
- Rewrite rules now support `ttl_seconds`, `max_matches`, `auto_disable`, and debounced match-count persistence.
- `burp_mcp_list` now exposes tool documentation by section and topic.

### Added

- Added `burp_marked_flows(host=...)` for retrieving commented or highlighted flows by host.
- Added architecture, operation, and evidence-handling documentation.

### Compatibility

- Montoya compile baseline: `2025.10`.
- Burp Suite validation baseline: Professional `2026.4.2`.

## 1.1.0

### Added

- Added `burp_target_overview` for host-oriented traffic correlation.
- Added staged tool documentation through `burp_mcp_list`.
- Added functional `modify`, `drop`, and `spoof` rewrite actions.
- Added `proxy`, `tool`, and `all` rule scopes.
- Added runtime integration with selection capture, internal-tool drop/spoof, BCheck import, and Bambda import when supported by the loaded Burp version.

### Changed

- Simplified MCP configuration to run `wsl-mcp/server.py` directly with `BURP_MCP_BRIDGE_URL`.

## 1.0.0

### Added

- Initial Windows Burp to WSL/local MCP bridge release.
- Added Proxy and logger-like traffic retrieval.
- Added replay, rewrite rules, Repeater handoff, and raw evidence export.
