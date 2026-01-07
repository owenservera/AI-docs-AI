"""
Minimal test server to verify everything works on Windows
"""

from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import os

app = FastAPI()


@app.get("/")
async def root():
    return {"status": "ok", "message": "Server is working!", "platform": os.name}


@app.get("/test", response_class=HTMLResponse)
async def test_page():
    return """
    <!DOCTYPE html>
    <html>
    <head><title>Test Page</title></head>
    <body>
        <h1>Server is Working!</h1>
        <p>If you can see this, the server is running correctly.</p>
        <p>Platform: Windows</p>
        <p>Next step: Try <a href="/">JSON endpoint</a></p>
    </body>
    </html>
    """


if __name__ == "__main__":
    print("=" * 60)
    print("  TEST SERVER - Windows Compatible")
    print("=" * 60)
    print("Starting server on: http://localhost:8000")
    print("Test page: http://localhost:8000/test")
    print("Press Ctrl+C to stop")
    print("=" * 60)

    try:
        uvicorn.run(app, host="127.0.0.1", port=8000, log_level="info")
    except KeyboardInterrupt:
        print("\n[*] Server stopped")
