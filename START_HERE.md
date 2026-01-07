# WINDOWS QUICK START - READY TO USE

## 🚀 Get Started in 30 Seconds

### Option 1: Test First (Recommended)

**Step 1:** Double-click `diagnose.bat`
- Checks if everything is installed
- Shows what's working and what's not

**Step 2:** Double-click `launch_test.bat`
- Opens a server on port 8000
- Test page: http://localhost:8000/test

**Step 3:** If test works, double-click `run_app.bat`
- Main app on port 8001
- Open: http://localhost:8001

### Option 2: Just Run It

Double-click: `run_app.bat`

Then open: **http://localhost:8001**

### Option 3: Universal Call System (CLI)

Use `docs.bat` in your terminal to manage downloaded documentation:
```cmd
docs list              # List all docs
docs context <alias>   # Get AI context for a doc set
```

---

## 💡 Important Windows Tips

✅ **Keep the server window OPEN** - minimize it, don't close it
✅ **Use localhost or 127.0.0.1** - both work
✅ **Allow Python through firewall** - if Windows asks
✅ **Server stops when you close the window** - use Ctrl+C to stop gracefully

---

## 🔧 If Something Doesn't Work

### "Can't connect to server"
1. Make sure server window is open and shows "Uvicorn running"
2. Check the URL matches what the console shows
3. Try `127.0.0.1` instead of `localhost`

### "Server won't start"
1. Run `diagnose.bat` to find the issue
2. Install missing packages:
   ```
   py -m pip install fastapi uvicorn aiohttp beautifulsoup4 lxml aiofiles
   ```

### General Issues
1. Run `diagnose.bat` first
2. Read `README_WINDOWS.md` for detailed help
3. Check the console output for errors

---

## 📁 What's What

**Files to use:**
- `diagnose.bat` - Check your setup
- `launch_test.bat` - Quick test server
- `run_app.bat` - Main application
- `docs.bat` - CLI for library management

**Documentation:**
- `README_WINDOWS.md` - Detailed Windows guide
- `QUICKSTART.md` - Original quick start guide
- `README.md` - Full documentation

**Python files:**
- `main.py` - Main FastAPI app
- `test_server.py` - Minimal test server
- `startup.py` - Auto-setup script

---

## ✅ Quick Verification Checklist

Run `diagnose.bat` and you should see:
- [+] Python is installed
- [+] fastapi installed
- [+] uvicorn installed
- [+] aiohttp installed
- [+] beautifulsoup4 installed
- [+] lxml installed
- [+] aiofiles installed
- [+] main.py found
- [+] crawler.py found
- [+] file_manager.py found
- [+] templates/index.html found
- [+] Server responded: 200

If all show [+] or [*], you're good to go!

---

## 🎯 That's It!

**For immediate use:**
1. Double-click `diagnose.bat` (optional but recommended)
2. Double-click `run_app.bat`
3. Open browser to http://localhost:8001
4. Start downloading documentation!

**Questions?** Check `README_WINDOWS.md` for detailed help.
