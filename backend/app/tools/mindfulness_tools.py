"""
Mindfulness & Coaching Tools

Tools for generating micro-lessons, journaling prompts, mood analysis, and breathing guides.
"""

from typing import Dict, Any, List
import random

from .base import BaseTool
from ..orchestration.context import OrchestrationContext


# Template-based micro-lessons
MICRO_LESSON_TEMPLATES = {
    "post_workout": [
        "Breathe in for 4 counts, hold for 2, out for 6. Repeat 6 times. You built consistency today — that compounds. Remember one progress point.",
        "Take 5 deep breaths. Each rep you completed is a step toward your goal. Progress isn't always linear, but you showed up. That's what matters.",
        "Inhale strength, exhale doubt. You pushed through today. Notice how your body feels — acknowledge the effort you just made."
    ],
    "pre_workout": [
        "Take 3 deep breaths. Set your intention: what do you want to accomplish today? Visualize success.",
        "Breathe in confidence, out any hesitation. You're prepared. Trust your training and give your best effort.",
    ],
    "general": [
        "Breathe in for 4, hold 2, out 6. This moment is yours. What's one thing you're grateful for today?",
        "Take a moment. Inhale presence, exhale distraction. You're exactly where you need to be right now.",
    ]
}

JOURNAL_PROMPTS = {
    "post_workout": [
        "What did you push through just now?",
        "What's one thing you learned about yourself during this workout?",
        "How did your body feel during the hardest part?",
        "What progress did you notice today, even if small?",
    ],
    "pre_workout": [
        "What's your intention for today's session?",
        "What are you hoping to achieve or improve?",
    ],
    "general": [
        "What's one thing you're grateful for today?",
        "What challenge did you overcome recently?",
        "How are you feeling right now, and why?",
    ]
}

BREATHING_PATTERNS = [
    {"name": "Box Breathing", "pattern": "4-4-4-4", "description": "Inhale 4, hold 4, exhale 4, hold 4"},
    {"name": "4-7-8 Breathing", "pattern": "4-7-8", "description": "Inhale 4, hold 7, exhale 8"},
    {"name": "Equal Breathing", "pattern": "4-4", "description": "Inhale 4, exhale 4"},
]


class GenerateMicroLessonTool(BaseTool):
    """Generate a short mindfulness micro-lesson"""
    
    def __init__(self):
        super().__init__(
            name="generate_micro_lesson",
            description="Generate a short mindfulness or grit micro-lesson",
            parameters={
                "context": "Context (post_workout, pre_workout, general)",
                "mood_analysis": "Optional mood analysis",
                "workout_summary": "Optional workout summary",
                "user_history": "Optional user history",
                "duration_seconds": "Desired duration in seconds"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Generate micro-lesson"""
        lesson_context = parameters.get("context", "general")
        mood_analysis = parameters.get("mood_analysis")
        workout_summary = parameters.get("workout_summary", {})
        duration_seconds = parameters.get("duration_seconds", 60)
        
        # Select template based on context
        templates = MICRO_LESSON_TEMPLATES.get(lesson_context, MICRO_LESSON_TEMPLATES["general"])
        lesson_text = random.choice(templates)
        
        # Customize based on workout summary if available
        if workout_summary and "form_score" in workout_summary:
            score = workout_summary["form_score"]
            if score >= 90:
                lesson_text += " Excellent form today!"
            elif score >= 75:
                lesson_text += " Good effort — keep refining."
        
        return {
            "lesson_text": lesson_text,
            "context": lesson_context,
            "duration_seconds": duration_seconds,
            "type": "micro_lesson"
        }


class CreateJournalPromptTool(BaseTool):
    """Create a journaling prompt"""
    
    def __init__(self):
        super().__init__(
            name="create_journal_prompt",
            description="Create a journaling prompt for reflection",
            parameters={
                "context": "Context for the prompt",
                "workout_summary": "Optional workout summary",
                "mood_analysis": "Optional mood analysis"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Create journal prompt"""
        prompt_context = parameters.get("context", "general")
        workout_summary = parameters.get("workout_summary", {})
        
        prompts = JOURNAL_PROMPTS.get(prompt_context, JOURNAL_PROMPTS["general"])
        prompt = random.choice(prompts)
        
        return {
            "prompt": prompt,
            "context": prompt_context,
            "max_words": 50,
            "type": "journal_prompt"
        }


class AnalyzeMoodTool(BaseTool):
    """Analyze user mood from hints and context"""
    
    def __init__(self):
        super().__init__(
            name="analyze_mood",
            description="Analyze user mood and emotional state",
            parameters={
                "mood_hint": "User-provided mood hint",
                "context": "Context (post_workout, etc.)",
                "workout_summary": "Optional workout summary"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Analyze mood"""
        mood_hint = parameters.get("mood_hint", "neutral")
        workout_context = parameters.get("context", "general")
        workout_summary = parameters.get("workout_summary", {})
        
        # Simple mood mapping
        mood_map = {
            "frustrated": {"valence": -0.5, "energy": 0.3, "label": "Frustrated"},
            "tired": {"valence": -0.2, "energy": -0.5, "label": "Tired"},
            "motivated": {"valence": 0.7, "energy": 0.8, "label": "Motivated"},
            "neutral": {"valence": 0.0, "energy": 0.0, "label": "Neutral"},
        }
        
        mood_data = mood_map.get(mood_hint.lower(), mood_map["neutral"])
        
        # Adjust based on workout performance
        if workout_summary and "form_score" in workout_summary:
            score = workout_summary["form_score"]
            if score >= 90:
                mood_data["valence"] += 0.2
            elif score < 60:
                mood_data["valence"] -= 0.1
        
        return {
            "mood": mood_data["label"],
            "valence": mood_data["valence"],
            "energy": mood_data["energy"],
            "context": workout_context,
            "recommendations": self._get_mood_recommendations(mood_data["label"])
        }
    
    def _get_mood_recommendations(self, mood: str) -> List[str]:
        """Get recommendations based on mood"""
        recommendations = {
            "Frustrated": ["Focus on one small win", "Take a moment to breathe", "Remember progress takes time"],
            "Tired": ["Listen to your body", "Consider a lighter session", "Rest is part of training"],
            "Motivated": ["Channel this energy", "Set a challenging but achievable goal", "Enjoy the momentum"],
        }
        return recommendations.get(mood, ["Stay present", "Focus on the process"])


class GenerateBreathingGuideTool(BaseTool):
    """Generate a breathing exercise guide"""
    
    def __init__(self):
        super().__init__(
            name="generate_breathing_guide",
            description="Generate a guided breathing exercise",
            parameters={
                "context": "Context for breathing guide",
                "duration_seconds": "Duration of breathing exercise"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Generate breathing guide"""
        breathing_context = parameters.get("context", "general")
        duration_seconds = parameters.get("duration_seconds", 60)
        
        pattern = random.choice(BREATHING_PATTERNS)
        
        # Calculate cycles based on duration
        if pattern["pattern"] == "4-4-4-4":
            cycle_time = 16  # 4+4+4+4
        elif pattern["pattern"] == "4-7-8":
            cycle_time = 19  # 4+7+8
        else:
            cycle_time = 8  # 4+4
        
        cycles = max(1, duration_seconds // cycle_time)
        
        return {
            "pattern_name": pattern["name"],
            "pattern": pattern["pattern"],
            "description": pattern["description"],
            "cycles": cycles,
            "duration_seconds": duration_seconds,
            "instructions": f"Repeat {cycles} cycles of {pattern['description']}"
        }

