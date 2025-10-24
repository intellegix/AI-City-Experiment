# Xbox Controller Guide - 3D GTA Style

**Full Xbox controller support for immersive 3D exploration!**

**Crafted by Intellegix** | Licensed under Apache 2.0

---

## 🎮 Controller Layout

```
        [LB]                    [RB]
   (Zoom Out)              (Zoom In)

    [LT]                        [RT]
(Zoom Out Gradual)      (Zoom In Gradual)

    [Left Stick]           [Right Stick]
  (Move Player)          (Rotate Camera + Zoom)

         [D-Pad]         [Y]
                     [X]   [B]
                         [A]

      [View]  [Start]
              (Pause - Future)
```

---

## 🕹️ Controls

### Player Movement (GTA Style)

**Left Analog Stick:**
- **Up** - Move forward (relative to camera)
- **Down** - Move backward
- **Left** - Strafe left
- **Right** - Strafe right

*Movement is camera-relative, just like GTA V!*

---

### Camera Control

**Right Analog Stick (Horizontal):**
- **Left** - Rotate camera left around player
- **Right** - Rotate camera right around player

**Right Analog Stick (Vertical):**
- **Up** - Zoom in
- **Down** - Zoom out

**Bumpers (Discrete Zoom):**
- **LB** - Zoom out quickly
- **RB** - Zoom in quickly

**Triggers (Smooth Zoom):**
- **LT** - Gradual zoom out
- **RT** - Gradual zoom in

---

## 🎯 Pro Tips

### For Best GTA-Style Experience:

1. **Use Left Stick** for all movement
   - Smooth analog control like driving in GTA
   - Camera follows automatically

2. **Use Right Stick Horizontal** for camera rotation
   - Look around your character
   - Explore the city from all angles

3. **Use Triggers** for smooth zoom
   - LT to pull back (overview)
   - RT to get closer (details)

4. **Combine Controls** for dynamic exploration
   - Move with left stick while rotating camera with right stick
   - Zoom with triggers while moving

---

## 📋 Complete Control Mapping

| Input | Action | Notes |
|-------|--------|-------|
| **Left Stick** | Move player | Camera-relative (like GTA) |
| **Right Stick (Horizontal)** | Rotate camera | 360° rotation around player |
| **Right Stick (Vertical)** | Zoom camera | Smooth analog zoom |
| **LT** | Zoom out (gradual) | Pressure-sensitive |
| **RT** | Zoom in (gradual) | Pressure-sensitive |
| **LB** | Zoom out (discrete) | Quick zoom step |
| **RB** | Zoom in (discrete) | Quick zoom step |
| **D-Pad** | Future features | Reserved |
| **A/B/X/Y** | Future features | Reserved |
| **Start** | Future: Pause menu | Coming soon |

---

## ⚙️ Sensitivity Settings

### Current Defaults:
- **Movement Speed**: 1.5x (faster than keyboard)
- **Camera Rotation**: 120°/second
- **Zoom Speed**: 15 units/second (right stick)
- **Trigger Zoom**: 10 units/second
- **Bumper Zoom**: 3 units/step

### To Adjust (edit world_3d.py):

**Movement Speed (line 429):**
```python
pos.x += speed * (...) * 1.5  # Change 1.5 to your preference
```

**Camera Rotation (line 450):**
```python
self.camera_angle -= stick_x * 120 * dt  # Change 120 for faster/slower
```

**Zoom Sensitivity (line 455):**
```python
zoom_delta = -stick_y * 15 * dt  # Change 15 for sensitivity
```

---

## 🔧 Connection Methods

### Bluetooth (Wireless)
1. Press **Xbox button + Pairing button** on controller
2. Go to Windows **Settings > Bluetooth > Add device**
3. Select **Xbox Wireless Controller**
4. Launch simulation - controller detected automatically!

### USB (Wired)
1. Plug controller into USB port
2. Launch simulation - controller works instantly!

---

## 🎨 Camera Behaviors

