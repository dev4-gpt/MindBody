"""
Streamlit Frontend for MindBody Strength Coach

MVP frontend with multi-agent orchestration integration.
"""

import streamlit as st
import requests
import json
import uuid
from typing import Optional
import cv2
import numpy as np
from PIL import Image
import base64
from io import BytesIO

# Configuration
API_BASE_URL = "http://localhost:8000"

# Page configuration
st.set_page_config(
    page_title="MindBody Strength Coach",
    page_icon="💪",
    layout="wide"
)

# Initialize session state
if "session_id" not in st.session_state:
    st.session_state.session_id = str(uuid.uuid4())
if "user_id" not in st.session_state:
    st.session_state.user_id = None


def encode_image(image: Image.Image) -> str:
    """Encode PIL image to base64"""
    buffered = BytesIO()
    image.save(buffered, format="JPEG")
    return base64.b64encode(buffered.getvalue()).decode()


def call_api(endpoint: str, data: dict) -> dict:
    """Call API endpoint"""
    try:
        response = requests.post(
            f"{API_BASE_URL}{endpoint}",
            json=data,
            timeout=30
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"API Error: {str(e)}")
        return {}


# Header
st.title("💪 MindBody Strength Coach")
st.markdown("**Multi-Agent Orchestration Framework** - Real-time form correction, nutrition estimation, and mindfulness coaching")

# Sidebar
st.sidebar.title("Navigation")
page = st.sidebar.radio(
    "Choose Mode",
    ["🏋️ Workout", "🍎 Nutrition", "🧘 Mindfulness", "📊 Session Summary"]
)

