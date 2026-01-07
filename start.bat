@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
echo ================================================
echo   Documentation Download Agent
echo ================================================
echo.
echo Starting server...
echo.
py startup.py
