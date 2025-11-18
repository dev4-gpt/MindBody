# Changelog - Version 1.1

## New Features

### Exercise Support
- ✅ Added 7 new exercises:
  - Bicep Curl
  - Tricep Extension
  - Chest Press
  - Shoulder Press
  - Lunge
  - Plank
  - Row
- ✅ Total of 10 exercises now supported

### Video Support
- ✅ Added video upload option (MP4, MOV, AVI)
- ✅ Video frame extraction using OpenCV
- ✅ Multi-frame analysis for better rep counting
- ✅ Video playback after analysis

### UI Improvements
- ✅ Fixed Streamlit image display issue
- ✅ Added input mode selection (Photo vs Video)
- ✅ Enhanced exercise tips for all exercises
- ✅ Better video processing feedback

## Bug Fixes

- ✅ Fixed `use_container_width` parameter error in Streamlit
- ✅ Fixed video file pointer reset issue
- ✅ Improved error handling for video processing

## Backend Updates

### Pose Tools
- ✅ Added form detection for all new exercises
- ✅ Exercise-specific rep counting algorithms
- ✅ Enhanced form error detection
- ✅ Exercise-specific recommendations

### Form Detection Rules
- **Bicep Curl**: Elbow swing detection
- **Tricep Extension**: Upper arm movement detection
- **Chest Press**: Elbow flare detection
- **Shoulder Press**: Back arch detection
- **Lunge**: Knee position alignment
- **Plank**: Hip sag/raise detection
- **Row**: Shoulder blade retraction detection

## Technical Details

### Video Processing
- Extracts up to 30 frames from uploaded video
- Processes frames sequentially for analysis
- Provides comprehensive feedback on entire exercise set

### Rep Counting
- Exercise-specific algorithms:
  - Squat: Hip height analysis
  - Arm exercises: Elbow position cycles
  - Lunge: Hip movement patterns
  - Plank: Time-based (no reps)

## Next Steps

- [ ] Real-time video streaming (WebSocket)
- [ ] Live pose overlay on video
- [ ] Frame-by-frame feedback
- [ ] Export analysis report
- [ ] Comparison with previous sessions

