@echo off
set "SCRIPT_DIR=%~dp0"
set "PYTHONPATH=%SCRIPT_DIR%"
py "%SCRIPT_DIR%mcp_server.py"
