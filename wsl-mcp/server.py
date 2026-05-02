from __future__ import annotations

import argparse
import json
import os
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

from mcp.server.fastmcp import FastMCP

_NO_PROXY_OPENER = urllib.request.build_opener(urllib.request.ProxyHandler({}))
DEFAULT_HOST = os.environ.get("BURP_MCP_BRIDGE_HOST", "127.0.0.1")
DEFAULT_PORT = int(os.environ.get("BURP_MCP_BRIDGE_PORT", "9639"))
MCP_TRANSPORT = os.environ.get("BURP_MCP_TRANSPORT", "stdio")
MCP_SERVER_HOST = os.environ.get("BURP_MCP_SERVER_HOST", "127.0.0.1")
MCP_SERVER_PORT = int(os.environ.get("BURP_MCP_SERVER_PORT", "9640"))
MCP_SERVER_PATH = os.environ.get("BURP_MCP_SERVER_PATH", "/mcp")
PLUGIN_ROOT = Path(os.environ.get("BURP_MCP_PLUGIN_ROOT", Path(__file__).resolve().parent.parent))
ARTIFACT_ROOT = PLUGIN_ROOT / "artifacts"

mcp = FastMCP(
    "BurpSuite MCP Bridge",
    instructions=(
        "Use these tools to read and operate Burp proxy traffic from Windows Burp in WSL mirrored mode. "
        "Prefer burp_live_overview or burp_live_poll for incremental triage, then burp_flow_get for a decisive request/response pair. "
        "Use burp_replay_flow or burp_send_raw_request when you need AI-driven request mutation and replay. "
        "Use burp_rule_upsert to install automatic request/response rewrite rules for proxied traffic."
    ),
    host=MCP_SERVER_HOST,
    port=MCP_SERVER_PORT,
    streamable_http_path=MCP_SERVER_PATH,
)


def resolve_bridge_base() -> str:
    explicit = os.environ.get("BURP_MCP_BRIDGE_URL")
    if explicit:
        return explicit.rstrip("/")
    return f"http://{DEFAULT_HOST}:{DEFAULT_PORT}"


def _request_json(path: str, method: str = "GET", payload: dict[str, Any] | None = None, query: dict[str, Any] | None = None) -> Any:
    url = resolve_bridge_base() + path
    if query:
        filtered = {k: v for k, v in query.items() if v is not None}
        if filtered:
            url += "?" + urllib.parse.urlencode(filtered)

    body = None
    headers = {"Accept": "application/json"}
    if payload is not None:
        body = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    request = urllib.request.Request(url, data=body, method=method, headers=headers)
    try:
        with _NO_PROXY_OPENER.open(request, timeout=30) as response:
            data = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        response_body = exc.read().decode("utf-8", errors="ignore")
        raise RuntimeError(f"bridge HTTP {exc.code}: {response_body}") from exc
    except urllib.error.URLError as exc:
        raise RuntimeError(
            "无法连接 Burp MCP Bridge。请确认：1) Windows Burp 已加载扩展；2) Burp 扩展已启用；"
            f"3) WSL mirrored 下可访问 {resolve_bridge_base()}/health。底层错误：{exc.reason}"
        ) from exc

    if isinstance(data, dict) and data.get("ok") is False:
        raise RuntimeError(data.get("error", "bridge returned failure"))
    return data


def _timestamp() -> str:
    return time.strftime("%Y%m%d-%H%M%S")


def _edits_payload(
    method: str | None = None,
    path: str | None = None,
    target_host: str | None = None,
    target_port: int | None = None,
    use_https: bool | None = None,
    headers: dict[str, str] | None = None,
    add_headers: dict[str, str] | None = None,
    remove_headers: list[str] | None = None,
    body: str | None = None,
    path_replace_from: str | None = None,
    path_replace_to: str | None = None,
    body_replace_from: str | None = None,
    body_replace_to: str | None = None,
    status_code: int | None = None,
    reason_phrase: str | None = None,
) -> dict[str, Any]:
    return {
        "method": method,
        "path": path,
        "targetHost": target_host,
        "targetPort": target_port,
        "useHttps": use_https,
        "headers": headers,
        "addHeaders": add_headers,
        "removeHeaders": remove_headers,
        "body": body,
        "pathReplaceFrom": path_replace_from,
        "pathReplaceTo": path_replace_to,
        "bodyReplaceFrom": body_replace_from,
        "bodyReplaceTo": body_replace_to,
        "statusCode": status_code,
        "reasonPhrase": reason_phrase,
    }


