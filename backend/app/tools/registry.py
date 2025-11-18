"""
Tool Registry

Central registry for all tools in the system, allowing agents to discover
and use tools dynamically.
"""

from typing import Dict, List, Optional
from .base import BaseTool
import logging

logger = logging.getLogger(__name__)


class ToolRegistry:
    """
    Registry for managing and discovering tools.
    """
    
    def __init__(self):
        self._tools: Dict[str, BaseTool] = {}
        self._tools_by_category: Dict[str, List[str]] = {}
    
    def register(self, tool: BaseTool, category: Optional[str] = None) -> None:
        """
        Register a tool in the registry.
        
        Args:
            tool: Tool instance to register
            category: Optional category for grouping
        """
        if tool.name in self._tools:
            logger.warning(f"Tool {tool.name} already registered, overwriting")
        
        self._tools[tool.name] = tool
        
        if category:
            if category not in self._tools_by_category:
                self._tools_by_category[category] = []
            if tool.name not in self._tools_by_category[category]:
                self._tools_by_category[category].append(tool.name)
        
        logger.info(f"Registered tool {tool.name} (category: {category or 'none'})")
    
    def get_tool(self, name: str) -> Optional[BaseTool]:
        """Get a tool by name"""
        return self._tools.get(name)
    
    def get_tools_by_category(self, category: str) -> List[BaseTool]:
        """Get all tools in a category"""
        tool_names = self._tools_by_category.get(category, [])
        return [self._tools[name] for name in tool_names if name in self._tools]
    
    def list_tools(self) -> List[str]:
        """List all registered tool names"""
        return list(self._tools.keys())
    
    def get_tool_info(self, name: str) -> Optional[Dict]:
        """Get information about a tool"""
        tool = self.get_tool(name)
        if tool:
            return tool.get_info()
        return None
    
    def list_all_tool_info(self) -> List[Dict]:
        """Get information about all tools"""
        return [tool.get_info() for tool in self._tools.values()]