# Workout Page
if page == "🏋️ Workout":
    st.header("Real-Time Exercise Form Analysis")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Exercise Selection")
        exercise_type = st.selectbox(
            "Select Exercise",
            ["squat", "pushup", "deadlift", "bicep_curl", "tricep_extension", 
             "chest_press", "shoulder_press", "lunge", "plank", "row"]
        )
        
        # Input mode selection
        input_mode = st.radio(
            "Input Mode",
            ["📷 Single Photo", "🎥 Video Recording"],
            horizontal=True
        )
        
        if input_mode == "📷 Single Photo":
            # Camera input for single photo
            camera_input = st.camera_input("Take a photo of your exercise form", key="workout_camera")
            
            if camera_input:
                # Convert to PIL Image
                image = Image.open(camera_input)
                
                # Encode frame
                frame_b64 = encode_image(image)
                
                # Call pose API
                with st.spinner("Analyzing form..."):
                    result = call_api("/api/v1/pose/infer", {
                        "frames": [frame_b64],
                        "exercise_type": exercise_type,
                        "session_id": st.session_state.session_id,
                        "user_id": st.session_state.user_id
                    })
                
                if result and "pose_analysis" in result:
                    pose_data = result["pose_analysis"]
                    
                    # Display results
                    st.image(image, caption="Current Frame", width=None)
                    
                    if pose_data.get("success"):
                        # Form score
                        form_score = pose_data.get("form_score", {})
                        score = form_score.get("overall_score", 0)
                        grade = form_score.get("grade", "N/A")
                        
                        st.metric("Form Score", f"{score:.1f}/100", grade)
                        
                        # Rep count
                        rep_count = pose_data.get("rep_count", 0)
                        st.metric("Rep Count", rep_count)
                        
                        # Form errors
                        form_errors = pose_data.get("form_errors", {})
                        top_errors = form_errors.get("top_errors", [])
                        
                        if top_errors:
                            st.subheader("⚠️ Form Corrections")
                            for error in top_errors:
                                severity = error.get("severity", 0.5)
                                color = "🔴" if severity > 0.7 else "🟡" if severity > 0.4 else "🟢"
                                st.write(f"{color} **{error.get('type', 'Error')}**: {error.get('message', '')}")
                        
                        # Recommendations
                        recommendations = form_errors.get("recommendations", [])
                        if recommendations:
                            st.subheader("💡 Recommendations")
                            for rec in recommendations:
                                st.write(f"• {rec}")
                        
                        # Trigger mindfulness if workout complete
                        if pose_data.get("workout_complete"):
                            st.success("🎉 Workout Complete! Check Mindfulness tab for a recovery session.")
        
        else:  # Video Recording
            st.info("🎥 **Video Mode**: Record your exercise and get real-time feedback!")
            
            # Video upload
            video_file = st.file_uploader(
                "Upload exercise video (MP4, MOV, AVI)",
                type=["mp4", "mov", "avi"],
                key="workout_video"
            )
            
            if video_file:
                # Store video in session state
                st.session_state.workout_video = video_file
                
                # Show video preview
                st.video(video_file)
                
                # Process video frames
                if st.button("Analyze Video", type="primary"):
                    with st.spinner("Processing video frames..."):
                        # For MVP, extract frames from video
                        # In production, use OpenCV to extract frames
                        import cv2
                        import tempfile
                        import os
                        
                        # Reset file pointer and save uploaded video temporarily
                        video_file.seek(0)  # Reset file pointer
                        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as tmp_file:
                            tmp_file.write(video_file.read())
                            tmp_path = tmp_file.name
                        
                        try:
                            # Extract frames using OpenCV
                            cap = cv2.VideoCapture(tmp_path)
                            frames_b64 = []
                            frame_count = 0
                            max_frames = 30  # Limit to 30 frames for performance
                            
                            while cap.isOpened() and frame_count < max_frames:
                                ret, frame = cap.read()
                                if not ret:
                                    break
                                
                                # Convert BGR to RGB
                                frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                                frame_pil = Image.fromarray(frame_rgb)
                                frame_b64 = encode_image(frame_pil)
                                frames_b64.append(frame_b64)
                                frame_count += 1
                            
                            cap.release()
                            
                            if frames_b64:
                                # Call pose API with all frames
                                result = call_api("/api/v1/pose/infer", {
                                    "frames": frames_b64,
                                    "exercise_type": exercise_type,
                                    "session_id": st.session_state.session_id,
                                    "user_id": st.session_state.user_id
                                })
                                
                                if result and "pose_analysis" in result:
                                    pose_data = result["pose_analysis"]
                                    
                                    if pose_data.get("success"):
                                        # Display summary
                                        form_score = pose_data.get("form_score", {})
                                        score = form_score.get("overall_score", 0)
                                        grade = form_score.get("grade", "N/A")
                                        
                                        col_score, col_reps = st.columns(2)
                                        with col_score:
                                            st.metric("Overall Form Score", f"{score:.1f}/100", grade)
                                        with col_reps:
                                            rep_count = pose_data.get("rep_count", 0)
                                            st.metric("Total Reps", rep_count)
                                        
                                        # Form errors
                                        form_errors = pose_data.get("form_errors", {})
                                        top_errors = form_errors.get("top_errors", [])
                                        
                                        if top_errors:
                                            st.subheader("⚠️ Form Corrections Detected")
                                            for error in top_errors:
                                                severity = error.get("severity", 0.5)
                                                color = "🔴" if severity > 0.7 else "🟡" if severity > 0.4 else "🟢"
                                                st.write(f"{color} **{error.get('type', 'Error')}**: {error.get('message', '')}")
                                        
                                        # Recommendations
                                        recommendations = form_errors.get("recommendations", [])
                                        if recommendations:
                                            st.subheader("💡 Recommendations")
                                            for rec in recommendations:
                                                st.write(f"• {rec}")
                                        
                                        # Trigger mindfulness if workout complete
                                        if pose_data.get("workout_complete"):
                                            st.success("🎉 Workout Complete! Check Mindfulness tab for a recovery session.")
                            else:
                                st.error("Could not extract frames from video")
                        
                        finally:
                            # Clean up temp file
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
    
    with col2:
        st.subheader("Session Info")
        st.write(f"**Session ID**: {st.session_state.session_id[:8]}...")
        if st.session_state.user_id:
            st.write(f"**User ID**: {st.session_state.user_id}")
        
        st.subheader("Exercise Tips")
        exercise_tips = {
            "squat": """
            **Squat Form Tips:**
            - Keep knees aligned with ankles
            - Maintain straight back
            - Go below parallel for full depth
            """,
            "pushup": """
            **Push-up Form Tips:**
            - Keep body in straight line
            - Lower chest to ground
            - Engage core throughout
            """,
            "deadlift": """
            **Deadlift Form Tips:**
            - Keep back straight
            - Hinge at hips
            - Drive through heels
            """,
            "bicep_curl": """
            **Bicep Curl Form Tips:**
            - Keep elbows close to body
            - Control the weight (no swinging)
            - Full range of motion
            """,
            "tricep_extension": """
            **Tricep Extension Form Tips:**
            - Keep upper arms stationary
            - Extend fully at bottom
            - Control the negative
            """,
            "chest_press": """
            **Chest Press Form Tips:**
            - Keep shoulder blades retracted
            - Lower to chest level
            - Press in controlled motion
            """,
            "shoulder_press": """
            **Shoulder Press Form Tips:**
            - Keep core engaged
            - Press straight up
            - Don't arch back excessively
            """,
            "lunge": """
            **Lunge Form Tips:**
            - Step forward, not down
            - Keep front knee over ankle
            - Maintain upright torso
            """,
            "plank": """
            **Plank Form Tips:**
            - Keep body in straight line
            - Engage core and glutes
            - Don't let hips sag
            """,
            "row": """
            **Row Form Tips:**
            - Pull to lower chest/upper abs
            - Squeeze shoulder blades
            - Keep core engaged
            """
        }
        
        tip = exercise_tips.get(exercise_type, "Select an exercise to see tips")
        st.info(tip)

