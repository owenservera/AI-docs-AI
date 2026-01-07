import sys
import asyncio
from mcp_server import mcp

print("✅ MCP Server module loaded successfully.")
print(f"   Server Name: {mcp.name}")
print("   Tools available:")
for tool in mcp._tool_manager.list_tools():
    print(f"   - {tool.name}: {tool.description[:50]}...")
