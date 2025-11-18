"""
Mindfulness & Grit Coaching Agent

Provides short mindfulness micro-lessons, journaling prompts,
and motivational coaching using LLM capabilities.
"""

from typing import Dict, Any, List
import logging

from .base import BaseAgent
from ..orchestration.context import OrchestrationContext
from ..tools.mindfulness_tools import (
    GenerateMicroLessonTool,
    CreateJournalPromptTool,
    AnalyzeMoodTool,
    GenerateBreathingGuideTool
)

logger = logging.getLogger(__name__)


class MindfulnessAgent(BaseAgent):
    """
    Agent responsible for mindfulness coaching and mental resilience.
    """
    
    def __init__(self):
        tools = [
            GenerateMicroLessonTool(),
            CreateJournalPromptTool(),
            AnalyzeMoodTool(),
            GenerateBreathingGuideTool()
        ]
        super().__init__(
            name="mindfulness",
            description="Mindfulness coaching and grit micro-lessons",
            tools=tools
        )
        self.llm_model = None
        
    async def _initialize(self) -> None:
        """Initialize LLM model"""
        logger.info("Initializing mindfulness LLM model...")
        # In production, load Llama 3.1 8B, Gemma 2 9B, or similar
        self.llm_model = "llama3.1-8b"  # Placeholder
        logger.info("Mindfulness LLM model initialized")
    
    async def execute(
        self,
        task: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """
        Execute mindfulness coaching task.
        
        Expected task format:
        {
            "context": str,           # post_workout, pre_workout, general
            "mood_hint": str,        # Optional: frustrated, tired, motivated
            "workout_summary": dict, # Optional: workout results
            "user_history": str      # Optional: previous interactions
        }
        """
        self._update_execution_state()
        
        coaching_context = task.get("context", "general")
        mood_hint = task.get("mood_hint")
        workout_summary = task.get("workout_summary", {})
        user_history = task.get("user_history", "")
        
        try:
            # Analyze mood if hint provided
            mood_analysis = None
            if mood_hint:
                mood_analysis = await self.use_tool(
                    "analyze_mood",
                    {
                        "mood_hint": mood_hint,
                        "context": coaching_context,
                        "workout_summary": workout_summary
                    },
                    context
                )
            
            # Generate micro-lesson
            micro_lesson = await self.use_tool(
                "generate_micro_lesson",
                {
                    "context": coaching_context,
                    "mood_analysis": mood_analysis,
                    "workout_summary": workout_summary,
                    "user_history": user_history,
                    "duration_seconds": 60
                },
                context
            )
            
            # Generate breathing guide
            breathing_guide = await self.use_tool(
                "generate_breathing_guide",
                {
                    "context": coaching_context,
                    "duration_seconds": 60
                },
                context
            )
            
            # Create journaling prompt
            journal_prompt = await self.use_tool(
                "create_journal_prompt",
                {
                    "context": coaching_context,
                    "workout_summary": workout_summary,
                    "mood_analysis": mood_analysis
                },
                context
            )
            
            return {
                "success": True,
                "micro_lesson": micro_lesson,
                "breathing_guide": breathing_guide,
                "journal_prompt": journal_prompt,
                "mood_analysis": mood_analysis,
                "context": coaching_context,
                "timestamp": context.timestamp.isoformat()
            }
            
        except Exception as e:
            logger.error(f"Error in mindfulness agent execution: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tools_used(self) -> List[str]:
        """Return tools used in execution"""
        return ["generate_micro_lesson", "create_journal_prompt", "analyze_mood", "generate_breathing_guide"]

