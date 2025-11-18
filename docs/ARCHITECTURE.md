# Architecture Documentation

## Multi-Agent Orchestration Framework

### Overview

The MindBody Strength Coach uses a sophisticated multi-agent orchestration framework that coordinates specialized agents for different health coaching tasks. This architecture enables modular, scalable, and maintainable code while providing advanced features like tool usage, guardrails, and memory management.

### Core Components

#### 1. Orchestration Engine

The `OrchestrationEngine` is the central coordinator that:

- Manages agent execution and coordination
- Applies guardrails before and after agent execution
- Maintains session context and memory
- Handles multi-agent workflows (sequential and parallel)
- Provides high-level orchestration methods for common workflows

**Key Features:**
- Session management
- Context passing between agents
- Error handling and recovery
- Execution tracking and metrics

#### 2. Agents

Agents are specialized components that handle specific domains:

**Pose Agent** (`PoseAgent`)
- Real-time exercise form analysis
- Form error detection
- Rep counting
- Form scoring

**Nutrition Agent** (`NutritionAgent`)
- Food image classification
- Portion estimation
- Nutrition calculation
- Improvement suggestions

**Mindfulness Agent** (`MindfulnessAgent`)
- Micro-lesson generation
- Journaling prompts
- Mood analysis
- Breathing guides

All agents inherit from `BaseAgent` which provides:
- Tool registration and execution
- State management
- Initialization lifecycle
- Execution tracking

#### 3. Tools

Tools are reusable functions that agents can call:

**Pose Tools:**
- `AnalyzePoseTool`: Extract keypoints from frames
- `DetectFormErrorsTool`: Detect form errors
- `CountRepsTool`: Count repetitions
- `CalculateFormScoreTool`: Calculate overall form score

**Nutrition Tools:**
- `ClassifyFoodTool`: Classify food from images
- `EstimatePortionTool`: Estimate portion sizes
- `CalculateNutritionTool`: Calculate calories and macros
- `SuggestImprovementsTool`: Suggest healthier alternatives

**Mindfulness Tools:**
- `GenerateMicroLessonTool`: Generate micro-lessons
- `CreateJournalPromptTool`: Create journaling prompts
- `AnalyzeMoodTool`: Analyze user mood
- `GenerateBreathingGuideTool`: Generate breathing exercises

#### 4. Guardrails

The `GuardrailValidator` ensures safety and compliance:

**Input Validation:**
- Dangerous exercise advice detection
- Self-harm content detection
- Rate limiting

**Output Validation:**
- Medical advice filtering
- Content sanitization
- Disclaimer enforcement

**Safety Features:**
- Keyword-based filtering
- Pattern matching
- Automatic sanitization
- Compliance enforcement

#### 5. Memory System

The `MemoryManager` provides context-aware memory:

**Session Memory:**
- Stores all interactions in a session
- Maintains conversation history
- Tracks agent execution order

**User Memory:**
- Long-term user preferences
- Historical patterns
- Personalized context

**Pattern Recognition:**
- Exercise frequency tracking
- Form score trends
- User behavior patterns

### Data Flow

```
User Request
    ↓
FastAPI Endpoint
    ↓
Orchestration Engine
    ↓
Guardrail Validation (Input)
    ↓
Memory Context Loading
    ↓
Agent Execution
    ├─ Tool Execution
    └─ Result Generation
    ↓
Guardrail Validation (Output)
    ↓
Memory Storage
    ↓
Response to User
```

### Workflow Examples

#### Workout Session Workflow

1. User starts workout session
2. Frames sent to Pose Agent
3. Pose Agent uses tools to analyze form
4. Form errors detected and scored
5. Reps counted
6. If workout complete, trigger Mindfulness Agent
7. Results stored in memory
8. Response returned to user

#### Nutrition Analysis Workflow

1. User uploads food image
2. Image sent to Nutrition Agent
3. Nutrition Agent classifies food
4. Portion estimated
5. Nutrition calculated
6. Improvements suggested
7. Results stored in memory
8. Response returned to user

### Scalability Considerations

**Horizontal Scaling:**
- Agents can be deployed as separate services
- Tool execution can be distributed
- Memory can use distributed storage (Redis, etc.)

**Vertical Scaling:**
- Model inference can use GPU acceleration
- Caching for frequently used tools
- Async execution for I/O-bound operations

### Security

- Input validation at multiple layers
- Output sanitization
- Rate limiting
- Session isolation
- User data privacy

### Future Enhancements

- Vector storage for semantic memory search
- Agent-to-agent communication protocols
- Dynamic tool discovery
- Learning from user feedback
- Multi-modal agent coordination

