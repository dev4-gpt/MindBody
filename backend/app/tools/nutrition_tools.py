"""
Nutrition Analysis Tools

Tools for food classification, portion estimation, and nutrition calculation.
"""

from typing import Dict, Any
import random

from .base import BaseTool
from ..orchestration.context import OrchestrationContext


# Food database with calories per 100g
FOOD_DATABASE = {
    "grilled_chicken": {"calories_per_100g": 165, "protein_per_100g": 31},
    "rice": {"calories_per_100g": 130, "protein_per_100g": 2.7},
    "pasta": {"calories_per_100g": 131, "protein_per_100g": 5},
    "salad": {"calories_per_100g": 20, "protein_per_100g": 1},
    "burger": {"calories_per_100g": 295, "protein_per_100g": 16},
    "fries": {"calories_per_100g": 312, "protein_per_100g": 3.4},
    "banana": {"calories_per_100g": 89, "protein_per_100g": 1.1},
    "apple": {"calories_per_100g": 52, "protein_per_100g": 0.3},
    "eggs": {"calories_per_100g": 155, "protein_per_100g": 13},
    "salmon": {"calories_per_100g": 208, "protein_per_100g": 20},
}


class ClassifyFoodTool(BaseTool):
    """Classify food from image"""
    
    def __init__(self):
        super().__init__(
            name="classify_food",
            description="Classify food type from image",
            parameters={
                "image": "Food image",
                "model": "Classification model",
                "top_k": "Number of top predictions"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Classify food"""
        image = parameters.get("image")
        model = parameters.get("model", "efficientnet_b0")
        top_k = parameters.get("top_k", 3)
        
        # Placeholder: In production, run EfficientNet inference
        # For MVP, return mock predictions
        possible_foods = list(FOOD_DATABASE.keys())
        predictions = []
        
        for i in range(top_k):
            food = random.choice(possible_foods)
            confidence = random.uniform(0.6, 0.95)
            predictions.append({
                "label": food,
                "confidence": round(confidence, 2)
            })
        
        # Sort by confidence
        predictions.sort(key=lambda x: x["confidence"], reverse=True)
        
        return {
            "top_class": predictions[0]["label"],
            "confidence": predictions[0]["confidence"],
            "predictions": predictions,
            "model": model
        }


class EstimatePortionTool(BaseTool):
    """Estimate portion size from image"""
    
    def __init__(self):
        super().__init__(
            name="estimate_portion",
            description="Estimate food portion size in grams",
            parameters={
                "image": "Food image",
                "food_class": "Classified food type",
                "user_hints": "Optional user corrections"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Estimate portion"""
        image = parameters.get("image")
        food_class = parameters.get("food_class", "grilled_chicken")
        user_hints = parameters.get("user_hints", {})
        
        # Use user hint if provided
        if "size_hint" in user_hints:
            size = user_hints["size_hint"]
        else:
            # Estimate from image (placeholder)
            size = "medium"
        
        # Map size to grams (rough estimates)
        size_to_grams = {
            "small": 100,
            "medium": 200,
            "large": 300
        }
        
        portion_grams = size_to_grams.get(size, 200)
        
        return {
            "portion_grams": portion_grams,
            "size_estimate": size,
            "confidence": 0.7,
            "food_class": food_class
        }


class CalculateNutritionTool(BaseTool):
    """Calculate nutrition from food class and portion"""
    
    def __init__(self):
        super().__init__(
            name="calculate_nutrition",
            description="Calculate calories and macros from food and portion",
            parameters={
                "food_class": "Classified food type",
                "portion_grams": "Portion size in grams",
                "confidence": "Classification confidence"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Calculate nutrition"""
        food_class = parameters.get("food_class", "grilled_chicken")
        portion_grams = parameters.get("portion_grams", 200)
        confidence = parameters.get("confidence", 0.7)
        
        food_data = FOOD_DATABASE.get(food_class, FOOD_DATABASE["grilled_chicken"])
        
        # Calculate based on portion
        calories = (food_data["calories_per_100g"] * portion_grams) / 100
        protein = (food_data["protein_per_100g"] * portion_grams) / 100
        
        # Add uncertainty based on confidence
        uncertainty = 1 - confidence
        calories_range = (calories * (1 - uncertainty), calories * (1 + uncertainty))
        protein_range = (protein * (1 - uncertainty), protein * (1 + uncertainty))
        
        return {
            "calories": round(calories, 1),
            "calories_range": [round(c, 1) for c in calories_range],
            "protein_grams": round(protein, 1),
            "protein_range": [round(p, 1) for p in protein_range],
            "portion_grams": portion_grams,
            "food_class": food_class,
            "confidence": confidence
        }


class SuggestImprovementsTool(BaseTool):
    """Suggest nutritional improvements"""
    
    def __init__(self):
        super().__init__(
            name="suggest_improvements",
            description="Suggest healthier alternatives or improvements",
            parameters={
                "food_class": "Current food type",
                "current_nutrition": "Current nutrition data"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Generate improvement suggestions"""
        food_class = parameters.get("food_class", "grilled_chicken")
        current_nutrition = parameters.get("current_nutrition", {})
        
        suggestions = []
        
        # Simple suggestion logic
        if food_class == "fries":
            suggestions.append({
                "swap": "roasted_sweet_potato",
                "reason": "Lower calories, more fiber and nutrients",
                "calorie_savings": 50
            })
        elif food_class == "burger":
            suggestions.append({
                "swap": "grilled_chicken",
                "reason": "Higher protein, lower saturated fat",
                "calorie_savings": 30
            })
        
        return {
            "suggestions": suggestions,
            "tips": [
                "Add a side of vegetables for more fiber",
                "Consider portion size - aim for palm-sized protein portions"
            ]
        }

