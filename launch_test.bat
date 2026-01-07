@echo off
chcp 65001 >nul
cls
echo.
echo ===============================================================
echo   DOCUMENTATION DOWNLOAD AGENT - Windows Launcher
echo ===============================================================
echo.
echo [1/3] Starting server...
echo.

py test_server.py

echo.
echo [!] Server stopped
pause