# Nutrition Page
elif page == "🍎 Nutrition":
    st.header("Food Nutrition Estimation")
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Upload Food Image")
        uploaded_file = st.file_uploader(
            "Choose a food image",
            type=["jpg", "jpeg", "png"]
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", width=None)
            
            # Encode image
            image_b64 = encode_image(image)
            
            # Portion size hint
            size_hint = st.selectbox(
                "Portion Size (optional)",
                ["", "small", "medium", "large"],
                help="Help improve accuracy by selecting portion size"
            )
            
            user_hints = {}
            if size_hint:
                user_hints["size_hint"] = size_hint
            
            # Analyze button
            if st.button("Analyze Nutrition", type="primary"):
                with st.spinner("Analyzing food..."):
                    result = call_api("/api/v1/food/estimate", {
                        "image": image_b64,
                        "session_id": st.session_state.session_id,
                        "user_id": st.session_state.user_id,
                        "user_hints": user_hints
                    })
                
                if result and "nutrition" in result:
                    nutrition_data = result["nutrition"]
                    
                    if nutrition_data and nutrition_data.get("success"):
                        st.session_state.nutrition_result = nutrition_data
    
    with col2:
        st.subheader("Nutrition Results")
        
        if "nutrition_result" in st.session_state:
            nutrition = st.session_state.nutrition_result
            
            # Classification
            classification = nutrition.get("classification", {})
            if classification:
                st.write(f"**Food**: {classification.get('top_class', 'Unknown').replace('_', ' ').title()}")
                st.write(f"**Confidence**: {classification.get('confidence', 0):.1%}")
            
            # Nutrition values
            nutrition_info = nutrition.get("nutrition", {})
            if nutrition_info:
                calories = nutrition_info.get("calories", 0)
                protein = nutrition_info.get("protein_grams", 0)
                
                col_cal, col_prot = st.columns(2)
                with col_cal:
                    st.metric("Calories", f"{calories:.0f}")
                with col_prot:
                    st.metric("Protein", f"{protein:.1f}g")
                
                # Portion info
                portion = nutrition.get("portion_estimate", {})
                if portion:
                    st.write(f"**Estimated Portion**: {portion.get('portion_grams', 0):.0f}g")
            
            # Suggestions
            suggestions = nutrition.get("suggestions", {})
            if suggestions:
                st.subheader("💡 Suggestions")
                suggestion_list = suggestions.get("suggestions", [])
                for sug in suggestion_list:
                    st.info(f"**Swap**: {sug.get('swap', '').replace('_', ' ').title()} - {sug.get('reason', '')}")
                
                tips = suggestions.get("tips", [])
                for tip in tips:
                    st.write(f"• {tip}")

# Mindfulness Page
elif page == "🧘 Mindfulness":
    st.header("Mindfulness & Grit Coaching")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Coaching Session")
        
        context = st.selectbox(
            "Context",
            ["post_workout", "pre_workout", "general"],
            help="When are you using this coaching?"
        )
        
        mood_hint = st.selectbox(
            "How are you feeling? (optional)",
            ["", "motivated", "tired", "frustrated", "neutral"]
        )
        
        if st.button("Get Micro-Lesson", type="primary"):
            with st.spinner("Generating coaching..."):
                result = call_api("/api/v1/mind/short", {
                    "context": context,
                    "session_id": st.session_state.session_id,
                    "user_id": st.session_state.user_id,
                    "mood_hint": mood_hint if mood_hint else None
                })
            
            if result and result.get("success"):
                st.session_state.mindfulness_result = result
    
    with col2:
        st.subheader("Session Info")
        st.write(f"**Session ID**: {st.session_state.session_id[:8]}...")
    
    # Display results
    if "mindfulness_result" in st.session_state:
        result = st.session_state.mindfulness_result
        
        # Micro-lesson
        micro_lesson = result.get("micro_lesson", {})
        if micro_lesson:
            st.subheader("📖 Micro-Lesson")
            st.info(micro_lesson.get("lesson_text", ""))
        
        # Breathing guide
        breathing = result.get("breathing_guide", {})
        if breathing:
            st.subheader("🌬️ Breathing Exercise")
            st.write(f"**Pattern**: {breathing.get('pattern_name', '')}")
            st.write(f"**Instructions**: {breathing.get('instructions', '')}")
            st.write(f"**Duration**: {breathing.get('duration_seconds', 0)} seconds")
        
        # Journal prompt
        journal = result.get("journal_prompt", {})
        if journal:
            st.subheader("✍️ Journal Prompt")
            prompt = journal.get("prompt", "")
            st.write(f"**{prompt}**")
            
            journal_entry = st.text_area(
                "Your response (optional)",
                height=100,
                max_chars=500
            )
            
            if st.button("Save Entry"):
                st.success("Entry saved! (In production, this would be stored)")

# Session Summary Page
elif page == "📊 Session Summary":
    st.header("Session Summary")
    
    if st.button("Refresh Summary"):
        try:
            response = requests.get(
                f"{API_BASE_URL}/api/v1/session/{st.session_state.session_id}/summary",
                timeout=10
            )
            response.raise_for_status()
            summary = response.json()
            st.session_state.session_summary = summary
        except Exception as e:
            st.error(f"Error loading summary: {str(e)}")
    
    if "session_summary" in st.session_state:
        summary = st.session_state.session_summary
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Orchestration Summary")
            orch = summary.get("orchestration", {})
            st.write(f"**Agents Used**: {', '.join(orch.get('agents_used', []))}")
            st.write(f"**Total Executions**: {orch.get('agent_executions', 0)}")
            st.write(f"**Total Time**: {orch.get('total_execution_time', 0):.2f}s")
        
        with col2:
            st.subheader("Memory Summary")
            memory = summary.get("memory", {})
            st.write(f"**Total Interactions**: {memory.get('total_interactions', 0)}")
            st.write(f"**Duration**: {memory.get('duration_seconds', 0):.1f}s")
    
    # Agent status
    st.subheader("Agent Status")
    try:
        response = requests.get(f"{API_BASE_URL}/api/v1/agents", timeout=10)
        response.raise_for_status()
        agents = response.json()
        
        for agent_name, agent_info in agents.items():
            status = "✅" if agent_info.get("initialized") else "❌"
            st.write(f"{status} **{agent_name}**: {agent_info.get('execution_count', 0)} executions")
    except Exception as e:
        st.error(f"Error loading agent status: {str(e)}")

# Footer
st.markdown("---")
st.markdown("**Disclaimer**: This is for educational purposes only and not medical advice.")
st.markdown("Built with multi-agent orchestration framework for NittanyAI competition.")

