# AI City Simulation

A sophisticated procedural city simulation featuring emergent AI NPCs, built from the comprehensive game development blueprint. This project demonstrates modern AI science and gaming programming techniques including procedural generation, behavior trees, pathfinding, and utility AI.

## Features

### Phase 2: Terrain & World Generation
- **Multi-octave Perlin noise** terrain generation
- **5 distinct biomes**: Water, Sand, Grass, Forest, Mountain
- **Moisture mapping** for diverse terrain
- **Erosion simulation** for realistic landscapes
- **Island effect** generation for natural boundaries

### Phase 3: City Layout & Asset Placement
- **Hybrid road network** (radial + grid pattern)
- **Zone-based city planning**: Commercial, Residential, Industrial, Parks, Mixed
- **Procedural building placement** with grammar-based rules
- **NetworkX graph** for efficient pathfinding
- **Terrain-aware layout** avoiding water and steep slopes

### Phase 4: NPC Framework & Emergent AI
- **Behavior tree system** for decision-making
- **Utility AI** for action selection
- **Memory system** with event storage and decay
- **Need-based motivation**: Hunger, Energy, Social, Safety
- **A* pathfinding** with path smoothing
- **Perception system** for environmental awareness
- **5 NPC types**: Civilian, Shopkeeper, Guard, Vendor, Child

### Phase 5: Rendering & Optimization
- **Level of Detail (LOD)** system with 4 detail levels
- **Frustum culling** for off-screen objects
- **Multi-layer rendering**: Terrain → Roads → Buildings → NPCs
- **Camera system** with smooth movement and zoom
- **Xbox Controller Support** via Bluetooth or USB (full analog control!)
- **Performance monitoring**: FPS counter, draw call tracking
- **Target: 60 FPS** with 100-500 NPCs

## Installation

### Requirements
- Python 3.8+
- 8GB+ RAM recommended
- GPU with 2GB+ VRAM recommended (for larger simulations)

### Setup

1. **Clone or download this project**

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Dependencies
- `numpy` - Numerical computing
- `pygame` - Rendering and game loop
- `noise` - Perlin noise generation
- `networkx` - Graph-based pathfinding
- `scipy` - Scientific computing

## Usage

### Basic Usage

Run with default settings (512x512 grid, 100 NPCs):
```bash
python main.py
```

### Command Line Options

```bash
python main.py --help
```

**Available options:**
- `--seed SEED` - Random seed for reproducible worlds (default: random)
- `--npcs COUNT` - Number of NPCs to spawn (default: 100, max: 500)
- `--size SIZE` - World grid size: 256, 512, or 1024 (default: 512)

### Examples

Generate a specific world:
```bash
python main.py --seed 42
```

Create a crowded city:
```bash
python main.py --npcs 300 --seed 12345
```

Large world (requires powerful hardware):
```bash
python main.py --size 1024 --npcs 500
```

Small, fast simulation:
```bash
python main.py --size 256 --npcs 50
```

## Controls

### Keyboard & Mouse
**Camera:**
- **W/A/S/D** - Move camera up/left/down/right
- **Q/E** - Zoom in/out
- **Mouse Wheel** - Zoom in/out

**Simulation:**
- **Space** - Pause/Resume simulation
- **D** - Toggle debug information
- **ESC** - Quit simulation

### Xbox Controller (Bluetooth/USB)
**Camera:**
- **Left Stick** - Move camera (analog)
- **Right Stick (Vertical)** - Zoom in/out
- **D-Pad** - Move camera (discrete)
- **LB/RB Bumpers** - Zoom out/in
- **LT/RT Triggers** - Gradual zoom

**Simulation:**
- **Start Button** - Pause/Resume
- **Y Button** - Toggle debug info

**See [CONTROLLER_GUIDE.md](CONTROLLER_GUIDE.md) for full controller setup and troubleshooting!**

## Architecture

### Project Structure

