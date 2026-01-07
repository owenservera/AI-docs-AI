import os
import json
import shutil
import logging
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LibraryManager:
    def __init__(self, base_dir: str = "."):
        self.base_dir = os.path.abspath(base_dir)
        self.library_dir = os.path.join(self.base_dir, "library")
        self.registry_file = os.path.join(self.library_dir, "registry.json")
        
        # Ensure library directory exists
        os.makedirs(self.library_dir, exist_ok=True)
        self._load_registry()

    def _load_registry(self):
        """Load the library registry from disk"""
        if os.path.exists(self.registry_file):
            try:
                with open(self.registry_file, 'r', encoding='utf-8') as f:
                    self.registry = json.load(f)
            except Exception as e:
                logger.error(f"Failed to load registry: {e}")
                self.registry = {"items": {}}
        else:
            self.registry = {"items": {}}
            self._save_registry()

    def _save_registry(self):
        """Save the library registry to disk"""
        try:
            with open(self.registry_file, 'w', encoding='utf-8') as f:
                json.dump(self.registry, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save registry: {e}")

    def add_to_library(self, source_path: str, alias: str, metadata: Dict = None) -> bool:
        """Register a documentation folder into the library with an alias"""
        source_path = os.path.abspath(source_path)
        
        if not os.path.exists(source_path):
            logger.error(f"Source path does not exist: {source_path}")
            return False

        # Sanitize alias
        alias = "".join(c for c in alias if c.isalnum() or c in ('-', '_')).lower()
        target_link = os.path.join(self.library_dir, alias)

        # Remove existing link/folder if it exists
        if os.path.exists(target_link):
            if os.path.islink(target_link) or os.path.isfile(target_link):
                os.remove(target_link)
            elif os.path.isdir(target_link):
                # On Windows, junctions are dirs, but we can remove them with rmdir if they are junctions
                # Python's rmtree is safer
                try:
                    os.rmdir(target_link) # Try rmdir first for junctions
                except OSError:
                    pass # Might not be a junction or might be non-empty normal dir

        # Create Symlink / Junction
        try:
            # Python 3.8+ supports symlinks on Windows if developer mode is on, or admin.
            # Fallback to junction for Windows if symlink fails, or copy if all fails.
            if os.name == 'nt':
                import _winapi
                try:
                    _winapi.CreateJunction(source_path, target_link)
                except Exception as e:
                    logger.warning(f"Failed to create junction: {e}. Trying symlink.")
                    os.symlink(source_path, target_link, target_is_directory=True)
            else:
                os.symlink(source_path, target_link)
        except Exception as e:
            logger.error(f"Failed to create link for {alias}: {e}")
            return False

        # Update Registry
        self.registry["items"][alias] = {
            "path": source_path,
            "link_path": target_link,
            "added_at": datetime.now().isoformat(),
            "metadata": metadata or {}
        }
        self._save_registry()
        logger.info(f"Added '{alias}' to library linked to {source_path}")
        return True

    def get_item(self, alias: str) -> Optional[Dict]:
        """Get info for a library item"""
        return self.registry["items"].get(alias)

    def list_items(self) -> Dict[str, Dict]:
        """List all items in the library"""
        return self.registry["items"]

    def remove_item(self, alias: str) -> bool:
        """Remove an item from the library"""
        if alias not in self.registry["items"]:
            return False
        
        target_link = os.path.join(self.library_dir, alias)
        if os.path.exists(target_link):
            try:
                if os.name == 'nt':
                     os.rmdir(target_link) # Remove junction
                else:
                    os.unlink(target_link)
            except Exception:
                pass # Best effort
        
        del self.registry["items"][alias]
        self._save_registry()
        return True

    def get_context_path(self, alias: str, context_file: str = "llms.txt") -> Optional[str]:
        """Get the absolute path to a specific context file for an alias"""
        item = self.get_item(alias)
        if not item:
            return None
        
        # Check both the link path and original path
        paths_to_check = [item["link_path"], item["path"]]
        
        for base_path in paths_to_check:
            candidate = os.path.join(base_path, context_file)
            if os.path.exists(candidate):
                return candidate
            
        return None

    def get_vector_store_path(self, alias: str) -> Optional[str]:
        """Get the directory path where vector store indices are kept for an alias"""
        item = self.get_item(alias)
        if not item:
            return None
        return item["link_path"]
