@echo off
chcp 65001 >nul
cls
echo.
echo ===============================================================
echo   DOCUMENTATION DOWNLOAD AGENT
echo ===============================================================
echo.
echo [1/3] Initializing...
echo.

py startup.py

echo.
echo [!] Server stopped
pause