```
AI City Experiment/
├── main.py                  # Main application entry point
├── config.py                # Configuration and constants
├── terrain_generator.py     # Procedural terrain generation
├── city_generator.py        # City layout and road networks
├── ai_behavior.py           # Behavior tree system
├── pathfinding.py           # A* pathfinding algorithm
├── npc_system.py           # NPC agents with emergent AI
├── renderer.py              # Pygame rendering with LOD
├── graphics_enhanced.py     # Realistic graphics & shaders
├── controller_input.py      # Xbox controller support
├── requirements.txt         # Python dependencies
├── README.md               # This file
├── QUICKSTART.md           # Quick start guide
├── CONTROLLER_GUIDE.md     # Controller setup guide
├── GRAPHICS_FEATURES.md    # Graphics documentation
├── LICENSING.md            # Licensing guide
├── NOTICE                  # Attribution requirements
└── LICENSE/                # License files
    ├── LICENSE.md          # Apache 2.0 full text
    ├── NOTICE-updated.md   # Intellegix notice
    └── TRADEMARK-POLICY-updated.md  # Trademark policy
```

### Core Systems

#### 1. Terrain Generation (`terrain_generator.py`)
- Multi-octave Perlin noise for realistic terrain
- Biome classification based on elevation and moisture
- Hydraulic erosion simulation
- Island effect for natural boundaries

#### 2. City Layout (`city_generator.py`)
- Radial main roads from city center
- Ring roads at different radii
- Grid-pattern secondary streets
- Zone-based building placement
- NetworkX graph for pathfinding

#### 3. AI Behavior (`ai_behavior.py`)
Implements classic behavior tree pattern:
- **Composite nodes**: Sequence, Selector, Parallel
- **Decorator nodes**: Inverter, Repeater, Succeeder
- **Leaf nodes**: Condition, Action
- **Blackboard**: Shared memory system
- **Utility AI**: Score-based decision making

#### 4. NPC System (`npc_system.py`)
Each NPC has:
- **Internal needs**: Hunger, energy, social, safety
- **Memory system**: Remembers events and relationships
- **Behavior tree**: Drives decision-making
- **Pathfinding**: A* for navigation
- **Perception**: Awareness of nearby NPCs

#### 5. Pathfinding (`pathfinding.py`)
- **A\* algorithm** with optimizations
- **Path smoothing** for natural movement
- **Flow field** for crowd pathfinding
- **Diagonal movement** support
- **Line-of-sight** checks

#### 6. Rendering (`renderer.py`)
- **LOD system**: 4 detail levels based on distance
- **Frustum culling**: Only render visible objects
- **Cached surfaces**: Pre-render static layers
- **Camera system**: Smooth movement and zoom
- **Debug UI**: FPS, draw calls, NPC stats

## Performance Tuning

### Grid Size Impact
- **256x256**: Fast, good for testing (~60+ FPS)
- **512x512**: Default, balanced (~45-60 FPS)
- **1024x1024**: Large, requires powerful hardware (~30-45 FPS)

### NPC Count Impact
- **50 NPCs**: Minimal impact
- **100 NPCs**: Default, good balance
- **300 NPCs**: Noticeable impact on older hardware
- **500 NPCs**: Maximum, requires good CPU

### Optimization Tips
1. **Reduce grid size** for lower-end hardware
2. **Decrease NPC count** if FPS drops below 30
3. **Zoom out less** - distant objects use LOD
4. **Close other applications** to free RAM

## Technical Specifications

### Performance Targets (from Blueprint)
- **Target FPS**: 60 FPS
- **Minimum FPS**: 30 FPS
- **Max Draw Calls**: <500 per frame
- **Max NPC Count**: 500 active agents
- **City Size**: 5km x 5km equivalent (512x512 grid)
- **Loading Time**: <30 seconds

### AI Specifications
- **Perception Radius**: 50 units
- **Interaction Radius**: 10 units
- **Memory Size**: 20 events per NPC
- **Memory Decay**: Events fade after 5 minutes
- **Path Smoothing**: 2 iterations

## Emergent Behaviors

