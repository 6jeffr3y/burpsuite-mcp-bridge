# BurpSuite MCP Bridge v2.0.1

## 修复与增强

- 修复 MCP 客户端把 JSON body 作为 object/list 传给 `burp_replay_flow` 时的 Pydantic string 校验问题；MCP server 会自动把可 JSON 序列化的 body 转成字符串再交给 Burp bridge。
- 新增时间窗口搜索：
  - `burp_history_search(time_from=..., time_to=..., sort="newest|oldest")`
  - `burp_live_poll(created_from=..., created_to=..., sort=...)`
  - `burp_logger_poll(created_from=..., created_to=..., sort=...)`
  - `burp_selection_poll(created_from=..., created_to=..., sort=...)`
  - `burp_target_overview(time_from=..., time_to=...)`
  - `burp_marked_flows(time_from=..., time_to=...)`
- 时间值支持 epoch seconds、epoch milliseconds 和 ISO-8601。

## 说明

本次变更需要更新 Burp 扩展 JAR，并重启 Codex/MCP server 后才能使用新工具 schema。
