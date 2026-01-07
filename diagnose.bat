@echo off
chcp 65001 >nul
cls
echo ===============================================================
echo   DIAGNOSTIC TOOL - Windows Setup Verification
echo ===============================================================
echo.

echo [1/5] Checking Python installation...
py --version
if errorlevel 1 (
    echo [!] Python not found or not in PATH
    echo     Install Python from: https://python.org/downloads/
    pause
    exit /b 1
)
echo [+] Python is installed
echo.

echo [2/5] Checking required packages...
py -c "import fastapi; print('    [+] fastapi installed')" 2>nul || echo "    [!] fastapi not installed"
py -c "import uvicorn; print('    [+] uvicorn installed')" 2>nul || echo "    [!] uvicorn not installed"
py -c "import aiohttp; print('    [+] aiohttp installed')" 2>nul || echo "    [!] aiohttp not installed"
py -c "import bs4; print('    [+] beautifulsoup4 installed')" 2>nul || echo "    [!] beautifulsoup4 not installed"
py -c "import lxml; print('    [+] lxml installed')" 2>nul || echo "    [!] lxml not installed"
py -c "import aiofiles; print('    [+] aiofiles installed')" 2>nul || echo "    [!] aiofiles not installed"
echo.

echo [3/5] Checking project files...
if exist "main.py" (echo "    [+] main.py found") else (echo "    [!] main.py missing")
if exist "crawler.py" (echo "    [+] crawler.py found") else (echo "    [!] crawler.py missing")
if exist "file_manager.py" (echo "    [+] file_manager.py found") else (echo "    [!] file_manager.py missing")
if exist "templates\index.html" (echo "    [+] templates/index.html found") else (echo "    [!] templates/index.html missing")
echo.

echo [4/5] Checking directories...
if exist "downloads" (echo "    [+] downloads/ exists") else (echo "    [*] downloads/ will be created")
if exist "static" (echo "    [+] static/ exists") else (echo "    [*] static/ will be created")
if exist "templates" (echo "    [+] templates/ exists") else (echo "    [*] templates/ will be created")
echo.

echo [5/5] Testing minimal server...
echo [*] Starting test server for 3 seconds...
start /b py test_server.py >nul 2>&1
timeout /t 3 /nobreak >nul
py -c "import urllib.request; r = urllib.request.urlopen('http://127.0.0.1:8000'); print('    [+] Server responded:', r.status)" 2>nul || echo "    [!] Server not responding"
taskkill /f /im python.exe >nul 2>&1
echo.

echo ===============================================================
echo   DIAGNOSTIC COMPLETE
echo ===============================================================
echo.
echo If all checks show [+], you're ready to go!
echo.
echo Next steps:
echo   1. Double-click: launch_test.bat
echo   2. Then double-click: run_app.bat
echo   3. Open browser to: http://localhost:8001
echo.
pause
