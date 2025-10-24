"""
Xbox Controller Input System
Supports Xbox controllers via Bluetooth or USB

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import pygame
from typing import Optional, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class ControllerButton(Enum):
    """Xbox controller button mappings"""
    A = 0
    B = 1
    X = 2
    Y = 3
    LB = 4  # Left bumper
    RB = 5  # Right bumper
    BACK = 6
    START = 7
    LEFT_STICK = 8
    RIGHT_STICK = 9


class ControllerAxis(Enum):
    """Xbox controller axis mappings"""
    LEFT_STICK_X = 0
    LEFT_STICK_Y = 1
    LEFT_TRIGGER = 2
    RIGHT_STICK_X = 3
    RIGHT_STICK_Y = 4
    RIGHT_TRIGGER = 5


@dataclass
class ControllerState:
    """Current state of controller inputs"""
    # Analog sticks
    left_stick_x: float = 0.0
    left_stick_y: float = 0.0
    right_stick_x: float = 0.0
    right_stick_y: float = 0.0

    # Triggers
    left_trigger: float = 0.0
    right_trigger: float = 0.0

    # D-pad
    dpad_x: int = 0
    dpad_y: int = 0

    # Buttons (pressed this frame)
    button_a: bool = False
    button_b: bool = False
    button_x: bool = False
    button_y: bool = False
    button_lb: bool = False
    button_rb: bool = False
    button_back: bool = False
    button_start: bool = False
    button_left_stick: bool = False
    button_right_stick: bool = False


class XboxController:
    """
    Xbox Controller handler with full button and axis support.

    Features:
    - Automatic controller detection
    - Bluetooth and USB support
    - Dead zone filtering
    - Button press detection
    - Rumble support (if available)
    """

    def __init__(self, controller_index: int = 0, dead_zone: float = 0.15):
        """
        Initialize Xbox controller.

        Args:
            controller_index: Controller device index (0 for first controller)
            dead_zone: Analog stick dead zone (0.0 to 1.0)
        """
        self.controller_index = controller_index
        self.dead_zone = dead_zone

        self.joystick: Optional[pygame.joystick.Joystick] = None
        self.connected = False
        self.state = ControllerState()

        # Button state tracking (for press/release detection)
        self.prev_buttons: Dict[int, bool] = {}

        # Try to connect
        self.connect()

    def connect(self) -> bool:
        """
        Connect to Xbox controller.

        Returns:
            True if connected successfully
        """
        try:
            pygame.joystick.init()

            # Check if controller exists
            if pygame.joystick.get_count() <= self.controller_index:
                self.connected = False
                return False

            # Initialize controller
            self.joystick = pygame.joystick.Joystick(self.controller_index)
            self.joystick.init()

            self.connected = True

            print(f"Xbox Controller Connected: {self.joystick.get_name()}")
            print(f"  Axes: {self.joystick.get_numaxes()}")
            print(f"  Buttons: {self.joystick.get_numbuttons()}")
            print(f"  Hats: {self.joystick.get_numhats()}")

            return True

        except pygame.error as e:
            print(f"Failed to connect controller: {e}")
            self.connected = False
            return False

    def disconnect(self):
        """Disconnect controller"""
        if self.joystick:
            self.joystick.quit()
            self.joystick = None
        self.connected = False
        print("Xbox Controller Disconnected")

    def update(self):
        """
        Update controller state.
        Should be called once per frame.
        """
        if not self.connected or not self.joystick:
            return

        try:
            # Update analog sticks
            if self.joystick.get_numaxes() >= 2:
                self.state.left_stick_x = self._apply_dead_zone(
                    self.joystick.get_axis(ControllerAxis.LEFT_STICK_X.value)
                )
                self.state.left_stick_y = self._apply_dead_zone(
                    self.joystick.get_axis(ControllerAxis.LEFT_STICK_Y.value)
                )

            if self.joystick.get_numaxes() >= 5:
                self.state.right_stick_x = self._apply_dead_zone(
                    self.joystick.get_axis(ControllerAxis.RIGHT_STICK_X.value)
                )
                self.state.right_stick_y = self._apply_dead_zone(
                    self.joystick.get_axis(ControllerAxis.RIGHT_STICK_Y.value)
                )

            # Update triggers (some controllers use axes, some use buttons)
            if self.joystick.get_numaxes() >= 6:
                # Triggers as axes (-1 to 1, normalize to 0 to 1)
                self.state.left_trigger = (
                    self.joystick.get_axis(ControllerAxis.LEFT_TRIGGER.value) + 1.0
                ) / 2.0
                self.state.right_trigger = (
                    self.joystick.get_axis(ControllerAxis.RIGHT_TRIGGER.value) + 1.0
                ) / 2.0

            # Update D-pad (hat)
            if self.joystick.get_numhats() > 0:
                hat = self.joystick.get_hat(0)
                self.state.dpad_x = hat[0]
                self.state.dpad_y = hat[1]

            # Update buttons
            if self.joystick.get_numbuttons() >= 10:
                self.state.button_a = self.joystick.get_button(ControllerButton.A.value)
                self.state.button_b = self.joystick.get_button(ControllerButton.B.value)
                self.state.button_x = self.joystick.get_button(ControllerButton.X.value)
                self.state.button_y = self.joystick.get_button(ControllerButton.Y.value)
                self.state.button_lb = self.joystick.get_button(ControllerButton.LB.value)
                self.state.button_rb = self.joystick.get_button(ControllerButton.RB.value)
                self.state.button_back = self.joystick.get_button(ControllerButton.BACK.value)
                self.state.button_start = self.joystick.get_button(ControllerButton.START.value)
                self.state.button_left_stick = self.joystick.get_button(ControllerButton.LEFT_STICK.value)
                self.state.button_right_stick = self.joystick.get_button(ControllerButton.RIGHT_STICK.value)

        except pygame.error:
            # Controller disconnected
            self.disconnect()

    def _apply_dead_zone(self, value: float) -> float:
        """
        Apply dead zone to analog input.

        Args:
            value: Raw analog value (-1.0 to 1.0)

        Returns:
            Filtered value with dead zone applied
        """
        if abs(value) < self.dead_zone:
            return 0.0

        # Scale value to compensate for dead zone
        sign = 1.0 if value > 0 else -1.0
        scaled = (abs(value) - self.dead_zone) / (1.0 - self.dead_zone)
        return sign * scaled

    def is_button_pressed(self, button: ControllerButton) -> bool:
        """
        Check if button was pressed this frame (not held).

        Args:
            button: Button to check

        Returns:
            True if button was just pressed
        """
        if not self.connected or not self.joystick:
            return False

        current = self.joystick.get_button(button.value)
        previous = self.prev_buttons.get(button.value, False)

        self.prev_buttons[button.value] = current

        return current and not previous

    def rumble(self, low_frequency: float = 0.0, high_frequency: float = 0.0, duration_ms: int = 500):
        """
        Activate controller rumble (if supported).

        Args:
            low_frequency: Low frequency motor intensity (0.0 to 1.0)
            high_frequency: High frequency motor intensity (0.0 to 1.0)
            duration_ms: Duration in milliseconds
        """
        if not self.connected or not self.joystick:
            return

        try:
            # Try to use rumble (not all controllers support this)
            if hasattr(self.joystick, 'rumble'):
                self.joystick.rumble(low_frequency, high_frequency, duration_ms)
        except:
            pass  # Rumble not supported

    def stop_rumble(self):
        """Stop controller rumble"""
        if self.connected and self.joystick:
            try:
                if hasattr(self.joystick, 'stop_rumble'):
                    self.joystick.stop_rumble()
            except:
                pass


class ControllerManager:
    """
    Manager for multiple controllers.
    Handles hot-plugging and auto-detection.
    """

    def __init__(self, max_controllers: int = 4):
        """
        Initialize controller manager.

        Args:
            max_controllers: Maximum number of controllers to support
        """
        self.max_controllers = max_controllers
        self.controllers: Dict[int, XboxController] = {}

        pygame.joystick.init()

        # Detect initial controllers
        self.scan_controllers()

    def scan_controllers(self):
        """Scan for connected controllers"""
        num_joysticks = pygame.joystick.get_count()

        print(f"Scanning for controllers... Found: {num_joysticks}")

        for i in range(min(num_joysticks, self.max_controllers)):
            if i not in self.controllers:
                controller = XboxController(i)
                if controller.connected:
                    self.controllers[i] = controller

    def update_all(self):
        """Update all connected controllers"""
        # Check for new controllers
        if pygame.joystick.get_count() > len(self.controllers):
            self.scan_controllers()

        # Update existing controllers
        disconnected = []
        for index, controller in self.controllers.items():
            if controller.connected:
                controller.update()
            else:
                disconnected.append(index)

        # Remove disconnected controllers
        for index in disconnected:
            del self.controllers[index]

    def get_controller(self, index: int = 0) -> Optional[XboxController]:
        """
        Get controller by index.

        Args:
            index: Controller index

        Returns:
            XboxController instance or None
        """
        return self.controllers.get(index)

    def get_primary_controller(self) -> Optional[XboxController]:
        """Get first connected controller"""
        if self.controllers:
            return self.controllers[min(self.controllers.keys())]
        return None

    def disconnect_all(self):
        """Disconnect all controllers"""
        for controller in self.controllers.values():
            controller.disconnect()
        self.controllers.clear()


def get_controller_display_name(joystick_name: str) -> str:
    """
    Get friendly display name for controller.

    Args:
        joystick_name: Raw joystick name from pygame

    Returns:
        Friendly name
    """
    name_lower = joystick_name.lower()

    if 'xbox' in name_lower:
        if '360' in name_lower:
            return "Xbox 360 Controller"
        elif 'one' in name_lower:
            return "Xbox One Controller"
        elif 'series' in name_lower:
            return "Xbox Series X|S Controller"
        else:
            return "Xbox Controller"
    elif 'playstation' in name_lower or 'ps' in name_lower:
        return "PlayStation Controller"
    elif 'switch' in name_lower:
        return "Nintendo Switch Controller"
    else:
        return joystick_name


# Example usage and testing
if __name__ == "__main__":
    import time

    pygame.init()

    # Create controller manager
    manager = ControllerManager()

    if not manager.controllers:
        print("No controllers found! Please connect an Xbox controller.")
        print("\nFor Bluetooth connection on Windows:")
        print("1. Put controller in pairing mode (hold Xbox + Pair buttons)")
        print("2. Go to Settings > Bluetooth & devices")
        print("3. Click 'Add device' and select your controller")
        exit()

    print("\nTesting controller input...")
    print("Move sticks, press buttons, or press START to exit\n")

    running = True
    clock = pygame.time.Clock()

    while running:
        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Update controllers
        manager.update_all()

        # Get primary controller
        controller = manager.get_primary_controller()

        if controller and controller.connected:
            state = controller.state

            # Print active inputs
            active_inputs = []

            if abs(state.left_stick_x) > 0.1 or abs(state.left_stick_y) > 0.1:
                active_inputs.append(f"Left Stick: ({state.left_stick_x:.2f}, {state.left_stick_y:.2f})")

            if abs(state.right_stick_x) > 0.1 or abs(state.right_stick_y) > 0.1:
                active_inputs.append(f"Right Stick: ({state.right_stick_x:.2f}, {state.right_stick_y:.2f})")

            if state.left_trigger > 0.1:
                active_inputs.append(f"LT: {state.left_trigger:.2f}")

            if state.right_trigger > 0.1:
                active_inputs.append(f"RT: {state.right_trigger:.2f}")

            if state.button_a:
                active_inputs.append("A")
            if state.button_b:
                active_inputs.append("B")
            if state.button_x:
                active_inputs.append("X")
            if state.button_y:
                active_inputs.append("Y")
            if state.button_lb:
                active_inputs.append("LB")
            if state.button_rb:
                active_inputs.append("RB")

            if state.dpad_x != 0 or state.dpad_y != 0:
                active_inputs.append(f"D-Pad: ({state.dpad_x}, {state.dpad_y})")

            if active_inputs:
                print(f"\r{' | '.join(active_inputs)}", end="          ", flush=True)

            # Test rumble on A button press
            if controller.is_button_pressed(ControllerButton.A):
                controller.rumble(0.5, 0.5, 200)

            # Exit on START button
            if state.button_start:
                running = False

        clock.tick(60)

    print("\n\nController test complete!")
    manager.disconnect_all()
    pygame.quit()
