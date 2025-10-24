# 🎨 AI City Experiment - UI Options

You have **TWO ways** to experience your AI City!

---

## 🎮 Option 1: Tuxemon Graphical UI (RECOMMENDED)

**Full 2D RPG-style interface with sprites, maps, and visual NPCs!**

### Features:
✨ **Beautiful 2D Graphics** - See your AI city come to life
🏃 **Walk around the city** - Explore with arrow keys
👥 **Visual NPCs** - See AI citizens as sprites moving around
🗺️ **Tile-based world** - Procedurally generated city maps
🎮 **Game-like controls** - Arrow keys to move, SPACE to interact

### Launch:
```bash
cd ~/AI_City_Experiment
./launch_with_tuxemon_ui.sh
```

Or with custom citizen count:
```bash
python launch_tuxemon_civilization.py --citizens 30
```

### Controls:
- **Arrow Keys** - Move your character around the city
- **SPACE / ENTER** - Interact with NPCs (talk to AI citizens!)
- **ESC** - Open menu
- **Mouse** - Click to interact

### Requirements:
- Pygame (installed automatically)
- Display (works on VNC or Android X11)

---

## 📊 Option 2: Terminal/Text UI

**Fast, lightweight, text-based simulation - works anywhere!**

### Features:
⚡ **Super fast** - No graphics overhead
📈 **Real-time stats** - Live NPC statistics and graphs
📱 **Works everywhere** - No display needed
🔋 **Battery friendly** - Minimal resource usage
📊 **Detailed metrics** - Performance monitoring

### Launch:
```bash
cd ~/AI_City_Experiment
./launch_termux.sh
```

Or with custom parameters:
```bash
python main_headless.py --npc-count 15 --grid-size 256 --duration 120
```

### What You See:
```
NPC STATISTICS:
WALKING        : ██████████ (10)
IDLE           : ███ (3)

PERFORMANCE:
Total Ticks: 453
Ticks/Second: 14.3

SAMPLE NPC (ID: 0):
Type: GUARD
Position: (91.7, 121.9)
Energy: █████████- 99.5%
```

---

## 🏆 Which Should You Choose?

### Choose **Tuxemon UI** if you want:
✅ Visual experience
✅ Game-like exploration
✅ To see NPCs moving around
✅ Beautiful 2D graphics
✅ Interactive gameplay

### Choose **Terminal UI** if you want:
✅ Maximum performance
✅ No display setup needed
✅ Detailed statistics
✅ Battery efficiency
✅ Works on any device

---

## 🎯 Quick Comparison

| Feature | Tuxemon UI | Terminal UI |
|---------|------------|-------------|
| Graphics | ✅ Full 2D | ❌ Text only |
| Speed | ⚡ Fast | ⚡⚡ Very Fast |
| Battery | 🔋🔋 Medium | 🔋🔋🔋 Low |
| Stats | Basic | Detailed |
| Controls | Arrow keys | Automatic |
| Display | Required | Optional |
| File Size | ~300MB | ~180MB |

---

## 📱 Home Screen Widgets

Both UIs have dedicated widgets:

### Tuxemon GUI Widget:
```
Add widget: "AI-City-GUI"
```

### Terminal Widget:
```
Add widget: "AI-City"
```

---

## 🔧 Setup Display for Tuxemon UI

If you want to use the Tuxemon UI, you need a display:

### Method 1: VNC (Recommended)
```bash
# Install VNC
pkg install x11-repo tigervnc

# Set password
vncpasswd

# Start VNC
vncserver :1 -geometry 1280x720

# Connect with VNC Viewer app to localhost:5901
```

### Method 2: Termux:X11
```bash
# Install from GitHub or F-Droid
# Follow Termux:X11 setup guide
```

---

## 🎮 Running Both UIs

You can switch between UIs anytime:

```bash
# Terminal UI (quick test)
./launch_termux.sh

# Tuxemon UI (full experience)
./launch_with_tuxemon_ui.sh
```

---

## 💡 Pro Tips

### For Best Tuxemon Experience:
1. Use VNC for larger screen
2. Start with 20 citizens
3. Interact with NPCs to see AI personalities
4. Explore the procedurally generated city

### For Best Terminal Experience:
1. Use landscape orientation
2. Adjust NPC count for performance
3. Monitor statistics in real-time
4. Great for testing/debugging

---

## 🐛 Troubleshooting

### Tuxemon UI Issues:

**Black screen:**
```bash
# Make sure VNC is running
vncserver :1

# Check display variable
echo $DISPLAY
```

**NPCs not spawning:**
```bash
# Wait ~10 seconds after map loads
# Citizens spawn automatically
```

**Slow performance:**
```bash
# Reduce citizens
python launch_tuxemon_civilization.py --citizens 10
```

### Terminal UI Issues:

**Output too fast:**
```bash
# Increase duration, reduce NPCs
python main_headless.py --npc-count 5 --duration 30
```

---

## 🎨 Customization

### Tuxemon UI:
- Edit `mods/ai_civilization/` for custom NPCs
- Modify `launch_tuxemon_civilization.py` for spawn settings
- Create custom maps in Tuxemon editor

### Terminal UI:
- Edit `config_android.py` for simulation settings
- Modify `main_headless.py` for display options
- Adjust parameters via command line

---

## 📚 Learn More

- `README_ANDROID.md` - Full Android guide
- `TUXEMON_README.md` - Tuxemon integration details
- `AI_CIVILIZATION_README.md` - AI systems documentation

---

**🎉 Enjoy your AI City in whichever way you prefer!**

Crafted by Intellegix
