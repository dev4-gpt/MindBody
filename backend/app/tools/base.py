"""
Base Tool Class

All tools inherit from this base class, which provides common functionality
for parameter validation, execution tracking, and error handling.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

from ..orchestration.context import OrchestrationContext

logger = logging.getLogger(__name__)


@dataclass
class ToolResult:
    """Result from tool execution"""
    success: bool
    data: Any
    error: Optional[str] = None
    execution_time: float = 0.0
    metadata: Dict[str, Any] = None


class BaseTool(ABC):
    """
    Base class for all tools in the system.
    
    Tools are reusable functions that agents can call to perform specific tasks.
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        parameters: Optional[Dict[str, Any]] = None
    ):
        self.name = name
        self.description = description
        self.parameters = parameters or {}
        self.execution_count = 0
        
    @abstractmethod
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Any:
        """
        Execute the tool with given parameters.
        
        Args:
            parameters: Tool-specific parameters
            context: Orchestration context
            
        Returns:
            Tool execution result
        """
        pass
    
    def validate_parameters(self, parameters: Dict[str, Any]) -> bool:
        """
        Validate tool parameters.
        
        Override in subclasses for specific validation.
        """
        return True
    
    async def _execute_with_validation(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> ToolResult:
        """Execute tool with parameter validation and error handling"""
        start_time = datetime.now()
        
        try:
            if not self.validate_parameters(parameters):
                return ToolResult(
                    success=False,
                    data=None,
                    error="Invalid parameters"
                )
            
            result = await self.execute(parameters, context)
            execution_time = (datetime.now() - start_time).total_seconds()
            
            self.execution_count += 1
            
            return ToolResult(
                success=True,
                data=result,
                execution_time=execution_time
            )
            
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {str(e)}", exc_info=True)
            execution_time = (datetime.now() - start_time).total_seconds()
            return ToolResult(
                success=False,
                data=None,
                error=str(e),
                execution_time=execution_time
            )
    
    def get_info(self) -> Dict[str, Any]:
        """Get tool information"""
        return {
            "name": self.name,
            "description": self.description,
            "parameters": self.parameters,
            "execution_count": self.execution_count
        }

