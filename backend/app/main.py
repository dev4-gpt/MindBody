"""
FastAPI Main Application

Entry point for the MindBody Coach API with multi-agent orchestration.
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, WebSocket
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
from contextlib import asynccontextmanager
import uvicorn
import logging
import uuid
import base64
from io import BytesIO

from .orchestration.engine import OrchestrationEngine, AgentRole
from .agents.pose_agent import PoseAgent
from .agents.nutrition_agent import NutritionAgent
from .agents.mindfulness_agent import MindfulnessAgent
from .guardrails.validator import GuardrailValidator
from .memory.manager import MemoryManager
from .tools.registry import ToolRegistry

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize components
guardrail_validator = GuardrailValidator()
memory_manager = MemoryManager()
tool_registry = ToolRegistry()

# Initialize agents
pose_agent = PoseAgent()
nutrition_agent = NutritionAgent()
mindfulness_agent = MindfulnessAgent()

# Initialize FastAPI app with lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown"""
    # Startup
    await pose_agent.initialize()
    await nutrition_agent.initialize()
    await mindfulness_agent.initialize()
    logger.info("All agents initialized")
    yield
    # Shutdown (if needed)
    logger.info("Shutting down...")

app = FastAPI(
    title="MindBody Strength Coach API",
    description="Multi-agent orchestration framework for health coaching",
    version="1.0.0",
    lifespan=lifespan
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify allowed origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Create orchestration engine
orchestration_engine = OrchestrationEngine(
    agents={
        AgentRole.POSE.value: pose_agent,
        AgentRole.NUTRITION.value: nutrition_agent,
        AgentRole.MINDFULNESS.value: mindfulness_agent,
    },
    guardrail_validator=guardrail_validator,
    memory_manager=memory_manager,
    tool_registry=tool_registry
)


# Request/Response Models
class PoseRequest(BaseModel):
    frames: List[str]  # Base64 encoded frames
    exercise_type: str
    session_id: Optional[str] = None
    user_id: Optional[str] = None


class NutritionRequest(BaseModel):
    image: str  # Base64 encoded image
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    user_hints: Optional[Dict[str, Any]] = None


class MindfulnessRequest(BaseModel):
    context: str  # post_workout, pre_workout, general
    session_id: Optional[str] = None
    user_id: Optional[str] = None
    mood_hint: Optional[str] = None
    workout_summary: Optional[Dict[str, Any]] = None


# API Endpoints

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "MindBody Strength Coach API",
        "version": "1.0.0",
        "agents": list(orchestration_engine.agents.keys())
    }


@app.get("/health")
async def health():
    """Health check endpoint"""
    return {"status": "healthy", "agents_initialized": all(
        agent.state.initialized for agent in orchestration_engine.agents.values()
    )}


@app.post("/api/v1/pose/infer")
async def infer_pose(request: PoseRequest):
    """
    Analyze pose from frames and provide form feedback.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Decode frames (in production, handle actual frame data)
        frames = request.frames  # Placeholder - decode base64 in production
        
        result = await orchestration_engine.orchestrate_workout_session(
            session_id=session_id,
            frames=frames,
            exercise_type=request.exercise_type,
            user_id=request.user_id
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in pose inference: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/food/estimate")
async def estimate_food(request: NutritionRequest):
    """
    Estimate nutrition from food image.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        # Decode image (in production, handle actual image data)
        image = request.image  # Placeholder - decode base64 in production
        
        result = await orchestration_engine.orchestrate_nutrition_analysis(
            session_id=session_id,
            image=image,
            user_id=request.user_id
        )
        
        return JSONResponse(content=result)
        
    except Exception as e:
        logger.error(f"Error in food estimation: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/api/v1/mind/short")
async def mindfulness_coaching(request: MindfulnessRequest):
    """
    Generate mindfulness micro-lesson and journaling prompt.
    """
    try:
        session_id = request.session_id or str(uuid.uuid4())
        
        response = await orchestration_engine.execute_agent(
            agent_name=AgentRole.MINDFULNESS.value,
            task={
                "context": request.context,
                "mood_hint": request.mood_hint,
                "workout_summary": request.workout_summary or {}
            },
            session_id=session_id,
            user_id=request.user_id
        )
        
        if not response.success:
            raise HTTPException(status_code=400, detail=response.error)
        
        return JSONResponse(content=response.data)
        
    except Exception as e:
        logger.error(f"Error in mindfulness coaching: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/session/{session_id}/summary")
async def get_session_summary(session_id: str):
    """
    Get summary of a session.
    """
    try:
        summary = orchestration_engine.get_session_summary(session_id)
        memory_summary = memory_manager.get_session_summary(session_id)
        
        return JSONResponse(content={
            "orchestration": summary,
            "memory": memory_summary
        })
        
    except Exception as e:
        logger.error(f"Error getting session summary: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/agents")
async def list_agents():
    """List all available agents and their states"""
    agents_info = {}
    for name, agent in orchestration_engine.agents.items():
        agents_info[name] = agent.get_state()
    
    return JSONResponse(content=agents_info)


@app.get("/api/v1/tools")
async def list_tools():
    """List all available tools"""
    tools_info = tool_registry.list_all_tool_info()
    return JSONResponse(content={"tools": tools_info})


# WebSocket endpoint for real-time pose analysis
@app.websocket("/ws/pose")
async def websocket_pose(websocket: WebSocket):
    """WebSocket endpoint for real-time pose analysis"""
    await websocket.accept()
    session_id = str(uuid.uuid4())
    
    try:
        while True:
            # Receive frame data
            data = await websocket.receive_json()
            frame = data.get("frame")
            exercise_type = data.get("exercise_type", "squat")
            
            # Process frame
            response = await orchestration_engine.execute_agent(
                agent_name=AgentRole.POSE.value,
                task={
                    "frames": [frame],
                    "exercise_type": exercise_type,
                    "mode": "real_time"
                },
                session_id=session_id,
                user_id=data.get("user_id")
            )
            
            # Send response
            await websocket.send_json({
                "success": response.success,
                "data": response.data,
                "session_id": session_id
            })
            
    except Exception as e:
        logger.error(f"WebSocket error: {str(e)}", exc_info=True)
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

