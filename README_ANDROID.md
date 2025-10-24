# AI City Simulation - Android/Termux Edition

Running the AI City Experiment on Android devices using Termux.

## Prerequisites

1. **Termux** app installed from F-Droid (not Play Store version)
2. **Termux:X11** or **VNC Viewer** for graphical display
3. At least 2GB free storage
4. 4GB+ RAM recommended

## Quick Start

### Option 1: Using the Bash Launcher (Recommended)
```bash
cd ~/AI_City_Experiment
./launch_android.sh
```

### Option 2: Using the Python Launcher
```bash
cd ~/AI_City_Experiment
python launch_android.py
```

### Option 3: Manual Launch
```bash
cd ~/AI_City_Experiment
python main.py --npc-count 5 --grid-size 256
```

## Installation Steps

### 1. Install Python and Dependencies
```bash
pkg install python x11-repo
pkg install termux-x11-nightly
pip install numpy pygame noise networkx scipy dataclasses-json
```

### 2. Set Up Display (Choose One Method)

#### Method A: Using Termux:X11 (Recommended)
```bash
# Install Termux:X11 app from GitHub releases
# Start Termux:X11 app
export DISPLAY=:0
```

#### Method B: Using VNC Server
```bash
pkg install tigervnc
vncserver :1
# Connect with VNC Viewer app to localhost:5901
export DISPLAY=:1
```

### 3. Run the Simulation
```bash
./launch_android.sh
```

## Android Optimizations

The Android version includes these optimizations:

- **Reduced Grid Size**: 256x256 (vs 512x512 desktop)
- **Fewer NPCs**: Maximum 50 NPCs (vs 150 desktop)
- **Lower Resolution**: 800x600 (adjustable)
- **Simplified Terrain**: 4 octaves (vs 6 desktop)
- **Aggressive LOD Culling**: Objects beyond 200 units culled
- **Lower Target FPS**: 30 FPS (vs 60 desktop)

## Controls

- **Arrow Keys / WASD**: Move camera
- **Q / E**: Zoom in/out
- **ESC**: Exit simulation
- **Space**: Pause/Resume

## Performance Tips

1. **Start Small**: Begin with 5 NPCs and increase gradually
2. **Close Other Apps**: Free up RAM
3. **Lower Grid Size**: Use `--grid-size 128` for better performance
4. **Reduce NPCs**: Use `--npc-count 3` if lagging
5. **Check Temperature**: Mobile devices may throttle when hot

## Troubleshooting

### Display Issues
```bash
# If you see "No display found"
export DISPLAY=:0
# Or try
export SDL_VIDEODRIVER=x11
```

### Out of Memory
```bash
# Reduce simulation size
python main.py --npc-count 3 --grid-size 128
```

### Slow Performance
```bash
# Use minimal settings
python main.py --npc-count 1 --grid-size 64
```

### Package Installation Errors
```bash
# Update packages first
pkg update && pkg upgrade
# Try installing one at a time
pip install numpy
pip install pygame
pip install noise
pip install networkx
pip install scipy
pip install dataclasses-json
```

## Advanced Configuration

Edit `config_android.py` to customize:

```python
# Change window size
RENDER.WINDOW_WIDTH = 640
RENDER.WINDOW_HEIGHT = 480

# Adjust NPC limits
NPC.MAX_NPC_COUNT = 25

# Change terrain size
TERRAIN.SIZE = 128
```

## Known Limitations

1. **No 3D Graphics**: Panda3D not supported on Android (uses 2D Pygame instead)
2. **Touch Controls**: Limited touch support (keyboard recommended)
3. **Performance**: Slower than desktop due to mobile hardware
4. **Display Setup**: Requires X11 server or VNC

## System Requirements

### Minimum
- Android 7.0+
- 2GB RAM
- Quad-core processor
- 1GB free storage

### Recommended
- Android 10.0+
- 4GB+ RAM
- Octa-core processor
- 2GB free storage

## File Structure

```
AI_City_Experiment/
├── launch_android.sh        # Bash launcher
├── launch_android.py        # Python launcher with auto-install
├── config_android.py        # Android-optimized config
├── README_ANDROID.md        # This file
└── main.py                  # Main simulation
```

## Support

For issues specific to Android:
1. Check Termux logs
2. Verify display is working: `echo $DISPLAY`
3. Test pygame: `python -c "import pygame; print(pygame.ver)"`
4. Report issues to: https://github.com/anthropics/claude-code/issues

## Credits

AI City Simulation crafted by Intellegix
Android port optimized for Termux
Licensed under Apache License 2.0