The NPCs exhibit emergent behaviors through interaction of simple rules:

### Need-Driven Actions
- **High hunger** → Seek food at commercial buildings
- **Low energy** → Rest at current location
- **Low social** → Seek interaction with nearby NPCs
- **Low safety** → Flee to random location

### Social Dynamics
- NPCs remember interactions with others
- Relationship values increase with each interaction
- Preferred NPCs are sought out for socializing

### Daily Routines
- NPCs wander when no urgent needs
- Buildings serve as destinations (home, work, food)
- Time-based behaviors create emergent schedules

## Extending the Simulation

### Adding New NPC Types

Edit `npc_system.py`:
```python
class NPCType(Enum):
    # Add new type
    POLICE = 5
```

### Customizing Behavior Trees

Edit `_create_behavior_tree()` in `npc_system.py` to add new behaviors:
```python
Sequence("NewBehavior", [
    Condition("CheckCondition", lambda bb: bb.get('value', 0) > 50),
    Action("PerformAction", custom_action_function)
])
```

### Adjusting World Generation

Modify constants in `config.py`:
```python
# Terrain
TERRAIN.OCTAVES = 8  # More detail
TERRAIN.WATER_LEVEL = 0.4  # More water

# City
CITY.BLOCK_SIZE = 50  # Larger blocks
CITY.BUILDING_DENSITY = 0.8  # More buildings
```

## Troubleshooting

### "Module not found" error
```bash
pip install -r requirements.txt
```

### Slow performance
- Reduce grid size: `--size 256`
- Reduce NPCs: `--npcs 50`
- Close other applications

### NPCs not moving
- Check that roads were generated (zoom out to see)
- Try a different seed
- NPCs need time to calculate paths

### Blank screen
- Wait 10-30 seconds for world generation
- Check console for error messages
- Ensure all dependencies are installed

## Development

### Running Tests

Each module can be tested independently:

```bash
# Test terrain generation
python terrain_generator.py

# Test city layout
python city_generator.py

# Test behavior trees
python ai_behavior.py

# Test pathfinding
python pathfinding.py

# Test NPC system
python npc_system.py

# Test Xbox controller
python controller_input.py
```

### Configuration

Edit `config.py` to customize:
- Performance targets
- Terrain parameters
- City layout rules
- NPC behavior settings
- Rendering options

## Credits

Built following modern game development practices:
- **Procedural Generation**: Perlin noise, grammar-based systems
- **AI Architecture**: Behavior trees, utility AI, A* pathfinding
- **Game Programming**: Entity-component patterns, LOD systems
- **Optimization**: Frustum culling, spatial partitioning, caching

## License

Copyright 2025 Intellegix

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

See the [LICENSE](LICENSE/LICENSE.md), [NOTICE](NOTICE), and [LICENSING.md](LICENSING.md) files for complete information.

**Crafted by Intellegix** - https://intellegix.ai

This is an educational and commercial-friendly project demonstrating AI-powered game development techniques. Feel free to use, modify, and distribute under the Apache 2.0 license terms.

## Future Enhancements

Potential additions based on the blueprint:
- **Time of day system** with day/night cycles
- **Weather simulation** affecting NPC behavior
- **Traffic simulation** with vehicles
- **Building interiors** for NPCs to enter
- **Job system** with work schedules
- **Economics** with resources and trading
- **Player interaction** modes
- **Save/Load** functionality
- **Dialogue system** for NPC conversations
- **Quest generation** for player objectives

## Contact & Support

For issues or questions:
1. Check the troubleshooting section
2. Review the blueprint documentation
3. Test individual modules to isolate issues

---

**Built with modern AI science and gaming programming expertise**

Total Development Time: ~20.5 hours (as per blueprint)
- Phase 1: Environment Setup (2.5h)
- Phase 2: Terrain Generation (3.0h)
- Phase 3: City Layout (4.0h)
- Phase 4: NPC AI Framework (6.0h)
- Phase 5: Polish & Testing (5.0h)
