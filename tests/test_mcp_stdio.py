"""Verify the locked SDK can start the adapter without a running Burp instance."""

import asyncio
import os
from pathlib import Path
import sys
import unittest

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


class StdioSmokeTest(unittest.IsolatedAsyncioTestCase):
    async def test_initialize_and_list_tools(self):
        server = Path(__file__).resolve().parents[1] / "mcp-server" / "server.py"
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(server), "--transport", "stdio"],
            env={**os.environ, "BURP_MCP_TRANSPORT": "stdio"},
        )
        async with asyncio.timeout(30):
            async with stdio_client(params) as streams:
                async with ClientSession(*streams) as session:
                    initialized = await session.initialize()
                    self.assertEqual(initialized.serverInfo.name, "BurpSuite MCP Bridge")
                    response = await session.list_tools()
                    names = {tool.name for tool in response.tools}
                    self.assertTrue(
                        {"burp_bridge_status", "burp_target_overview", "burp_replay_flow"}
                        <= names,
                        names,
                    )
                    self.assertEqual(len(names), len(response.tools))


if __name__ == "__main__":
    unittest.main()
