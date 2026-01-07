# Windows Setup Guide

## Quick Start

1. **Test the server first:**
   ```cmd
   launch_test.bat
   ```
   Then open: http://localhost:8000

2. **If test works, run the main app:**
   ```cmd
   run_app.bat
   ```
   Then open: http://localhost:8001

## Troubleshooting

### Server won't start
- Make sure Python 3.8+ is installed: `py --version`
- Install dependencies: `py -m pip install fastapi uvicorn aiohttp beautifulsoup4 lxml aiofiles`
- Check firewall: Windows Firewall might block localhost connections

### Can't connect in browser
- Try: `http://127.0.0.1:8001` instead of `http://localhost:8001`
- Make sure the server window shows "Uvicorn running"
- Try a different port (edit main.py line 262, change port=8001)

### Background processes
- Windows handles background processes differently than Linux
- Keep the server window open - closing it stops the server
- Use Ctrl+C in the server window to stop gracefully

## Windows-Specific Notes

- File paths use backslashes (`\`) but Python handles both
- The server runs on `127.0.0.1` (localhost) not `0.0.0.0`
- Keep the command window open while using the app
- PowerShell users can also run: `py main.py` directly

## Directory Structure

After successful runs, you'll see:
```
downloads/
  └── {domain}_{timestamp}/
      ├── index.html
      ├── *.html files
      ├── css/
      ├── js/
      └── images/
downloads/archives/
  └── documentation_{crawl_id}.zip
```

## Next Steps

1. Double-click `launch_test.bat` to verify everything works
2. Double-click `run_app.bat` to start the full application
3. Open browser to the URL shown in the console
4. Start downloading documentation!
