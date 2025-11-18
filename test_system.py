"""
System Test Script

Tests the multi-agent orchestration framework end-to-end.

Note: This script modifies sys.path at runtime to import from the backend directory.
IDE linters may show import warnings, but the code executes correctly because
Python resolves the imports at runtime after the path modification.
"""

import asyncio
import sys
import os

# Add backend to path
# Note: This runtime path modification allows imports to work at execution time.
# IDE linters may show warnings, but the code runs correctly.
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

# Type checking: ignore import warnings - these resolve at runtime via sys.path
# pyright: reportMissingImports=false
# pylint: disable=import-error
from app.orchestration.engine import OrchestrationEngine, AgentRole  # type: ignore
from app.agents.pose_agent import PoseAgent  # type: ignore
from app.agents.nutrition_agent import NutritionAgent  # type: ignore
from app.agents.mindfulness_agent import MindfulnessAgent  # type: ignore
from app.guardrails.validator import GuardrailValidator  # type: ignore
from app.memory.manager import MemoryManager  # type: ignore
from app.tools.registry import ToolRegistry  # type: ignore


async def test_system():
    """Test the complete system"""
    print("🧪 Testing Multi-Agent Orchestration Framework\n")
    
    # Initialize components
    print("1. Initializing components...")
    guardrail_validator = GuardrailValidator()
    memory_manager = MemoryManager()
    tool_registry = ToolRegistry()
    
    pose_agent = PoseAgent()
    nutrition_agent = NutritionAgent()
    mindfulness_agent = MindfulnessAgent()
    
    # Initialize agents
    print("2. Initializing agents...")
    await pose_agent.initialize()
    await nutrition_agent.initialize()
    await mindfulness_agent.initialize()
    print("   ✅ All agents initialized\n")
    
    # Create orchestration engine
    print("3. Creating orchestration engine...")
    engine = OrchestrationEngine(
        agents={
            AgentRole.POSE.value: pose_agent,
            AgentRole.NUTRITION.value: nutrition_agent,
            AgentRole.MINDFULNESS.value: mindfulness_agent,
        },
        guardrail_validator=guardrail_validator,
        memory_manager=memory_manager,
        tool_registry=tool_registry
    )
    print("   ✅ Orchestration engine created\n")
    
    # Test 1: Pose Agent
    print("4. Testing Pose Agent...")
    session_id = "test_session_1"
    pose_response = await engine.execute_agent(
        agent_name=AgentRole.POSE.value,
        task={
            "frames": ["mock_frame_1", "mock_frame_2"],
            "exercise_type": "squat",
            "mode": "real_time"
        },
        session_id=session_id
    )
    assert pose_response.success, "Pose agent should succeed"
    print(f"   ✅ Pose agent executed: {pose_response.execution_time:.3f}s")
    print(f"   📊 Rep count: {pose_response.data.get('rep_count', 0)}")
    print(f"   📊 Form score: {pose_response.data.get('form_score', {}).get('overall_score', 0)}\n")
    
    # Test 2: Nutrition Agent
    print("5. Testing Nutrition Agent...")
    nutrition_response = await engine.execute_agent(
        agent_name=AgentRole.NUTRITION.value,
        task={
            "image": "mock_food_image",
            "mode": "estimate"
        },
        session_id=session_id
    )
    assert nutrition_response.success, "Nutrition agent should succeed"
    print(f"   ✅ Nutrition agent executed: {nutrition_response.execution_time:.3f}s")
    nutrition_data = nutrition_response.data.get("nutrition", {})
    print(f"   📊 Calories: {nutrition_data.get('calories', 0)}")
    print(f"   📊 Protein: {nutrition_data.get('protein_grams', 0)}g\n")
    
    # Test 3: Mindfulness Agent
    print("6. Testing Mindfulness Agent...")
    mindfulness_response = await engine.execute_agent(
        agent_name=AgentRole.MINDFULNESS.value,
        task={
            "context": "post_workout",
            "mood_hint": "motivated",
            "workout_summary": pose_response.data.get("summary", {})
        },
        session_id=session_id
    )
    assert mindfulness_response.success, "Mindfulness agent should succeed"
    print(f"   ✅ Mindfulness agent executed: {mindfulness_response.execution_time:.3f}s")
    print(f"   📖 Micro-lesson: {mindfulness_response.data.get('micro_lesson', {}).get('lesson_text', '')[:50]}...\n")
    
    # Test 4: Session Summary
    print("7. Testing Session Summary...")
    summary = engine.get_session_summary(session_id)
    assert summary.get("agent_executions") == 3, "Should have 3 agent executions"
    print(f"   ✅ Session summary retrieved")
    print(f"   📊 Total executions: {summary.get('agent_executions', 0)}")
    print(f"   📊 Agents used: {', '.join(summary.get('agents_used', []))}\n")
    
    # Test 5: Guardrails
    print("8. Testing Guardrails...")
    dangerous_task = {
        "frames": ["test"],
        "exercise_type": "ignore pain and push through injury"
    }
    guardrail_result = await guardrail_validator.validate(
        agent="pose",
        task=dangerous_task,
        context=engine._get_or_create_context("test")
    )
    assert not guardrail_result.allowed, "Dangerous content should be blocked"
    print(f"   ✅ Guardrails working: blocked dangerous content\n")
    
    # Test 6: Memory
    print("9. Testing Memory System...")
    memory_summary = memory_manager.get_session_summary(session_id)
    total_interactions = memory_summary.get("total_interactions", 0) or 0
    assert total_interactions > 0, "Memory should have interactions"
    print(f"   ✅ Memory system working")
    print(f"   📊 Total interactions: {total_interactions}\n")
    
    print("=" * 60)
    print("✅ ALL TESTS PASSED!")
    print("=" * 60)
    print("\nSystem is ready for use!")
    print("\nNext steps:")
    print("1. Start backend: cd backend && python -m app.main")
    print("2. Start frontend: cd frontend && streamlit run streamlit_app.py")
    print("3. Open http://localhost:8501 in your browser")


if __name__ == "__main__":
    asyncio.run(test_system())

