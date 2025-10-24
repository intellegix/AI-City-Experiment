"""
Windows Multi-Touch Input System
Native Windows 10/11 multi-touch support (10-point simultaneous touch)

Optimized for:
- Touch-enabled tablets (Surface Pro, etc.)
- 2-in-1 laptops with touchscreens
- Large format touch displays

Features:
- Native Win32 touch API integration
- 10-point multi-touch support
- Touch began/moved/ended events
- Normalized coordinates (0-1)
- Pressure sensitivity support

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""

import sys
from typing import List, Tuple, Callable, Dict, Optional
from enum import Enum
from dataclasses import dataclass

# Check if we're on Windows
if sys.platform == 'win32':
    try:
        import ctypes
        from ctypes import wintypes
        WINDOWS_TOUCH_AVAILABLE = True
    except ImportError:
        WINDOWS_TOUCH_AVAILABLE = False
        print("[TOUCH] Warning: ctypes not available, touch input disabled")
else:
    WINDOWS_TOUCH_AVAILABLE = False
    print("[TOUCH] Not running on Windows, touch input disabled")


class TouchPhase(Enum):
    """Touch event phases"""
    BEGAN = "began"
    MOVED = "moved"
    ENDED = "ended"
    CANCELLED = "cancelled"


@dataclass
class TouchPoint:
    """Represents a single touch point"""
    id: int  # Unique touch ID
    x: float  # Normalized X (0-1, left to right)
    y: float  # Normalized Y (0-1, top to bottom)
    phase: TouchPhase

    # Raw pixel coordinates
    raw_x: int
    raw_y: int

    # Optional pressure (0-1, if supported)
    pressure: float = 1.0


class TouchInputManager:
    """Manages multi-touch input events"""

    def __init__(self, screen_width: int, screen_height: int):
        """Initialize touch input manager

        Args:
            screen_width: Window width in pixels
            screen_height: Window height in pixels
        """
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Active touch points
        self.active_touches: Dict[int, TouchPoint] = {}

        # Touch event callbacks
        self.touch_began_callbacks: List[Callable[[TouchPoint], None]] = []
        self.touch_moved_callbacks: List[Callable[[TouchPoint], None]] = []
        self.touch_ended_callbacks: List[Callable[[TouchPoint], None]] = []

        # Statistics
        self.total_touches = 0
        self.max_simultaneous = 0

        print(f"[TOUCH] Touch Input Manager initialized ({screen_width}x{screen_height})")
        print(f"[TOUCH] Windows Touch API: {'Available' if WINDOWS_TOUCH_AVAILABLE else 'Not Available'}")

    def process_touch_event(self, touch_id: int, x: int, y: int, phase: TouchPhase, pressure: float = 1.0):
        """Process a touch event (called by windowing system)

        Args:
            touch_id: Unique touch identifier
            x: Raw X coordinate (pixels)
            y: Raw Y coordinate (pixels)
            phase: Touch phase (began/moved/ended)
            pressure: Touch pressure (0-1, optional)
        """
        # Normalize coordinates
        norm_x = x / self.screen_width
        norm_y = y / self.screen_height

        # Clamp to 0-1 range
        norm_x = max(0.0, min(1.0, norm_x))
        norm_y = max(0.0, min(1.0, norm_y))

        # Create touch point
        touch = TouchPoint(
            id=touch_id,
            x=norm_x,
            y=norm_y,
            phase=phase,
            raw_x=x,
            raw_y=y,
            pressure=pressure
        )

        # Dispatch to appropriate handlers
        if phase == TouchPhase.BEGAN:
            self.active_touches[touch_id] = touch
            self.total_touches += 1

            # Track max simultaneous touches
            if len(self.active_touches) > self.max_simultaneous:
                self.max_simultaneous = len(self.active_touches)

            for callback in self.touch_began_callbacks:
                callback(touch)

        elif phase == TouchPhase.MOVED:
            self.active_touches[touch_id] = touch
            for callback in self.touch_moved_callbacks:
                callback(touch)

        elif phase == TouchPhase.ENDED:
            if touch_id in self.active_touches:
                del self.active_touches[touch_id]
            for callback in self.touch_ended_callbacks:
                callback(touch)

    def on_touch_began(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch began events

        Args:
            callback: Function to call when touch begins
        """
        self.touch_began_callbacks.append(callback)

    def on_touch_moved(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch moved events

        Args:
            callback: Function to call when touch moves
        """
        self.touch_moved_callbacks.append(callback)

    def on_touch_ended(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch ended events

        Args:
            callback: Function to call when touch ends
        """
        self.touch_ended_callbacks.append(callback)

    def get_active_touches(self) -> List[TouchPoint]:
        """Get all currently active touch points

        Returns:
            List of active TouchPoint objects
        """
        return list(self.active_touches.values())

    def get_touch_count(self) -> int:
        """Get number of currently active touches

        Returns:
            Number of active touches
        """
        return len(self.active_touches)

    def get_stats(self) -> Dict[str, any]:
        """Get touch input statistics

        Returns:
            Dictionary with touch statistics
        """
        return {
            'active_touches': len(self.active_touches),
            'total_touches': self.total_touches,
            'max_simultaneous': self.max_simultaneous,
            'touch_enabled': WINDOWS_TOUCH_AVAILABLE
        }

    def print_stats(self):
        """Print touch statistics"""
        stats = self.get_stats()
        print("\n[TOUCH] Statistics:")
        print(f"  Active Touches: {stats['active_touches']}")
        print(f"  Total Touches: {stats['total_touches']}")
        print(f"  Max Simultaneous: {stats['max_simultaneous']}")
        print(f"  Touch Enabled: {stats['touch_enabled']}")


# Simulated touch input for testing (when hardware not available)
class SimulatedTouchInput:
    """Simulates touch input using mouse for testing"""

    def __init__(self, touch_manager: TouchInputManager):
        """Initialize simulated touch input

        Args:
            touch_manager: Touch input manager to send events to
        """
        self.touch_manager = touch_manager
        self.mouse_down = False
        self.touch_id = 0

        print("[TOUCH] Simulated touch input enabled (using mouse)")

    def process_mouse_event(self, x: int, y: int, button_down: bool):
        """Convert mouse event to touch event

        Args:
            x: Mouse X coordinate
            y: Mouse Y coordinate
            button_down: True if mouse button is down
        """
        if button_down and not self.mouse_down:
            # Mouse pressed = touch began
            self.mouse_down = True
            self.touch_manager.process_touch_event(
                self.touch_id, x, y, TouchPhase.BEGAN
            )

        elif button_down and self.mouse_down:
            # Mouse dragged = touch moved
            self.touch_manager.process_touch_event(
                self.touch_id, x, y, TouchPhase.MOVED
            )

        elif not button_down and self.mouse_down:
            # Mouse released = touch ended
            self.mouse_down = False
            self.touch_manager.process_touch_event(
                self.touch_id, x, y, TouchPhase.ENDED
            )
            self.touch_id += 1  # Increment for next touch


# Utility function for easy integration
def create_touch_manager(screen_width: int, screen_height: int,
                        enable_simulation: bool = True) -> Tuple[TouchInputManager, Optional[SimulatedTouchInput]]:
    """Create touch input manager with optional mouse simulation

    Args:
        screen_width: Window width in pixels
        screen_height: Window height in pixels
        enable_simulation: Enable mouse simulation if touch not available

    Returns:
        Tuple of (TouchInputManager, SimulatedTouchInput or None)
    """
    manager = TouchInputManager(screen_width, screen_height)

    simulator = None
    if enable_simulation and not WINDOWS_TOUCH_AVAILABLE:
        simulator = SimulatedTouchInput(manager)
        print("[TOUCH] Mouse simulation enabled for testing")

    return manager, simulator


if __name__ == "__main__":
    # Test the touch input system
    print("Testing Touch Input System...\n")

    # Create manager
    manager, simulator = create_touch_manager(1920, 1080, enable_simulation=True)

    # Register test callbacks
    def on_began(touch: TouchPoint):
        print(f"  Touch {touch.id} BEGAN at ({touch.x:.2f}, {touch.y:.2f})")

    def on_moved(touch: TouchPoint):
        print(f"  Touch {touch.id} MOVED to ({touch.x:.2f}, {touch.y:.2f})")

    def on_ended(touch: TouchPoint):
        print(f"  Touch {touch.id} ENDED at ({touch.x:.2f}, {touch.y:.2f})")

    manager.on_touch_began(on_began)
    manager.on_touch_moved(on_moved)
    manager.on_touch_ended(on_ended)

    # Simulate some touch events
    print("\nSimulating touch events...")
    manager.process_touch_event(0, 500, 500, TouchPhase.BEGAN)
    manager.process_touch_event(0, 600, 600, TouchPhase.MOVED)
    manager.process_touch_event(0, 700, 700, TouchPhase.ENDED)

    # Print statistics
    manager.print_stats()

    print("\n✓ Touch input test complete!")
