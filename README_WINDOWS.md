# Documentation Download Agent - Windows Quick Start

## Ready to Run (3 Steps)

### Step 1: Test Installation
Double-click: `launch_test.bat`

If successful, you'll see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
```

Open: **http://localhost:8000/test**

### Step 2: Start Main App
Double-click: `run_app.bat`

You'll see:
```
[*] Starting Documentation Download Agent...
[*] Open browser to: http://localhost:8001
```

Open: **http://localhost:8001**

### Step 3: Use the App
1. Enter a documentation URL (e.g., https://docs.python.org/3/)
2. Click "Start Crawling"
3. Monitor progress in real-time
4. Download as ZIP when complete

---

## Windows-Specific Tips

### Keep Server Window Open
- The server MUST stay running in the command window
- Closing the window stops the server
- Minimize it, don't close it

### Browser Connection
- Use: `http://localhost:8001` OR `http://127.0.0.1:8001`
- Both work the same on Windows

### Firewall Warning
- Windows Firewall might ask to allow Python
- Click "Allow" for both public and private networks
- This is needed only for localhost connections

---

## Troubleshooting

### "localhost refused to connect"
1. Make sure the server window shows "Uvicorn running"
2. Check the URL matches exactly what the console shows
3. Try using `127.0.0.1` instead of `localhost`

### "Server won't start"
1. Open a new command prompt in this folder
2. Run: `py --version` (should show Python 3.x)
3. Run: `py test_server.py`
4. If errors appear, see setup below

### Dependencies Missing
```cmd
py -m pip install fastapi uvicorn aiohttp beautifulsoup4 lxml aiofiles typing_extensions
```

---

## Manual Setup (If Needed)

### Check Python
```cmd
py --version
```
Should show Python 3.8 or higher

### Install Dependencies
```cmd
py -m pip install fastapi uvicorn aiohttp beautifulsoup4 lxml aiofiles typing_extensions
```

### Create Directories (auto-created)
```cmd
mkdir downloads
mkdir downloads\archives
mkdir static
mkdir templates
```

---

## Advanced Usage

### Run from Command Line
```cmd
cd "C:\0-BlackBoxProject-0\DocsEngine\docs-ai"
py main.py
```

### Check Server Health
Open in browser: `http://localhost:8001/health`

Expected response:
```json
{"status":"healthy","service":"documentation-download-agent"}
```

---

## Files Overview

- `launch_test.bat` - Quick test to verify setup works
- `run_app.bat` - Main application launcher
- `startup.py` - Auto-setup and dependency checker
- `main.py` - FastAPI server application
- `test_server.py` - Minimal test server
- `WINDOWS_SETUP.md` - This file

---

## Need Help?

1. First: Run `launch_test.bat` - this isolates the issue
2. Then: Check `WINDOWS_SETUP.md` troubleshooting section
3. Check console output for error messages
4. Make sure Python and dependencies are installed

---

**That's it!** Double-click `launch_test.bat` to get started.
