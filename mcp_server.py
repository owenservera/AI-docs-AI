import asyncio
import os
import sys
import logging
from typing import Any, List

from mcp.server.fastmcp import FastMCP
from library_manager import LibraryManager

# Initialize FastMCP server
mcp = FastMCP("DocsAI")

# Fix: Ensure we look for library in the script's directory, not CWD
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
library_manager = LibraryManager(base_dir=BASE_DIR)

@mcp.tool()
def list_documentation() -> str:
    """List all available documentation sets in the library."""
    items = library_manager.list_items()
    if not items:
        return "No documentation sets found."
    
    result = ["Available Documentation:"]
    for alias, info in items.items():
        result.append(f"- {alias} (Source: {os.path.basename(info['path'])})")
    return "\n".join(result)

@mcp.tool()
def get_documentation_context(alias: str) -> str:
    """Get the full AI context (llms.txt) for a documentation set."""
    path = library_manager.get_context_path(alias)
    if not path:
        return f"Error: No context found for '{alias}'"
    
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"Error reading context: {str(e)}"

@mcp.tool()
def search_documentation(alias: str, query: str) -> str:
    """
    Search for specific information within a documentation set.
    Use this to find relevant code snippets, API details, or guides.
    """
    try:
        from vector_store import VectorStore
    except ImportError:
        return "Error: Vector search dependencies not installed."

    store_path = library_manager.get_vector_store_path(alias)
    if not store_path:
        return f"Error: Documentation '{alias}' not found."

    store = VectorStore(store_path, collection_name=alias)
    if store.embeddings is None:
        return f"Error: Index not built for '{alias}'. Please ask user to run 'docs index {alias}'."

    results = store.search(query, k=5)
    if not results:
        return f"No results found for '{query}' in {alias}."

    formatted = [f"Search results for '{query}' in {alias}:\n"]
    for i, res in enumerate(results, 1):
        formatted.append(f"Result {i} (Score: {res['score']:.2f}):")
        formatted.append(f"{res['content']}")
        formatted.append("-" * 20)

    return "\n".join(formatted)

if __name__ == "__main__":
    # fastmcp uses run() to start the stdio server
    mcp.run()
