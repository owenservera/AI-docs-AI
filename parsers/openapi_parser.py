import json
import yaml
from typing import Dict, Any, List, Optional
from .base_parser import BaseParser

class OpenAPIParser(BaseParser):
    """Parser for OpenAPI/Swagger specifications"""
    
    def can_parse(self, content: str, url: str) -> bool:
        """Check if content is an OpenAPI spec"""
        if url.endswith('.json') or url.endswith('.yaml') or url.endswith('.yml'):
            try:
                data = self._load_data(content, url)
                return 'openapi' in data or 'swagger' in data
            except:
                return False
        return False

    def parse(self, content: str, url: str) -> Dict[str, Any]:
        """Parse OpenAPI spec into AI-friendly tools definition"""
        data = self._load_data(content, url)
        
        operations = []
        
        paths = data.get('paths', {})
        for path, methods in paths.items():
            for method, op in methods.items():
                if method.lower() not in ['get', 'post', 'put', 'delete', 'patch']:
                    continue
                    
                operation_id = op.get('operationId', f"{method}_{path}")
                description = op.get('summary') or op.get('description', '')
                
                tool_def = {
                    "name": operation_id,
                    "description": description,
                    "parameters": self._parse_parameters(op),
                    "path": path,
                    "method": method.upper()
                }
                operations.append(tool_def)
                
        return {
            "type": "openapi",
            "title": data.get('info', {}).get('title', 'API'),
            "version": data.get('info', {}).get('version', ''),
            "operations": operations,
            "raw_spec": data # Optional: keep raw spec if needed
        }

    def _load_data(self, content: str, url: str) -> Dict:
        if url.endswith('.yaml') or url.endswith('.yml'):
            return yaml.safe_load(content)
        return json.loads(content)

    def _parse_parameters(self, op: Dict) -> Dict:
        """Convert OpenAPI parameters to JSON Schema for tools"""
        properties = {}
        required = []
        
        # Handle path/query parameters
        for param in op.get('parameters', []):
            name = param.get('name')
            if param.get('required'):
                required.append(name)
            
            schema = param.get('schema', {})
            properties[name] = {
                "type": schema.get('type', 'string'),
                "description": param.get('description', '')
            }

        # Handle request body
        if 'requestBody' in op:
            content = op['requestBody'].get('content', {})
            if 'application/json' in content:
                schema = content['application/json'].get('schema', {})
                # Merge body properties (simplified)
                # In a full implementation, you'd handle nested schemas deeply
                body_props = schema.get('properties', {})
                for prop_name, prop_def in body_props.items():
                    properties[prop_name] = prop_def
                    if prop_name in schema.get('required', []):
                        required.append(prop_name)

        return {
            "type": "object",
            "properties": properties,
            "required": required
        }
