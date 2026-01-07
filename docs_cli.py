import argparse
import sys
import os
from library_manager import LibraryManager

def main():
    parser = argparse.ArgumentParser(description="Documentation Library CLI")
    subparsers = parser.add_subparsers(dest="command", help="Command to execute")

    # List command
    subparsers.add_parser("list", help="List all available documentation sets")

    # Path command
    path_parser = subparsers.add_parser("path", help="Get absolute path to a documentation set")
    path_parser.add_argument("alias", help="Alias of the documentation")

    # Context command
    ctx_parser = subparsers.add_parser("context", help="Get AI context content (llms.txt)")
    ctx_parser.add_argument("alias", help="Alias of the documentation")

    # Query command
    query_parser = subparsers.add_parser("query", help="Semantic search in documentation")
    query_parser.add_argument("alias", help="Alias of the documentation")
    query_parser.add_argument("text", help="The query text")
    query_parser.add_argument("-k", type=int, default=3, help="Number of results to return")

    # Index command
    idx_parser = subparsers.add_parser("index", help="Build/Rebuild vector index for a doc set")
    idx_parser.add_argument("alias", help="Alias of the documentation")

    # Add command
    add_parser = subparsers.add_parser("add", help="Manually add a folder to library")
    add_parser.add_argument("path", help="Path to the documentation folder")
    add_parser.add_argument("alias", help="Alias to assign")

    args = parser.parse_args()
    
    manager = LibraryManager()

    if args.command == "list":
        items = manager.list_items()
        if not items:
            print("No documentation sets in library.")
            return
        print(f"{'ALIAS':<20} {'ADDED':<20} {'SOURCE'}")
        print("-" * 60)
        for alias, info in items.items():
            added = info['added_at'][:10]
            source = os.path.basename(info['path'])
            print(f"{alias:<20} {added:<20} {source}")

    elif args.command == "path":
        item = manager.get_item(args.alias)
        if item:
            print(item['link_path'])
        else:
            print(f"Error: Alias '{args.alias}' not found.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "context":
        path = manager.get_context_path(args.alias)
        if path:
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    print(f.read())
            except Exception as e:
                print(f"Error reading context file: {e}", file=sys.stderr)
                sys.exit(1)
        else:
            print(f"Error: Context (llms.txt) not found for '{args.alias}'.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "query":
        try:
            from vector_store import VectorStore
        except ImportError:
            print("Error: sentence-transformers not installed. Install with: pip install sentence-transformers numpy", file=sys.stderr)
            sys.exit(1)
            
        store_path = manager.get_vector_store_path(args.alias)
        if not store_path:
            print(f"Error: Alias '{args.alias}' not found.", file=sys.stderr)
            sys.exit(1)
            
        store = VectorStore(store_path, collection_name=args.alias)
        
        # Check if index exists
        if store.embeddings is None:
            print(f"No index found for '{args.alias}'. Run 'docs index {args.alias}' first.", file=sys.stderr)
            sys.exit(1)
            
        results = store.search(args.text, k=args.k)
        
        print(f"\nTop {len(results)} results for '{args.text}' in {args.alias}:\n")
        for i, res in enumerate(results, 1):
            score = res['score']
            content = res['content']
            source = res['metadata'].get('url', 'Unknown Source')
            print(f"{i}. [Score: {score:.3f}] Source: {source}")
            print("-" * 40)
            print(content.strip())
            print("=" * 60 + "\n")

    elif args.command == "index":
        try:
            from vector_store import VectorStore
            from content_chunker import ContentChunker
            import json
        except ImportError:
            print("Error: Missing dependencies. pip install sentence-transformers numpy", file=sys.stderr)
            sys.exit(1)
            
        store_path = manager.get_vector_store_path(args.alias)
        if not store_path:
            print(f"Error: Alias '{args.alias}' not found.", file=sys.stderr)
            sys.exit(1)
            
        print(f"Indexing '{args.alias}'... This may take a while.")
        
        # Load chunks.json if it exists, otherwise generate from content
        chunks_path = os.path.join(store_path, "chunks.json")
        chunks = []
        
        if os.path.exists(chunks_path):
            print(f"Loading chunks from {chunks_path}...")
            with open(chunks_path, 'r', encoding='utf-8') as f:
                chunks = json.load(f)
        else:
            print("chunks.json not found. Generating chunks from raw files...")
            # Simple fallback: walk directory, read .md/.html, use chunker
            chunker = ContentChunker()
            for root, dirs, files in os.walk(store_path):
                for file in files:
                    if file.endswith('.md'):
                        fpath = os.path.join(root, file)
                        with open(fpath, 'r', encoding='utf-8', errors='ignore') as f:
                            content = f.read()
                            file_chunks = chunker.chunk_markdown_file(content, url=file)
                            chunks.extend(file_chunks)
        
        if not chunks:
            print("No content found to index.", file=sys.stderr)
            sys.exit(1)
            
        store = VectorStore(store_path, collection_name=args.alias)
        
        # Prepare data for vector store
        texts = [c["content"] for c in chunks]
        metadatas = [c["metadata"] for c in chunks]
        # Ensure content is in metadata for retrieval
        for i, meta in enumerate(metadatas):
            meta["content"] = texts[i]
            
        success = store.add_texts(texts, metadatas)
        
        if success:
            print(f"Successfully indexed {len(texts)} chunks for '{args.alias}'.")
        else:
            print("Failed to index content.", file=sys.stderr)
            sys.exit(1)

    elif args.command == "add":
        success = manager.add_to_library(args.path, args.alias)
        if success:
            print(f"Successfully added '{args.alias}' to library.")
        else:
            print("Failed to add to library.", file=sys.stderr)
            sys.exit(1)

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
