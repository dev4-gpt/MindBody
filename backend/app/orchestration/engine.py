"""
Multi-Agent Orchestration Engine

Coordinates multiple agents, manages tool execution, applies guardrails,
and maintains context through the memory system.
"""

from typing import Dict, List, Any, Optional, Callable
from enum import Enum
from dataclasses import dataclass, field
from datetime import datetime
import asyncio
import logging

from .context import OrchestrationContext
from ..agents.base import BaseAgent
from ..guardrails.validator import GuardrailValidator
from ..memory.manager import MemoryManager
from ..tools.registry import ToolRegistry

logger = logging.getLogger(__name__)


class AgentRole(str, Enum):
    """Agent roles in the system"""
    POSE = "pose"
    NUTRITION = "nutrition"
    MINDFULNESS = "mindfulness"
    COORDINATOR = "coordinator"


@dataclass
class AgentResponse:
    """Response from an agent execution"""
    agent: str
    success: bool
    data: Dict[str, Any]
    error: Optional[str] = None
    execution_time: float = 0.0
    tools_used: List[str] = field(default_factory=list)


# OrchestrationContext moved to context.py to avoid circular imports


class OrchestrationEngine:
    """
    Main orchestration engine that coordinates agents, tools, guardrails, and memory.
    """
    
    def __init__(
        self,
        agents: Dict[str, BaseAgent],
        guardrail_validator: GuardrailValidator,
        memory_manager: MemoryManager,
        tool_registry: ToolRegistry
    ):
        self.agents = agents
        self.guardrail_validator = guardrail_validator
        self.memory_manager = memory_manager
        self.tool_registry = tool_registry
        self.active_sessions: Dict[str, OrchestrationContext] = {}
        
    async def execute_agent(
        self,
        agent_name: str,
        task: Dict[str, Any],
        session_id: str,
        user_id: Optional[str] = None
    ) -> AgentResponse:
        """
        Execute a single agent with task, applying guardrails and memory.
        
        Args:
            agent_name: Name of the agent to execute
            task: Task parameters for the agent
            session_id: Session identifier
            user_id: Optional user identifier
            
        Returns:
            AgentResponse with execution results
        """
        if agent_name not in self.agents:
            return AgentResponse(
                agent=agent_name,
                success=False,
                data={},
                error=f"Agent {agent_name} not found"
            )
        
        agent = self.agents[agent_name]
        start_time = datetime.now()
        
        # Get or create session context
        context = self._get_or_create_context(session_id, user_id)
        
        try:
            # Load relevant memory
            memory_context = await self.memory_manager.get_context(
                session_id=session_id,
                user_id=user_id,
                agent=agent_name
            )
            
            # Merge memory context into task
            enriched_task = {**task, **memory_context}
            
            # Apply guardrails before execution
            guardrail_result = await self.guardrail_validator.validate(
                agent=agent_name,
                task=enriched_task,
                context=context
            )
            
            if not guardrail_result.allowed:
                return AgentResponse(
                    agent=agent_name,
                    success=False,
                    data={},
                    error=f"Guardrail violation: {guardrail_result.reason}"
                )
            
            # Execute agent
            result = await agent.execute(enriched_task, context)
            
            # Validate output with guardrails
            output_validation = await self.guardrail_validator.validate_output(
                agent=agent_name,
                output=result,
                context=context
            )
            
            if not output_validation.allowed:
                logger.warning(f"Output validation failed for {agent_name}: {output_validation.reason}")
                result = await self._apply_output_sanitization(result, output_validation)
            
            # Store in memory
            await self.memory_manager.store_interaction(
                session_id=session_id,
                user_id=user_id,
                agent=agent_name,
                task=enriched_task,
                result=result
            )
            
            execution_time = (datetime.now() - start_time).total_seconds()
            
            response = AgentResponse(
                agent=agent_name,
                success=True,
                data=result,
                execution_time=execution_time,
                tools_used=agent.get_tools_used() if hasattr(agent, 'get_tools_used') else []
            )
            
            context.agent_history.append(response)
            return response
            
        except Exception as e:
            logger.error(f"Error executing agent {agent_name}: {str(e)}", exc_info=True)
            execution_time = (datetime.now() - start_time).total_seconds()
            return AgentResponse(
                agent=agent_name,
                success=False,
                data={},
                error=str(e),
                execution_time=execution_time
            )
    
    async def execute_multi_agent(
        self,
        tasks: List[Dict[str, Any]],
        session_id: str,
        user_id: Optional[str] = None,
        parallel: bool = False
    ) -> List[AgentResponse]:
        """
        Execute multiple agents, either sequentially or in parallel.
        
        Args:
            tasks: List of {agent_name, task} dictionaries
            session_id: Session identifier
            user_id: Optional user identifier
            parallel: If True, execute agents in parallel
            
        Returns:
            List of AgentResponse objects
        """
        if parallel:
            # Execute all agents in parallel
            coroutines = [
                self.execute_agent(
                    agent_name=task['agent_name'],
                    task=task.get('task', {}),
                    session_id=session_id,
                    user_id=user_id
                )
                for task in tasks
            ]
            return await asyncio.gather(*coroutines)
        else:
            # Execute sequentially
            responses = []
            for task in tasks:
                response = await self.execute_agent(
                    agent_name=task['agent_name'],
                    task=task.get('task', {}),
                    session_id=session_id,
                    user_id=user_id
                )
                responses.append(response)
            return responses
    
    async def orchestrate_workout_session(
        self,
        session_id: str,
        frames: List[Any],
        exercise_type: str,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate a complete workout session with pose analysis and mindfulness.
        
        Args:
            session_id: Session identifier
            frames: Video frames for analysis
            exercise_type: Type of exercise (squat, pushup, etc.)
            user_id: Optional user identifier
            
        Returns:
            Combined results from pose and mindfulness agents
        """
        # Execute pose agent for form analysis
        pose_response = await self.execute_agent(
            agent_name=AgentRole.POSE.value,
            task={
                "frames": frames,
                "exercise_type": exercise_type,
                "mode": "real_time"
            },
            session_id=session_id,
            user_id=user_id
        )
        
        # If workout completed, trigger mindfulness agent
        mindfulness_response = None
        if pose_response.success and pose_response.data.get("workout_complete"):
            mindfulness_response = await self.execute_agent(
                agent_name=AgentRole.MINDFULNESS.value,
                task={
                    "context": "post_workout",
                    "workout_summary": pose_response.data.get("summary", {}),
                    "mood_hint": None
                },
                session_id=session_id,
                user_id=user_id
            )
        
        return {
            "pose_analysis": pose_response.data if pose_response.success else None,
            "mindfulness_coaching": mindfulness_response.data if mindfulness_response and mindfulness_response.success else None,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    async def orchestrate_nutrition_analysis(
        self,
        session_id: str,
        image: Any,
        user_id: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Orchestrate nutrition analysis with food classification and estimation.
        
        Args:
            session_id: Session identifier
            image: Food image
            user_id: Optional user identifier
            
        Returns:
            Nutrition analysis results
        """
        nutrition_response = await self.execute_agent(
            agent_name=AgentRole.NUTRITION.value,
            task={
                "image": image,
                "mode": "estimate"
            },
            session_id=session_id,
            user_id=user_id
        )
        
        return {
            "nutrition": nutrition_response.data if nutrition_response.success else None,
            "session_id": session_id,
            "timestamp": datetime.now().isoformat()
        }
    
    def _get_or_create_context(
        self,
        session_id: str,
        user_id: Optional[str] = None
    ) -> OrchestrationContext:
        """Get existing context or create new one"""
        if session_id not in self.active_sessions:
            self.active_sessions[session_id] = OrchestrationContext(
                session_id=session_id,
                user_id=user_id
            )
        return self.active_sessions[session_id]
    
    async def _apply_output_sanitization(
        self,
        output: Dict[str, Any],
        validation_result: Any
    ) -> Dict[str, Any]:
        """Apply sanitization based on validation results"""
        # Remove or modify problematic content
        sanitized = output.copy()
        
        if 'text' in sanitized:
            # Remove flagged content
            sanitized['text'] = self.guardrail_validator.sanitize_text(
                sanitized['text']
            )
        
        return sanitized
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of a session"""
        if session_id not in self.active_sessions:
            return {"error": "Session not found"}
        
        context = self.active_sessions[session_id]
        return {
            "session_id": session_id,
            "user_id": context.user_id,
            "start_time": context.timestamp.isoformat(),
            "agent_executions": len(context.agent_history),
            "agents_used": list(set(r.agent for r in context.agent_history)),
            "total_execution_time": sum(r.execution_time for r in context.agent_history)
        }

