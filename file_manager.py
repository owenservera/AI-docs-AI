import os
import zipfile
import shutil
from pathlib import Path
from typing import Dict, List, Optional
import json

class FileManager:
    def __init__(self):
        pass
    
    def get_file_structure(self, directory: str) -> Dict:
        """Get complete file structure of a directory"""
        structure = {
            "name": os.path.basename(directory),
            "type": "directory",
            "path": directory,
            "children": [],
            "size": 0,
            "file_count": 0
        }
        
        try:
            for item in sorted(os.listdir(directory)):
                item_path = os.path.join(directory, item)
                
                if os.path.isfile(item_path):
                    file_info = {
                        "name": item,
                        "type": "file",
                        "path": item_path,
                        "size": os.path.getsize(item_path),
                        "extension": os.path.splitext(item)[1].lower()
                    }
                    structure["children"].append(file_info)
                    structure["size"] += file_info["size"]
                    structure["file_count"] += 1
                    
                elif os.path.isdir(item_path):
                    subdir_structure = self.get_file_structure(item_path)
                    structure["children"].append(subdir_structure)
                    structure["size"] += subdir_structure["size"]
                    structure["file_count"] += subdir_structure["file_count"]
                    
        except PermissionError:
            pass  # Skip directories we can't access
            
        return structure
    
    def calculate_total_size(self, directory: str) -> int:
        """Calculate total size of directory in bytes"""
        total_size = 0
        
        for dirpath, dirnames, filenames in os.walk(directory):
            for filename in filenames:
                filepath = os.path.join(dirpath, filename)
                try:
                    total_size += os.path.getsize(filepath)
                except (OSError, IOError):
                    pass  # Skip files we can't access
                    
        return total_size
    
    def create_zip_archive(self, source_directory: str, archive_name: str) -> str:
        """Create a ZIP archive of the documentation"""
        # Ensure output directory exists
        output_dir = "downloads/archives"
        os.makedirs(output_dir, exist_ok=True)
        
        # Generate ZIP file path
        zip_path = os.path.join(output_dir, f"{archive_name}.zip")
        
        # Create ZIP archive
        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            # Walk through the directory structure
            for root, dirs, files in os.walk(source_directory):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, source_directory)
                    
                    try:
                        zipf.write(file_path, arcname)
                    except (OSError, IOError) as e:
                        print(f"Warning: Could not add {file_path} to ZIP: {e}")
        
        return zip_path
    
    def cleanup_directory(self, directory: str):
        """Remove a directory and all its contents"""
        if os.path.exists(directory):
            shutil.rmtree(directory, ignore_errors=True)
    
    def generate_file_index(self, directory: str) -> Dict:
        """Generate a searchable index of all files"""
        index = {
            "total_files": 0,
            "total_size": 0,
            "files": [],
            "directories": []
        }
        
        for root, dirs, files in os.walk(directory):
            # Add directories
            for dir_name in dirs:
                dir_path = os.path.join(root, dir_name)
                relative_path = os.path.relpath(dir_path, directory)
                index["directories"].append({
                    "name": dir_name,
                    "path": relative_path,
                    "full_path": dir_path
                })
            
            # Add files
            for file_name in files:
                file_path = os.path.join(root, file_name)
                relative_path = os.path.relpath(file_path, directory)
                
                try:
                    file_size = os.path.getsize(file_path)
                    file_extension = os.path.splitext(file_name)[1].lower()
                    
                    file_info = {
                        "name": file_name,
                        "path": relative_path,
                        "full_path": file_path,
                        "size": file_size,
                        "extension": file_extension,
                        "size_human": self._format_file_size(file_size)
                    }
                    
                    index["files"].append(file_info)
                    index["total_files"] += 1
                    index["total_size"] += file_size
                    
                except (OSError, IOError):
                    pass  # Skip files we can't access
        
        index["total_size_human"] = self._format_file_size(index["total_size"])
        return index
    
    def search_files(self, directory: str, query: str) -> List[Dict]:
        """Search for files by name or path"""
        results = []
        query = query.lower()
        
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if query in file_name.lower():
                    file_path = os.path.join(root, file_name)
                    relative_path = os.path.relpath(file_path, directory)
                    
                    try:
                        file_size = os.path.getsize(file_path)
                        results.append({
                            "name": file_name,
                            "path": relative_path,
                            "size": file_size,
                            "extension": os.path.splitext(file_name)[1].lower(),
                            "size_human": self._format_file_size(file_size)
                        })
                    except (OSError, IOError):
                        pass
        
        return results
    
    def get_file_preview(self, file_path: str, max_lines: int = 50) -> Optional[str]:
        """Get a preview of a text file"""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                lines = []
                for i, line in enumerate(f):
                    if i >= max_lines:
                        break
                    lines.append(line.rstrip())
                
                content = '\n'.join(lines)
                if len(content) > 2000:  # Limit preview size
                    content = content[:2000] + '...'
                
                return content
        except (OSError, IOError, UnicodeDecodeError):
            return None
    
    def _format_file_size(self, size_bytes: int) -> str:
        """Format file size in human readable format"""
        if size_bytes == 0:
            return "0 B"
        
        size_names = ["B", "KB", "MB", "GB"]
        i = 0
        size = float(size_bytes)
        
        while size >= 1024.0 and i < len(size_names) - 1:
            size /= 1024.0
            i += 1
        
        return f"{size:.1f} {size_names[i]}"
    
    def create_navigation_index(self, file_structure: Dict, base_path: str = "") -> str:
        """Create HTML navigation index from file structure"""
        html_parts = []
        
        def build_navigation(structure, current_path=""):
            if structure["type"] == "directory":
                folder_name = structure["name"]
                folder_path = os.path.join(current_path, folder_name) if current_path else folder_name
                
                html_parts.append(f'<div class="folder">')
                html_parts.append(f'<span class="folder-name">📁 {folder_name}</span>')
                
                if structure["children"]:
                    html_parts.append('<div class="folder-contents">')
                    for child in structure["children"]:
                        build_navigation(child, folder_path)
                    html_parts.append('</div>')
                
                html_parts.append('</div>')
            else:
                file_name = structure["name"]
                file_path = os.path.join(current_path, file_name) if current_path else file_name
                file_icon = self._get_file_icon(structure.get("extension", ""))
                html_parts.append(f'<div class="file"><a href="{file_path}">{file_icon} {file_name}</a></div>')
        
        build_navigation(file_structure)
        return '\n'.join(html_parts)
    
    def _get_file_icon(self, extension: str) -> str:
        """Get appropriate icon for file type"""
        icon_map = {
            '.html': '🌐',
            '.css': '🎨',
            '.js': '⚡',
            '.json': '📋',
            '.png': '🖼️',
            '.jpg': '🖼️',
            '.jpeg': '🖼️',
            '.gif': '🖼️',
            '.svg': '🖼️',
            '.pdf': '📄',
            '.md': '📝',
            '.txt': '📝',
            '.zip': '📦',
            '.xml': '📰',
        }
        
        return icon_map.get(extension.lower(), '📄')
    
    def validate_download_directory(self, directory: str) -> Dict:
        """Validate if directory contains valid documentation"""
        validation_result = {
            "valid": False,
            "has_index": False,
            "html_files": 0,
            "total_files": 0,
            "warnings": []
        }
        
        if not os.path.exists(directory):
            validation_result["warnings"].append("Directory does not exist")
            return validation_result
        
        # Check for index.html
        index_path = os.path.join(directory, 'index.html')
        if os.path.exists(index_path):
            validation_result["has_index"] = True
        
        # Count files
        for root, dirs, files in os.walk(directory):
            for file in files:
                validation_result["total_files"] += 1
                if file.endswith('.html'):
                    validation_result["html_files"] += 1
        
        # Validation logic
        if validation_result["html_files"] > 0:
            validation_result["valid"] = True
        
        if validation_result["total_files"] == 0:
            validation_result["warnings"].append("No files found in directory")
        elif validation_result["html_files"] == 0:
            validation_result["warnings"].append("No HTML files found")
        
        return validation_result