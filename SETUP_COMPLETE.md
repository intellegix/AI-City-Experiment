# AI City Experiment - Android Setup Complete! 🎉

## ✅ What's Been Installed

### Core Components
- ✓ Python 3.12.11
- ✓ NumPy 2.2.5 (pre-built from Termux)
- ✓ SciPy 1.16.2 (pre-built from Termux)
- ✓ NetworkX 3.5
- ✓ Noise 1.2.2
- ✓ dataclasses-json 0.6.7

### Display System
- ✓ TigerVNC Server
- ✓ XFCE4 Desktop Environment
- ✓ X11 Support Libraries

### Project Files Created
- ✓ `config_android.py` - Mobile-optimized configuration
- ✓ `main_headless.py` - Text-mode simulation (no graphics needed)
- ✓ `launch_android.sh` - Bash launcher for graphics mode
- ✓ `launch_termux.sh` - Launcher for headless/text mode
- ✓ `start-vnc.sh` - VNC server startup script
- ✓ `README_ANDROID.md` - Complete Android documentation

## 🚀 How to Run

### Option 1: Headless/Text Mode (RECOMMENDED - Works Immediately)

This mode runs in your terminal without needing graphics:

```bash
cd ~/AI_City_Experiment
./launch_termux.sh
```

OR manually:
```bash
cd ~/AI_City_Experiment
python main_headless.py --npc-count 10 --duration 60
```

This will show you:
- Live NPC statistics
- Performance metrics
- Real-time simulation updates
- No graphics/display setup needed!

### Option 2: Graphical Mode with VNC (Requires Setup)

#### Step 1: Set VNC Password
```bash
vncpasswd
# Enter a password when prompted (at least 6 characters)
```

#### Step 2: Start VNC Server
```bash
~/start-vnc.sh
# OR manually:
vncserver :1 -geometry 800x600
```

#### Step 3: Connect with VNC Viewer
- Install "VNC Viewer" app from Play Store
- Connect to: `localhost:5901`
- Enter the password you set

#### Step 4: Run AI City (in VNC terminal)
```bash
export DISPLAY=:1
cd ~/AI_City_Experiment
python main_headless.py --npc-count 10
```

## 📝 Configuration

### Android-Optimized Settings (config_android.py)
```
Grid Size: 256x256 (reduced from 512x512)
Max NPCs: 50 (reduced from 150)
Window: 800x600 (reduced from 1280x720)
Target FPS: 30 (reduced from 60)
Terrain Detail: Reduced by 33%
```

### Adjust Settings
Edit `config_android.py` to customize:
```python
# Smaller/faster simulation
TERRAIN.SIZE = 128
NPC.MAX_NPC_COUNT = 25

# Larger/slower simulation
TERRAIN.SIZE = 512
NPC.MAX_NPC_COUNT = 100
```

## 🎮 Controls

### Headless Mode
- Simulation runs automatically
- CTRL+C to stop
- Updates every second

### Parameters
```bash
python main_headless.py \
  --npc-count 10 \      # Number of NPCs (1-50)
  --grid-size 256 \     # World size (64-512)
  --seed 42 \           # Random seed
  --duration 60         # Run time in seconds
```

## 🐛 Troubleshooting

### "Module not found" errors
```bash
cd ~/AI_City_Experiment
pip install numpy scipy networkx noise dataclasses-json
```

### VNC won't start
```bash
# Kill existing servers
vncserver -kill :1
# Set password first
vncpasswd
# Try again
vncserver :1 -geometry 800x600
```

### Slow performance
```bash
# Use minimal settings
python main_headless.py --npc-count 3 --grid-size 128 --duration 30
```

### Out of memory
```bash
# Close other apps
# Use smaller grid
python main_headless.py --grid-size 64 --npc-count 5
```

## 📊 What to Expect

### Headless Mode Output
```
==================================================
AI CITY SIMULATION - 20:45:32
==================================================

Runtime: 15.3s / 60s
Progress: [###############---------------]

NPC STATISTICS:
--------------------------------------------------
  Wandering      : ████ (4)
  Walking        : ███ (3)
  Idle           : ██ (2)
  Working        : █ (1)

PERFORMANCE:
--------------------------------------------------
  Total Ticks: 459
  Avg Tick Time: 0.0032s
  Ticks/Second: 31.2

SAMPLE NPC (ID: 0):
--------------------------------------------------
  Type: Civilian
  Position: (128.4, 95.7)
  Hunger: ████████-- 80%
  Energy: ██████---- 60%
  Social: ████------ 40%
```

## 🎯 Next Steps

1. **Try Headless Mode First**
   ```bash
   cd ~/AI_City_Experiment
   ./launch_termux.sh
   ```

2. **Set up VNC for Graphics** (if desired)
   - Set VNC password with `vncpasswd`
   - Start server with `~/start-vnc.sh`
   - Connect with VNC Viewer app

3. **Experiment with Settings**
   - Adjust NPC count: `--npc-count 5`
   - Change world size: `--grid-size 128`
   - Set duration: `--duration 120`

4. **Monitor Performance**
   - Watch tick rate (should be >20 TPS)
   - Check memory with `free -h`
   - Adjust settings if slow

## 📚 Documentation Files

- `README_ANDROID.md` - Full Android guide
- `ANDROID_SETUP_SUMMARY.md` - Quick reference
- `SETUP_COMPLETE.md` - This file
- `README.md` - Original project documentation

## 🎬 Quick Start Command

```bash
cd ~/AI_City_Experiment && ./launch_termux.sh
```

This runs the headless version with default settings for 60 seconds.

## ⚙️ System Info

```
Location: ~/AI_City_Experiment
Python: 3.12.11
NumPy: 2.2.5
SciPy: 1.16.2
Platform: Android/Termux
Display: VNC or Headless
```

## 🆘 Need Help?

1. Check `README_ANDROID.md` for detailed troubleshooting
2. Run headless mode to test without graphics: `./launch_termux.sh`
3. Verify packages: `pip list | grep -E "numpy|scipy|networkx|noise"`
4. Check memory: `free -h`

## 🎉 You're All Set!

The AI City Experiment is ready to run on your Android device. Start with headless mode to see it in action immediately, then optionally set up VNC for graphical display later.

Happy simulating! 🏙️

---
Setup completed by Claude Code
Crafted by Intellegix
