# Documentation Download Agent

A powerful web application that allows you to download and archive complete documentation websites with a single click. Perfect for developers who need offline access to documentation, creating local backups, or archiving important technical resources.

## Features

### 🚀 Core Capabilities
- **Smart URL Discovery**: Automatically discovers and downloads all pages within a documentation site
- **Complete Asset Download**: Downloads HTML, CSS, JavaScript, images, and fonts
- **Organized Structure**: Maintains original site hierarchy and generates navigation index
- **ZIP Export**: Creates clean, downloadable ZIP archives with all documentation

### 🎨 Modern Interface
- **Dark Theme**: Developer-friendly dark interface with neon accents
- **Real-time Progress**: Live crawling status with progress bars and statistics
- **File Browser**: Browse downloaded content with search functionality
- **Advanced Options**: Configure crawling depth, rate limits, and file types

### 🔧 Technical Features
- **Recursive Crawling**: Configurable depth levels for comprehensive coverage
- **Rate Limiting**: Respectful crawling with adjustable delays
- **Error Handling**: Comprehensive error logging and recovery
- **Progress Tracking**: Real-time monitoring of pages found and downloaded
- **Asset Preservation**: Maintains all CSS, JS, and image dependencies

## Universal Call System

The application includes a powerful "Universal Call System" that allows you to manage and access your downloaded documentation sets via a unified CLI. This is particularly useful for pointing AI coding agents (like Gemini CLI, OpenCode CLI, Claude Code CLI) to specific documentation contexts.

### CLI Usage

The `docs` command (accessible via `docs.bat` on Windows) provides the following subcommands:

- **`docs list`**: List all registered documentation sets in your library.
- **`docs path <alias>`**: Get the absolute path to the documentation folder for a given alias.
- **`docs context <alias>`**: Output the content of the `llms.txt` context file for the given alias (if it exists).
- **`docs add <path> <alias>`**: Manually register a documentation folder with a specific alias.

### Automatic Registration

When you download documentation using the web interface, it is automatically registered in the library using the domain name as the alias (e.g., `react.dev` becomes `react`).

### AI Integration Example

You can easily feed documentation context to your AI tools:

```bash
# Feed React documentation context to an AI agent
docs context react | ai-agent "How do I use useEffect?"
```

## Advanced AI Features

### 🧠 Semantic Search (RAG)
Instead of reading the entire documentation, you can now index and query it for specific answers using local vector search.

1.  **Index a library**:
    ```bash
    docs index react
    ```
2.  **Query the library**:
    ```bash
    docs query react "How do I optimize useEffect?"
    ```

### 🤖 MCP Server Integration
This tool acts as a **Model Context Protocol (MCP)** server, allowing AI assistants (like Claude Desktop or Cursor) to directly access your documentation library.

To use with Claude Desktop, add this to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "docs-ai": {
      "command": "py",
      "args": ["/path/to/docs-ai/mcp_server.py"]
    }
  }
}
```

### 🔌 Intelligent Parsing
The crawler now automatically detects **OpenAPI/Swagger** specifications and parses them into AI-friendly "Tool Definitions" (`tools.json`), making it easier for agents to understand API capabilities.

## Quick Start

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Installation

1. Clone or download the application files
2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to `http://localhost:8000`

### Usage

1. **Enter URL**: Paste the root URL of the documentation you want to download (e.g., `https://opencode.ai/docs/`)
2. **Configure Options**: Adjust crawling depth, rate limits, and file type preferences
3. **Start Crawling**: Click "Start Crawling" to begin the download process
4. **Monitor Progress**: Watch real-time progress updates and statistics
5. **Download ZIP**: Once complete, download the organized documentation as a ZIP file

## Configuration Options

### Basic Settings
- **URL**: The root URL of the documentation site
- **Max Depth**: How many levels deep to crawl (1-5)
- **Rate Limit**: Delay between requests in seconds (0-5s)

### File Type Filters
- **Images**: Download PNG, JPG, GIF, SVG files
- **CSS**: Download stylesheets and maintain visual appearance
- **JavaScript**: Download scripts for interactive features
- **Fonts**: Download web fonts for proper typography

## Architecture

### Backend Components
- **FastAPI Server**: Handles API requests and web interface
- **Documentation Crawler**: Async crawler with rate limiting and error handling
- **File Manager**: Organizes files and creates ZIP archives

### Frontend Components
- **Modern JavaScript**: ES6+ with async/await patterns
- **Anime.js**: Smooth animations and micro-interactions
- **ECharts.js**: Data visualization for progress tracking
- **Tailwind CSS**: Utility-first styling with custom dark theme

## API Endpoints

### Core Endpoints
- `POST /api/start_crawl`: Initiate documentation crawling
- `GET /api/crawl_status/{crawl_id}`: Get current crawling progress
- `GET /api/list_files/{crawl_id}`: List all downloaded files
- `GET /api/download_zip/{crawl_id}`: Download ZIP archive
- `POST /api/stop_crawl/{crawl_id}`: Stop ongoing crawl

## Examples

### Downloading Python Documentation
```
URL: https://docs.python.org/3/
Max Depth: 3
Include: All file types
Rate Limit: 1 second
```

### Archiving a JavaScript Library Docs
```
URL: https://developer.mozilla.org/en-US/docs/Web/JavaScript
Max Depth: 2
Include: HTML, CSS, JS only
Rate Limit: 2 seconds
```

## Best Practices

### Respectful Crawling
- Use appropriate rate limits (1-2 seconds for most sites)
- Check robots.txt if available
- Avoid crawling during peak hours
- Consider the target server's capacity

### Large Documentation Sites
- Start with lower depth settings (2-3)
- Monitor memory usage during crawling
- Download in multiple sessions if needed
- Use file type filters to reduce download size

### Troubleshooting
- **Slow downloads**: Increase rate limit or reduce depth
- **Missing files**: Check if all file types are enabled
- **Connection errors**: Verify URL accessibility and network connection
- **Large archives**: Consider downloading smaller sections

## Technical Details

### File Structure
```
downloads/
├── {domain}_{timestamp}/
│   ├── index.html (navigation index)
│   ├── {page1}.html
│   ├── {page2}.html
│   ├── css/
│   │   └── {stylesheets}
│   ├── js/
│   │   └── {scripts}
│   └── images/
│       └── {assets}
└── archives/
    └── documentation_{crawl_id}.zip
```

### Error Handling
- Network timeouts and retries
- Invalid content type handling
- Permission and access restrictions
- Graceful degradation for missing resources

### Performance Considerations
- Concurrent request management
- Memory-efficient file processing
- Progressive download tracking
- Optimized ZIP compression

## Browser Compatibility

- **Chrome**: 88+ (Recommended)
- **Firefox**: 85+
- **Safari**: 14+
- **Edge**: 88+

## Contributing

This is a complete, production-ready application. The modular architecture makes it easy to extend:

- Add new file type handlers in `crawler.py`
- Extend UI components in `main.js`
- Add new API endpoints in `main.py`
- Customize styling in `style.css`

## License

This project is provided as-is for educational and personal use. Please respect the terms of service of websites you crawl and ensure you have permission to download and archive content.

## Support

For issues, feature requests, or contributions:
- Check the troubleshooting section
- Review the technical documentation
- Test with different documentation sites
- Monitor browser console for errors

---

**Documentation Download Agent** - Empowering developers with offline documentation access since 2024.