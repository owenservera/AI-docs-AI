import asyncio
import aiohttp
import aiofiles
from urllib.parse import urljoin, urlparse, parse_qs
from bs4 import BeautifulSoup
import os
import re
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Set, Optional, Tuple, Any
import time
import json

# AI-friendly modules
from content_extractor import ContentExtractor
from metadata_generator import MetadataGenerator
from content_chunker import ContentChunker
from ai_sitemap_generator import AISitemapGenerator
from parsers import OpenAPIParser


class DocumentationCrawler:
    def __init__(
        self,
        base_url: str,
        max_depth: int = 3,
        include_images: bool = True,
        include_css: bool = True,
        include_js: bool = True,
        include_fonts: bool = True,
        rate_limit: float = 1.0,
        user_agent: str = "DocumentationAgent/1.0",
        output_formats: Optional[List[str]] = None,
        generate_metadata: bool = True,
        chunk_size: int = 400,
        chunk_overlap: float = 0.15,
    ):
        self.base_url = base_url.rstrip("/")
        self.max_depth = max_depth
        self.include_images = include_images
        self.include_css = include_css
        self.include_js = include_js
        self.include_fonts = include_fonts
        self.rate_limit = rate_limit
        self.user_agent = user_agent

        # AI-friendly output options
        self.output_formats = output_formats or ["html"]
        self.generate_metadata = generate_metadata
        self.chunk_size = chunk_size
        self.chunk_overlap = chunk_overlap

        # Initialize AI modules
        self.content_extractor = ContentExtractor()
        self.metadata_generator = MetadataGenerator()
        self.content_chunker = ContentChunker(chunk_size, chunk_overlap)
        self.ai_sitemap_generator = AISitemapGenerator()
        self.openapi_parser = OpenAPIParser()

        # State management
        self.visited_urls: Set[str] = set()
        self.pending_urls: List[Tuple[str, int]] = [(base_url, 0)]
        self.downloaded_files: List[Dict] = []
        self.errors: List[str] = []
        self.current_page: Optional[str] = None
        self.is_running = False
        self.should_stop = False

        # Statistics
        self.start_time: Optional[datetime] = None
        self.pages_found = 0
        self.pages_downloaded = 0

        # Output directory
        self.output_dir = None

        # Session
        self.session = None

    async def crawl(self) -> Dict:
        """Main crawling method"""
        self.is_running = True
        self.start_time = datetime.now()

        try:
            # Create output directory
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(self.base_url).netloc.replace(".", "_")
            self.output_dir = f"downloads/{domain}_{timestamp}"
            os.makedirs(self.output_dir, exist_ok=True)

            # Create aiohttp session
            timeout = aiohttp.ClientTimeout(total=30)
            headers = {"User-Agent": self.user_agent}

            async with aiohttp.ClientSession(
                timeout=timeout, headers=headers
            ) as session:
                self.session = session

                while self.pending_urls and not self.should_stop:
                    if not self.pending_urls:
                        break

                    url, depth = self.pending_urls.pop(0)

                    if url in self.visited_urls or depth > self.max_depth:
                        continue

                    try:
                        await self._process_page(url, depth)
                    except Exception as e:
                        self.errors.append(f"Error processing {url}: {str(e)}")

                    # Rate limiting
                    await asyncio.sleep(self.rate_limit)

            self.is_running = False

            # Generate index file
            await self._generate_index()

            # Generate AI-friendly outputs
            await self._generate_ai_summaries()

            return {
                "status": "completed"
                if (len(self.errors) == 0 or self.pages_downloaded > 0)
                else "failed",
                "success": len(self.errors) == 0 or self.pages_downloaded > 0,
                "pages_found": self.pages_found,
                "pages_downloaded": self.pages_downloaded,
                "errors": self.errors,
                "output_path": self.output_dir,
                "file_structure": self._get_file_structure(),
                "ai_outputs": self._get_ai_outputs_summary(),
            }

        except Exception as e:
            self.is_running = False
            self.errors.append(f"Crawl failed: {str(e)}")
            return {
                "status": "failed",
                "success": False,
                "pages_found": self.pages_found,
                "pages_downloaded": self.pages_downloaded,
                "errors": self.errors,
                "output_path": self.output_dir if hasattr(self, "output_dir") else None,
                "file_structure": self._get_file_structure()
                if hasattr(self, "downloaded_files")
                else {},
                "ai_outputs": self._get_ai_outputs_summary()
                if hasattr(self, "ai_outputs")
                else {},
            }

    async def _generate_ai_summaries(self):
        """Generate AI-friendly summary files and sitemaps"""

        if not self.generate_metadata or not self.output_dir:
            return

        # Collect all page metadata
        pages_metadata = []
        metadata_dir = os.path.join(self.output_dir, "metadata")

        if os.path.exists(metadata_dir):
            for file_name in os.listdir(metadata_dir):
                if file_name.endswith(".metadata.json"):
                    metadata_path = os.path.join(metadata_dir, file_name)
                    try:
                        with open(metadata_path, "r", encoding="utf-8") as f:
                            page_metadata = json.load(f)
                            pages_metadata.append(page_metadata)
                    except Exception as e:
                        self.errors.append(
                            f"Failed to load metadata {file_name}: {str(e)}"
                        )

        if not pages_metadata:
            return

        # Extract site name
        site_name = urlparse(self.base_url).netloc

        # Generate AI sitemap (llms.txt)
        try:
            llms_txt = self.ai_sitemap_generator.generate_llms_txt(
                pages_metadata, site_name, self.base_url
            )
            llms_path = os.path.join(self.output_dir, "llms.txt")
            await self._save_file(llms_txt, llms_path, "text/plain")
        except Exception as e:
            self.errors.append(f"Failed to generate llms.txt: {str(e)}")

        # Generate AI sitemap JSON
        try:
            ai_sitemap_json = self.ai_sitemap_generator.generate_ai_sitemap_json(
                pages_metadata, site_name, self.base_url
            )
            sitemap_path = os.path.join(self.output_dir, "ai-sitemap.json")
            await self._save_file(
                json.dumps(ai_sitemap_json, indent=2), sitemap_path, "application/json"
            )
        except Exception as e:
            self.errors.append(f"Failed to generate ai-sitemap.json: {str(e)}")

        # Generate navigation index
        try:
            nav_index = self.ai_sitemap_generator.generate_navigation_index(
                pages_metadata, self.base_url
            )
            index_path = os.path.join(self.output_dir, "ai-index.html")
            await self._save_file(nav_index, index_path, "text/html")
        except Exception as e:
            self.errors.append(f"Failed to generate AI navigation index: {str(e)}")

        # Generate summary report
        try:
            summary = self.ai_sitemap_generator.generate_summary_report(pages_metadata)
            summary_path = os.path.join(self.output_dir, "ai-summary.json")
            await self._save_file(
                json.dumps(summary, indent=2), summary_path, "application/json"
            )
        except Exception as e:
            self.errors.append(f"Failed to generate AI summary: {str(e)}")

    def _get_ai_outputs_summary(self) -> Dict[str, Any]:
        """Get summary of AI-generated outputs"""
        summary = {}
        if not self.output_dir:
            return summary
        output_dir = Path(self.output_dir)

        # Count files by type
        if "markdown" in self.output_formats:
            md_files = list(output_dir.glob("**/*.md"))
            summary["markdown_files"] = len(md_files)

        if "json" in self.output_formats:
            json_files = list(output_dir.glob("**/*.json"))
            # Exclude metadata and chunks files from count
            json_files = [
                f
                for f in json_files
                if not any(x in str(f) for x in ["metadata", "chunks", "summary"])
            ]
            summary["json_files"] = len(json_files)

        if "chunks" in self.output_formats:
            chunk_files = list(output_dir.glob("**/chunks.json"))
            summary["chunk_files"] = len(chunk_files)

        if self.generate_metadata:
            metadata_files = list(output_dir.glob("**/metadata.json"))
            schema_files = list(output_dir.glob("**/schema.jsonld"))
            summary["metadata_files"] = len(metadata_files)
            summary["schema_files"] = len(schema_files)

        # AI summary files
        ai_files = {
            "llms.txt": list(output_dir.glob("llms.txt")),
            "ai-sitemap.json": list(output_dir.glob("ai-sitemap.json")),
            "ai-index.html": list(output_dir.glob("ai-index.html")),
            "ai-summary.json": list(output_dir.glob("ai-summary.json")),
        }

        summary["ai_summary_files"] = {k: len(v) for k, v in ai_files.items()}

        return summary

    async def _process_page(self, url: str, depth: int):
        """Process a single page"""
        if self.should_stop:
            return

        self.current_page = url
        self.visited_urls.add(url)

        if not self.session:
            self.errors.append(f"Session not initialized for {url}")
            return

        try:
            async with self.session.get(url) as response:
                if response.status != 200:
                    self.errors.append(f"HTTP {response.status} for {url}")
                    return

                content_type = response.headers.get("content-type", "").lower()

                if "text/html" in content_type:
                    await self._process_html(url, depth, response)
                else:
                    await self._process_asset(url, response, content_type)

        except Exception as e:
            self.errors.append(f"Failed to fetch {url}: {str(e)}")

    async def _process_html(self, url: str, depth: int, response):
        """Process HTML page and extract links"""
        content = await response.text()
        soup = BeautifulSoup(content, "html.parser")

        # Save HTML file
        if "html" in self.output_formats:
            file_path = self._get_file_path(url, "html")
            await self._save_file(content, file_path, "text/html")

        # Generate AI-friendly outputs
        await self._generate_ai_outputs(url, content, soup)

        self.pages_downloaded += 1

        # Extract and queue new URLs
        if depth < self.max_depth:
            links = self._extract_links(soup, url)
            for link in links:
                if link not in self.visited_urls:
                    self.pending_urls.append((link, depth + 1))
                    self.pages_found += 1

        # Download assets
        await self._download_assets(soup, url)

    async def _generate_ai_outputs(self, url: str, content: str, soup: BeautifulSoup):
        """Generate AI-friendly output formats"""

        # Generate Markdown
        if "markdown" in self.output_formats:
            markdown = self.content_extractor.extract_markdown(soup, self.base_url)
            markdown_path = self._get_file_path(url, "md")
            await self._save_file(markdown, markdown_path, "text/markdown")

        # Generate JSON
        if "json" in self.output_formats:
            json_data = self.content_extractor.extract_structured_json(soup, url)
            json_path = self._get_file_path(url, "json")
            await self._save_file(
                json.dumps(json_data, indent=2), json_path, "application/json"
            )

        # Generate metadata
        if self.generate_metadata:
            metadata = self.metadata_generator.generate_page_metadata(
                url, content, soup
            )
            metadata_path = self._get_file_path(url, "metadata.json")
            await self._save_file(
                json.dumps(metadata, indent=2), metadata_path, "application/json"
            )

            # Generate JSON-LD schema
            jsonld_schema = self.metadata_generator.generate_jsonld_schema(
                metadata, soup
            )
            schema_path = self._get_file_path(url, "schema.jsonld")
            await self._save_file(
                json.dumps(jsonld_schema, indent=2), schema_path, "application/ld+json"
            )

        # Generate chunks
        if "chunks" in self.output_formats:
            sections = self.content_extractor.extract_structured_json(soup, url).get(
                "sections", []
            )
            chunks = self.content_chunker.chunk_by_sections(sections, url)

            # Save chunks as JSON
            chunks_path = self._get_file_path(url, "chunks.json")
            await self._save_file(
                json.dumps(chunks, indent=2), chunks_path, "application/json"
            )

    async def _process_asset(self, url: str, response, content_type: str):
        """Process non-HTML assets (images, CSS, JS)"""
        
        # Check for OpenAPI spec
        if self.openapi_parser.can_parse("", url): # URL check first
            try:
                content_bytes = await response.read()
                content_str = content_bytes.decode('utf-8')
                
                if self.openapi_parser.can_parse(content_str, url):
                    parsed_data = self.openapi_parser.parse(content_str, url)
                    
                    # Save parsed tools definition
                    tools_path = self._get_file_path(url, "tools.json")
                    await self._save_file(
                        json.dumps(parsed_data, indent=2), 
                        tools_path, 
                        "application/json"
                    )
            except Exception as e:
                # Fallback to normal download if parsing fails
                pass

        if not self._should_download_asset(content_type):
            return

        file_path = self._get_file_path(url, self._get_file_extension(content_type))
        # Ensure we haven't already read the stream
        # (in real implementation, would need to handle stream consumption carefully)
        # Re-reading response might be an issue if not buffered. 
        # For this snippet, assuming we can re-read or didn't read if not openapi.
        
        # NOTE: aiohttp response.read() caches the result, so calling it again is fine.
        content = await response.read()
        await self._save_file(content, file_path, content_type, binary=True)

    async def _download_assets(self, soup: BeautifulSoup, base_url: str):
        """Download CSS, JS, and image assets"""
        assets = []

        # CSS files
        if self.include_css:
            for link in soup.find_all("link", rel="stylesheet"):
                href = link.get("href")
                if href:
                    assets.append(urljoin(base_url, href))

        # JS files
        if self.include_js:
            for script in soup.find_all("script", src=True):
                src = script.get("src")
                if src:
                    assets.append(urljoin(base_url, src))

        # Images - skip all images when include_images is False
        if self.include_images:
            for img in soup.find_all("img"):
                src = img.get("src")
                if src:
                    assets.append(urljoin(base_url, src))

        # Optimize HTML for text-only mode
        if not self.include_images:
            # Remove img tags entirely to save space and speed up processing
            for img in soup.find_all("img"):
                img.decompose()

        if not self.include_fonts:
            # Remove font-related links and styles
            for link in soup.find_all("link", rel=lambda x: x and "font" in x.lower()):
                link.decompose()

        # Download assets
        for asset_url in assets:
            if asset_url not in self.visited_urls:
                self.visited_urls.add(asset_url)
                try:
                    async with self.session.get(asset_url) as response:
                        if response.status == 200:
                            content_type = response.headers.get("content-type", "")
                            content = await response.read()
                            file_path = self._get_file_path(
                                asset_url, self._get_file_extension(content_type)
                            )
                            await self._save_file(
                                content, file_path, content_type, binary=True
                            )
                except Exception as e:
                    self.errors.append(
                        f"Failed to download asset {asset_url}: {str(e)}"
                    )

    def _extract_links(self, soup: BeautifulSoup, base_url: str) -> List[str]:
        """Extract all internal links from HTML"""
        links = []

        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")
            if href:
                # Normalize URL
                full_url = urljoin(base_url, href)

                # Check if it's internal link
                if self._is_internal_link(full_url):
                    # Remove fragment and query parameters for comparison
                    clean_url = full_url.split("#")[0].split("?")[0]
                    if clean_url not in self.visited_urls:
                        links.append(clean_url)

        return links

    def _is_internal_link(self, url: str) -> bool:
        """Check if URL is internal to the documentation site"""
        base_domain = urlparse(self.base_url).netloc
        link_domain = urlparse(url).netloc

        # Empty domain means relative link
        if not link_domain:
            return True

        return link_domain == base_domain

    def _should_download_asset(self, content_type: str) -> bool:
        """Check if asset type should be downloaded"""
        content_type = content_type.lower()

        if "text/css" in content_type and self.include_css:
            return True
        if "javascript" in content_type and self.include_js:
            return True
        if "image" in content_type and self.include_images:
            return True
        if "font" in content_type and self.include_fonts:
            return True
        # Skip media files for text-only mode
        if "video" in content_type or "audio" in content_type:
            return False
        return False

    def _get_file_extension(self, content_type: str) -> str:
        """Get file extension from content type"""
        content_type = content_type.lower()

        if "text/html" in content_type:
            return "html"
        elif "text/css" in content_type:
            return "css"
        elif "javascript" in content_type:
            return "js"
        elif "image/png" in content_type:
            return "png"
        elif "image/jpeg" in content_type or "image/jpg" in content_type:
            return "jpg"
        elif "image/svg" in content_type:
            return "svg"
        elif "image/gif" in content_type:
            return "gif"
        elif "font/woff2" in content_type:
            return "woff2"
        elif "font/woff" in content_type:
            return "woff"
        elif "font/ttf" in content_type:
            return "ttf"
        else:
            return "bin"

    def _get_file_path(self, url: str, extension: str) -> str:
        """Generate file path for URL"""
        parsed = urlparse(url)

        # Ensure output_dir exists
        if not hasattr(self, "output_dir") or self.output_dir is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            domain = urlparse(self.base_url).netloc.replace(".", "_")
            self.output_dir = f"downloads/{domain}_{timestamp}"
            os.makedirs(self.output_dir, exist_ok=True)

        # Remove base URL path
        base_parsed = urlparse(self.base_url)
        relative_path = parsed.path.replace(base_parsed.path, "", 1).lstrip("/")

        # Handle root URL
        if not relative_path:
            relative_path = "index"

        # Remove file extension if present
        relative_path = re.sub(r"\.[^.]+$", "", relative_path)

        # Create directory structure
        if "/" in relative_path:
            dirs = relative_path.rsplit("/", 1)[0]
            os.makedirs(os.path.join(self.output_dir, dirs), exist_ok=True)

        # Generate filename
        if parsed.query:
            query_hash = hash(parsed.query) % 10000
            filename = f"{relative_path}_{query_hash}.{extension}"
        else:
            filename = f"{relative_path}.{extension}"

        return os.path.join(self.output_dir, filename)

    async def _save_file(
        self, content, file_path: str, content_type: str, binary=False
    ):
        """Save file to disk"""
        mode = "wb" if binary else "w"
        encoding = None if binary else "utf-8"

        async with aiofiles.open(file_path, mode, encoding=encoding) as f:
            await f.write(content)

        # Record downloaded file
        self.downloaded_files.append(
            {
                "path": file_path,
                "url": self.current_page,
                "content_type": content_type,
                "size": os.path.getsize(file_path),
            }
        )

    async def _generate_index(self):
        """Generate index.html file for navigation"""
        index_content = f"""
<!DOCTYPE html>
<html>
<head>
    <title>Documentation Archive</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            margin: 40px;
            background-color: #f5f5f5;
        }}
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background: white;
            padding: 30px;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }}
        h1 {{
            color: #333;
            border-bottom: 2px solid #007acc;
            padding-bottom: 10px;
        }}
        .stats {{
            background: #f8f9fa;
            padding: 20px;
            border-radius: 5px;
            margin: 20px 0;
        }}
        .file-tree {{
            margin-top: 30px;
        }}
        .file-tree ul {{
            list-style: none;
            padding-left: 20px;
        }}
        .file-tree li {{
            margin: 5px 0;
            padding: 5px;
            border-radius: 3px;
        }}
        .file-tree li:hover {{
            background-color: #f0f0f0;
        }}
        .file-tree a {{
            text-decoration: none;
            color: #007acc;
        }}
        .file-tree a:hover {{
            text-decoration: underline;
        }}
        .folder {{
            font-weight: bold;
            color: #666;
        }}
    </style>
</head>
<body>
    <div class="container">
        <h1>📚 Documentation Archive</h1>
        <p><strong>Source:</strong> {self.base_url}</p>
        <p><strong>Generated:</strong> {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        
        <div class="stats">
            <h3>Statistics</h3>
            <p><strong>Pages Downloaded:</strong> {self.pages_downloaded}</p>
            <p><strong>Total Files:</strong> {len(self.downloaded_files)}</p>
            <p><strong>Output Directory:</strong> {os.path.basename(self.output_dir)}</p>
        </div>
        
        <div class="file-tree">
            <h3>File Structure</h3>
            {self._generate_file_tree_html()}
        </div>
    </div>
</body>
</html>
"""

        index_path = os.path.join(self.output_dir, "index.html")
        async with aiofiles.open(index_path, "w", encoding="utf-8") as f:
            await f.write(index_content)

    def _generate_file_tree_html(self) -> str:
        """Generate HTML file tree structure"""
        tree = {}
        for file_info in self.downloaded_files:
            path = os.path.relpath(file_info["path"], self.output_dir)
            parts = path.split("/")

            current = tree
            for part in parts[:-1]:
                if part not in current:
                    current[part] = {}
                current = current[part]

            current[parts[-1]] = file_info["url"]

        def build_html(tree, level=0):
            html = "<ul>"
            for name, value in sorted(tree.items()):
                if isinstance(value, dict):
                    html += f'<li class="folder">📁 {name}</li>'
                    html += build_html(value, level + 1)
                else:
                    html += f'<li><a href="{name}">📄 {name}</a></li>'
            html += "</ul>"
            return html

        return build_html(tree)

    def _get_file_structure(self) -> Dict:
        """Get file structure as dictionary"""
        structure = {"directories": {}, "files": []}

        for file_info in self.downloaded_files:
            path = os.path.relpath(file_info["path"], self.output_dir)
            structure["files"].append(
                {
                    "path": path,
                    "url": file_info["url"],
                    "size": file_info["size"],
                    "content_type": file_info["content_type"],
                }
            )

        return structure

    async def get_status(self) -> Dict:
        """Get current crawling status"""
        elapsed = (
            (datetime.now() - self.start_time).total_seconds() if self.start_time else 0
        )

        # Calculate estimated completion
        estimated_completion = None
        if self.pages_downloaded > 0 and self.pages_found > 0:
            pages_remaining = self.pages_found - self.pages_downloaded
            estimated_seconds = (pages_remaining * self.rate_limit) + elapsed
            estimated_completion = (
                datetime.now() + timedelta(seconds=estimated_seconds)
            ).isoformat()

        return {
            "crawl_id": "unknown",  # Will be set by the caller
            "status": "running" if self.is_running else "stopped",
            "pages_found": self.pages_found,
            "pages_downloaded": self.pages_downloaded,
            "current_page": self.current_page,
            "errors": self.errors[-10:],  # Last 10 errors
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "elapsed_seconds": elapsed,
            "estimated_completion": estimated_completion,
            "pending_urls": len(self.pending_urls),
            "visited_urls": len(self.visited_urls),
        }

    async def stop(self):
        """Stop the crawling process"""
        self.should_stop = True
        self.is_running = False
