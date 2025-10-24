"""
Professional Gamer-Quality HUD System
Minimalist, color-coded FPS meter with GTA/Forza-inspired styling

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""

from direct.gui.OnscreenText import OnscreenText
from panda3d.core import TextNode
from config import UI


class GamerHUD:
    """
    Professional minimal HUD with color-coded FPS meter.
   
    Features:
    - Color-coded FPS (Green >50, Yellow 30-50, Red <30)
    - Minimal design (GTA/Forza style)
    - Optimized updates (0.5s interval to reduce overhead)
    - Toggle visibility with F key
    """
   
    def __init__(self, enable_hud=True):
        self.visible = enable_hud
        self.update_interval = 0.5  # Update every 0.5s for performance
        self.time_since_update = 0.0
        self.current_fps = 60  # Default value
       
        # FPS meter with color coding (top-left corner)
        self.fps_text = OnscreenText(
            text="60 FPS",
            pos=(-1.3, 0.88),
            scale=0.05,
            fg=(0.2, 1.0, 0.2, UI.HUD_OPACITY),  # Green by default
            align=TextNode.ALeft,
            mayChange=True
        )
       
        # Camera mode indicator (below FPS)
        self.mode_text = OnscreenText(
            text="MODE: SPECTATOR",
            pos=(-1.3, 0.82),
            scale=0.045,
            fg=(1, 1, 1, UI.HUD_OPACITY),
            align=TextNode.ALeft,
            mayChange=True
        )
       
        # Optional debug info (position, heading - bottom-left)
        self.debug_text = OnscreenText(
            text="",
            pos=(-1.3, -0.95),
            scale=0.04,
            fg=(0.8, 0.8, 0.8, UI.HUD_OPACITY * 0.7),
            align=TextNode.ALeft,
            mayChange=True
        )
       
        # Hide all if not visible
        if not self.visible:
            self.hide()
   
    def update(self, dt: float, current_fps: int, camera_mode: str = "SPECTATOR",
               debug_info: dict = None):
        """
        Update HUD elements.
       
        Args:
            dt: Delta time since last frame
            current_fps: Current frames per second
            camera_mode: Current camera mode string
            debug_info: Optional dict with keys: pos_x, pos_y, pos_z, heading
        """
        if not self.visible:
            return
           
        self.time_since_update += dt
       
        # Only update at specified interval to reduce overhead
        if self.time_since_update >= self.update_interval:
            self.time_since_update = 0.0
            self.current_fps = current_fps
           
            # Update FPS text
            self.fps_text.setText(f"{current_fps} FPS")
           
            # Color code based on performance
            if current_fps >= UI.FPS_COLOR_GREEN_THRESHOLD:  # 50+
                self.fps_text['fg'] = (0.2, 1.0, 0.2, UI.HUD_OPACITY)  # Green
            elif current_fps >= UI.FPS_COLOR_YELLOW_THRESHOLD:  # 30-50
                self.fps_text['fg'] = (1.0, 0.8, 0.2, UI.HUD_OPACITY)  # Yellow
            else:  # <30
                self.fps_text['fg'] = (1.0, 0.2, 0.2, UI.HUD_OPACITY)  # Red
           
            # Update mode indicator
            self.mode_text.setText(f"MODE: {camera_mode.upper()}")
           
            # Update debug info if provided
            if debug_info and UI.SHOW_DEBUG_INFO:
                debug_str = f"POS: ({debug_info.get('pos_x', 0):.1f}, " \
                           f"{debug_info.get('pos_y', 0):.1f}, " \
                           f"{debug_info.get('pos_z', 0):.1f}) | " \
                           f"HDG: {debug_info.get('heading', 0):.0f}°"
                self.debug_text.setText(debug_str)
            elif not UI.SHOW_DEBUG_INFO:
                self.debug_text.setText("")
   
    def set_mode(self, mode: str):
        """Update camera mode text."""
        if self.visible:
            self.mode_text.setText(f"MODE: {mode.upper()}")
   
    def toggle_visibility(self):
        """Toggle HUD visibility (F key)."""
        self.visible = not self.visible
        if self.visible:
            self.show()
        else:
            self.hide()
   
    def show(self):
        """Show all HUD elements."""
        self.visible = True
        self.fps_text.show()
        self.mode_text.show()
        if UI.SHOW_DEBUG_INFO:
            self.debug_text.show()
   
    def hide(self):
        """Hide all HUD elements."""
        self.visible = False
        self.fps_text.hide()
        self.mode_text.hide()
        self.debug_text.hide()
   
    def cleanup(self):
        """Clean up HUD resources."""
        self.fps_text.destroy()
        self.mode_text.destroy()
        self.debug_text.destroy()


# Example usage in main app
if __name__ == "__main__":
    print("GamerHUD Module")
    print("Import this in your main world file and create instance:")
    print("  from gamer_hud import GamerHUD")
    print("  self.hud = GamerHUD(enable_hud=True)")
    print("\nIn update loop:")
    print("  self.hud.update(dt, current_fps, camera_mode)")
    print("\nKey bindings:")
    print("  F: Toggle HUD visibility")
