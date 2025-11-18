"""
Guardrail Validator

Validates agent inputs and outputs to ensure safety, prevent harmful content,
and enforce compliance with medical disclaimers.
"""

from typing import Dict, Any, List, Optional
from dataclasses import dataclass
import re
import logging

from ..orchestration.context import OrchestrationContext

logger = logging.getLogger(__name__)


@dataclass
class GuardrailResult:
    """Result of guardrail validation"""
    allowed: bool
    reason: Optional[str] = None
    sanitized_data: Optional[Dict[str, Any]] = None


class GuardrailValidator:
    """
    Validates agent inputs and outputs against safety rules and compliance requirements.
    """
    
    def __init__(self):
        # Medical advice keywords to block
        self.medical_keywords = [
            "diagnose", "diagnosis", "prescribe", "prescription", "treatment",
            "cure", "disease", "illness", "symptom", "medical condition",
            "see a doctor", "consult a physician", "medical professional"
        ]
        
        # Self-harm keywords
        self.self_harm_keywords = [
            "suicide", "self-harm", "hurt yourself", "end your life"
        ]
        
        # Dangerous exercise keywords
        self.dangerous_exercise_keywords = [
            "ignore pain", "push through injury", "ignore doctor", "ignore medical advice"
        ]
        
        # Disclaimer text
        self.disclaimer = "This is for educational purposes only and not medical advice."
    
    async def validate(
        self,
        agent: str,
        task: Dict[str, Any],
        context: OrchestrationContext
    ) -> GuardrailResult:
        """
        Validate agent input/task before execution.
        
        Args:
            agent: Agent name
            task: Task parameters
            context: Orchestration context
            
        Returns:
            GuardrailResult indicating if execution is allowed
        """
        # Check for dangerous exercise advice
        task_str = str(task).lower()
        
        for keyword in self.dangerous_exercise_keywords:
            if keyword in task_str:
                return GuardrailResult(
                    allowed=False,
                    reason=f"Dangerous exercise advice detected: {keyword}"
                )
        
        # Check for self-harm content
        for keyword in self.self_harm_keywords:
            if keyword in task_str:
                return GuardrailResult(
                    allowed=False,
                    reason=f"Self-harm content detected: {keyword}"
                )
        
        # Rate limiting check (simple implementation)
        if self._check_rate_limit(context):
            return GuardrailResult(
                allowed=False,
                reason="Rate limit exceeded"
            )
        
        return GuardrailResult(allowed=True)
    
    async def validate_output(
        self,
        agent: str,
        output: Dict[str, Any],
        context: OrchestrationContext
    ) -> GuardrailResult:
        """
        Validate agent output before returning to user.
        
        Args:
            agent: Agent name
            output: Agent output
            context: Orchestration context
            
        Returns:
            GuardrailResult with sanitized data if needed
        """
        output_str = str(output).lower()
        
        # Check for medical advice
        medical_advice_found = False
        for keyword in self.medical_keywords:
            if keyword in output_str:
                medical_advice_found = True
                break
        
        if medical_advice_found:
            logger.warning(f"Medical advice detected in {agent} output")
            sanitized = self.sanitize_output(output, remove_medical=True)
            return GuardrailResult(
                allowed=True,  # Allow but sanitize
                reason="Medical advice detected and removed",
                sanitized_data=sanitized
            )
        
        # Check for self-harm content
        for keyword in self.self_harm_keywords:
            if keyword in output_str:
                return GuardrailResult(
                    allowed=False,
                    reason=f"Self-harm content in output: {keyword}"
                )
        
        # Ensure disclaimer is present for mindfulness agent
        if agent == "mindfulness" and "text" in output:
            if self.disclaimer.lower() not in str(output.get("text", "")).lower():
                # Add disclaimer
                sanitized = output.copy()
                if "micro_lesson" in sanitized:
                    sanitized["micro_lesson"]["lesson_text"] += f" {self.disclaimer}"
                return GuardrailResult(
                    allowed=True,
                    reason="Disclaimer added",
                    sanitized_data=sanitized
                )
        
        return GuardrailResult(allowed=True)
    
    def sanitize_text(self, text: str) -> str:
        """
        Sanitize text by removing flagged content.
        
        Args:
            text: Text to sanitize
            
        Returns:
            Sanitized text
        """
        sanitized = text
        
        # Remove medical advice patterns
        for keyword in self.medical_keywords:
            # Remove sentences containing medical keywords
            sentences = re.split(r'[.!?]+', sanitized)
            sanitized = '. '.join([
                s for s in sentences
                if keyword.lower() not in s.lower()
            ])
        
        return sanitized.strip()
    
    def sanitize_output(
        self,
        output: Dict[str, Any],
        remove_medical: bool = True
    ) -> Dict[str, Any]:
        """
        Sanitize agent output.
        
        Args:
            output: Output dictionary
            remove_medical: Whether to remove medical advice
            
        Returns:
            Sanitized output
        """
        sanitized = output.copy()
        
        if remove_medical:
            # Sanitize text fields
            for key, value in sanitized.items():
                if isinstance(value, str):
                    sanitized[key] = self.sanitize_text(value)
                elif isinstance(value, dict):
                    sanitized[key] = self.sanitize_output(value, remove_medical)
                elif isinstance(value, list):
                    sanitized[key] = [
                        self.sanitize_output(item, remove_medical) if isinstance(item, dict)
                        else self.sanitize_text(item) if isinstance(item, str)
                        else item
                        for item in value
                    ]
        
        return sanitized
    
    def _check_rate_limit(self, context: OrchestrationContext) -> bool:
        """
        Check if rate limit is exceeded.
        
        Simple implementation: check agent execution count in session.
        """
        # Simple rate limiting: max 100 executions per session
        if len(context.agent_history) > 100:
            return True
        return False
    
    def add_disclaimer(self, text: str) -> str:
        """Add disclaimer to text"""
        if self.disclaimer.lower() not in text.lower():
            return f"{text} {self.disclaimer}"
        return text