### Follow Camera
The camera **always follows** your player character, maintaining:
- **Distance**: 5-30 units (adjustable with zoom)
- **Height**: 8 units above player
- **Smooth movement**: No jittering

### Rotation
- **Full 360° rotation** around player
- **Smooth interpolation** for natural camera movement
- **No collision** - camera passes through buildings (for now)

---

## 🆚 Keyboard vs Controller

| Feature | Keyboard | Controller |
|---------|----------|------------|
| **Movement** | Digital (WASD) | Analog (smooth) ✨ |
| **Camera Rotation** | Q/E keys | Right stick ✨ |
| **Zoom** | Mouse wheel | Triggers + Right stick ✨ |
| **Speed** | Standard | 1.5x faster ✨ |
| **Feel** | Precise | Immersive GTA-style ⭐ |

**Controller is recommended for the full GTA experience!**

---

## 🌟 GTA V Comparison

This 3D simulation's controls match GTA V:

| GTA V | AI City 3D |
|-------|------------|
| Left stick = Move | ✅ Same |
| Right stick = Camera | ✅ Same |
| Triggers = Not used | Used for zoom |
| Running | Always running (no sprint) |

The main difference: GTA V doesn't use triggers for zoom, but we added it for convenience!

---

## 🐛 Troubleshooting

### Controller Not Detected

**Symptom:** Console says "No Xbox controller detected"

**Solutions:**
1. Check Bluetooth connection in Windows settings
2. Try USB cable connection
3. Press Xbox button to wake controller
4. Restart simulation after connecting controller

### Controller Connected But Not Working

**Symptom:** Controller shown as connected but no movement

**Solutions:**
1. Check battery level (low battery = poor response)
2. Try pressing buttons to "wake" the controller
3. Reconnect via Bluetooth/USB
4. Close other programs using controller (Steam, etc.)

### Movement in Wrong Direction

**Explanation:** Movement is **camera-relative**, not world-relative.
- When camera faces north, left stick up = north
- When camera faces east, left stick up = east

**This is intentional GTA-style behavior!**

### Camera Rotation Too Fast/Slow

**Solution:** Adjust sensitivity in `world_3d.py` line 450:
```python
self.camera_angle -= stick_x * 120 * dt  # Default: 120
# Try: 60 (slower), 180 (faster)
```

---

## 🎮 Future Controller Features

Planned additions:
- [ ] **Start button** - Pause menu
- [ ] **D-Pad** - Quick camera angles
- [ ] **Y button** - Toggle debug overlay
- [ ] **Rumble feedback** - On collisions
- [ ] **Analog acceleration** - Walk vs run speed
- [ ] **Vehicle controls** (when vehicles added)

---

## 📊 Technical Details

### Input Polling
- **Rate**: 60 Hz (every frame)
- **Latency**: ~16ms (one frame)
- **Dead Zone**: 15% (prevents drift)

### Analog Precision
- **Sticks**: -1.0 to 1.0 (normalized)
- **Triggers**: 0.0 to 1.0 (0% to 100%)
- **Dead zone applied** to prevent stick drift

---

## ✨ Pro Gameplay Tips

1. **Smooth Exploration**
   - Use gentle stick movements for cinematic camera
   - Pull triggers gradually for smooth zooms

2. **Fast Navigation**
   - Push left stick fully for max speed
   - Rotate camera while moving for dynamic views

3. **City Survey**
   - Zoom out with LT
   - Rotate 360° with right stick
   - Watch NPCs from above

4. **Detail Inspection**
   - Zoom in with RT
   - Get close to buildings
   - Observe NPC behaviors

---

## 🎯 Ready to Play?

**Launch the 3D simulation:**
```bash
python world_3d.py --size 64
```

**Or double-click:** `launch_3d.bat`

**Then:**
1. Connect Xbox controller (Bluetooth or USB)
2. See "Xbox Controller Connected!" message
3. Use left stick to move, right stick to look
4. Explore your GTA-style AI city!

---

**Enjoy the immersive GTA-style controller experience!**

**Crafted by Intellegix** - https://intellegix.ai

*Apache License 2.0 | See LICENSE and NOTICE files*
