# API Documentation

## Base URL

```
http://localhost:8000
```

## Endpoints

### Health Check

**GET** `/health`

Check API health status.

**Response:**
```json
{
  "status": "healthy",
  "agents_initialized": true
}
```

### Root

**GET** `/`

Get API information.

**Response:**
```json
{
  "message": "MindBody Strength Coach API",
  "version": "1.0.0",
  "agents": ["pose", "nutrition", "mindfulness"]
}
```

### Pose Analysis

**POST** `/api/v1/pose/infer`

Analyze exercise form from video frames.

**Request Body:**
```json
{
  "frames": ["base64_encoded_frame1", "base64_encoded_frame2"],
  "exercise_type": "squat",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id"
}
```

**Response:**
```json
{
  "pose_analysis": {
    "success": true,
    "exercise_type": "squat",
    "form_score": {
      "overall_score": 85.5,
      "grade": "Good"
    },
    "rep_count": 12,
    "form_errors": {
      "errors": [...],
      "top_errors": [...],
      "recommendations": [...]
    },
    "workout_complete": false
  },
  "session_id": "session_id",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Nutrition Estimation

**POST** `/api/v1/food/estimate`

Estimate nutrition from food image.

**Request Body:**
```json
{
  "image": "base64_encoded_image",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id",
  "user_hints": {
    "size_hint": "medium"
  }
}
```

**Response:**
```json
{
  "nutrition": {
    "success": true,
    "classification": {
      "top_class": "grilled_chicken",
      "confidence": 0.85
    },
    "portion_estimate": {
      "portion_grams": 200,
      "size_estimate": "medium"
    },
    "nutrition": {
      "calories": 330,
      "protein_grams": 62
    },
    "suggestions": {
      "suggestions": [...],
      "tips": [...]
    }
  },
  "session_id": "session_id",
  "timestamp": "2024-01-01T12:00:00"
}
```

### Mindfulness Coaching

**POST** `/api/v1/mind/short`

Generate mindfulness micro-lesson and journaling prompt.

**Request Body:**
```json
{
  "context": "post_workout",
  "session_id": "optional_session_id",
  "user_id": "optional_user_id",
  "mood_hint": "motivated",
  "workout_summary": {
    "form_score": 85,
    "rep_count": 12
  }
}
```

**Response:**
```json
{
  "success": true,
  "micro_lesson": {
    "lesson_text": "Breathe in for 4 counts...",
    "context": "post_workout",
    "duration_seconds": 60
  },
  "breathing_guide": {
    "pattern_name": "Box Breathing",
    "pattern": "4-4-4-4",
    "instructions": "Repeat 6 cycles..."
  },
  "journal_prompt": {
    "prompt": "What did you push through just now?",
    "max_words": 50
  },
  "mood_analysis": {
    "mood": "Motivated",
    "valence": 0.7,
    "energy": 0.8
  }
}
```

### Session Summary

**GET** `/api/v1/session/{session_id}/summary`

Get summary of a session.

**Response:**
```json
{
  "orchestration": {
    "session_id": "session_id",
    "agent_executions": 5,
    "agents_used": ["pose", "mindfulness"],
    "total_execution_time": 2.5
  },
  "memory": {
    "total_interactions": 5,
    "duration_seconds": 300,
    "start_time": "2024-01-01T12:00:00",
    "end_time": "2024-01-01T12:05:00"
  }
}
```

### List Agents

**GET** `/api/v1/agents`

List all agents and their states.

**Response:**
```json
{
  "pose": {
    "name": "pose",
    "initialized": true,
    "execution_count": 10,
    "available_tools": ["analyze_pose", "detect_form_errors", ...]
  },
  "nutrition": {...},
  "mindfulness": {...}
}
```

### List Tools

**GET** `/api/v1/tools`

List all available tools.

**Response:**
```json
{
  "tools": [
    {
      "name": "analyze_pose",
      "description": "Extract pose keypoints from a video frame",
      "execution_count": 50
    },
    ...
  ]
}
```

## WebSocket

### Real-time Pose Analysis

**WebSocket** `/ws/pose`

Real-time pose analysis via WebSocket.

**Message Format (Client → Server):**
```json
{
  "frame": "base64_encoded_frame",
  "exercise_type": "squat",
  "user_id": "optional_user_id"
}
```

**Message Format (Server → Client):**
```json
{
  "success": true,
  "data": {
    "keypoints": {...},
    "form_errors": {...},
    "rep_count": 5
  },
  "session_id": "session_id"
}
```

## Error Responses

All endpoints may return errors in the following format:

```json
{
  "detail": "Error message"
}
```

**Status Codes:**
- `400`: Bad Request
- `500`: Internal Server Error

