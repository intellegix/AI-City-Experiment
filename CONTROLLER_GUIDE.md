# Xbox Controller Guide

The AI City Simulation now supports Xbox controllers via Bluetooth or USB! This guide will help you connect and use your controller.

**Crafted by Intellegix** | Licensed under Apache 2.0

## Supported Controllers

- Xbox One Controllers
- Xbox Series X|S Controllers
- Xbox 360 Controllers (USB only)
- Xbox Elite Controllers
- Compatible third-party Xbox controllers

PlayStation and Nintendo Switch controllers may also work but are not officially supported.

## Connecting Your Controller

### Bluetooth Connection (Windows)

1. **Put controller in pairing mode:**
   - Press and hold the **Xbox button** to turn on the controller
   - Press and hold the **Pairing button** (small button on top, near USB port) for 3 seconds
   - The Xbox button will flash rapidly when in pairing mode

2. **Connect via Windows:**
   - Go to **Settings > Bluetooth & devices**
   - Click **Add device**
   - Select **Bluetooth**
   - Select your **Xbox Wireless Controller** from the list
   - Wait for "Connected" message

3. **Run the simulation:**
   ```bash
   python main.py
   ```

4. **Verify connection:**
   - You should see "Xbox Controller Connected" in the console
   - Green "Controller: [Name]" text appears in the debug overlay

### USB Connection

Simply plug your controller into a USB port and run the simulation:
```bash
python main.py
```

The controller will be detected automatically!

### Bluetooth Connection (Linux)

```bash
# Install necessary packages
sudo apt-get install bluetooth bluez

# Put controller in pairing mode, then:
bluetoothctl
scan on
pair [CONTROLLER_MAC_ADDRESS]
connect [CONTROLLER_MAC_ADDRESS]
trust [CONTROLLER_MAC_ADDRESS]
```

### Bluetooth Connection (macOS)

1. Put controller in pairing mode
2. Open **System Preferences > Bluetooth**
3. Click **Connect** next to Xbox Wireless Controller
4. Run the simulation

## Controller Layout

```
        [LB]                    [RB]

    [LT]                        [RT]

    [Left Stick]           [Right Stick]

         [D-Pad]         [Y]
                     [X]   [B]
                         [A]

      [View]  [Menu]
       [Xbox]  [Share]
```

## Controls

### Camera Movement
- **Left Stick** - Move camera smoothly in any direction
- **D-Pad** - Move camera discretely (4 directions)
- **WASD Keys** - Keyboard alternative

### Zoom
- **Right Stick (Up/Down)** - Zoom in/out
- **Left Trigger (LT)** - Zoom out
- **Right Trigger (RT)** - Zoom in
- **Left Bumper (LB)** - Zoom out (discrete)
- **Right Bumper (RB)** - Zoom in (discrete)
- **Q/E Keys** - Keyboard alternative

### Simulation Controls
- **Start Button** - Pause/Resume simulation
- **Y Button** - Toggle debug overlay
- **View Button** - (Reserved for future features)
- **Space Key** - Keyboard pause alternative
- **D Key** - Keyboard debug toggle

### Exit
- **ESC Key** - Quit simulation (no controller button)

## Features

### Analog Precision
The left stick provides smooth, precise camera movement with:
- **Dead zone filtering** (15% by default) - No drift when stick is centered
- **Analog scaling** - Partial stick movement = slower camera
- **Full range** - Maximum stick deflection = fastest camera

### Multiple Input Methods
- **Analog sticks** for smooth movement
- **D-pad** for precise discrete movement
- **Bumpers** for quick zoom changes
- **Triggers** for gradual zoom control
- **Keyboard** works simultaneously (either input method works)

### Hot-Plugging
- **Connect anytime** - Plug in controller before or during simulation
- **Disconnect safely** - Controller can be removed without crashing
- **Auto-detection** - New controllers are detected automatically
- **Status display** - Green text shows connected controller name

### Rumble Support
Rumble/vibration is supported on compatible controllers (feature can be expanded in future updates).

## Troubleshooting

### Controller Not Detected

**Problem:** "No controllers found" message

**Solutions:**
1. Make sure controller is on and in pairing mode
2. Check Bluetooth connection in system settings
3. Try USB connection instead
4. Restart simulation after connecting controller
5. Run the controller test:
   ```bash
   python controller_input.py
   ```

### Controller Connected But Not Working

**Problem:** Controller connected but inputs don't work

**Solutions:**
1. Check if controller is connected to another program
2. Restart the simulation
3. Try pressing different buttons to "wake" the controller
4. Check battery level (low battery can cause issues)

### Input Lag or Stuttering

**Problem:** Controller input feels delayed

**Solutions:**
1. Use USB connection instead of Bluetooth
2. Reduce distance between controller and PC
3. Check for Bluetooth interference (Wi-Fi, other devices)
4. Update controller firmware via Xbox Accessories app

### Wrong Controller Mapping

**Problem:** Buttons do wrong things

