from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from pydantic import BaseModel, HttpUrl
import asyncio
import os
import json
from datetime import datetime
from typing import Dict, List, Optional
import uuid
import logging

from crawler import DocumentationCrawler
from file_manager import FileManager
from library_manager import LibraryManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Documentation Download Agent", version="1.0.0")

# Mount static files
app.mount("/static", StaticFiles(directory="static"), name="static")

# Global state management
active_crawls: Dict[str, DocumentationCrawler] = {}
crawl_results: Dict[str, Dict] = {}
library_manager = LibraryManager()


class CrawlRequest(BaseModel):
    url: HttpUrl
    max_depth: int = 3
    include_images: bool = True
    include_css: bool = True
    include_js: bool = True
    include_fonts: bool = True
    rate_limit: float = 1.0
    user_agent: str = "DocumentationAgent/1.0"


class CrawlStatus(BaseModel):
    crawl_id: str
    status: str
    pages_found: int
    pages_downloaded: int
    current_page: Optional[str]
    errors: List[str]
    start_time: str
    estimated_completion: Optional[str]


@app.get("/", response_class=HTMLResponse)
async def serve_frontend():
    """Serve the main application interface"""
    try:
        with open("templates/index.html", "r", encoding="utf-8") as f:
            return HTMLResponse(content=f.read())
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>404 - Frontend not found</h1>", status_code=404
        )


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "documentation-download-agent"}


@app.post("/api/start_crawl")
async def start_crawl(request: CrawlRequest, background_tasks: BackgroundTasks):
    """Start a new documentation crawling process"""
    crawl_id = str(uuid.uuid4())

    # Initialize crawler
    crawler = DocumentationCrawler(
        base_url=str(request.url),
        max_depth=request.max_depth,
        include_images=request.include_images,
        include_css=request.include_css,
        include_js=request.include_js,
        include_fonts=request.include_fonts,
        rate_limit=request.rate_limit,
        user_agent=request.user_agent,
    )

    active_crawls[crawl_id] = crawler

    # Start crawling in background
    background_tasks.add_task(run_crawl, crawl_id, crawler)

    return {
        "crawl_id": crawl_id,
        "status": "started",
        "message": "Documentation crawling started successfully",
    }


async def run_crawl(crawl_id: str, crawler: DocumentationCrawler):
    """Run the crawling process in background"""
    try:
        start_time = datetime.now()
        result = await crawler.crawl()

        # Store results
        crawl_results[crawl_id] = {
            "status": "completed" if result["success"] else "failed",
            "pages_found": result.get("pages_found", 0),
            "pages_downloaded": result.get("pages_downloaded", 0),
            "file_structure": result.get("file_structure", {}),
            "errors": result.get("errors", []),
            "output_path": result.get("output_path", ""),
            "completion_time": datetime.now().isoformat(),
        }

        # Auto-register to library if successful
        if result["success"] and result.get("output_path"):
            try:
                # Extract domain for alias (e.g., fastapi_tiangolo_com -> fastapi)
                # or use the first part of the domain
                base_url = crawler.base_url
                from urllib.parse import urlparse
                domain = urlparse(base_url).netloc
                # Simple alias generation: first part of domain (e.g., 'react' from 'react.dev')
                alias = domain.split('.')[0]
                if alias == 'www':
                    alias = domain.split('.')[1]
                
                # Make alias unique if needed or just overwrite?
                # User preference "universal call" implies stable names.
                # Let's use the simple alias and let the user know.
                
                library_manager.add_to_library(
                    result["output_path"], 
                    alias,
                    metadata={"url": base_url, "crawl_id": crawl_id}
                )
                logger.info(f"Auto-registered {alias} to library")
                
                # Also add to results so frontend knows
                crawl_results[crawl_id]["library_alias"] = alias
                
            except Exception as e:
                logger.error(f"Failed to auto-register to library: {e}")

        logger.info(f"Crawl {crawl_id} completed: {result}")

        # Clean up active crawl
        if crawl_id in active_crawls:
            del active_crawls[crawl_id]

    except Exception as e:
        logger.error(f"Crawl {crawl_id} failed: {str(e)}")
        crawl_results[crawl_id] = {
            "status": "failed",
            "error": str(e),
            "completion_time": datetime.now().isoformat(),
        }
        if crawl_id in active_crawls:
            del active_crawls[crawl_id]


@app.get("/api/crawl_status/{crawl_id}")
async def get_crawl_status(crawl_id: str):
    """Get current crawling progress and status"""
    if crawl_id in active_crawls:
        crawler = active_crawls[crawl_id]
        status = await crawler.get_status()
        return status
    elif crawl_id in crawl_results:
        return crawl_results[crawl_id]
    else:
        raise HTTPException(status_code=404, detail="Crawl not found")


