"""
Base Agent Class

All agents inherit from this base class, which provides common functionality
for tool execution, state management, and communication.
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from dataclasses import dataclass, field
from datetime import datetime
import logging

from ..tools.base import BaseTool
from ..orchestration.context import OrchestrationContext

logger = logging.getLogger(__name__)


@dataclass
class AgentState:
    """Internal state of an agent"""
    name: str
    initialized: bool = False
    tools: Dict[str, BaseTool] = field(default_factory=dict)
    execution_count: int = 0
    last_execution: Optional[datetime] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


class BaseAgent(ABC):
    """
    Base class for all agents in the system.
    
    Agents are specialized components that handle specific domains:
    - Pose Agent: Exercise form analysis
    - Nutrition Agent: Food classification and nutrition estimation
    - Mindfulness Agent: Coaching and journaling
    """
    
    def __init__(
        self,
        name: str,
        description: str,
        tools: Optional[List[BaseTool]] = None
    ):
        self.name = name
        self.description = description
        self.state = AgentState(name=name)
        self._tools = {tool.name: tool for tool in (tools or [])}
        self.state.tools = self._tools
        
    @abstractmethod
    async def execute(
        self,
        task: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """
        Execute the agent's main task.
        
        Args:
            task: Task parameters specific to the agent
            context: Orchestration context with session info
            
        Returns:
            Dictionary with execution results
        """
        pass
    
    def register_tool(self, tool: BaseTool) -> None:
        """Register a tool for this agent"""
        self._tools[tool.name] = tool
        self.state.tools = self._tools
        logger.info(f"Registered tool {tool.name} for agent {self.name}")
    
    async def use_tool(
        self,
        tool_name: str,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Any:
        """
        Execute a tool registered to this agent.
        
        Args:
            tool_name: Name of the tool to execute
            parameters: Parameters for the tool
            context: Orchestration context
            
        Returns:
            Tool execution result
        """
        if tool_name not in self._tools:
            raise ValueError(f"Tool {tool_name} not found for agent {self.name}")
        
        tool = self._tools[tool_name]
        
        try:
            result = await tool.execute(parameters, context)
            logger.debug(f"Tool {tool_name} executed successfully for agent {self.name}")
            return result
        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}", exc_info=True)
            raise
    
    def get_available_tools(self) -> List[str]:
        """Get list of available tool names"""
        return list(self._tools.keys())
    
    def get_tools_used(self) -> List[str]:
        """Get list of tools used in last execution (to be overridden)"""
        return []
    
    async def initialize(self) -> None:
        """Initialize the agent (load models, connect to services, etc.)"""
        if self.state.initialized:
            return
        
        try:
            await self._initialize()
            self.state.initialized = True
            logger.info(f"Agent {self.name} initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize agent {self.name}: {str(e)}", exc_info=True)
            raise
    
    @abstractmethod
    async def _initialize(self) -> None:
        """Agent-specific initialization logic"""
        pass
    
    def get_state(self) -> Dict[str, Any]:
        """Get current agent state"""
        return {
            "name": self.state.name,
            "initialized": self.state.initialized,
            "execution_count": self.state.execution_count,
            "last_execution": self.state.last_execution.isoformat() if self.state.last_execution else None,
            "available_tools": self.get_available_tools(),
            "metadata": self.state.metadata
        }
    
    def _update_execution_state(self) -> None:
        """Update state after execution"""
        self.state.execution_count += 1
        self.state.last_execution = datetime.now()

