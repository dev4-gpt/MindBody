# Quick Start Guide

## Prerequisites

- Python 3.10+
- Webcam (for pose analysis)
- 4GB+ RAM
- Optional: GPU for faster LLM inference

## Installation

### 1. Clone and Setup

```bash
# Navigate to project directory
cd "AI health coach"

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install backend dependencies
cd backend
pip install -r requirements.txt
```

### 2. Configure Environment

```bash
# Copy example environment file
cp ../.env.example ../.env

# Edit .env if needed (defaults should work)
```

### 3. Start Backend

```bash
# From backend directory
python -m app.main

# Or use uvicorn directly
uvicorn app.main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`

### 4. Start Frontend

```bash
# In a new terminal, from project root
cd frontend
streamlit run streamlit_app.py
```

The frontend will be available at `http://localhost:8501`

## Docker Setup (Alternative)

```bash
# From project root
docker-compose up -d

# Backend: http://localhost:8000
# Frontend: http://localhost:8501
```

## Testing the System

### 1. Test API Health

```bash
curl http://localhost:8000/health
```

### 2. Test Agents

```bash
curl http://localhost:8000/api/v1/agents
```

### 3. Test Pose Analysis

```bash
# Using Python
python -c "
import requests
import base64
from PIL import Image

# Create a test image
img = Image.new('RGB', (640, 480), color='red')
import io
buffered = io.BytesIO()
img.save(buffered, format='JPEG')
img_b64 = base64.b64encode(buffered.getvalue()).decode()

response = requests.post('http://localhost:8000/api/v1/pose/infer', json={
    'frames': [img_b64],
    'exercise_type': 'squat'
})
print(response.json())
"
```

### 4. Test Nutrition

```bash
# Similar to pose, but use /api/v1/food/estimate endpoint
```

### 5. Test Mindfulness

```bash
curl -X POST http://localhost:8000/api/v1/mind/short \
  -H "Content-Type: application/json" \
  -d '{
    "context": "post_workout",
    "mood_hint": "motivated"
  }'
```

## Using the Frontend

1. Open `http://localhost:8501` in your browser
2. Navigate between tabs:
   - **Workout**: Real-time pose analysis
   - **Nutrition**: Food image analysis
   - **Mindfulness**: Coaching and journaling
   - **Session Summary**: View session metrics

## Multi-Agent Features

### Orchestration

The system automatically orchestrates agents:
- Pose analysis triggers mindfulness after workout completion
- Nutrition analysis stores preferences for future sessions
- All interactions are tracked in memory

### Guardrails

Safety features are automatically applied:
- Medical advice filtering
- Dangerous exercise detection
- Rate limiting
- Content sanitization

### Memory

Context is maintained across sessions:
- Session history
- User preferences
- Pattern recognition
- Long-term trends

## Troubleshooting

### Backend won't start

- Check if port 8000 is available
- Verify Python version (3.10+)
- Check dependencies: `pip install -r requirements.txt`

### Frontend can't connect to backend

- Verify backend is running on port 8000
- Check `API_BASE_URL` in `streamlit_app.py`
- Check CORS settings in `main.py`

### Agents not initializing

- Check logs for initialization errors
- Verify model files are accessible (if using custom models)
- Check memory/disk space

## Next Steps

- Read [ARCHITECTURE.md](docs/ARCHITECTURE.md) for system design
- Read [API.md](docs/API.md) for API documentation
- Check [CONTRIBUTING.md](CONTRIBUTING.md) for development guidelines

## Demo Script

See `docs/demo_script.md` for the 3-minute demo script for NittanyAI competition.

