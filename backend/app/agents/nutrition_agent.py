"""
Nutrition Analysis Agent

Classifies food images, estimates portions, and calculates
nutritional information (calories, macros).
"""

from typing import Dict, Any, List
import logging

from .base import BaseAgent
from ..orchestration.context import OrchestrationContext
from ..tools.nutrition_tools import (
    ClassifyFoodTool,
    EstimatePortionTool,
    CalculateNutritionTool,
    SuggestImprovementsTool
)

logger = logging.getLogger(__name__)


class NutritionAgent(BaseAgent):
    """
    Agent responsible for food classification and nutrition estimation.
    """
    
    def __init__(self):
        tools = [
            ClassifyFoodTool(),
            EstimatePortionTool(),
            CalculateNutritionTool(),
            SuggestImprovementsTool()
        ]
        super().__init__(
            name="nutrition",
            description="Food classification and nutrition estimation",
            tools=tools
        )
        self.food_model = None
        
    async def _initialize(self) -> None:
        """Initialize food classification model"""
        logger.info("Initializing food classification model...")
        # In production, load EfficientNet or FoodNet model here
        self.food_model = "efficientnet_b0"  # Placeholder
        logger.info("Food classification model initialized")
    
    async def execute(
        self,
        task: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """
        Execute nutrition analysis task.
        
        Expected task format:
        {
            "image": image_data,      # Food image
            "mode": str,              # estimate, classify_only
            "user_hints": dict        # Optional user corrections
        }
        """
        self._update_execution_state()
        
        image = task.get("image")
        mode = task.get("mode", "estimate")
        user_hints = task.get("user_hints", {})
        
        if not image:
            return {
                "error": "No image provided",
                "success": False
            }
        
        try:
            # Classify food
            classification = await self.use_tool(
                "classify_food",
                {
                    "image": image,
                    "model": self.food_model,
                    "top_k": 3
                },
                context
            )
            
            if mode == "classify_only":
                return {
                    "success": True,
                    "classification": classification,
                    "mode": "classify_only"
                }
            
            # Estimate portion size
            portion_estimate = await self.use_tool(
                "estimate_portion",
                {
                    "image": image,
                    "food_class": classification.get("top_class"),
                    "user_hints": user_hints
                },
                context
            )
            
            # Calculate nutrition
            nutrition = await self.use_tool(
                "calculate_nutrition",
                {
                    "food_class": classification.get("top_class"),
                    "portion_grams": portion_estimate.get("portion_grams"),
                    "confidence": classification.get("confidence", 0.5)
                },
                context
            )
            
            # Suggest improvements
            suggestions = await self.use_tool(
                "suggest_improvements",
                {
                    "food_class": classification.get("top_class"),
                    "current_nutrition": nutrition
                },
                context
            )
            
            return {
                "success": True,
                "classification": classification,
                "portion_estimate": portion_estimate,
                "nutrition": nutrition,
                "suggestions": suggestions,
                "confidence": classification.get("confidence", 0.5)
            }
            
        except Exception as e:
            logger.error(f"Error in nutrition agent execution: {str(e)}", exc_info=True)
            return {
                "success": False,
                "error": str(e)
            }
    
    def get_tools_used(self) -> List[str]:
        """Return tools used in execution"""
        return ["classify_food", "estimate_portion", "calculate_nutrition", "suggest_improvements"]