@app.get("/api/list_files/{crawl_id}")
async def list_files(crawl_id: str):
    """List all downloaded files for a completed crawl"""
    if crawl_id not in crawl_results:
        raise HTTPException(status_code=404, detail="Crawl not found")

    result = crawl_results[crawl_id]
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Crawl not completed")

    output_path = result.get("output_path", "")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Download directory not found")

    file_manager = FileManager()
    file_structure = file_manager.get_file_structure(output_path)

    return {
        "crawl_id": crawl_id,
        "file_structure": file_structure,
        "total_size": file_manager.calculate_total_size(output_path),
        "file_count": file_structure.get("file_count", 0),
    }


@app.get("/api/download_zip/{crawl_id}")
async def download_zip(crawl_id: str):
    """Generate and download ZIP file of documentation"""
    if crawl_id not in crawl_results:
        raise HTTPException(status_code=404, detail="Crawl not found")

    result = crawl_results[crawl_id]
    if result["status"] != "completed":
        raise HTTPException(status_code=400, detail="Crawl not completed")

    output_path = result.get("output_path", "")
    if not os.path.exists(output_path):
        raise HTTPException(status_code=404, detail="Download directory not found")

    # Generate ZIP file
    file_manager = FileManager()
    zip_path = file_manager.create_zip_archive(output_path, crawl_id)

    if not os.path.exists(zip_path):
        raise HTTPException(status_code=500, detail="Failed to create ZIP file")

    return FileResponse(
        path=zip_path,
        filename=f"documentation_{crawl_id}.zip",
        media_type="application/zip",
    )


@app.post("/api/stop_crawl/{crawl_id}")
async def stop_crawl(crawl_id: str):
    """Stop an ongoing crawl"""
    if crawl_id not in active_crawls:
        raise HTTPException(status_code=404, detail="Active crawl not found")

    crawler = active_crawls[crawl_id]
    await crawler.stop()

    del active_crawls[crawl_id]

    return {
        "crawl_id": crawl_id,
        "status": "stopped",
        "message": "Crawl stopped successfully",
    }


@app.delete("/api/cleanup/{crawl_id}")
async def cleanup_crawl(crawl_id: str):
    """Clean up crawl data and files"""
    # Remove from active crawls if exists
    if crawl_id in active_crawls:
        del active_crawls[crawl_id]

    # Remove from results
    if crawl_id in crawl_results:
        result = crawl_results[crawl_id]
        output_path = result.get("output_path", "")

        # Clean up files
        if os.path.exists(output_path):
            file_manager = FileManager()
            file_manager.cleanup_directory(output_path)

        del crawl_results[crawl_id]

    return {
        "crawl_id": crawl_id,
        "status": "cleaned",
        "message": "Crawl data cleaned up successfully",
    }


@app.get("/api/active_crawls")
async def get_active_crawls():
    """Get list of all active crawls"""
    active_list = []
    for crawl_id, crawler in active_crawls.items():
        status = await crawler.get_status()
        active_list.append(
            {
                "crawl_id": crawl_id,
                "base_url": crawler.base_url,
                "status": status["status"],
                "pages_found": status["pages_found"],
                "pages_downloaded": status["pages_downloaded"],
            }
        )

    return {"active_crawls": active_list}


# Library API Endpoints

@app.get("/api/library")
async def list_library_items():
    """List all items in the library"""
    return library_manager.list_items()

@app.get("/api/library/{alias}")
async def get_library_item(alias: str):
    """Get details of a specific library item"""
    item = library_manager.get_item(alias)
    if not item:
        raise HTTPException(status_code=404, detail="Library item not found")
    return item

@app.delete("/api/library/{alias}")
async def remove_library_item(alias: str):
    """Remove an item from the library"""
    success = library_manager.remove_item(alias)
    if not success:
        raise HTTPException(status_code=404, detail="Library item not found")
    return {"status": "success", "message": f"Removed {alias} from library"}


if __name__ == "__main__":
    import uvicorn

    # Create necessary directories
    os.makedirs("static", exist_ok=True)
    os.makedirs("templates", exist_ok=True)
    os.makedirs("downloads", exist_ok=True)
    os.makedirs("downloads/archives", exist_ok=True)

    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    )

    print("[*] Starting Documentation Download Agent...")
    print("[*] Open browser to: http://localhost:8001")
    print("[*] Health check: http://localhost:8001/health")
    print("[*] Downloads will be saved to: downloads/")
    print("[*] Press Ctrl+C to stop the server")
    print("=" * 60)

    try:
        uvicorn.run(app, host="127.0.0.1", port=8001, log_level="info", access_log=True)
    except KeyboardInterrupt:
        print("\n[*] Server stopped by user")
    except Exception as e:
        print(f"[!] Server error: {e}")
        import traceback

        traceback.print_exc()
