# MindBody Strength Coach - Multi-Agent Orchestration Framework

A sophisticated health coaching platform featuring a multi-agent orchestration system with tools, guardrails, and memory for real-time exercise form correction, nutrition estimation, and mindfulness coaching.

## 🎯 Key Features

- **Multi-Agent Orchestration**: Coordinated agents for pose analysis, nutrition, and mindfulness
- **Tool System**: Specialized tools for each agent domain
- **Safety Guardrails**: Built-in safety checks and content filtering
- **Memory System**: Context-aware memory for personalized coaching
- **Real-time Pose Analysis**: MediaPipe/MoveNet integration with form correction
- **Nutrition Estimation**: Food image classification and calorie estimation
- **Mindfulness Coaching**: LLM-powered micro-lessons and journaling prompts

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────┐
│              Orchestration Engine                        │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐             │
│  │  Pose    │  │Nutrition │  │Mindfulness│             │
│  │  Agent   │  │  Agent   │  │   Agent   │             │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘             │
│       │             │              │                    │
│       └─────────────┴──────────────┘                    │
│                    │                                     │
│              ┌─────▼─────┐                              │
│              │  Memory   │                              │
│              │  Manager   │                              │
│              └─────┬─────┘                              │
│                    │                                     │
│              ┌─────▼─────┐                              │
│              │ Guardrails│                              │
│              └───────────┘                              │
└─────────────────────────────────────────────────────────┘
```

## 🚀 Quick Start

### Prerequisites

- Python 3.10+
- Node.js 18+ (for React frontend, optional)
- Webcam access
- GPU (optional, for faster LLM inference)

### Installation

```bash
# Clone the repository
git clone <repo-url>
cd mindbody-coach

# Install backend dependencies
cd backend
pip install -r requirements.txt

# Install frontend dependencies (if using React)
cd ../frontend/react_app
npm install

# Run the application
cd ../../backend
python -m app.main
```

### Docker Setup

```bash
docker-compose up -d
```

## 📁 Project Structure

```
mindbody-coach/
├── backend/
│   ├── app/
│   │   ├── agents/          # Agent implementations
│   │   ├── orchestration/   # Orchestration engine
│   │   ├── tools/           # Agent tools
│   │   ├── guardrails/      # Safety system
│   │   ├── memory/          # Memory management
│   │   └── main.py          # FastAPI entry point
│   └── requirements.txt
├── frontend/
│   ├── streamlit_app.py     # Streamlit MVP
│   └── react_app/           # React frontend (optional)
├── inference/
│   ├── pose_server/
│   ├── food_classifier/
│   └── llm_agent/
└── docs/
    └── PRD.md
```

## 🧠 Multi-Agent System

### Architecture Overview

The system uses a sophisticated multi-agent orchestration framework where specialized agents work together to provide comprehensive health coaching. Each agent has access to domain-specific tools and operates under a unified orchestration layer.

### Agents

1. **Pose Agent** (`PoseAgent`): Analyzes exercise form in real-time
   - **Tools**: 
     - `analyze_pose`: Extract keypoints from video frames
     - `detect_form_errors`: Detect form mistakes (knee valgus, torso sag, etc.)
     - `count_reps`: Count exercise repetitions
     - `calculate_form_score`: Calculate overall form score
   - **Capabilities**: Real-time pose estimation, form correction, rep counting
   
2. **Nutrition Agent** (`NutritionAgent`): Estimates calories and macros from food images
   - **Tools**:
     - `classify_food`: Classify food type from image
     - `estimate_portion`: Estimate portion size in grams
     - `calculate_nutrition`: Calculate calories and macros
     - `suggest_improvements`: Suggest healthier alternatives
   - **Capabilities**: Food classification, portion estimation, nutrition calculation
   
3. **Mindfulness Agent** (`MindfulnessAgent`): Provides coaching and journaling prompts
   - **Tools**:
     - `generate_micro_lesson`: Generate short mindfulness lessons
     - `create_journal_prompt`: Create journaling prompts
     - `analyze_mood`: Analyze user mood and emotional state
     - `generate_breathing_guide`: Generate breathing exercises
   - **Capabilities**: Personalized coaching, mood analysis, breathing guides

### Orchestration Engine

The `OrchestrationEngine` is the central coordinator that:

- **Coordinates Agents**: Manages agent execution and inter-agent communication
- **Applies Guardrails**: Validates inputs and outputs for safety and compliance
- **Manages Memory**: Maintains session context and user history
- **Handles Workflows**: Orchestrates complex multi-agent workflows (e.g., workout → mindfulness)
- **Tracks Execution**: Monitors agent performance and execution metrics

### Tool System

Tools are reusable, composable functions that agents can execute:

- **Domain-Specific**: Each agent has tools tailored to its domain
- **Composable**: Tools can be chained together for complex operations
- **Trackable**: All tool executions are logged and tracked
- **Validated**: Tool parameters are validated before execution

### Guardrails

Multi-layer safety system:

- **Input Validation**: Checks for dangerous content before agent execution
- **Output Sanitization**: Removes or modifies problematic content
- **Medical Advice Filtering**: Blocks medical advice and adds disclaimers
- **Rate Limiting**: Prevents abuse and ensures fair usage
- **Compliance**: Enforces safety standards and regulations

### Memory System

Context-aware memory management:

- **Session Memory**: Tracks all interactions within a session
- **User Memory**: Maintains long-term user preferences and history
- **Pattern Recognition**: Identifies trends and patterns in user behavior
- **Context Loading**: Provides relevant context to agents for personalized responses

## 🛡️ Guardrails

- Content filtering for medical advice
- Safety checks for exercise recommendations
- Input validation and sanitization
- Rate limiting and abuse prevention

## 💾 Memory System

- Session-based memory for user context
- Vector storage for semantic search
- Long-term habit tracking
- Personalized coaching history

## 📊 API Endpoints

See `docs/API.md` for detailed API documentation.

## 🧪 Testing

```bash
pytest tests/
```

## 📝 License

MIT License

## 🤝 Contributing

See `CONTRIBUTING.md` for guidelines.

