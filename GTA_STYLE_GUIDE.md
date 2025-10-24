# 🎮 GTA-Style 3D City Simulation - Quick Start

**Transform your AI city into an immersive 3D experience!**

---

## 🚀 Launch in 3 Steps

### Step 1: Navigate to Project Folder
```
C:\Users\akidw\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\AI City Experiment
```

### Step 2: Double-Click `launch_3d.bat`
This will:
- ✓ Install any missing 3D dependencies
- ✓ Generate a small city block (64x64)
- ✓ Launch the 3D window with GTA-style graphics

### Step 3: Explore!
- **Move**: WASD keys
- **Look around**: Q/E to rotate camera
- **Zoom**: Mouse wheel
- **Exit**: ESC

---

## 🎯 What You'll See

### During Loading (5-10 seconds)
```
================================================================================
AI CITY SIMULATION - 3D GTA STYLE
Crafted by Intellegix
================================================================================

Setting up realistic lighting...
[OK] Lighting system initialized

Setting up third-person camera...
[OK] Camera system ready

Generating 3D world...
[Phase 1: Terrain Generation]
[OK] Terrain generated

[Phase 2: City Layout]
[OK] City generated (50 buildings)

[Phase 3: NPCs]
[OK] 10 NPCs spawned

[Phase 4: Building 3D Scene]
Creating 3D buildings...
[OK] Created 50 buildings
Creating road network...
[OK] Road network created
Creating 3D NPCs...
[OK] Created 10 NPC models
[OK] 3D scene constructed

3D World ready! Use WASD to move, Mouse to look around
```

### The 3D Window Opens Showing:

**🌆 GTA-Style City:**
- ✨ **Realistic lighting** with sun, ambient, and shadows
- 🏗️ **3D buildings** in blue (commercial), beige (residential), gray (industrial)
- 🛣️ **Asphalt roads** connecting city blocks
- 🌫️ **Atmospheric fog** for depth
- 🚶 **Blue NPCs** walking around with AI behaviors
- 🎯 **Red player character** (you!) that you control

**📸 Third-Person Camera:**
- Follows behind and above your character
- Smooth movement and rotation
- Just like GTA, Assassin's Creed, or Tomb Raider!

---

## 🎮 Full Controls

### Player Movement
| Key | Action |
|-----|--------|
| **W** | Move forward (camera-relative) |
| **S** | Move backward |
| **A** | Strafe left |
| **D** | Strafe right |

### Camera Controls
| Key/Input | Action |
|-----------|--------|
| **Q** | Rotate camera left around player |
| **E** | Rotate camera right around player |
| **Mouse Wheel Up** | Zoom closer |
| **Mouse Wheel Down** | Zoom farther |

### System
| Key | Action |
|-----|--------|
| **ESC** | Exit simulation |

---

## 📊 Versions Comparison

### 2D Version (Original)
- ✓ Top-down bird's eye view
- ✓ 100-500 NPCs
- ✓ Fast performance
- ✓ Full city overview
- 🚀 Launch with: `launch.bat`

### 3D Version (NEW!) ⭐
- ✓ Third-person GTA perspective
- ✓ 10-50 NPCs
- ✓ Immersive exploration
- ✓ Realistic lighting and shadows
- ✓ 3D buildings and characters
- 🚀 Launch with: `launch_3d.bat`

**Both versions share the same AI and world generation!**

---

## 🎨 Graphics Features

### Lighting System
- **Directional sun** with warm golden color
- **Dynamic shadows** cast by buildings
- **Ambient light** prevents pure black
- **Blue fill light** simulates sky reflection
- **Atmospheric fog** for depth

### Buildings
- **Procedural 3D geometry** (boxes with 5 faces)
- **Zone-based colors**:
  - Commercial: Glass blue-gray
  - Residential: Warm beige/tan
  - Industrial: Dark gray concrete
- **Realistic proportions** based on building data

### Environment
- **Asphalt roads** in dark gray
- **Exponential fog** for GTA-style atmosphere
- **Shader-based rendering** for quality

---

## ⚙️ Customization

### Change World Size
Edit `launch_3d.bat` line 23:

```batch
REM Small city (fast)
python world_3d.py --size 32

REM Medium city (balanced) - DEFAULT
python world_3d.py --size 64

REM Large city (slow, needs good GPU)
python world_3d.py --size 128
```

### Change NPC Count
Edit `world_3d.py` line 69:
```python
# Change 10 to your desired NPC count (5-50 recommended)
self.npc_manager.spawn_random_npcs(10)
```

### Adjust Camera
Edit `world_3d.py` lines 53-55:
```python
self.camera_distance = 15.0  # How far back (5-30)
self.camera_height = 8.0     # How high up (3-15)
self.camera_angle = 45.0     # Initial rotation (0-360)
```

---

## 🔧 Troubleshooting

### Issue: Window doesn't open
**Solution**: Wait 10-20 seconds. World generation happens before window opens.

### Issue: Very slow FPS
**Solutions**:
1. Use smaller world: `python world_3d.py --size 32`
2. Reduce NPCs in code (line 69)
3. Close other applications
4. Update GPU drivers

### Issue: ImportError for panda3d
**Solution**:
```bash
pip install panda3d panda3d-gltf Pillow
```

### Issue: Black screen
**Solution**: This is normal during loading. Wait for console messages to complete.

---

## 🎯 Tips for Best Experience

1. **Start small**: First launch with default size 64
2. **Explore freely**: Walk around to see different buildings
3. **Rotate camera**: Use Q/E to see from all angles
4. **Watch NPCs**: Blue characters have real AI (wandering, socializing)
5. **Experiment**: Try different seeds for different cities

---

## 📁 Project Files

```
AI City Experiment/
├── world_3d.py          ⭐ Main 3D engine
├── launch_3d.bat        ⭐ 3D launcher (Windows)
├── launch_3d.ps1        ⭐ 3D launcher (PowerShell)
├── README_3D.md         ⭐ Full 3D documentation
├── GTA_STYLE_GUIDE.md   ⭐ This quick-start guide
│
├── main.py              📊 2D version
├── launch.bat           📊 2D launcher
├── renderer.py          📊 2D rendering
│
└── [Shared files]
    ├── terrain_generator.py
    ├── city_generator.py
    ├── npc_system.py
    ├── ai_behavior.py
    └── pathfinding.py
```

---

## 🚀 Ready to Launch?

### Quick Command (Copy & Paste)
```powershell
cd "C:\Users\akidw\ASR Dropbox\Austin Kidwell\02_DevelopmentProjects\AI City Experiment"
python world_3d.py --size 64
```

### OR

Just **double-click `launch_3d.bat`**!

---

## 📖 More Information

- **Full 3D docs**: See [README_3D.md](README_3D.md)
- **Original 2D docs**: See [README.md](README.md)
- **Controls guide**: See [CONTROLLER_GUIDE.md](CONTROLLER_GUIDE.md)
- **Graphics details**: See [GRAPHICS_FEATURES.md](GRAPHICS_FEATURES.md)

---

**🎮 Enjoy your GTA-style 3D city exploration!**

**Crafted by Intellegix** - https://intellegix.ai

Apache License 2.0 | See LICENSE and NOTICE files
