import json
import os
import sys

SETTINGS_PATH = r"C:\Users\VIVIM.inc\.gemini\settings.json"
MCP_SERVER_CONFIG = {
    "docs-ai": {
        "command": r"C:\0-BlackBoxProject-0\DocsEngine\docs-ai\connect_mcp.bat",
        "args": [],
        "enabled": True
    }
}

def update_config():
    if not os.path.exists(SETTINGS_PATH):
        print(f"Error: Settings file not found at {SETTINGS_PATH}")
        return False

    try:
        with open(SETTINGS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Add mcpServers section if missing
        if "mcpServers" not in data:
            data["mcpServers"] = {}
            
        # Update/Add docs-ai server
        data["mcpServers"].update(MCP_SERVER_CONFIG)
        
        with open(SETTINGS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print("Successfully updated settings.json with DocsAI MCP server.")
        return True
        
    except Exception as e:
        print(f"Error updating config: {e}")
        return False

if __name__ == "__main__":
    update_config()