@mcp.tool()
def burp_bridge_status() -> dict[str, Any]:
    """检查 Windows Burp 侧桥接状态、Burp 版本、实时缓冲区容量、规则数量与当前监听地址。"""
    return _request_json("/health")


@mcp.tool()
def burp_config_get() -> dict[str, Any]:
    """读取 Burp 扩展当前配置。适合确认端口、body 截断、scope-only、静态资源过滤和规则数量。"""
    return _request_json("/api/config")


@mcp.tool()
def burp_live_poll(
    after_seq: int = 0,
    limit: int = 20,
    text: str | None = None,
    host: str | None = None,
    path: str | None = None,
    method: str | None = None,
    has_response: bool | None = None,
    in_scope: bool | None = None,
    include_bodies: bool = False,
) -> dict[str, Any]:
    """从实时 ring buffer 增量读取 Burp Proxy 流量。优先用这个做低噪声轮询，再按 flowId 拉详情。"""
    return _request_json(
        "/api/flows",
        query={
            "afterSeq": after_seq,
            "limit": limit,
            "text": text,
            "host": host,
            "path": path,
            "method": method,
            "hasResponse": has_response,
            "inScope": in_scope,
            "includeBodies": include_bodies,
        },
    )


@mcp.tool()
def burp_flow_get(flow_id: int, source: str = "live", include_bodies: bool = True) -> dict[str, Any]:
    """读取单条流量的完整细节。source=live 读实时缓冲区，source=history 读 Burp Proxy 历史。"""
    if source not in {"live", "history"}:
        raise ValueError("source 必须是 live 或 history")
    path = f"/api/flows/{flow_id}" if source == "live" else f"/api/history/{flow_id}"
    return _request_json(path, query={"includeBodies": include_bodies})


@mcp.tool()
def burp_logger_poll(
    after_seq: int = 0,
    limit: int = 20,
    text: str | None = None,
    host: str | None = None,
    path: str | None = None,
    method: str | None = None,
    tool_type: str | None = None,
    has_response: bool | None = None,
    in_scope: bool | None = None,
    include_bodies: bool = False,
) -> dict[str, Any]:
    """读取 Burp 内部 HTTP 工具流量（logger-like）。适合看 Repeater/Intruder/Scanner/插件 fuzz 等非 Proxy 面板流量。"""
    return _request_json(
        "/api/logger/flows",
        query={
            "afterSeq": after_seq,
            "limit": limit,
            "text": text,
            "host": host,
            "path": path,
            "method": method,
            "toolType": tool_type,
            "hasResponse": has_response,
            "inScope": in_scope,
            "includeBodies": include_bodies,
        },
    )


@mcp.tool()
def burp_logger_flow_get(flow_id: int, include_bodies: bool = True) -> dict[str, Any]:
    """读取单条 Burp 内部 HTTP 工具流量详情。"""
    return _request_json(f"/api/logger/flows/{flow_id}", query={"includeBodies": include_bodies})


