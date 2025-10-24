"""
Virtual On-Screen Joysticks for Touch Input
Fortnite Mobile-style dynamic positioning

Features:
- Left joystick: Movement (spawns where finger touches left half of screen)
- Right joystick: Camera rotation (spawns where finger touches right half)
- Visual feedback with circular UI
- Dead zone support
- Dynamic repositioning on each touch
- Returns normalized input values (-1 to 1)

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""

from typing import Tuple, Optional
from dataclasses import dataclass
import math
from touch_input import TouchPoint, TouchPhase


@dataclass
class JoystickState:
    """Current state of a virtual joystick"""
    active: bool = False
    center_x: float = 0.0  # Normalized (0-1)
    center_y: float = 0.0  # Normalized (0-1)
    offset_x: float = 0.0  # Normalized offset from center
    offset_y: float = 0.0  # Normalized offset from center
    magnitude: float = 0.0  # 0-1 (1 = max deflection)
    angle: float = 0.0  # Radians


class VirtualJoystick:
    """Virtual joystick for touch input"""

    def __init__(self, max_radius: float = 0.1, dead_zone: float = 0.02):
        """Initialize virtual joystick

        Args:
            max_radius: Maximum joystick radius (normalized screen units, 0-1)
            dead_zone: Dead zone threshold (0-1, no input below this)
        """
        self.max_radius = max_radius
        self.dead_zone = dead_zone
        self.state = JoystickState()

        # Touch tracking
        self.touch_id: Optional[int] = None

    def touch_began(self, touch: TouchPoint):
        """Handle touch begin event

        Args:
            touch: Touch point
        """
        if self.state.active:
            return  # Already have a touch

        self.touch_id = touch.id
        self.state.active = True
        self.state.center_x = touch.x
        self.state.center_y = touch.y
        self.state.offset_x = 0
        self.state.offset_y = 0
        self.state.magnitude = 0
        self.state.angle = 0

    def touch_moved(self, touch: TouchPoint):
        """Handle touch move event

        Args:
            touch: Touch point
        """
        if not self.state.active or touch.id != self.touch_id:
            return

        # Calculate offset from center
        dx = touch.x - self.state.center_x
        dy = touch.y - self.state.center_y

        # Calculate magnitude and clamp to max_radius
        raw_magnitude = math.sqrt(dx**2 + dy**2)

        if raw_magnitude > self.max_radius:
            # Clamp to circle
            angle = math.atan2(dy, dx)
            dx = math.cos(angle) * self.max_radius
            dy = math.sin(angle) * self.max_radius
            raw_magnitude = self.max_radius

        # Apply dead zone
        if raw_magnitude < self.dead_zone:
            self.state.magnitude = 0
            self.state.offset_x = 0
            self.state.offset_y = 0
            self.state.angle = 0
        else:
            # Normalize magnitude (0 at dead zone, 1 at max_radius)
            self.state.magnitude = (raw_magnitude - self.dead_zone) / (self.max_radius - self.dead_zone)
            self.state.offset_x = dx / self.max_radius
            self.state.offset_y = dy / self.max_radius
            self.state.angle = math.atan2(dy, dx)

    def touch_ended(self, touch: TouchPoint):
        """Handle touch end event

        Args:
            touch: Touch point
        """
        if touch.id != self.touch_id:
            return

        self.state.active = False
        self.touch_id = None
        self.state.magnitude = 0
        self.state.offset_x = 0
        self.state.offset_y = 0

    def get_axis_x(self) -> float:
        """Get horizontal axis value

        Returns:
            X axis (-1 to 1, left to right)
        """
        return self.state.offset_x * self.state.magnitude if self.state.active else 0

    def get_axis_y(self) -> float:
        """Get vertical axis value

        Returns:
            Y axis (-1 to 1, up to down)
        """
        return self.state.offset_y * self.state.magnitude if self.state.active else 0

    def get_magnitude(self) -> float:
        """Get joystick deflection magnitude

        Returns:
            Magnitude (0 to 1)
        """
        return self.state.magnitude if self.state.active else 0


class VirtualJoystickManager:
    """Manages left and right virtual joysticks"""

    def __init__(self, split_position: float = 0.5):
        """Initialize joystick manager

        Args:
            split_position: Screen X position (0-1) that splits left/right regions
        """
        self.left_joystick = VirtualJoystick(max_radius=0.15, dead_zone=0.02)
        self.right_joystick = VirtualJoystick(max_radius=0.15, dead_zone=0.02)

        # Screen regions (left half vs right half)
        self.split_position = split_position

        print(f"[JOYSTICK] Virtual joystick manager initialized (split at {split_position:.1%})")

    def handle_touch_began(self, touch: TouchPoint):
        """Route touch to appropriate joystick

        Args:
            touch: Touch point
        """
        if touch.x < self.split_position:
            # Left side = movement joystick
            self.left_joystick.touch_began(touch)
        else:
            # Right side = camera joystick
            self.right_joystick.touch_began(touch)

    def handle_touch_moved(self, touch: TouchPoint):
        """Route touch movement to appropriate joystick

        Args:
            touch: Touch point
        """
        self.left_joystick.touch_moved(touch)
        self.right_joystick.touch_moved(touch)

    def handle_touch_ended(self, touch: TouchPoint):
        """Route touch end to appropriate joystick

        Args:
            touch: Touch point
        """
        self.left_joystick.touch_ended(touch)
        self.right_joystick.touch_ended(touch)

    def get_movement_input(self) -> Tuple[float, float]:
        """Get movement joystick input

        Returns:
            Tuple of (x, y) axes (-1 to 1)
        """
        return (
            self.left_joystick.get_axis_x(),
            self.left_joystick.get_axis_y()
        )

    def get_camera_input(self) -> Tuple[float, float]:
        """Get camera joystick input

        Returns:
            Tuple of (x, y) axes (-1 to 1)
        """
        return (
            self.right_joystick.get_axis_x(),
            self.right_joystick.get_axis_y()
        )

    def get_movement_magnitude(self) -> float:
        """Get movement joystick magnitude

        Returns:
            Magnitude (0 to 1)
        """
        return self.left_joystick.get_magnitude()

    def get_camera_magnitude(self) -> float:
        """Get camera joystick magnitude

        Returns:
            Magnitude (0 to 1)
        """
        return self.right_joystick.get_magnitude()

    def is_movement_active(self) -> bool:
        """Check if movement joystick is active

        Returns:
            True if movement joystick is being touched
        """
        return self.left_joystick.state.active

    def is_camera_active(self) -> bool:
        """Check if camera joystick is active

        Returns:
            True if camera joystick is being touched
        """
        return self.right_joystick.state.active


if __name__ == "__main__":
    # Test the virtual joystick system
    print("Testing Virtual Joystick System...\n")

    # Create manager
    manager = VirtualJoystickManager()

    # Simulate left joystick (movement)
    print("Simulating left joystick input (movement)...")

    # Touch begins at left side
    touch_began = TouchPoint(id=0, x=0.25, y=0.5, phase=TouchPhase.BEGAN, raw_x=480, raw_y=540)
    manager.handle_touch_began(touch_began)
    print(f"  Touch began at ({touch_began.x}, {touch_began.y})")

    # Touch moves right and down
    touch_moved = TouchPoint(id=0, x=0.35, y=0.6, phase=TouchPhase.MOVED, raw_x=672, raw_y=648)
    manager.handle_touch_moved(touch_moved)
    move_x, move_y = manager.get_movement_input()
    print(f"  Touch moved to ({touch_moved.x}, {touch_moved.y})")
    print(f"  Movement input: ({move_x:.2f}, {move_y:.2f})")

    # Touch ends
    touch_ended = TouchPoint(id=0, x=0.35, y=0.6, phase=TouchPhase.ENDED, raw_x=672, raw_y=648)
    manager.handle_touch_ended(touch_ended)
    print(f"  Touch ended")

    # Simulate right joystick (camera)
    print("\nSimulating right joystick input (camera)...")

    # Touch begins at right side
    touch_began2 = TouchPoint(id=1, x=0.75, y=0.5, phase=TouchPhase.BEGAN, raw_x=1440, raw_y=540)
    manager.handle_touch_began(touch_began2)
    print(f"  Touch began at ({touch_began2.x}, {touch_began2.y})")

    # Touch moves
    touch_moved2 = TouchPoint(id=1, x=0.80, y=0.55, phase=TouchPhase.MOVED, raw_x=1536, raw_y=594)
    manager.handle_touch_moved(touch_moved2)
    cam_x, cam_y = manager.get_camera_input()
    print(f"  Touch moved to ({touch_moved2.x}, {touch_moved2.y})")
    print(f"  Camera input: ({cam_x:.2f}, {cam_y:.2f})")

    print("\n✓ Virtual joystick test complete!")
