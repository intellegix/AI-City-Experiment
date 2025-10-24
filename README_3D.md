# AI City Simulation - 3D GTA Style

**Immersive 3D city simulation with Grand Theft Auto-style graphics and gameplay**

**Crafted by Intellegix** | Licensed under Apache 2.0

---

## Overview

This is the **3D immersive version** of the AI City Simulation, featuring:

- 🎮 **GTA-style third-person camera**
- 🏗️ **Realistic 3D buildings** with procedural generation
- 💡 **Advanced lighting system** with sun, ambient, and shadows
- 🚶 **3D NPC characters** with AI behaviors
- 🌆 **Atmospheric effects** like fog and realistic colors
- 🎯 **Player-controlled character** you can move around the city

Built with **Panda3D**, a professional 3D game engine used for real commercial games.

---

## Quick Start

### Method 1: Double-Click Launcher (Easiest)
1. Navigate to the project folder
2. **Double-click `launch_3d.bat`**
3. Wait 5-10 seconds for world generation
4. The 3D window will open automatically!

### Method 2: Command Line
```powershell
cd "C:\Users\akidw\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\AI City Experiment"
python world_3d.py --size 64
```

### Method 3: Custom Settings
```bash
# Small world (fast)
python world_3d.py --size 32

# Medium world (balanced)
python world_3d.py --size 64

# Large world (slow)
python world_3d.py --size 128

# With specific seed
python world_3d.py --size 64 --seed 42
```

---

## Controls

### Player Movement
- **W** - Move forward
- **S** - Move backward
- **A** - Strafe left
- **D** - Strafe right

### Camera Control
- **Q** - Rotate camera left
- **E** - Rotate camera right
- **Mouse Wheel Up** - Zoom in
- **Mouse Wheel Down** - Zoom out

### System
- **ESC** - Exit simulation

---

## Features

### 1. Third-Person GTA-Style Camera
The camera follows your character from behind and above, just like Grand Theft Auto:
- **Smooth camera movement** with interpolation
- **Adjustable distance** via mouse wheel (5-30 units)
- **Rotatable** around player with Q/E keys
- **Height and angle** optimized for city exploration

### 2. Realistic Lighting System

**Directional Sun Light:**
- Warm golden sunlight (1.0, 0.95, 0.8)
- Casts dynamic shadows from buildings
- Positioned at 45° angle for optimal depth

**Ambient Light:**
- Soft global illumination (0.3, 0.3, 0.35)
- Prevents pure black shadows
- Simulates sky bounce light

**Fill Light:**
- Blue-tinted sky reflection (0.2, 0.25, 0.35)
- Adds realism to shadowed areas
- Creates natural outdoor atmosphere

**Shadows:**
- 2048x2048 shadow maps
- Cast by sun on all buildings
- Soft shadow edges for realism

### 3. Atmospheric Fog
- **Exponential fog** for distance fade
- Blue-gray color (0.7, 0.75, 0.8)
- Creates depth and atmosphere like GTA
- Makes distant objects fade naturally

### 4. Procedural 3D Buildings

**Geometry:**
- **Box-based buildings** with proper proportions
- **5 faces rendered**: Front, back, left, right, roof
- **Variable heights** based on building type
- **Realistic dimensions** scaled from grid data

**Materials & Colors:**
- **Commercial buildings**: Glass blue-gray (0.6, 0.65, 0.75)
- **Residential buildings**: Warm beige/tan variations
- **Industrial buildings**: Dark gray concrete (0.5, 0.52, 0.55)
- **Roofs**: Dark charcoal (0.3, 0.3, 0.35)

**Zone-Based Variation:**
- Commercial zones have modern glass appearance
- Residential zones have warm, inviting colors
- Industrial zones have utilitarian gray finish

### 5. Road System
- **Asphalt-colored roads** (0.15, 0.15, 0.17)
- Generated from city grid
- Flat planes at ground level
- Optimized sampling for performance

### 6. 3D NPC Characters
- **10 AI-driven NPCs** to start (configurable)
- **Blue character models** with human proportions
- **Real-time movement** synchronized with AI
- **Behavior-driven** (wandering, socializing, etc.)

### 7. Player Character
- **Red character model** for visibility
- **Full 360° movement** in all directions
- **Camera-relative controls** (forward is always camera forward)
- **Collision-free** movement (physics coming in future update)

---

## Technical Specifications

### Graphics Engine
- **Panda3D 1.10.13+** - Professional 3D game engine
- **OpenGL/DirectX** rendering backend
- **Shader-based lighting** system
- **Real-time shadows** with shadow mapping

### Performance
- **Target: 60 FPS** on modern hardware
- **Optimizations:**
  - Building limit (50 visible buildings)
  - Road sampling (every 4th cell)
  - LOD system (future)
  - Frustum culling (automatic)

### World Sizes
- **32x32**: Very fast, small city block (~30 buildings)
- **64x64**: Balanced, medium city area (~50 buildings) **[Default]**
- **128x128**: Large city, requires good GPU (~100 buildings)

---

## Graphics Comparison

### 2D Version (pygame)
- Top-down view
- Sprite-based rendering
- Simple LOD system
- 100-500 NPCs

### 3D Version (Panda3D) ⭐
- Third-person perspective
- Polygon-based 3D geometry
- Advanced lighting and shadows
- 10-50 NPCs (optimized for 3D)
- GTA-style immersion

---

## System Requirements