@mcp.tool()
def burp_history_search(
    query: str | None = None,
    regex: bool = False,
    limit: int = 20,
    offset: int = 0,
    host_contains: str | None = None,
    path_contains: str | None = None,
    method: str | None = None,
    in_scope: bool | None = None,
    has_response: bool | None = None,
    status_min: int | None = None,
    status_max: int | None = None,
    include_bodies: bool = False,
    ignore_static: bool | None = True,
) -> dict[str, Any]:
    """搜索 Burp 全量 Proxy 历史。适合查旧流量、按关键字回溯登录/API/upload 等关键链路。"""
    return _request_json(
        "/api/history/search",
        method="POST",
        payload={
            "query": query,
            "regex": regex,
            "limit": limit,
            "offset": offset,
            "hostContains": host_contains,
            "pathContains": path_contains,
            "method": method,
            "inScope": in_scope,
            "hasResponse": has_response,
            "statusMin": status_min,
            "statusMax": status_max,
            "includeBodies": include_bodies,
            "ignoreStatic": ignore_static,
        },
    )


@mcp.tool()
def burp_send_to_repeater(flow_id: int, source: str = "live", tab_name: str = "AI review") -> dict[str, Any]:
    """把选中的请求发到 Burp Repeater，方便继续手工验证或配合 AI 给出的下一步变体。"""
    if source not in {"live", "history"}:
        raise ValueError("source 必须是 live 或 history")
    return _request_json(
        "/api/actions/send-to-repeater",
        method="POST",
        payload={"id": flow_id, "source": source, "tabName": tab_name},
    )


@mcp.tool()
def burp_clear_live_buffer() -> dict[str, Any]:
    """清空实时流量缓冲区，适合开始一个新的验证阶段前先降噪。"""
    return _request_json("/api/actions/clear-buffer", method="POST", payload={})


@mcp.tool()
def burp_clear_logger_buffer() -> dict[str, Any]:
    """清空 Burp 内部工具/logger-like 流量缓冲区。适合在 fuzz、重放或规则联调前先降噪。"""
    return _request_json("/api/actions/clear-logger-buffer", method="POST", payload={})


@mcp.tool()
def burp_export_flow_bundle(flow_id: int, source: str = "history") -> dict[str, Any]:
    """导出一条 flow 的完整原始 request/response 到 bridge 所在主机的临时目录。适合超大包场景下安全取证。"""
    if source not in {"live", "history", "logger"}:
        raise ValueError("source 必须是 live、history 或 logger")
    return _request_json(
        "/api/actions/export-flow-bundle",
        method="POST",
        payload={"id": flow_id, "source": source},
    )


@mcp.tool()
def burp_live_overview(after_seq: int = 0, limit: int = 80) -> dict[str, Any]:
    """快速汇总最近实时流量，按主机、状态码、标签统计，便于 AI 先做渗透流量定向。"""
    data = burp_live_poll(after_seq=after_seq, limit=limit, include_bodies=False)
    items = data.get("items", [])
    host_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    tag_counter: Counter[str] = Counter()
    interesting_by_host: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in items:
        host = item.get("host") or "<unknown>"
        host_counter[host] += 1
        status = item.get("statusCode")
        status_counter[str(status) if status is not None else "pending"] += 1
        for tag in item.get("tags", []):
            tag_counter[tag] += 1
        if len(interesting_by_host[host]) < 5:
            interesting_by_host[host].append(
                {
                    "flowId": item.get("flowId"),
                    "method": item.get("method"),
                    "path": item.get("path"),
                    "statusCode": item.get("statusCode"),
                    "tags": item.get("tags"),
                    "requestRuleHits": item.get("requestRuleHits", []),
                    "responseRuleHits": item.get("responseRuleHits", []),
                }
            )

    return {
        "ok": True,
        "count": len(items),
        "latestCursor": data.get("latestCursor"),
        "byHost": host_counter.most_common(),
        "byStatus": status_counter.most_common(),
        "byTag": tag_counter.most_common(),
        "interestingByHost": dict(interesting_by_host),
    }


