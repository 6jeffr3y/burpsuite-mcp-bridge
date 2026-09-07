# 贡献指南

[English](docs/en/contributing.md)

本仓库用于发布 BurpSuite MCP Bridge 的版本化构建产物、Python MCP Adapter、客户端配置示例及操作文档，不包含 Burp 扩展的完整构建工程。

## 文档与配置变更

欢迎通过 Pull Request 提交文档修正和部署示例。请保持 `README.md` 与 `README_EN.md` 的结构和含义一致，使用通用路径与示例主机，不要提交真实流量、凭据、令牌或本地环境信息。

提交前至少执行：

```bash
python3 -m py_compile mcp-server/server.py
python3 -m json.tool .codex-plugin/plugin.json >/dev/null
python3 -m json.tool .mcp.json >/dev/null
cd dist && sha256sum -c SHA256SUMS
```

## 运行时变更

运行时功能应在构建工程中完成实现、测试和版本化，再同步到本发布仓库。每次发布必须包含：

- 不可变的版本化扩展 JAR；
- 工具 schema 变化时同步更新 Python MCP Adapter；
- SHA-256 校验清单与 CycloneDX SBOM；
- 针对文档所列基线版本的兼容性验证；
- 所有 Proxy 阻塞路径的容量边界、超时恢复与卸载释放机制。

已有 flow、rule、intercept 或 evidence 抽象能够表达操作时，不应新增语义重叠的 MCP 工具。

## Pull Request 要求

- 说明变更目的、影响范围和验证步骤；
- 文档中的命令、路径和工具名称必须可复现；
- 中英文文档应在同一提交中同步；
- 不提交缓存文件、临时导出、测试流量或未版本化二进制文件。

## 依赖锁定与插件扫描

`requirements.txt` 声明支持的依赖范围；`mcp-server/requirements.lock` 锁定 Python 3.12 的跨平台完整依赖集及下载哈希。更新依赖时，在 Python 3.12 虚拟环境中安装 `uv`，然后重新生成并验证：

```bash
uv pip compile --universal --python-version 3.12 --generate-hashes --output-file mcp-server/requirements.lock requirements.txt
python3 -m pip install --require-hashes -r requirements.lock
python3 -m pip check
python3 -m unittest discover -s tests -v
```

`.github/workflows/hol-plugin-scanner.yml` 在 `main` 的 push 和 pull request 上运行 HOL Plugin Scanner，要求分数至少为 80，且没有 high 或 critical 级别发现。所有 Actions 固定到完整提交 SHA；Dependabot 每周检查 Actions 与 Python 依赖更新。

当前适配器使用 MCP SDK 1.x 的 `FastMCP` API，因此依赖范围暂时限制为 `mcp<2`。stdio 冒烟测试验证初始化和工具发现，不访问 Burp 或目标网络。

根目录 `requirements.lock` 转发到上述锁文件。manifest 显式声明 `scripts` 和 `skills` 路径，以便目录生成器自动包含适配器、依赖锁和操作指南，无需手工复制插件包。
