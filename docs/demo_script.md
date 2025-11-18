# Demo Script - MindBody Strength Coach

## 3-Minute Demo for NittanyAI Competition

### Setup (Before Demo)

1. Ensure backend is running (`http://localhost:8000`)
2. Ensure frontend is running (`http://localhost:8501`)
3. Have webcam ready
4. Have a food image ready (or use sample)
5. Test all features once before demo

---

### Demo Flow (3 minutes)

#### **Intro (10 seconds)**

> "This is MindBody Strength Coach: a multi-agent orchestration system that provides real-time exercise form correction, quick nutrition feedback, and short grit micro-coaching. Built with a sophisticated agent framework featuring tools, guardrails, and memory."

**[Show frontend homepage]**

---

#### **Live CV Demo - Pose Analysis (60 seconds)**

> "Let me demonstrate the pose analysis agent with real-time form correction."

**Actions:**
1. Navigate to "Workout" tab
2. Select "squat" from dropdown
3. Turn on webcam
4. Perform 2-3 squats

**While performing:**
> "The system is analyzing my form in real-time using MediaPipe pose estimation. Notice how it detects keypoints and provides feedback."

**After squats:**
> "The agent detected my form, counted reps, and calculated a form score. It identified specific errors like knee valgus and provided corrective recommendations. All of this is orchestrated through our multi-agent framework with automatic guardrails and memory storage."

**[Show form score, errors, recommendations]**

---

#### **Nutrition Analysis (30 seconds)**

> "Now let's analyze nutrition using our nutrition agent."

**Actions:**
1. Navigate to "Nutrition" tab
2. Upload food image
3. Click "Analyze Nutrition"

**While analyzing:**
> "The nutrition agent classifies the food, estimates portion size, and calculates calories and protein. It also suggests healthier alternatives."

**[Show results: classification, calories, protein, suggestions]**

> "Notice how the agent uses multiple tools: classification, portion estimation, nutrition calculation, and improvement suggestions - all coordinated through our orchestration engine."

---

#### **Mindfulness Coaching (30 seconds)**

> "After a workout, our mindfulness agent provides coaching."

**Actions:**
1. Navigate to "Mindfulness" tab
2. Select "post_workout" context
3. Select "motivated" mood
4. Click "Get Micro-Lesson"

**While generating:**
> "The mindfulness agent generates a personalized micro-lesson, breathing guide, and journaling prompt. All content is validated through our guardrails to ensure safety and compliance."

**[Show micro-lesson, breathing guide, journal prompt]**

> "The agent uses context from the workout session stored in memory to personalize the coaching."

---

#### **Session Summary & Architecture (20 seconds)**

> "Let me show you the session summary and system architecture."

**Actions:**
1. Navigate to "Session Summary" tab
2. Show agent status
3. Show session metrics

**While showing:**
> "You can see all agents are initialized and have executed multiple times. The orchestration engine has coordinated interactions, applied guardrails, and stored everything in memory. This multi-agent architecture makes the system modular, scalable, and maintainable."

**[Show session summary, agent states, execution counts]**

---

#### **Close (10 seconds)**

> "This demonstrates our complete multi-agent orchestration framework with tools, guardrails, and memory - all working together to provide a seamless mind-body coaching experience. Thank you!"

**[Show final slide or README]**

---

### Key Points to Emphasize

1. **Multi-Agent Orchestration**: Multiple specialized agents working together
2. **Tools**: Each agent uses specialized tools for its domain
3. **Guardrails**: Automatic safety and compliance validation
4. **Memory**: Context-aware memory for personalized coaching
5. **Real-time**: Live pose analysis with immediate feedback
6. **Integration**: Seamless flow between different agents

### Backup Plan

If live demo fails:
1. Have pre-recorded video ready
2. Show code architecture (orchestration engine, agents, tools)
3. Show API documentation
4. Demonstrate via curl/Postman

### Technical Highlights for Judges

- **Orchestration Engine**: Coordinates agents, applies guardrails, manages memory
- **Tool System**: Reusable, composable tools for each agent
- **Guardrails**: Input/output validation, safety checks, compliance
- **Memory**: Session and user-level context management
- **Scalability**: Modular design allows horizontal scaling
- **Safety**: Multiple layers of validation and sanitization

---

### Demo Checklist

- [ ] Backend running and healthy
- [ ] Frontend accessible
- [ ] Webcam working
- [ ] Food image ready
- [ ] All agents initialized
- [ ] Test run completed
- [ ] Backup video ready (optional)
- [ ] Slides ready (optional)

---

### Post-Demo Q&A Preparation

**Possible Questions:**

1. **"How does the orchestration work?"**
   - Explain OrchestrationEngine, agent coordination, context passing

2. **"What are the guardrails?"**
   - Medical advice filtering, dangerous exercise detection, rate limiting

3. **"How does memory work?"**
   - Session memory, user memory, pattern recognition

4. **"Can you add new agents?"**
   - Yes, inherit from BaseAgent, register tools, add to engine

5. **"How do tools work?"**
   - Tools are reusable functions agents can call, registered per agent

6. **"What about scalability?"**
   - Agents can be deployed separately, tools can be distributed, memory can use Redis

7. **"How accurate is the pose detection?"**
   - Uses MediaPipe/MoveNet, rule-based form detection, 85%+ accuracy target

8. **"How do you ensure safety?"**
   - Multiple guardrail layers, content sanitization, disclaimer enforcement

---

### Success Metrics to Mention

- Real-time pose inference at ≥15 FPS
- Form correction accuracy ≥85%
- Nutrition estimation MAPE ≤25%
- LLM response latency ≤2s
- End-to-end demo success: 100%