@mcp.tool()
def burp_logger_overview(after_seq: int = 0, limit: int = 80) -> dict[str, Any]:
    """快速汇总 Burp 内部工具流量，尤其适合看 fuzz 插件/Repeater/Intruder/Scanner 的请求响应。"""
    data = burp_logger_poll(after_seq=after_seq, limit=limit, include_bodies=False)
    items = data.get("items", [])
    host_counter: Counter[str] = Counter()
    status_counter: Counter[str] = Counter()
    tool_counter: Counter[str] = Counter()
    interesting_by_tool: dict[str, list[dict[str, Any]]] = defaultdict(list)

    for item in items:
        host = item.get("host") or "<unknown>"
        host_counter[host] += 1
        status = item.get("statusCode")
        status_counter[str(status) if status is not None else "pending"] += 1
        tool = item.get("toolType") or "<unknown>"
        tool_counter[tool] += 1
        if len(interesting_by_tool[tool]) < 5:
            interesting_by_tool[tool].append(
                {
                    "flowId": item.get("flowId"),
                    "method": item.get("method"),
                    "path": item.get("path"),
                    "statusCode": item.get("statusCode"),
                    "host": item.get("host"),
                }
            )

    return {
        "ok": True,
        "count": len(items),
        "latestCursor": data.get("latestCursor"),
        "byHost": host_counter.most_common(),
        "byStatus": status_counter.most_common(),
        "byToolType": tool_counter.most_common(),
        "interestingByToolType": dict(interesting_by_tool),
    }


@mcp.tool()
def burp_export_flow(flow_id: int, source: str = "live", include_bodies: bool = True, label: str | None = None) -> dict[str, Any]:
    """导出一条关键流量为本地 JSON 证据文件，便于归档、复盘或拼接正式漏洞报告。"""
    if source == "logger":
        detail = burp_logger_flow_get(flow_id=flow_id, include_bodies=include_bodies)
    else:
        detail = burp_flow_get(flow_id=flow_id, source=source, include_bodies=include_bodies)
    ARTIFACT_ROOT.mkdir(parents=True, exist_ok=True)
    safe_label = (label or f"{source}-{flow_id}").replace("/", "_").replace(" ", "-")
    output_path = ARTIFACT_ROOT / f"burp-flow-{safe_label}-{_timestamp()}.json"
    output_path.write_text(json.dumps(detail, ensure_ascii=False, indent=2), encoding="utf-8")
    return {"ok": True, "flowId": flow_id, "source": source, "path": str(output_path)}


@mcp.tool()
def burp_replay_flow(
    flow_id: int,
    source: str = "history",
    method: str | None = None,
    path: str | None = None,
    target_host: str | None = None,
    target_port: int | None = None,
    use_https: bool | None = None,
    headers: dict[str, str] | None = None,
    add_headers: dict[str, str] | None = None,
    remove_headers: list[str] | None = None,
    body: str | None = None,
    path_replace_from: str | None = None,
    path_replace_to: str | None = None,
    body_replace_from: str | None = None,
    body_replace_to: str | None = None,
    apply_rules: bool = False,
    send_to_repeater: bool = False,
    repeater_tab_name: str = "AI replay",
    include_bodies: bool = True,
) -> dict[str, Any]:
    """基于 live/history 里的已有请求进行改包重发。适合 AI 修改 token、body、header、path 后快速验证。"""
    if source not in {"live", "history"}:
        raise ValueError("source 必须是 live 或 history")
    payload = {
        "id": flow_id,
        "source": source,
        "applyRules": apply_rules,
        "sendToRepeater": send_to_repeater,
        "repeaterTabName": repeater_tab_name,
        "includeBodies": include_bodies,
    }
    payload.update(
        _edits_payload(
            method=method,
            path=path,
            target_host=target_host,
            target_port=target_port,
            use_https=use_https,
            headers=headers,
            add_headers=add_headers,
            remove_headers=remove_headers,
            body=body,
            path_replace_from=path_replace_from,
            path_replace_to=path_replace_to,
            body_replace_from=body_replace_from,
            body_replace_to=body_replace_to,
        )
    )
    return _request_json("/api/replay/flow", method="POST", payload=payload)


