# Keyboard Input Troubleshooting Guide

## Issue: QEWASD keys not responding in Spectator Mode

### Root Cause
The keyboard input system has been upgraded to **POLLING-BASED** input for maximum reliability. Mouse panning confirmed to work, so the window can receive input focus properly.

### Previous Issue
Event-driven keyboard input (`accept()` system) was not capturing key presses reliably, even when the window had focus (proven by working mouse input).

### Current Solution
Switched to **polling-based keyboard detection** using `mouseWatcherNode.is_button_down()` which checks keyboard state every frame - the same method that makes mouse input work reliably.

---

## ✅ SOLUTION: Use the PowerShell Launcher

### Method 1: PowerShell Script (Recommended)
```powershell
cd "C:\Users\akidw\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\AI City Experiment"
powershell -ExecutionPolicy Bypass -File .launch_ultra_realistic.ps1
```

**This script automatically:**
- Kills any existing instances
- Launches the simulation
- Attempts to focus the Panda3D window
- Shows clear instructions

### Method 2: Direct Python Launch
```bash
cd "C:\Users\akidw\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\AI City Experiment"
python world_ultra_realistic.py
```

**After launch:**
1. Wait for the window to appear (blue sky with buildings)
2. **CLICK ON THE 3D WINDOW** to give it focus
3. Now try WASD/Space/Shift/Q/E controls

---

## 🔍 Debugging Features Added

### Input Debugging (POLLING-BASED)
When you press keys, you should see in the console:
```
[INPUT DEBUG] W key detected (POLLING)
[INPUT DEBUG] A key detected (POLLING)
[INPUT DEBUG] SPACE key detected (POLLING)
```
**Note:** Each key logs once when first pressed, then stops until released and pressed again.

### Zoom Controls Debugging
When you zoom, you'll see:
```
[INPUT DEBUG] Zoom IN (Ctrl + '+' or Mouse Wheel Up)
[ZOOM] New position: (10.5, -45.2, 35.0)
[INPUT DEBUG] Zoom OUT (Ctrl + '-' or Mouse Wheel Down)
[ZOOM] New position: (0.5, -55.2, 25.0)
```

### Camera Movement Debugging
When the camera moves, you'll see:
```
[CAMERA DEBUG] Spectator pos: (10.5, -45.2, 35.0), heading: 45°
```

### AI Agent Statistics (Every 5 seconds)
```
[AI DEBUG] Agent Statistics:
  Total Agents: 10
  State Distribution: {'walking': 6, 'wandering': 2, 'stopped': 2}
  Average Speed: 1.73
  Agent 0: pos=(25.7, 24.5), state=walking, heading=-139°
```

---

## 📋 Controls Reference

### Spectator Mode (Default)
- **WASD**: Move forward/back/left/right
- **Space**: Move up
- **Shift**: Move down
- **Q**: Rotate left
- **E**: Rotate right
- **Ctrl + Plus (+)**: Zoom in (move forward faster)
- **Ctrl + Minus (-)**: Zoom out (move backward faster)
- **Mouse Wheel Up**: Zoom in
- **Mouse Wheel Down**: Zoom out
- **F1**: Cycle camera modes

### Third-Person Mode
- **WASD**: Move character
- **Q/E**: Rotate camera around character
- **F1**: Switch to First-Person mode

### First-Person Mode
- **WASD**: Move character
- **Q/E**: Rotate view
- **F1**: Switch to Spectator mode

---

## ✨ What's Working Now

### ✅ Advanced AI System
- **10 AI agents** with sophisticated behaviors
- **5 behavioral states**:
  - Walking: Moving towards destination (building)
  - Wandering: Random exploration
  - Stopped: Brief pause
  - Waiting: Long duration wait
  - Following Road: Navigating along roads

### ✅ AI Features
- Destination-based pathfinding
- Collision avoidance (personal space)
- Road network navigation
- Personality traits (speed, sociability, patience)
- Dynamic state transitions

