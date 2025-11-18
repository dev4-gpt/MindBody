"""
Memory Manager

Manages context and memory for agents, including session history,
user preferences, and long-term patterns.
"""

from typing import Dict, Any, List, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass, field
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class MemoryEntry:
    """Single memory entry"""
    session_id: str
    user_id: Optional[str]
    agent: str
    task: Dict[str, Any]
    result: Dict[str, Any]
    timestamp: datetime = field(default_factory=datetime.now)
    metadata: Dict[str, Any] = field(default_factory=dict)


class MemoryManager:
    """
    Manages memory and context for the multi-agent system.
    
    Supports:
    - Session-based memory
    - User-specific context
    - Long-term pattern recognition
    - Semantic search (with vector storage in production)
    """
    
    def __init__(self, max_session_memory: int = 1000):
        self.max_session_memory = max_session_memory
        self.session_memory: Dict[str, List[MemoryEntry]] = {}
        self.user_memory: Dict[str, List[MemoryEntry]] = {}
        self.patterns: Dict[str, Any] = {}
        
    async def store_interaction(
        self,
        session_id: str,
        user_id: Optional[str],
        agent: str,
        task: Dict[str, Any],
        result: Dict[str, Any],
        metadata: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Store an agent interaction in memory.
        
        Args:
            session_id: Session identifier
            user_id: Optional user identifier
            agent: Agent name
            task: Task that was executed
            result: Result from agent
            metadata: Optional metadata
        """
        entry = MemoryEntry(
            session_id=session_id,
            user_id=user_id,
            agent=agent,
            task=task,
            result=result,
            metadata=metadata or {}
        )
        
        # Store in session memory
        if session_id not in self.session_memory:
            self.session_memory[session_id] = []
        
        self.session_memory[session_id].append(entry)
        
        # Limit session memory size
        if len(self.session_memory[session_id]) > self.max_session_memory:
            self.session_memory[session_id] = self.session_memory[session_id][-self.max_session_memory:]
        
        # Store in user memory if user_id provided
        if user_id:
            if user_id not in self.user_memory:
                self.user_memory[user_id] = []
            self.user_memory[user_id].append(entry)
            
            # Limit user memory size
            if len(self.user_memory[user_id]) > self.max_session_memory * 10:
                self.user_memory[user_id] = self.user_memory[user_id][-self.max_session_memory * 10:]
        
        # Update patterns
        await self._update_patterns(entry)
    
    async def get_context(
        self,
        session_id: str,
        user_id: Optional[str] = None,
        agent: Optional[str] = None,
        limit: int = 10
    ) -> Dict[str, Any]:
        """
        Get relevant context for an agent.
        
        Args:
            session_id: Session identifier
            user_id: Optional user identifier
            agent: Optional agent name to filter by
            limit: Maximum number of entries to return
            
        Returns:
            Dictionary with relevant context
        """
        context = {
            "session_history": [],
            "user_preferences": {},
            "patterns": {}
        }
        
        # Get session history
        if session_id in self.session_memory:
            entries = self.session_memory[session_id]
            if agent:
                entries = [e for e in entries if e.agent == agent]
            context["session_history"] = [
                {
                    "agent": e.agent,
                    "task": e.task,
                    "result": e.result,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in entries[-limit:]
            ]
        
        # Get user-specific context
        if user_id and user_id in self.user_memory:
            user_entries = self.user_memory[user_id]
            if agent:
                user_entries = [e for e in user_entries if e.agent == agent]
            
            # Extract preferences from history
            context["user_preferences"] = self._extract_preferences(user_entries)
            
            # Get recent user history
            context["user_history"] = [
                {
                    "agent": e.agent,
                    "task": e.task,
                    "result": e.result,
                    "timestamp": e.timestamp.isoformat()
                }
                for e in user_entries[-limit:]
            ]
        
        # Get relevant patterns
        if agent:
            context["patterns"] = self.patterns.get(agent, {})
        
        return context
    
    def _extract_preferences(self, entries: List[MemoryEntry]) -> Dict[str, Any]:
        """Extract user preferences from memory entries"""
        preferences = {}
        
        # Extract exercise preferences
        exercise_types = []
        for entry in entries:
            if entry.agent == "pose" and "exercise_type" in entry.task:
                exercise_types.append(entry.task["exercise_type"])
        
        if exercise_types:
            preferences["favorite_exercises"] = list(set(exercise_types))
        
        # Extract mood patterns
        moods = []
        for entry in entries:
            if entry.agent == "mindfulness" and "mood_analysis" in entry.result:
                mood = entry.result["mood_analysis"].get("mood")
                if mood:
                    moods.append(mood)
        
        if moods:
            preferences["common_moods"] = list(set(moods))
        
        return preferences
    
    async def _update_patterns(self, entry: MemoryEntry) -> None:
        """Update pattern recognition based on new entry"""
        agent = entry.agent
        
        if agent not in self.patterns:
            self.patterns[agent] = {}
        
        # Update exercise patterns for pose agent
        if agent == "pose" and "exercise_type" in entry.task:
            exercise_type = entry.task["exercise_type"]
            if "exercise_frequency" not in self.patterns[agent]:
                self.patterns[agent]["exercise_frequency"] = {}
            
            self.patterns[agent]["exercise_frequency"][exercise_type] = \
                self.patterns[agent]["exercise_frequency"].get(exercise_type, 0) + 1
        
        # Update form score trends
        if agent == "pose" and "form_score" in entry.result:
            if "form_score_trend" not in self.patterns[agent]:
                self.patterns[agent]["form_score_trend"] = []
            
            score = entry.result.get("form_score", {}).get("overall_score", 0)
            self.patterns[agent]["form_score_trend"].append({
                "score": score,
                "timestamp": entry.timestamp.isoformat()
            })
            
            # Keep only last 100 scores
            if len(self.patterns[agent]["form_score_trend"]) > 100:
                self.patterns[agent]["form_score_trend"] = \
                    self.patterns[agent]["form_score_trend"][-100:]
    
    def get_session_summary(self, session_id: str) -> Dict[str, Any]:
        """Get summary of a session"""
        if session_id not in self.session_memory:
            return {"error": "Session not found"}
        
        entries = self.session_memory[session_id]
        
        agents_used = list(set(e.agent for e in entries))
        total_interactions = len(entries)
        
        # Calculate session duration
        if entries:
            start_time = entries[0].timestamp
            end_time = entries[-1].timestamp
            duration = (end_time - start_time).total_seconds()
        else:
            duration = 0
        
        return {
            "session_id": session_id,
            "total_interactions": total_interactions,
            "agents_used": agents_used,
            "duration_seconds": duration,
            "start_time": entries[0].timestamp.isoformat() if entries else None,
            "end_time": entries[-1].timestamp.isoformat() if entries else None
        }
    
    def clear_session(self, session_id: str) -> None:
        """Clear memory for a session"""
        if session_id in self.session_memory:
            del self.session_memory[session_id]
    
    def clear_user_memory(self, user_id: str) -> None:
        """Clear memory for a user"""
        if user_id in self.user_memory:
            del self.user_memory[user_id]

