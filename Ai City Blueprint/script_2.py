
# Create workflow and best practices guide

workflow_guide = """
# DEVELOPMENT WORKFLOW & BEST PRACTICES

## Daily Development Workflow (10-Hour Sprint Example)

### Hour 1-2: Setup & Environment (Phase 1)
**Morning Session - Foundation Building**
1. Start Claude Code in project directory: `claude`
2. Review CLAUDE.md for project context
3. Use slash command: `/init` to refresh AI context
4. Set daily goals: "Today we'll implement terrain generation"
5. Create feature branch: `git checkout -b feature/terrain-gen`

**Claude Prompts:**
- "Review project structure and suggest today's workflow"
- "What dependencies do we need for terrain generation?"
- "Set up empty scene with camera controller"

### Hour 3-5: Core Implementation (Phases 2-3)
**Mid-Morning to Lunch - Heavy Lifting**
1. Generate terrain with AI assistance
2. Iterate rapidly: generate → test → refine
3. Use Claude's autocomplete for boilerplate
4. Profile early: check frame rate after each major addition

**Claude Prompts:**
- "Generate terrain landscape with perlin noise, add 3 biome types"
- "Create road network connecting 4 city zones"
- "Add 500 procedurally placed buildings with LOD"
- "Fix terrain collision issues and optimize mesh density"

**Pro Tips:**
- Save after each working feature (git commit frequently)
- Use Claude's `/test` command to generate unit tests
- Profile every 30 minutes to catch performance issues early

### Hour 6-8: AI & Behavior (Phase 4)
**Afternoon Session - Intelligence Layer**
1. Implement NPC framework and behavior trees
2. Test AI decision-making in isolated environment
3. Integrate NPCs into city scene
4. Add basic interactions and dialogue

**Claude Prompts:**
- "Create AI controller with patrol, interact, and idle behaviors"
- "Implement behavior tree for NPC shopkeeper with daily routine"
- "Add simple dialogue system with 3 response options"
- "Configure NPC to react to player proximity and time of day"

**Debugging Strategy:**
- Use behavior tree visualization tools
- Add debug logs for AI decision points
- Test one NPC type at a time before spawning multiples

### Hour 9-10: Polish & Documentation (Phase 5)
**Late Afternoon - Quality Assurance**
1. Run profiler and optimize bottlenecks
2. Fix critical bugs found during testing
3. Document new features in CLAUDE.md
4. Prepare build for next session or demo

**Claude Prompts:**
- "Analyze profiler output and suggest 5 optimization targets"
- "Debug why NPCs are stuck at intersection X,Y coordinates"
- "Generate documentation for today's implemented features"
- "Create summary of remaining tasks for tomorrow"

## Claude Code Best Practices

### 1. Context Management
- **Always maintain CLAUDE.md** with current project state
- Update after major features: `# update CLAUDE.md with new terrain system`
- Include common errors and solutions you've encountered
- Document engine-specific quirks (e.g., "UE5 requires Nanite enabled for city meshes")

### 2. Effective Prompting Strategies
**Bad Prompt:**
"Make the city look better"

**Good Prompt:**
"Optimize city rendering: reduce draw calls by batching static meshes, enable GPU instancing for trees, and implement HLOD for buildings beyond 1km distance"

**Great Prompt:**
"Profile current city scene and create optimization plan. Current stats: 2,500 draw calls, 45 FPS. Target: <500 draw calls, 60 FPS. Focus on: (1) mesh batching, (2) texture atlases, (3) occlusion culling. Then implement top 3 fixes."

### 3. Iterative Development with AI
```
Cycle: Prompt → Generate → Test → Refine → Repeat

Example iteration:
1. "Create basic NPC patrol behavior" → Test → Works but choppy
2. "Smooth NPC movement with acceleration/deceleration" → Test → Better
3. "Add obstacle avoidance to NPC movement" → Test → Perfect
4. Commit and move to next feature
```

### 4. Version Control Integration
- Commit before major AI-generated code: `git commit -m "Pre-AI: terrain baseline"`
- Commit after testing AI changes: `git commit -m "AI-Gen: added terrain LOD system"`
- Use branches for experimental AI features
- Claude can generate commit messages: "Generate git commit message for these changes"

### 5. Error Handling & Debugging
When Claude generates code with errors:
1. Copy full error message to Claude: "Fix this error: [paste error]"
2. Include relevant code context (Claude reads your files automatically)
3. Ask for explanation: "Why did this error occur?"
4. Request prevention: "Add checks to prevent this error in future"

## Performance Optimization Workflow

### Stage 1: Profile (Always First!)
```
1. Run game profiler (Unity Profiler / UE5 Insights)
2. Identify top 5 performance bottlenecks
3. Take screenshots of profiler data
4. Share with Claude: "Analyze this profiler output and prioritize fixes"
```

### Stage 2: AI-Assisted Optimization
```
Claude Prompt Template:
"Optimize [system_name]. Current performance: [metrics]. Target: [goal].
Constraints: [visual_quality/memory/etc]. Suggest code changes with priority ranking."
```

### Stage 3: Validate Improvements
```
1. Implement Claude's suggestions one at a time
2. Profile after each change
3. Commit successful optimizations
4. Rollback if performance degrades
```

## Common Pitfalls & Solutions

### Pitfall 1: Over-relying on AI Without Understanding
**Problem:** Accepting all AI-generated code without review
**Solution:** 
- Ask Claude to explain: "Explain this code section line by line"
- Request comments: "Add detailed comments to this function"
- Understand trade-offs: "What are pros/cons of this approach?"

### Pitfall 2: Poor Context in CLAUDE.md
**Problem:** AI generates incompatible code due to missing context
**Solution:**
```markdown
# CLAUDE.md Example

## Project Architecture
- Engine: Unreal Engine 5.4
- Rendering: Nanite + Lumen enabled
- Target Platform: PC (Windows/Linux)
- Code Style: Follow Epic C++ guidelines

## Known Issues
- City plugin requires manual NavMesh rebuild after generation
- Mass AI entities need <100ms update budget or game stutters
- Terrain water shaders crash in editor preview mode (runtime only)

## Common Commands
- Build: Ctrl+Alt+F11
- Package: File > Package Project > Windows
- Profile: Ctrl+Shift+,
```

### Pitfall 3: Not Testing Incrementally
**Problem:** Generating entire systems at once, hard to debug
**Solution:**
- Build in layers: terrain → roads → buildings → NPCs
- Test each layer before proceeding
- Use Claude for incremental tasks: "Add just the building placement, not the interiors yet"

## Time-Saving Claude Workflows

### Auto-Documentation
```
Prompt: "Generate README.md documenting: project setup, controls, 
systems overview, known bugs, and how to build"
```

### Batch Code Generation
```
Prompt: "Create 5 NPC behavior variants: shopkeeper, guard, civilian, 
vendor, child. Each with unique behavior tree and movement patterns."
```

### Automated Testing
```
Prompt: "Generate unit tests for NPC pathfinding system with 10 test cases 
covering: straight paths, obstacles, multiple NPCs, edge cases"
```

### Refactoring Assistance
```
Prompt: "Refactor NPCController.cpp to use ECS pattern instead of 
inheritance. Maintain all current functionality."
```

## Recommended Daily Schedule (10-Hour Dev Day)

| Time | Activity | Focus |
|------|----------|-------|
| 08:00-09:00 | Setup & Planning | Review goals, update CLAUDE.md |
| 09:00-11:00 | Core Development | Primary feature implementation |
| 11:00-11:15 | Break + Profile | Check performance, commit progress |
| 11:15-13:00 | Feature Expansion | Secondary systems, integration |
| 13:00-14:00 | Lunch | Step away from computer |
| 14:00-16:00 | AI & Behavior | NPC logic, interactions |
| 16:00-16:15 | Break + Test | Playtest, identify bugs |
| 16:15-17:30 | Bug Fixes | Address critical issues |
| 17:30-18:00 | Documentation | Update docs, prepare for next day |

## Success Metrics

Track these daily to measure progress:
- **Features completed** vs. planned (aim for 80%+ completion)
- **Lines of code written** (with AI: 500-2000/day is realistic)
- **Performance targets met** (FPS, memory, draw calls)
- **Bugs introduced** vs. fixed (should trend toward fixed)
- **Time saved** compared to manual coding (track with time logs)

## Emergency Troubleshooting

When stuck for >30 minutes:
1. **Explain the problem to Claude in detail**
2. **Share error logs, screenshots, code snippets**
3. **Ask for multiple solution approaches**
4. **Try solutions in order of risk (safest first)**
5. **If still stuck: take a break, come back fresh**
6. **Last resort: revert to last working commit and try different approach**

## Collaboration with AI: The 70/30 Rule

**70% AI-Generated:**
- Boilerplate code
- Standard implementations
- Repetitive tasks
- Documentation
- Test cases

**30% Human-Designed:**
- Creative gameplay decisions
- Architecture choices
- Art direction
- User experience refinement
- Final quality polish
"""

# Save workflow guide
with open('workflow_best_practices.txt', 'w', encoding='utf-8') as f:
    f.write(workflow_guide)

print("Workflow & Best Practices Guide saved successfully!")
print("\n" + "=" * 80)
print(workflow_guide[:1500] + "\n\n[... document continues ...]")
