
import pandas as pd

# Create comprehensive blueprint data structure
blueprint_data = {
    'Phase': [
        'Phase 1: Environment Setup & Tool Configuration',
        'Phase 1: Environment Setup & Tool Configuration',
        'Phase 1: Environment Setup & Tool Configuration',
        'Phase 1: Environment Setup & Tool Configuration',
        'Phase 1: Environment Setup & Tool Configuration',
        
        'Phase 2: Terrain & World Generation',
        'Phase 2: Terrain & World Generation',
        'Phase 2: Terrain & World Generation',
        'Phase 2: Terrain & World Generation',
        'Phase 2: Terrain & World Generation',
        
        'Phase 3: City Layout & Asset Placement',
        'Phase 3: City Layout & Asset Placement',
        'Phase 3: City Layout & Asset Placement',
        'Phase 3: City Layout & Asset Placement',
        'Phase 3: City Layout & Asset Placement',
        
        'Phase 4: NPC Framework & Emergent AI',
        'Phase 4: NPC Framework & Emergent AI',
        'Phase 4: NPC Framework & Emergent AI',
        'Phase 4: NPC Framework & Emergent AI',
        'Phase 4: NPC Framework & Emergent AI',
        
        'Phase 5: Polish, Testing & Debug',
        'Phase 5: Polish, Testing & Debug',
        'Phase 5: Polish, Testing & Debug',
        'Phase 5: Polish, Testing & Debug',
        'Phase 5: Polish, Testing & Debug'
    ],
    
    'Task': [
        # Phase 1
        'Install and configure Claude Code CLI',
        'Set up game engine (Unreal 5 / Unity / Godot)',
        'Install procedural city generation plugins',
        'Create CLAUDE.md project configuration',
        'Set up version control and project structure',
        
        # Phase 2
        'Generate terrain using procedural tools',
        'Configure landscape parameters and biomes',
        'Implement terrain LOD system',
        'Add environmental features (water, vegetation)',
        'Optimize terrain rendering with Nanite/instancing',
        
        # Phase 3
        'Generate road network and city layout',
        'Place buildings using procedural rules',
        'Add city props and parking systems',
        'Implement Zone Graph for pathfinding',
        'Optimize city rendering with instancing',
        
        # Phase 4
        'Set up AI controller and blackboard system',
        'Create behavior tree structure',
        'Implement NPC decision-making nodes',
        'Add dialogue and interaction systems',
        'Configure emergent AI parameters',
        
        # Phase 5
        'Profile performance bottlenecks',
        'Debug AI behavior issues',
        'Optimize draw calls and batching',
        'Test core gameplay mechanics',
        'Final integration and documentation'
    ],
    
    'Time_Hours': [
        # Phase 1
        0.5, 0.5, 0.5, 0.5, 0.5,
        
        # Phase 2
        0.75, 0.5, 0.5, 0.75, 0.5,
        
        # Phase 3
        1.0, 1.5, 0.75, 0.5, 0.25,
        
        # Phase 4
        1.0, 1.5, 1.5, 1.5, 0.5,
        
        # Phase 5
        1.0, 1.0, 1.0, 1.5, 0.5
    ],
    
    'Tools_Required': [
        # Phase 1
        'Claude Code CLI, npm/node.js, API keys',
        'Unreal Engine 5 / Unity 2023+ / Godot 4.x',
        'City Builder DL, iPCC, or procedural plugins',
        'Text editor, Claude slash commands',
        'Git, GitHub/GitLab, project templates',
        
        # Phase 2
        'UE5 Landmass/PCG, Unity Terrain Tools',
        'Perlin noise libraries, heightmap generators',
        'LOD Group components, distance culling',
        'Foliage tools, water shaders, SpeedTree',
        'Nanite (UE5), GPU instancing, occlusion culling',
        
        # Phase 3
        'City Builder DL, iPCC, Road tools',
        'Grammar-based building generators, Kitbash assets',
        'Prop spawning systems, parking generators',
        'Zone Graph (UE5), NavMesh (Unity)',
        'Static batching, texture atlases, HLOD',
        
        # Phase 4
        'AI Controller blueprint/script, Blackboard',
        'Behavior Tree editor, custom task nodes',
        'Decision tree logic, utility AI systems',
        'Dialogue System, interaction triggers',
        'Behavior Designer, state machines',
        
        # Phase 5
        'Unity Profiler / UE5 Insights',
        'Claude Code debugging tools, breakpoints',
        'Frame Debugger, GPU profiling tools',
        'Playtesting framework, QA checklists',
        'Documentation tools, README generators'
    ],
    
    'Claude_Prompts': [
        # Phase 1
        '"Set up Claude Code for Unreal/Unity game dev with PCG support"',
        '"Create new [Engine] project for open-world city simulation"',
        '"Install and configure [plugin name] for procedural city generation"',
        '"Generate CLAUDE.md with project structure and common commands"',
        '"Initialize Git repo with .gitignore for [Engine], create dev branches"',
        
        # Phase 2
        '"Generate terrain landscape with perlin noise, 5km x 5km size"',
        '"Configure landscape layers: urban, suburban, parks with transitions"',
        '"Implement LOD system for terrain with 4 detail levels"',
        '"Add procedural rivers, lakes, and vegetation using foliage tool"',
        '"Optimize terrain with Nanite and implement frustum culling"',
        
        # Phase 3
        '"Create road network with main streets, intersections, sidewalks"',
        '"Generate buildings procedurally: residential, commercial, industrial zones"',
        '"Add street props: traffic lights, benches, trash cans, parking lots"',
        '"Set up Zone Graph/NavMesh for NPC pedestrian pathfinding"',
        '"Optimize city rendering: batch static meshes, use texture atlases"',
        
        # Phase 4
        '"Create AI controller with blackboard for NPC memory/state"',
        '"Build behavior tree: patrol, interact, respond to player, idle states"',
        '"Implement decision nodes for emergent behavior based on context"',
        '"Add dialogue system with dynamic responses and conversation trees"',
        '"Configure AI parameters: perception radius, reaction time, memory decay"',
        
        # Phase 5
        '"Profile the game and identify CPU/GPU bottlenecks"',
        '"Debug NPC behavior: fix stuck agents, improve pathfinding"',
        '"Reduce draw calls from [X] to under 500 using batching"',
        '"Test and fix: NPC interactions, terrain collisions, performance drops"',
        '"Generate documentation: setup guide, architecture overview, API reference"'
    ],
    
    'Key_Outputs': [
        # Phase 1
        'Working dev environment, API authentication',
        'Empty project with base scene/level',
        'Plugin installed and verified functional',
        'Project context file for AI assistant',
        'Version-controlled project structure',
        
        # Phase 2
        'Playable terrain with varied elevation',
        'Distinct zones: urban center, suburbs, nature',
        'Smooth performance at distance',
        'Realistic environmental features',
        '60+ FPS terrain rendering',
        
        # Phase 3
        'Navigable road network',
        'Populated city blocks with buildings',
        'Detailed urban environment',
        'NPC pathfinding infrastructure',
        'Optimized city rendering',
        
        # Phase 4
        'Autonomous NPC agents',
        'Context-aware AI behaviors',
        'Emergent interactions between NPCs',
        'Player-NPC communication system',
        'Self-learning AI simulation',
        
        # Phase 5
        'Performance metrics report',
        'Bug-free AI behavior',
        'Stable 60 FPS performance',
        'Validated gameplay experience',
        'Complete project documentation'
    ]
}

# Create DataFrame
blueprint_df = pd.DataFrame(blueprint_data)

# Calculate phase totals
phase_summary = blueprint_df.groupby('Phase')['Time_Hours'].sum().reset_index()
phase_summary.columns = ['Phase', 'Total_Hours']

# Save to CSV
blueprint_df.to_csv('blueprint_detailed.csv', index=False)
phase_summary.to_csv('blueprint_phase_summary.csv', index=False)

print("Blueprint Structure:")
print("=" * 80)
print(f"\nTotal Development Time: {blueprint_df['Time_Hours'].sum()} hours")
print(f"\nPhase Breakdown:")
print(phase_summary.to_string(index=False))
print("\n" + "=" * 80)
print("\nDetailed Task List:")
print(blueprint_df[['Phase', 'Task', 'Time_Hours']].to_string(index=False))
