# Enhanced 3D AI City - Quick Start Guide

**Professional GTA-style 3D city with modular procedural systems**

**Crafted by Intellegix** | Licensed under Apache 2.0

---

## 🚀 Launch the Enhanced World

### Windows (Batch File):
```
Double-click: launch_enhanced.bat
```

### PowerShell:
```powershell
.\launch_enhanced.ps1
```

### Command Line:
```bash
python world_3d_enhanced.py --size 64
```

---

## 🎮 What You'll See

### Procedural Buildings (50 total)
- **Commercial Zone**: Modern and Skyscraper styles (20-50 floors)
- **Residential Zones**: Residential and Classic styles (4-15 floors)
- **Industrial Zone**: Industrial style warehouses (3-8 floors)
- **Every building is unique** - different heights, colors, window patterns

### Vehicles (30 spawned)
- **11 Types**: Sedan, SUV, Hatchback, Truck, Van, Bus, Taxi, Police, Ambulance, Sports Car, Vintage
- **165+ Variations**: Different colors and markings
- **Realistic Proportions**: Buses are bigger than sedans, sports cars are lower

### AI Characters (10 NPCs)
- Walking around the city
- Following paths on roads
- Behavior-driven AI

---

## 🎮 Controls

### Keyboard:
- **WASD** - Move player (camera-relative)
- **Q/E** - Rotate camera
- **Mouse Wheel** - Zoom in/out
- **ESC** - Exit

### Xbox Controller (Recommended):
- **Left Stick** - Move player (GTA-style)
- **Right Stick (Horizontal)** - Rotate camera
- **Right Stick (Vertical)** - Zoom in/out
- **LT** - Zoom out (gradual)
- **RT** - Zoom in (gradual)
- **LB** - Zoom out (quick)
- **RB** - Zoom in (quick)

---

## 📊 Technical Specs

### Performance Targets:
- **60 FPS** at 1920x1080
- **50 procedural buildings** (12,000+ possible combinations)
- **30 vehicles** (165+ variations)
- **10 NPCs** with AI behaviors

### System Requirements:
- **Python**: 3.9 - 3.13
- **RAM**: 4GB minimum, 8GB recommended
- **GPU**: Any modern GPU (Intel HD 4000+)
- **OS**: Windows 10/11, macOS, Linux

---

## 🏗️ Modular Architecture

This enhanced version uses **professional modular systems**:

### Files:
- `procedural_buildings.py` - Building generation system
- `vehicle_system.py` - Vehicle spawning system
- `world_3d_enhanced.py` - Main 3D world integration
- `city_generator.py` - Road network and zones
- `ai_behavior.py` - NPC behavior trees
- `pathfinding.py` - A* navigation

---

## 🎨 Customization

### Want More Buildings?
Edit `world_3d_enhanced.py` line 119:
```python
max_buildings = 100  # Change from 50 to 100
```

### Want More Vehicles?
Edit `world_3d_enhanced.py` line 160:
```python
vehicle_count = 50  # Change from 30 to 50
```

### Want Different Spawn Rates?
Edit `vehicle_system.py` lines 268-280:
```python
self.spawn_weights = {
    VehicleType.SEDAN: 0.30,  # 30% of vehicles
    VehicleType.BUS: 0.05,    # 5% of vehicles
    # ... adjust as desired
}
```

### Add New Building Style:
See `ENHANCED_SYSTEMS.md` for detailed customization guide

---

## 📚 Documentation

- **ENHANCED_SYSTEMS.md** - Complete system architecture and features
- **CONTROLLER_3D.md** - Full Xbox controller guide
- **GTA_STYLE_GUIDE.md** - GTA-style controls overview
- **README_3D.md** - Original 3D world documentation
- **LICENSING.md** - Apache 2.0 license compliance

---

## 🔧 Troubleshooting

### "No module named 'panda3d'"
```bash
pip install -r requirements.txt
```

### "Xbox Controller Connected!" not showing
1. Connect controller via Bluetooth or USB
2. Press any button to wake it
3. Relaunch the simulation

### Low FPS
- Reduce building count (edit line 119 in world_3d_enhanced.py)
- Reduce vehicle count (edit line 160)
- Close other programs

### Buildings/Vehicles not appearing
- Check console for error messages
- Verify all modular system files exist:
  - procedural_buildings.py
  - vehicle_system.py
  - city_generator.py

---

## 🌟 Key Features

