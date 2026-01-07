# DocsAI: MCP Installation Guide for AI Tools

This guide explains how to connect your **DocsAI** library to various AI tools using the **Model Context Protocol (MCP)**.

✅ **Optimization Update:** We have created a universal connector script (`connect_mcp.bat`) that handles paths automatically. You should use this instead of the raw python script to avoid "File Not Found" errors.

## 📍 Server Connection Details

- **Type:** `stdio` (Standard Input/Output)
- **Command:** `C:\0-BlackBoxProject-0\DocsEngine\docs-ai\connect_mcp.bat`

---

## 🤖 1. Claude Desktop App (Anthropic)

**Step 1:** Open your config file.
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

**Step 2:** Add/Update the configuration:

```json
{
  "mcpServers": {
    "docs-ai": {
      "command": "C:\\0-BlackBoxProject-0\\DocsEngine\\docs-ai\\connect_mcp.bat",
      "args": []
    }
  }
}
```

**Step 3:** Restart Claude Desktop.

---

## 💻 2. Cursor (IDE)

**Step 1:** Go to **Cursor Settings** > **Features** > **MCP Servers**.
**Step 2:** Click **+ Add New MCP Server**.

- **Name:** `docs-ai`
- **Type:** `stdio`
- **Command:** `C:\0-BlackBoxProject-0\DocsEngine\docs-ai\connect_mcp.bat`

**Step 3:** Click **Save**. The status light should turn green.

---

## 🛠️ 3. OpenCode CLI / Custom Agents

If you are using OpenCode or other CLI agents, add this to your configuration (usually `~/.config/opencode/opencode.json`):

```json
{
  "mcpServers": {
    "docs-ai": {
      "command": "C:\\0-BlackBoxProject-0\\DocsEngine\\docs-ai\\connect_mcp.bat"
    }
  }
}
```

---

## ⚡ Verification

To test if the connector works, open a command prompt and run:
```cmd
C:\0-BlackBoxProject-0\DocsEngine\docs-ai\connect_mcp.bat
```
*It should sit silently (waiting for input). If it crashes or prints an error immediately, something is wrong.*

## 🔍 Capabilities

Once connected, your AI can:
1.  **List Docs:** "What documentation do I have locally?"
2.  **Read Context:** "Read the overview of the `react` docs."
3.  **Semantic Search:** "Search the `opencode` docs for how to configure plugins."