### ✅ Performance Optimized
- 50-60 FPS on AMD Radeon 780M
- Simplified geometry for integrated GPU
- No post-processing effects (performance mode)
- Efficient AI updates (every 5 frames)

### ✅ Auto-Cleanup
- Application kills old instances on startup
- Only one instance runs at a time
- No more hanging processes

---

## 🎯 Expected Behavior

### When Working Correctly:
1. Window opens showing blue sky
2. 12 buildings visible (colored by zone type)
3. 20 dark gray roads on ground
4. 8 colored vehicles on roads
5. 10 AI agents (colored rectangles) moving around
6. FPS counter in top-right
7. "MODE: SPECTATOR" text in top-left
8. Controls respond when window has focus

### If Controls Don't Respond:
1. Click on the 3D window
2. Check console for `[INPUT DEBUG]` messages when pressing keys
3. If no debug messages appear = window doesn't have focus
4. Try Alt+Tab to the Panda3D window
5. If still no response, restart using PowerShell launcher

---

## 📊 Visual Reference

### What You Should See:
```
Sky: Light blue (0.53, 0.81, 0.92)
Buildings: 12 boxes with colors:
  - Blue-gray (commercial)
  - Tan (commercial)
  - Warm beige (residential)
  - Gray (industrial)

Roads: 20 dark gray paths
Vehicles: 8 colored rectangles (red, blue, green, yellow, etc.)
AI Agents: 10 tall thin rectangles (blue, red, green, yellow, purple shirts)

Camera: Starting at (0, -50, 30) looking down slightly
```

---

## 🚀 Quick Start Steps

1. **Close any running instances**
2. **Run PowerShell launcher**:
   ```powershell
   powershell -ExecutionPolicy Bypass -File .launch_ultra_realistic.ps1
   ```
3. **Wait for window to appear** (2-3 seconds)
4. **Click on the 3D window**
5. **Press W** - you should see:
   - Console: `[INPUT DEBUG] Key pressed: W`
   - Console: `[CAMERA DEBUG] Spectator pos: ...`
   - Camera moves forward in the window
6. **Fly around with WASD + Space/Shift + Q/E**
7. **Watch AI agents move autonomously**

---

## 💡 Tips

- **Performance**: If FPS drops below 30, reduce world size or AI agent count
- **Visibility**: AI agents are 1.8 units tall, visible from far away
- **Navigation**: Start high up (Z=30) for best overview
- **AI Behaviors**: Watch agents for 30+ seconds to see state changes
- **Mode Switching**: Press F1 to try different camera perspectives

---

## 🔧 If Issues Persist

1. Check Python process:
   ```bash
   tasklist | findstr python
   ```

2. Kill all Python processes:
   ```powershell
   Get-Process python* | Stop-Process -Force
   ```

3. Check psutil is installed:
   ```bash
   pip install psutil
   ```

4. Verify window focus by checking for input debug messages

---

## 📝 Development Notes

### Files Modified
- `world_ultra_realistic.py`: Main simulation with AI agents
- `ai_agent_system.py`: Advanced AI behavioral system
- `.launch_ultra_realistic.ps1`: PowerShell launcher script

### Key Improvements (Latest Version)
- **Polling-based keyboard input** (`mouseWatcherNode.is_button_down()`) - more reliable than event-driven
- **Zoom controls** (Ctrl+Plus/Minus, Mouse Wheel) for faster navigation
- **One-time key logging** to prevent console spam
- Input debugging for troubleshooting
- Camera position logging
- Auto-cleanup of old processes
- Window focus management
- Detailed AI statistics

### Technical Details
**Input System:**
- Previous: Event-driven using `self.accept('key', callback)` with key_map dictionary
- Current: Polling-based using `self.mouseWatcherNode.is_button_down(KeyboardButton.ascii_key('w'))`
- Reason for change: Mouse polling works reliably, so keyboard polling should too
- Debug logging: Each key logs once when pressed, stops until released

---

**Last Updated**: 2025-10-20
**Version**: Advanced AI Social Experiment v1.1 (Polling-Based Input)