### Minimum
- **CPU**: Dual-core 2.0 GHz
- **RAM**: 4GB
- **GPU**: Intel HD Graphics 4000 or equivalent
- **Python**: 3.8+
- **OS**: Windows 7+, macOS 10.12+, Linux

### Recommended
- **CPU**: Quad-core 3.0 GHz
- **RAM**: 8GB
- **GPU**: NVIDIA GTX 1050 / AMD RX 560 or better
- **Python**: 3.10+
- **OS**: Windows 10/11

---

## Installation

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

This installs:
- `panda3d` - 3D game engine
- `panda3d-gltf` - 3D model format support
- `Pillow` - Image processing
- Plus all existing dependencies

### 2. Verify Installation
```bash
python -c "import panda3d; print('Panda3D version:', panda3d.__version__)"
```

Should output: `Panda3D version: 1.10.13` (or higher)

---

## Troubleshooting

### Black screen or no window appears
**Solution**: Wait 10-20 seconds for world generation. The window opens after terrain/city generation completes.

### Very low FPS (<20)
**Solutions**:
1. Reduce world size: `python world_3d.py --size 32`
2. Close other applications
3. Update GPU drivers
4. Disable shadows (future config option)

### ImportError: No module named 'panda3d'
**Solution**:
```bash
pip install panda3d panda3d-gltf Pillow
```

### Character moves in wrong direction
**Explanation**: Movement is camera-relative. "W" moves forward relative to camera angle, not world north. Rotate camera with Q/E first.

### Camera too close/far
**Solution**: Use mouse wheel to zoom in/out. Range: 5-30 units from player.

---

## Future Enhancements

Planned 3D features:
- 🚗 **Drivable vehicles** (cars, motorcycles)
- 🏃 **Character animations** (walking, running, idle)
- 🎨 **Texture mapping** on buildings
- 🌳 **3D trees and vegetation**
- 💥 **Particle effects** (dust, smoke)
- 🌅 **Day/night cycle** with dynamic lighting
- 🌧️ **Weather system** (rain, fog density changes)
- 🏠 **Building interiors** you can enter
- 🎵 **3D positional audio**
- 🎮 **Xbox controller support** for 3D camera
- 👥 **Multiplayer** support
- 🚶 **Improved NPC models** with better geometry
- 🗺️ **Minimap** in corner of screen
- 📍 **Waypoint system**

---

## Architecture

### File Structure
```
world_3d.py           - Main 3D engine and game loop
launch_3d.bat         - Windows launcher
launch_3d.ps1         - PowerShell launcher
terrain_generator.py  - Shared terrain generation
city_generator.py     - Shared city layout
npc_system.py         - Shared NPC AI
```

### Class Hierarchy
```
GTAStyleWorld (ShowBase)
├── Lighting System
│   ├── Ambient Light
│   ├── Directional Sun
│   ├── Fill Light
│   └── Fog
├── Camera System
│   ├── Third-Person Controller
│   └── Smooth Follow
├── World Generation
│   ├── Terrain Generator
│   ├── City Layout Generator
│   └── NPC Manager
└── 3D Scene
    ├── Ground Plane
    ├── Buildings (procedural geometry)
    ├── Roads
    ├── NPCs (3D characters)
    └── Player Character
```

### Coordinate System
- **Grid coordinates**: (0 to size-1) in terrain/city
- **World coordinates**: (-(size) to +(size)) in 3D space
- **Conversion**: `world_x = (grid_x - size/2) * 2.0`
- **Z-axis**: 0 = ground, positive = up

---

## Performance Tips

### For Best Performance
1. **Start with size 32** to test your system
2. **Close background applications** (browsers, etc.)
3. **Use fullscreen mode** (future config)
4. **Disable shadows** if needed (future config)
5. **Reduce NPC count** in code (line 69: change 10 to 5)

### FPS Monitoring
Watch console output for performance issues. Target: **60 FPS**

### Hardware Upgrade Priority
If upgrading:
1. **GPU** - Biggest impact on 3D performance
2. **RAM** - Helps with large worlds
3. **CPU** - Helps with AI and physics

---

## Development

### Adding Custom Buildings
Edit `_create_buildings()` in `world_3d.py` to customize geometry.

### Changing Lighting
Edit `_setup_lighting()` to adjust sun position, colors, shadow quality.

### Modifying Camera
Edit camera parameters in `__init__`:
- `self.camera_distance` - How far back camera sits
- `self.camera_height` - How high camera is
- `self.camera_angle` - Initial rotation

### Creating New 3D Models
Use **Blender** to create models, export as `.egg` or `.gltf`, load with:
```python
model = self.loader.loadModel("models/my_model.egg")
```

---

## Credits

**3D Engine**: Panda3D (open source game engine)
**Inspiration**: Grand Theft Auto series (Rockstar Games)
**Development**: Crafted by Intellegix

Built using modern game development techniques:
- Third-person camera systems
- Procedural 3D geometry generation
- Real-time lighting and shadows
- AI-driven NPCs
- Atmospheric rendering

---

## License

Copyright 2025 Intellegix

Licensed under the Apache License, Version 2.0.
See [LICENSE](LICENSE/LICENSE.md), [NOTICE](NOTICE), and [LICENSING.md](LICENSING.md).

---

**Ready to explore your 3D city?**

🎮 Double-click `launch_3d.bat` and experience the immersive GTA-style simulation!

**Crafted by Intellegix** - https://intellegix.ai