**Solutions:**
1. Some third-party controllers may have different mappings
2. Try official Xbox controller
3. Check controller compatibility
4. Update pygame: `pip install --upgrade pygame`

### Drift (Controller Moves on Its Own)

**Problem:** Camera moves when not touching controller

**Solutions:**
1. Increase dead zone in `controller_input.py`:
   ```python
   controller = XboxController(dead_zone=0.25)  # Default is 0.15
   ```
2. Calibrate controller in system settings
3. Clean analog sticks
4. Controller may be damaged - try different controller

## Advanced Configuration

### Adjust Dead Zone

Edit `controller_input.py` line 83:
```python
def __init__(self, controller_index: int = 0, dead_zone: float = 0.15):
```

Change `dead_zone` value:
- **0.10** - More sensitive (may drift)
- **0.15** - Default (good balance)
- **0.25** - Less sensitive (no drift, less precise)

### Adjust Controller Sensitivity

Edit `renderer.py` line 621:
```python
controller_vx = state.left_stick_x * camera_speed * 1.5  # Change 1.5
```

Increase value for faster camera movement, decrease for slower.

### Test Controller Inputs

Run the built-in controller test:
```bash
python controller_input.py
```

This shows:
- Connected controller name
- Active analog stick positions
- Button presses
- Trigger values
- D-pad state

Press buttons and move sticks to see live input values!

## Multiple Controllers

The system supports up to 4 controllers simultaneously:
- **Controller 1** - Controls camera
- **Controllers 2-4** - Reserved for future features (multiplayer, NPC control, etc.)

Only the first connected controller is used currently.

## Bluetooth Tips

### For Best Performance:
1. **Use 2.4GHz Wi-Fi** instead of 5GHz (less interference)
2. **Keep controller within 10 feet** of PC
3. **Remove obstacles** between controller and PC
4. **Update controller firmware** via Xbox Accessories app (Windows)
5. **Disable other Bluetooth devices** when gaming

### Battery Life:
- **Bluetooth**: 30-40 hours on 2x AA batteries
- **USB**: Unlimited (powered by cable)
- **Rechargeable battery pack**: 20-30 hours

## Controller Comparison

| Controller | Bluetooth | USB | Rumble | Tested |
|------------|-----------|-----|--------|--------|
| Xbox Series X/S | ✓ | ✓ | ✓ | ✓ |
| Xbox One | ✓ | ✓ | ✓ | ✓ |
| Xbox One S | ✓ | ✓ | ✓ | ✓ |
| Xbox 360 | ✗ | ✓ | ✓ | ✓ |
| Xbox Elite | ✓ | ✓ | ✓ | ✓ |
| Generic Xbox | Varies | ✓ | Varies | Varies |

## Example Session

1. **Start simulation:**
   ```bash
   python main.py --seed 42 --npcs 200
   ```

2. **Wait for world generation** (10-30 seconds)

3. **Connect controller:**
   - Hold Xbox + Pair buttons
   - Pair in Windows Bluetooth settings

4. **Verify connection:**
   - See "Xbox Controller Connected" in console
   - See green "Controller: Xbox Wireless Controller" in debug overlay

5. **Explore the city:**
   - Use left stick to move camera smoothly
   - Use triggers to zoom in and out
   - Press Start to pause/resume
   - Press Y to toggle debug info

6. **Enjoy!** The controller provides smooth, console-like experience for exploring your AI city.

## Technical Details

### Input Polling
- Controllers are polled at **60 Hz** (same as frame rate)
- Input lag: **~16ms** (one frame)
- Dead zone applied before processing

### Button States
- **Pressed** - Detected on frame button goes down
- **Held** - True while button remains down
- **Released** - Detected when button goes up

### Analog Values
- **Sticks**: -1.0 to 1.0 (normalized)
- **Triggers**: 0.0 to 1.0 (0% to 100%)
- **Dead zone**: Applied to both sticks and triggers

### Supported Events
```python
pygame.JOYDEVICEADDED   # Controller connected
pygame.JOYDEVICEREMOVED # Controller disconnected
pygame.JOYAXISMOTION    # Stick/trigger moved
pygame.JOYBUTTONDOWN    # Button pressed
pygame.JOYBUTTONUP      # Button released
pygame.JOYHATMOTION     # D-pad pressed
```

## Future Features

Planned controller enhancements:
- [ ] Haptic feedback for NPC interactions
- [ ] Adaptive triggers (on supported controllers)
- [ ] Controller profiles (save custom mappings)
- [ ] Multiplayer support (each player controls NPCs)
- [ ] NPC possession mode (control individual NPCs)
- [ ] Gyroscope support for camera tilt
- [ ] LED color customization
- [ ] Button remapping in-game

## Credits

Xbox controller support powered by:
- **Pygame** - Joystick/gamepad API
- **SDL2** - Low-level controller drivers
- **Xbox Wireless Protocol** - Microsoft's Bluetooth standard

Compatible with official Xbox Design Lab custom controllers!

---

**Need help?** Run the controller test: `python controller_input.py`

**Enjoy exploring your AI city with console-quality controls!**
