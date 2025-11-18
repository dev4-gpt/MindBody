"""
Pose Analysis Tools

Tools for pose estimation, form error detection, rep counting, and scoring.
"""

from typing import Dict, Any, List
import numpy as np

from .base import BaseTool
from ..orchestration.context import OrchestrationContext


class AnalyzePoseTool(BaseTool):
    """Analyze pose from a single frame"""
    
    def __init__(self):
        super().__init__(
            name="analyze_pose",
            description="Extract pose keypoints from a video frame",
            parameters={
                "frame": "Video frame (numpy array or image)",
                "model": "Pose model to use (mediapipe, movenet)"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Extract keypoints from frame"""
        frame = parameters.get("frame")
        model = parameters.get("model", "mediapipe")
        
        # Placeholder: In production, call MediaPipe/MoveNet here
        # For MVP, return mock keypoints
        keypoints = {
            "left_shoulder": {"x": 0.3, "y": 0.2, "z": 0.0, "visibility": 0.9},
            "right_shoulder": {"x": 0.7, "y": 0.2, "z": 0.0, "visibility": 0.9},
            "left_elbow": {"x": 0.25, "y": 0.4, "z": 0.0, "visibility": 0.85},
            "right_elbow": {"x": 0.75, "y": 0.4, "z": 0.0, "visibility": 0.85},
            "left_hip": {"x": 0.35, "y": 0.5, "z": 0.0, "visibility": 0.9},
            "right_hip": {"x": 0.65, "y": 0.5, "z": 0.0, "visibility": 0.9},
            "left_knee": {"x": 0.35, "y": 0.7, "z": 0.0, "visibility": 0.85},
            "right_knee": {"x": 0.65, "y": 0.7, "z": 0.0, "visibility": 0.85},
            "left_ankle": {"x": 0.35, "y": 0.9, "z": 0.0, "visibility": 0.8},
            "right_ankle": {"x": 0.65, "y": 0.9, "z": 0.0, "visibility": 0.8},
        }
        
        return {
            "keypoints": keypoints,
            "model": model,
            "frame_timestamp": context.timestamp.isoformat()
        }


class DetectFormErrorsTool(BaseTool):
    """Detect form errors based on keypoints"""
    
    def __init__(self):
        super().__init__(
            name="detect_form_errors",
            description="Detect exercise form errors from keypoint sequences",
            parameters={
                "keypoints_list": "List of keypoint dictionaries",
                "exercise_type": "Type of exercise (squat, pushup, deadlift)"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Detect form errors"""
        keypoints_list = parameters.get("keypoints_list", [])
        exercise_type = parameters.get("exercise_type", "squat")
        
        errors = []
        recommendations = []
        
        if exercise_type == "squat":
            # Check for knee valgus
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_knee = keypoints.get("left_knee", {})
                left_ankle = keypoints.get("left_ankle", {})
                
                if abs(left_knee.get("x", 0) - left_ankle.get("x", 0)) > 0.1:
                    errors.append({
                        "type": "knee_valgus",
                        "severity": 0.7,
                        "message": "Knees tracking inward - keep them aligned with ankles"
                    })
                    recommendations.append("Focus on pushing knees out over toes")
        
        elif exercise_type == "pushup":
            # Check for torso sag
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                left_hip = keypoints.get("left_hip", {})
                
                if left_hip.get("y", 0) - left_shoulder.get("y", 0) > 0.15:
                    errors.append({
                        "type": "torso_sag",
                        "severity": 0.6,
                        "message": "Torso sagging - engage core and maintain straight line"
                    })
                    recommendations.append("Tighten your core and keep your body straight")
        
        elif exercise_type == "bicep_curl":
            # Check for elbow movement and swinging
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_elbow = keypoints.get("left_elbow", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                
                # Check if elbow is moving forward (swinging)
                if abs(left_elbow.get("x", 0) - left_shoulder.get("x", 0)) > 0.2:
                    errors.append({
                        "type": "elbow_swing",
                        "severity": 0.65,
                        "message": "Elbows moving forward - keep them close to your body"
                    })
                    recommendations.append("Control the weight, avoid swinging")
        
        elif exercise_type == "tricep_extension":
            # Check for upper arm movement
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_elbow = keypoints.get("left_elbow", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                
                # Upper arm should stay relatively stationary
                if abs(left_elbow.get("y", 0) - left_shoulder.get("y", 0)) < 0.05:
                    errors.append({
                        "type": "upper_arm_movement",
                        "severity": 0.6,
                        "message": "Upper arm moving - keep it stationary"
                    })
                    recommendations.append("Lock your upper arm in place")
        
        elif exercise_type == "chest_press":
            # Check for shoulder blade position
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                left_elbow = keypoints.get("left_elbow", {})
                
                # Elbows should not flare out too much
                if abs(left_elbow.get("x", 0) - left_shoulder.get("x", 0)) > 0.3:
                    errors.append({
                        "type": "elbow_flare",
                        "severity": 0.7,
                        "message": "Elbows flaring out - keep them at 45-60 degrees"
                    })
                    recommendations.append("Keep elbows closer to body")
        
        elif exercise_type == "shoulder_press":
            # Check for excessive back arch
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                left_hip = keypoints.get("left_hip", {})
                
                # Shoulders should not be too far back
                if left_shoulder.get("x", 0) < left_hip.get("x", 0) - 0.1:
                    errors.append({
                        "type": "back_arch",
                        "severity": 0.65,
                        "message": "Excessive back arch - engage core"
                    })
                    recommendations.append("Keep core tight and avoid arching")
        
        elif exercise_type == "lunge":
            # Check for knee position
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_knee = keypoints.get("left_knee", {})
                left_ankle = keypoints.get("left_ankle", {})
                
                # Knee should be over ankle
                if abs(left_knee.get("x", 0) - left_ankle.get("x", 0)) > 0.15:
                    errors.append({
                        "type": "knee_position",
                        "severity": 0.7,
                        "message": "Knee not aligned with ankle - step forward more"
                    })
                    recommendations.append("Keep front knee over ankle")
        
        elif exercise_type == "plank":
            # Check for hip position
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                left_hip = keypoints.get("left_hip", {})
                left_knee = keypoints.get("left_knee", {})
                
                # Hips should be in line with shoulders
                if left_hip.get("y", 0) > left_shoulder.get("y", 0) + 0.1:
                    errors.append({
                        "type": "hip_sag",
                        "severity": 0.7,
                        "message": "Hips sagging - engage core and glutes"
                    })
                    recommendations.append("Tighten core and squeeze glutes")
                elif left_hip.get("y", 0) < left_shoulder.get("y", 0) - 0.1:
                    errors.append({
                        "type": "hip_raised",
                        "severity": 0.6,
                        "message": "Hips too high - lower to straight line"
                    })
                    recommendations.append("Lower hips to align with shoulders")
        
        elif exercise_type == "row":
            # Check for shoulder blade retraction
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_shoulder = keypoints.get("left_shoulder", {})
                left_elbow = keypoints.get("left_elbow", {})
                
                # Elbows should pull back, not just up
                if left_elbow.get("x", 0) > left_shoulder.get("x", 0) + 0.1:
                    errors.append({
                        "type": "shoulder_retraction",
                        "severity": 0.65,
                        "message": "Not retracting shoulder blades - pull elbows back"
                    })
                    recommendations.append("Squeeze shoulder blades together")
        
        # Get top errors by severity
        top_errors = sorted(errors, key=lambda x: x.get("severity", 0), reverse=True)[:3]
        
        return {
            "errors": errors,
            "top_errors": top_errors,
            "recommendations": list(set(recommendations)),
            "exercise_type": exercise_type
        }


class CountRepsTool(BaseTool):
    """Count repetitions from keypoint sequence"""
    
    def __init__(self):
        super().__init__(
            name="count_reps",
            description="Count exercise repetitions from keypoint sequence",
            parameters={
                "keypoints_list": "List of keypoint dictionaries",
                "exercise_type": "Type of exercise"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Count reps"""
        keypoints_list = parameters.get("keypoints_list", [])
        exercise_type = parameters.get("exercise_type", "squat")
        
        # Rep counting based on exercise type
        if exercise_type == "squat":
            hip_heights = []
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_hip = keypoints.get("left_hip", {})
                hip_heights.append(left_hip.get("y", 0.5))
            
            # Count peaks (lowest points = bottom of squat)
            if len(hip_heights) > 10:
                rep_count = max(1, len(hip_heights) // 30)
            else:
                rep_count = 0
        
        elif exercise_type in ["bicep_curl", "tricep_extension", "shoulder_press"]:
            # Count based on arm movement cycles
            elbow_positions = []
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_elbow = keypoints.get("left_elbow", {})
                elbow_positions.append(left_elbow.get("y", 0.5))
            
            if len(elbow_positions) > 10:
                rep_count = max(1, len(elbow_positions) // 25)
            else:
                rep_count = 0
        
        elif exercise_type == "lunge":
            # Count based on hip movement
            hip_heights = []
            for kp in keypoints_list:
                keypoints = kp.get("keypoints", {})
                left_hip = keypoints.get("left_hip", {})
                hip_heights.append(left_hip.get("y", 0.5))
            
            if len(hip_heights) > 10:
                rep_count = max(1, len(hip_heights) // 40)
            else:
                rep_count = 0
        
        elif exercise_type == "plank":
            # Plank is time-based, not rep-based
            rep_count = 0  # Planks are held, not repeated
        
        else:
            # Generic rep counting for other exercises
            rep_count = max(1, len(keypoints_list) // 20)
        
        return {
            "rep_count": rep_count,
            "exercise_type": exercise_type,
            "frames_analyzed": len(keypoints_list)
        }


class CalculateFormScoreTool(BaseTool):
    """Calculate overall form score"""
    
    def __init__(self):
        super().__init__(
            name="calculate_form_score",
            description="Calculate overall exercise form score",
            parameters={
                "form_errors": "Dictionary of detected form errors",
                "rep_count": "Number of repetitions",
                "exercise_type": "Type of exercise"
            }
        )
    
    async def execute(
        self,
        parameters: Dict[str, Any],
        context: OrchestrationContext
    ) -> Dict[str, Any]:
        """Calculate form score"""
        form_errors = parameters.get("form_errors", {})
        rep_count = parameters.get("rep_count", 0)
        exercise_type = parameters.get("exercise_type", "squat")
        
        errors = form_errors.get("errors", [])
        
        # Calculate score based on errors
        base_score = 100.0
        for error in errors:
            severity = error.get("severity", 0.5)
            base_score -= severity * 10
        
        overall_score = max(0, min(100, base_score))
        
        # Grade
        if overall_score >= 90:
            grade = "Excellent"
        elif overall_score >= 75:
            grade = "Good"
        elif overall_score >= 60:
            grade = "Fair"
        else:
            grade = "Needs Improvement"
        
        return {
            "overall_score": round(overall_score, 1),
            "grade": grade,
            "error_count": len(errors),
            "rep_count": rep_count,
            "exercise_type": exercise_type
        }