### Procedural Buildings
- ✅ Infinite unique variations (12,000+ combinations)
- ✅ Zone-based architectural styles
- ✅ Realistic proportions (3-50 floors)
- ✅ Window patterns (Grid, Strips, Random)
- ✅ Rooftop details (AC units, antennas)
- ✅ Entrance canopies

### Vehicle System
- ✅ 11 vehicle types with realistic dimensions
- ✅ 165+ color/type combinations
- ✅ Special markings (police stripes, taxi signs)
- ✅ Weighted spawning (more sedans, fewer buses)
- ✅ Procedurally generated (no 3D assets needed)

### GTA-Style Experience
- ✅ Third-person follow camera
- ✅ Camera-relative movement
- ✅ Xbox controller support
- ✅ Realistic lighting (3 lights + shadows + fog)
- ✅ Smooth 60 FPS performance

---

## 🎯 Compare to Original 2D Version

| Feature | 2D Version | Enhanced 3D |
|---------|-----------|-------------|
| **Graphics** | Top-down 2D | GTA-style 3D |
| **Buildings** | Simple boxes | Procedural 3D (5 styles) |
| **Vehicles** | Placeholders | Full 3D (11 types) |
| **Camera** | Fixed top-down | Third-person follow |
| **Controller** | Basic support | Full GTA-style |
| **Variety** | Limited | Infinite (procedural) |

---

## 🚗 Vehicle Types You'll See

Common (70%):
- **Sedan** (30%) - Standard cars in various colors
- **SUV** (20%) - Larger family vehicles
- **Hatchback** (15%) - Compact city cars
- **Truck** (10%) - Pickup trucks

Uncommon (25%):
- **Van** (8%) - Cargo and passenger vans
- **Taxi** (5%) - Yellow taxis with roof signs
- **Sports Car** (4%) - Low, sleek sports cars
- **Police** (3%) - Dark with blue stripes

Rare (5%):
- **Bus** (2%) - Large orange buses (12m long!)
- **Ambulance** (2%) - White with red cross
- **Vintage** (1%) - Classic cars

---

## 🏢 Building Styles You'll See

### Commercial Zone:
- **Modern** (60%): 8-20 floors, glass and steel, blue-gray colors
- **Skyscraper** (40%): 20-50 floors, towering buildings

### Residential Zones:
- **Residential** (70%): 4-12 floors, warm cream/beige colors
- **Classic** (30%): 5-15 floors, brick red/orange colors

### Industrial Zone:
- **Industrial** (100%): 3-8 floors, dark concrete gray

---

## 🎓 Learning Resource

This codebase demonstrates:

**Game Development:**
- Procedural generation algorithms
- Modular system architecture
- Third-person camera systems
- Level of Detail (LOD) preparation

**Python/Panda3D:**
- CardMaker for procedural geometry
- Node graph management
- Lighting and shadow systems
- Controller input handling

**AI Systems:**
- Behavior trees
- A* pathfinding
- NPC state machines

---

## 💡 Next Steps

After exploring the enhanced world:

1. **Read the documentation**
   - ENHANCED_SYSTEMS.md for system details
   - CONTROLLER_3D.md for control mastery

2. **Customize the world**
   - Adjust spawn counts
   - Change building styles
   - Modify vehicle types

3. **Extend the systems**
   - Add new building styles
   - Create new vehicle types
   - Add street props

---

## ✨ What Makes This Special?

### No 3D Assets Needed
- **Traditional approach**: Hire 3D artists, create 100+ models, $20,000+ cost
- **Our approach**: Procedural code generates infinite variations, $0 cost

### Infinite Variety
- **12,000+ building combinations** from 5 styles
- **165+ vehicle variations** from 11 types
- **Every playthrough is unique**

### Professional Architecture
- **Modular design** - easy to extend
- **Clean interfaces** - simple to use
- **Type-safe** - enums prevent errors
- **Documented** - every class and method

### GTA-Style Feel
- **Third-person camera** follows player
- **Camera-relative movement** (just like GTA V)
- **Xbox controller support** (feels like console game)
- **Realistic lighting** (shadows, fog, ambient)

---

## 🎮 Ready to Explore?

**Launch now:**
```
Double-click: launch_enhanced.bat
```

**Enjoy your GTA-style AI city with infinite procedural variety!**

---

**Crafted by Intellegix** - https://intellegix.ai

*Apache License 2.0 | See LICENSE and NOTICE files*
