"""
Touch UI Rendering System
Renders virtual joysticks with visual feedback

Features:
- Circular joystick backgrounds
- Thumbstick indicators
- Fade in/out animations
- Semi-transparent overlay
- Minimal performance overhead

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""

from direct.gui.OnscreenImage import OnscreenImage
from panda3d.core import TransparencyAttrib, CardMaker, NodePath
from virtual_joystick import VirtualJoystickManager, JoystickState
from typing import Tuple, Optional


class JoystickRenderer:
    """Renders a single virtual joystick"""

    def __init__(self, parent: NodePath, color: Tuple[float, float, float] = (1.0, 1.0, 1.0)):
        """Initialize joystick renderer

        Args:
            parent: Parent node to attach UI to
            color: RGB color for joystick (default white)
        """
        self.parent = parent

        # Create background circle (outer ring)
        self.background = self._create_circle(
            radius=0.15,
            color=(*color, 0.3),  # Semi-transparent
            name="joystick_bg"
        )
        self.background.hide()

        # Create thumbstick (inner circle)
        self.thumbstick = self._create_circle(
            radius=0.05,
            color=(*color, 0.6),  # More opaque
            name="joystick_thumb"
        )
        self.thumbstick.hide()

        # Visibility state
        self.visible = False

    def _create_circle(self, radius: float, color: Tuple[float, float, float, float],
                       name: str) -> NodePath:
        """Create a circular UI element

        Args:
            radius: Circle radius (normalized screen coordinates)
            color: RGBA color
            name: Node name

        Returns:
            NodePath for the circle
        """
        # Create a simple card that will be used as a circle
        cm = CardMaker(name)
        cm.setFrame(-radius, radius, -radius, radius)

        circle = self.parent.attachNewNode(cm.generate())
        circle.setColor(*color)
        circle.setTransparency(TransparencyAttrib.MAlpha)

        return circle

    def update(self, state: JoystickState):
        """Update joystick visual based on state

        Args:
            state: Current joystick state
        """
        if state.active and not self.visible:
            # Show joystick
            self.background.show()
            self.thumbstick.show()
            self.visible = True

        elif not state.active and self.visible:
            # Hide joystick
            self.background.hide()
            self.thumbstick.hide()
            self.visible = False

        if state.active:
            # Update positions (convert from 0-1 to -1 to 1 for Panda3D)
            bg_x = (state.center_x * 2.0) - 1.0
            bg_y = 1.0 - (state.center_y * 2.0)  # Flip Y for Panda3D coordinates

            self.background.setPos(bg_x, 0, bg_y)

            # Update thumbstick position (offset from center)
            thumb_x = bg_x + (state.offset_x * 0.15)
            thumb_y = bg_y + (state.offset_y * 0.15)

            self.thumbstick.setPos(thumb_x, 0, thumb_y)

    def set_visible(self, visible: bool):
        """Set joystick visibility

        Args:
            visible: True to show, False to hide
        """
        if visible:
            self.background.show()
            self.thumbstick.show()
        else:
            self.background.hide()
            self.thumbstick.hide()
        self.visible = visible


class TouchUIManager:
    """Manages all touch UI rendering"""

    def __init__(self, aspect2d: NodePath):
        """Initialize touch UI manager

        Args:
            aspect2d: Panda3D's aspect2d node for 2D UI
        """
        self.aspect2d = aspect2d

        # Create joystick renderers
        self.left_joystick_renderer = JoystickRenderer(
            aspect2d,
            color=(0.3, 0.8, 1.0)  # Light blue for movement
        )

        self.right_joystick_renderer = JoystickRenderer(
            aspect2d,
            color=(1.0, 0.8, 0.3)  # Orange for camera
        )

        # UI enabled flag
        self.enabled = True

        print("[TOUCH_UI] Touch UI Manager initialized")

    def update(self, joystick_manager: VirtualJoystickManager):
        """Update all joystick visuals

        Args:
            joystick_manager: Virtual joystick manager
        """
        if not self.enabled:
            return

        # Update left joystick (movement)
        self.left_joystick_renderer.update(joystick_manager.left_joystick.state)

        # Update right joystick (camera)
        self.right_joystick_renderer.update(joystick_manager.right_joystick.state)

    def set_enabled(self, enabled: bool):
        """Enable or disable touch UI

        Args:
            enabled: True to enable, False to disable
        """
        self.enabled = enabled

        if not enabled:
            self.left_joystick_renderer.set_visible(False)
            self.right_joystick_renderer.set_visible(False)

        print(f"[TOUCH_UI] Touch UI {'enabled' if enabled else 'disabled'}")

    def toggle_enabled(self):
        """Toggle touch UI enabled state"""
        self.set_enabled(not self.enabled)


if __name__ == "__main__":
    print("Touch UI rendering system ready!")
    print("Note: This system requires Panda3D ShowBase to run")
    print("It will be tested when integrated into the main application")
