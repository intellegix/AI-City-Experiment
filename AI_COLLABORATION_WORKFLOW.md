# Multi-AI Collaboration Workflow
**AI City Experiment - Coordinated Development**

## Purpose
This document coordinates work between Claude Code (primary) and Gemini CLI (secondary) for UI/UX improvements and visual enhancements to the Panda3D AI city simulation.

---

## Current Status (2025-10-20)

### ✅ Completed (Claude Code)
1. **Keyboard input fixed** - Event-driven system working perfectly
2. **Zoom controls added** - Ctrl+Plus/Minus and mouse wheel
3. **Camera planes adjusted** - Near=0.1, Far=10,000 (prevents clipping)
4. **Mouse cursor hidden** - Immersive spectator mode
5. **AI agent system** - 10 autonomous agents with sophisticated behaviors

### 🔄 In Progress
- UI/UX visual improvements (z-fighting, graphics quality)
- Testing latest camera fixes

### 📝 Pending Tasks
1. Address remaining z-fighting between geometry layers
2. Improve visual quality without sacrificing performance
3. Add textures and materials to buildings/roads
4. Enhance lighting system for better atmosphere
5. Optional: Implement basic post-processing effects (performance-conscious)

---

## AI Collaboration Roles

### **Claude Code (Primary AI)**
- **Focus**: Code structure, debugging, system architecture
- **Strengths**: File operations, code editing, git operations
- **Current Tasks**:
  - Monitor and fix keyboard/camera input issues
  - Maintain AI agent system
  - Performance optimization for AMD Radeon 780M

### **Gemini CLI (Secondary AI)**
- **Focus**: UI/UX design suggestions, visual improvements, research
- **Strengths**: Creative solutions, alternative approaches, web research
- **Proposed Tasks**:
  - Research optimal z-fighting solutions for Panda3D
  - Suggest visual enhancement strategies
  - Provide material/texture recommendations
  - Review code for visual improvements

### **Claude Code (Coordinator Instance)**
- **Focus**: Managing communication between AIs
- **Responsibilities**:
  - Route questions from Claude (primary) to Gemini
  - Synthesize Gemini responses into actionable code changes
  - Track progress across both AI workstreams
  - Maintain this coordination document

---

## Communication Protocol

### **Format for Gemini Queries**
```
[GEMINI QUERY]
**Context**: <Brief description of current problem>
**Question**: <Specific question for Gemini>
**Expected Output**: <What type of response you need>
**Files to Review**: <List of relevant files if any>
```

### **Format for Gemini Responses**
```
[GEMINI RESPONSE]
**Query ID**: <Reference to original query>
**Recommendations**: <List of suggestions>
**Code Examples**: <If applicable>
**Resources**: <Links or references>
```

### **Integration Workflow**
1. Claude (Primary) identifies problem/question
2. Coordinator formats query for Gemini
3. User runs: `npx @google/gemini-cli` with formatted query
4. User pastes Gemini response
5. Claude (Primary) implements solution based on Gemini advice
6. Test and iterate

---

## Current Priority Queue

### **High Priority** (Immediate - Next Session)
1. **Z-Fighting Fix**
   - Problem: Geometry flickering at same depth (roads/ground/objects)
   - Current depths: Ground=0, Roads=0.01, Vehicles=0.75, Agents=0.9
   - Needs: Better depth separation strategy
   - **Gemini Task**: Research Panda3D best practices for depth layering

2. **Visual Quality Improvements**
   - Problem: Flat-shaded, untextured placeholder graphics
   - Current: Performance mode (no post-processing)
   - Needs: Balance between visual quality and 60 FPS target
   - **Gemini Task**: Suggest lightweight material/texture strategies

### **Medium Priority** (This Week)
3. **Lighting Enhancement**
   - Current: Simple directional light (performance mode)
   - Needs: Better atmosphere without heavy post-processing
   - **Gemini Task**: Recommend lighting setups for city scenes

4. **Material System**
   - Current: Flat colors only
   - Needs: Simple materials for buildings/roads/vehicles
   - **Gemini Task**: Panda3D material examples for urban environments

### **Low Priority** (Future)
5. **Optional Post-Processing**
   - Current: All post-processing disabled
   - Consideration: Enable bloom and color grading if performance allows
   - **Gemini Task**: Identify lowest-cost post-processing effects

---

## File Reference

### **Core Files**
- `world_ultra_realistic.py` - Main simulation (1000+ lines)
- `ai_agent_system.py` - AI agent behaviors
- `post_processing.py` - Visual effects system (currently disabled)
- `KEYBOARD_INPUT_TROUBLESHOOTING.md` - Debugging guide

### **Configuration**
- `.launch_ultra_realistic.ps1` - PowerShell launcher
- Performance target: 50-60 FPS on AMD Radeon 780M

---

## Gemini CLI Usage Notes

### **Running Gemini CLI**
```bash
npx @google/gemini-cli
```

### **Example Query Format**
```
I'm working on a Panda3D city simulation with z-fighting issues.

Current setup:
- Ground plane at z=0
- Roads at z=0.01
- Vehicles at z=0.75
- AI agents at z=0.9

The ground and roads are flickering (z-fighting). What's the best practice for depth separation in Panda3D to avoid this issue? Should I increase the z-offset between layers, or use a different approach?

Performance context: AMD Radeon 780M integrated GPU, targeting 60 FPS.
```

---

## Progress Tracking

### Session Log

**2025-10-20 Session 1**
- Fixed keyboard input (polling → event-driven)
- Added zoom controls (Ctrl+Plus/Minus, mouse wheel)
- Adjusted camera planes (near=0.1, far=10000)
- Hidden mouse cursor for immersive mode
- Status: Application running, keyboard controls working
- Next: Address z-fighting and visual quality

---

## Notes for Coordinator Claude Instance

### **Workflow Steps**
1. Monitor this file for updates from Primary Claude
2. Review priority queue for Gemini-suitable tasks
3. Format queries using protocol above
4. Wait for user to paste Gemini responses
5. Parse Gemini advice and create actionable tasks for Primary Claude
6. Update progress tracking section
7. Maintain clear separation of concerns between AIs

### **Key Considerations**
- Keep queries specific and actionable
- Include relevant context (performance constraints, hardware)
- Request code examples when applicable
- Track which AI handled which task
- Avoid duplicate work between AIs

---

**Last Updated**: 2025-10-20
**Maintained By**: Claude Code (Coordinator Instance)
