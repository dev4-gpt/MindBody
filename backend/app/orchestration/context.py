"""
Orchestration Context

Context classes used across the orchestration system to avoid circular imports.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, TYPE_CHECKING
from datetime import datetime

if TYPE_CHECKING:
    from .engine import AgentResponse


@dataclass
class OrchestrationContext:
    """Context passed between agents"""
    session_id: str
    user_id: Optional[str] = None
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)
    agent_history: List[Any] = field(default_factory=list)  # List[AgentResponse] when available

