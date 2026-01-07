from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseParser(ABC):
    """Abstract base class for specialized documentation parsers"""
    
    @abstractmethod
    def can_parse(self, content: str, url: str) -> bool:
        """Check if this parser can handle the content"""
        pass
        
    @abstractmethod
    def parse(self, content: str, url: str) -> Dict[str, Any]:
        """Parse content into structured data"""
        pass