@mcp.tool()
def burp_send_raw_request(
    raw_request: str,
    target_host: str,
    target_port: int,
    use_https: bool = False,
    apply_rules: bool = False,
    send_to_repeater: bool = False,
    repeater_tab_name: str = "AI raw replay",
    include_bodies: bool = True,
) -> dict[str, Any]:
    """直接发送原始 HTTP 请求文本。适合 AI 组合完整数据包后通过 Burp 内部 HTTP 栈重放。"""
    return _request_json(
        "/api/replay/raw",
        method="POST",
        payload={
            "rawRequest": raw_request,
            "targetHost": target_host,
            "targetPort": target_port,
            "useHttps": use_https,
            "applyRules": apply_rules,
            "sendToRepeater": send_to_repeater,
            "repeaterTabName": repeater_tab_name,
            "includeBodies": include_bodies,
        },
    )


@mcp.tool()
def burp_rules_list() -> dict[str, Any]:
    """列出当前启用/禁用的自动请求/响应改写规则。"""
    return _request_json("/api/rules")


@mcp.tool()
def burp_rule_upsert(
    direction: str,
    name: str | None = None,
    rule_id: str | None = None,
    enabled: bool = True,
    match_host_contains: str | None = None,
    match_path_contains: str | None = None,
    match_method: str | None = None,
    match_body_contains: str | None = None,
    match_status_min: int | None = None,
    match_status_max: int | None = None,
    method: str | None = None,
    path: str | None = None,
    target_host: str | None = None,
    target_port: int | None = None,
    use_https: bool | None = None,
    headers: dict[str, str] | None = None,
    add_headers: dict[str, str] | None = None,
    remove_headers: list[str] | None = None,
    body: str | None = None,
    path_replace_from: str | None = None,
    path_replace_to: str | None = None,
    body_replace_from: str | None = None,
    body_replace_to: str | None = None,
    status_code: int | None = None,
    reason_phrase: str | None = None,
) -> dict[str, Any]:
    """新增或更新自动改写规则。direction=request 时改写代理请求，direction=response 时改写返回客户端的响应。"""
    if direction not in {"request", "response"}:
        raise ValueError("direction 必须是 request 或 response")
    payload = {
        "id": rule_id,
        "name": name,
        "direction": direction,
        "enabled": enabled,
        "matchHostContains": match_host_contains,
        "matchPathContains": match_path_contains,
        "matchMethod": match_method,
        "matchBodyContains": match_body_contains,
        "matchStatusMin": match_status_min,
        "matchStatusMax": match_status_max,
    }
    payload.update(
        _edits_payload(
            method=method,
            path=path,
            target_host=target_host,
            target_port=target_port,
            use_https=use_https,
            headers=headers,
            add_headers=add_headers,
            remove_headers=remove_headers,
            body=body,
            path_replace_from=path_replace_from,
            path_replace_to=path_replace_to,
            body_replace_from=body_replace_from,
            body_replace_to=body_replace_to,
            status_code=status_code,
            reason_phrase=reason_phrase,
        )
    )
    return _request_json("/api/rules", method="POST", payload=payload)


@mcp.tool()
def burp_rule_delete(rule_id: str) -> dict[str, Any]:
    """删除一条自动改写规则。"""
    return _request_json(f"/api/rules/{urllib.parse.quote(rule_id, safe='')}", method="DELETE")


if __name__ == "__main__":
    try:
        parser = argparse.ArgumentParser(description="BurpSuite MCP Bridge server")
        parser.add_argument("--transport", choices=["stdio", "streamable-http", "sse"], default=MCP_TRANSPORT)
        parser.add_argument("--host", default=MCP_SERVER_HOST, help="Host for HTTP MCP transports")
        parser.add_argument("--port", type=int, default=MCP_SERVER_PORT, help="Port for HTTP MCP transports")
        parser.add_argument("--path", default=MCP_SERVER_PATH, help="Path for Streamable HTTP MCP transport")
        args = parser.parse_args()

        mcp.settings.host = args.host
        mcp.settings.port = args.port
        mcp.settings.streamable_http_path = args.path
        mcp.run(transport=args.transport)
    except Exception as exc:  # pragma: no cover
        print(f"[burpsuite-mcp-bridge] fatal: {exc}", file=os.sys.stderr)
        raise
