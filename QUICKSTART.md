# Quick Start Guide

Get the AI City Simulation running in 5 minutes!

**Crafted by Intellegix** | Licensed under Apache 2.0

## Installation (2 minutes)

### Step 1: Install Python
Make sure you have Python 3.8 or newer:
```bash
python --version
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

That's it! Installation complete.

## Run the Simulation (30 seconds)

### Default Settings
```bash
python main.py
```

This will:
- Generate a 512x512 world
- Create terrain with multiple biomes
- Build a city with roads and buildings
- Spawn 100 NPCs with AI

**Wait 10-30 seconds** for world generation, then the simulation window will appear.

## First Time Tips

### 1. Wait for Generation
The console will show progress:
```
[Phase 2: Terrain & World Generation]
✓ Terrain generated...

[Phase 3: City Layout & Asset Placement]
✓ City layout generated...

[Phase 4: NPC Framework & Emergent AI]
✓ 100 NPCs spawned...
```

### 2. Explore the World
Once the window appears:
- Press **W/A/S/D** to move camera
- Press **Q/E** to zoom
- Press **D** to toggle debug info

### 3. Watch the NPCs
- **Blue dots** = Idle NPCs
- **Green dots** = Walking NPCs
- **Yellow dots** = Eating NPCs
- **Purple dots** = Socializing NPCs

## Common First-Run Issues

### Too Slow?
Try a smaller world:
```bash
python main.py --size 256 --npcs 50
```

### Want More Action?
Spawn more NPCs:
```bash
python main.py --npcs 300
```

### Want Same World?
Use a seed:
```bash
python main.py --seed 42
```

## Next Steps

1. **Read README.md** for full documentation
2. **Experiment with settings** using command-line options
3. **Modify config.py** to customize behavior
4. **Explore the code** to understand the systems

## Controls Reference

### Keyboard & Mouse
**Camera:**
- **W** - Move up
- **A** - Move left
- **S** - Move down
- **D** - Move right (if debug is off)
- **Q** - Zoom out
- **E** - Zoom in
- **Mouse Wheel** - Zoom

**Simulation:**
- **Space** - Pause/Resume
- **D** - Toggle debug overlay
- **ESC** - Quit

### Xbox Controller (Optional)
**Plug and play!** Controllers work automatically via Bluetooth or USB.

- **Left Stick** - Smooth camera movement
- **Right Stick** - Zoom
- **Triggers** - Zoom in/out
- **Start** - Pause
- **Y** - Toggle debug

**Full guide:** See [CONTROLLER_GUIDE.md](CONTROLLER_GUIDE.md)

## What's Happening?

The simulation demonstrates:
1. **Procedural terrain** generated with Perlin noise
2. **City layout** with roads and buildings
3. **Emergent AI** where NPCs have needs and goals
4. **Pathfinding** as NPCs navigate the city
5. **Social dynamics** as NPCs interact

Watch NPCs:
- Wander when content
- Seek food when hungry
- Rest when tired
- Socialize when lonely
- Navigate using roads

## Performance Expectations

### Good Performance (60 FPS)
- Grid: 256 or 512
- NPCs: 50-150
- Modern hardware

### Acceptable Performance (30-45 FPS)
- Grid: 512
- NPCs: 200-300
- Average hardware

### Slow Performance (<30 FPS)
- Reduce grid size to 256
- Reduce NPCs to 50
- Close other applications

## Getting Help

### No Window Appears
- Check console for errors
- Ensure pygame is installed: `pip install pygame`
- Try: `python main.py --size 256`

### NPCs Not Moving
- Normal! They need time to plan paths
- Zoom out to see the city
- Wait 10-20 seconds
- NPCs may be idle (blue) - this is normal

### Import Errors
```bash
pip install -r requirements.txt --upgrade
```

### Still Having Issues?
1. Check Python version: `python --version` (need 3.8+)
2. Update pip: `pip install --upgrade pip`
3. Reinstall dependencies: `pip install -r requirements.txt --force-reinstall`

## Have Fun!

Explore the emergent behaviors and watch your AI city come to life!

For advanced usage, see **README.md**
