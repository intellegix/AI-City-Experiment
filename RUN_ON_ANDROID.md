# 🎮 AI City Experiment - Complete Android Setup

## ✅ EVERYTHING IS READY TO RUN!

Your AI City Experiment is fully configured for Android/Termux and ready to go!

## 🚀 QUICKSTART - Run Now!

### Option 1: Headless/Text Mode (Works Immediately!)
```bash
cd ~/AI_City_Experiment
./launch_termux.sh
```

This runs a text-based simulation showing:
- Live NPC statistics
- Real-time updates
- Performance metrics
- NO graphics setup needed!

### Option 2: Custom Run
```bash
cd ~/AI_City_Experiment
python main_headless.py --npc-count 10 --grid-size 256 --duration 60
```

## 📦 What's Installed & Working

✅ Python 3.12.11
✅ NumPy 2.2.5 (optimized for Android)
✅ SciPy 1.16.2
✅ NetworkX 3.5
✅ Noise 1.2.2
✅ dataclasses-json 0.6.7
✅ VNC Server + XFCE Desktop
✅ All simulation code

## 🎯 Available Modes

### 1. Headless Terminal Mode ⭐ RECOMMENDED
**Best for**: Immediate use, low resource usage
```bash
./launch_termux.sh
```

**Features**:
- Real-time statistics
- Live NPC tracking
- Performance monitoring
- Works on ANY Android device
- No display setup required

### 2. VNC Graphical Mode
**Best for**: Visual experience
**Requires**: VNC Viewer app + setup

**Setup Steps**:
```bash
# 1. Set VNC password
vncpasswd

# 2. Start VNC
vncserver :1 -geometry 800x600

# 3. Connect with VNC Viewer app
# Address: localhost:5901
```

## ⚙️ Configuration Files

All configurations optimized for Android:

| File | Purpose |
|------|---------|
| `config_android.py` | Mobile-optimized settings |
| `main_headless.py` | Text-mode simulation |
| `launch_termux.sh` | Quick launcher |
| `start-vnc.sh` | VNC startup |

## 🎮 Simulation Parameters

### Adjust Performance
Edit these in commands:

```bash
# Ultra-fast (low-end phone)
python main_headless.py --npc-count 3 --grid-size 64 --duration 30

# Balanced (mid-range phone)
python main_headless.py --npc-count 10 --grid-size 128 --duration 60

# Full (high-end phone)
python main_headless.py --npc-count 25 --grid-size 256 --duration 120
```

### Edit Config File
```bash
nano config_android.py
```

Change:
```python
NPC.MAX_NPC_COUNT = 50      # Lower for better performance
TERRAIN.SIZE = 256          # Smaller = faster
```

## 📊 What You'll See

### Terminal Output Example:
```
================================================================================
AI CITY SIMULATION - 20:45:32
================================================================================

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

## 🤖 AI Features (Currently Available)

The simulation includes smart AI systems:

✅ **Behavior Trees** - Complex decision making
✅ **Utility AI** - Need-based actions
✅ **Pathfinding** - A* algorithm navigation
✅ **Memory System** - NPCs remember events
✅ **Emergent Behavior** - Unexpected interactions
✅ **Multiple NPC Types** - Civilians, Guards, Shopkeepers, etc.

## 🚀 Future AI Enhancements (When Available)

When LLM support comes to Termux, you'll be able to add:
- Real LLM-powered conversations
- Dynamic story generation
- Unique NPC personalities
- Context-aware responses

## 💡 Tips for Best Performance

1. **Close Background Apps** - Free up RAM
2. **Start Small** - Begin with 5 NPCs
3. **Monitor Performance** - Watch tick rate
4. **Adjust Grid Size** - Smaller = faster
5. **Use Headless Mode** - No graphics overhead

## 🔧 Troubleshooting

### Simulation Won't Start
```bash
cd ~/AI_City_Experiment
pip install numpy scipy networkx noise dataclasses-json
```

### Out of Memory
```bash
# Use minimal settings
python main_headless.py --npc-count 3 --grid-size 64
```

### Slow Performance
```bash
# Reduce complexity
python main_headless.py --npc-count 5 --grid-size 128
```

### VNC Issues
```bash
vncserver -kill :1
vncpasswd
vncserver :1 -geometry 800x600
```

## 📁 File Structure

```
~/AI_City_Experiment/
├── main_headless.py          # Headless simulator ⭐
├── config_android.py          # Android config
├── launch_termux.sh           # Quick launcher ⭐
├── terrain_generator.py       # World generation
├── city_generator.py          # City layout
├── npc_system.py              # AI NPCs
├── README_ANDROID.md          # Full docs
├── SETUP_COMPLETE.md          # Setup guide
└── RUN_ON_ANDROID.md          # This file ⭐
```

## 🎯 Quick Commands Reference

```bash
# Run simulation (default settings)
./launch_termux.sh

# Run custom simulation
python main_headless.py --npc-count 10 --duration 60

# View logs
less ~/.kivy/logs/kivy_*.txt

# Check installed packages
pip list | grep -E "numpy|scipy|networkx|noise"

# Monitor system
free -h && df -h

# Start VNC
~/start-vnc.sh
```

## 📚 Documentation

- `README_ANDROID.md` - Complete Android guide
- `SETUP_COMPLETE.md` - Installation summary
- `AI_MODELS_ON_ANDROID.md` - Future LLM integration
- `RUN_ON_ANDROID.md` - This file

## 🎉 You're All Set!

Just run:
```bash
cd ~/AI_City_Experiment && ./launch_termux.sh
```

And watch your AI city come to life! 🏙️🤖

---

**Need Help?**
- Check `README_ANDROID.md` for troubleshooting
- Adjust parameters if too slow
- Start with headless mode first

**Crafted by Intellegix**
**Optimized for Android/Termux**
