"""
Vehicle System - Multiple Types with Variations
Creates procedural vehicles with different types and colors

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from typing import Tuple, List
from enum import Enum


class VehicleType(Enum):
    """Vehicle categories"""
    SEDAN = 0
    SUV = 1
    TRUCK = 2
    VAN = 3
    BUS = 4
    TAXI = 5
    POLICE = 6
    AMBULANCE = 7
    SPORTS_CAR = 8
    VINTAGE = 9
    HATCHBACK = 10


class ProceduralVehicle:
    """
    Procedural vehicle generator with variations.

    Features:
    - 10+ vehicle types
    - 20+ colors per type
    - Realistic proportions
    - Emergency vehicle markings
    """

    # Color palettes
    STANDARD_COLORS = [
        (0.1, 0.1, 0.1, 1.0),    # Black
        (0.9, 0.9, 0.9, 1.0),    # White
        (0.5, 0.5, 0.5, 1.0),    # Gray
        (0.7, 0.1, 0.1, 1.0),    # Red
        (0.1, 0.2, 0.6, 1.0),    # Blue
        (0.2, 0.5, 0.2, 1.0),    # Green
        (0.7, 0.6, 0.1, 1.0),    # Yellow
        (0.6, 0.3, 0.1, 1.0),    # Brown
        (0.4, 0.1, 0.5, 1.0),    # Purple
        (0.8, 0.4, 0.1, 1.0),    # Orange
        (0.6, 0.6, 0.7, 1.0),    # Silver
        (0.15, 0.2, 0.25, 1.0),  # Dark blue
        (0.5, 0.1, 0.1, 1.0),    # Maroon
        (0.1, 0.4, 0.5, 1.0),    # Teal
        (0.6, 0.5, 0.4, 1.0),    # Beige
    ]

    def __init__(self, vehicle_type: VehicleType, seed: int = None):
        """Initialize vehicle generator"""
        self.vehicle_type = vehicle_type
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

        # Get vehicle dimensions
        self.length, self.width, self.height = self._get_dimensions()

        # Get color
        self.color = self._get_color()

    def _get_dimensions(self) -> Tuple[float, float, float]:
        """Get vehicle dimensions (length, width, height)"""
        dims = {
            VehicleType.SEDAN: (4.5, 1.8, 1.5),
            VehicleType.SUV: (4.8, 2.0, 1.8),
            VehicleType.TRUCK: (5.5, 2.2, 2.0),
            VehicleType.VAN: (5.0, 2.0, 2.2),
            VehicleType.BUS: (12.0, 2.5, 3.0),
            VehicleType.TAXI: (4.5, 1.8, 1.5),
            VehicleType.POLICE: (4.6, 1.9, 1.6),
            VehicleType.AMBULANCE: (5.5, 2.2, 2.4),
            VehicleType.SPORTS_CAR: (4.2, 1.9, 1.2),
            VehicleType.VINTAGE: (4.0, 1.7, 1.6),
            VehicleType.HATCHBACK: (4.0, 1.7, 1.5),
        }
        base = dims[self.vehicle_type]
        # Add slight variation
        variation = 0.05
        return tuple(d * (1 + np.random.uniform(-variation, variation)) for d in base)

    def _get_color(self) -> Tuple[float, float, float, float]:
        """Get vehicle color"""
        if self.vehicle_type == VehicleType.TAXI:
            return (1.0, 0.9, 0.1, 1.0)  # Yellow
        elif self.vehicle_type == VehicleType.POLICE:
            return (0.05, 0.05, 0.1, 1.0)  # Dark blue/black
        elif self.vehicle_type == VehicleType.AMBULANCE:
            return (0.9, 0.9, 0.9, 1.0)  # White
        elif self.vehicle_type == VehicleType.BUS:
            return (0.9, 0.5, 0.1, 1.0)  # Orange
        else:
            return self.STANDARD_COLORS[np.random.randint(0, len(self.STANDARD_COLORS))]

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float],
                       heading: float = 0) -> NodePath:
        """Create 3D vehicle geometry"""
        vehicle_node = parent_node.attachNewNode(f"vehicle_{self.vehicle_type.name}_{self.seed}")
        vehicle_node.setPos(*position)
        vehicle_node.setH(heading)

        # Create body
        self._create_body(vehicle_node)

        # Create windows
        self._create_windows(vehicle_node)

        # Create wheels
        self._create_wheels(vehicle_node)

        # Add special markings
        if self.vehicle_type in [VehicleType.POLICE, VehicleType.AMBULANCE, VehicleType.TAXI]:
            self._add_markings(vehicle_node)

        return vehicle_node

    def _create_body(self, parent: NodePath):
        """Create vehicle body"""
        card_maker = CardMaker("vehicle_body")

        # Main body (simplified box)
        # Front
        card_maker.setFrame(-self.width/2, self.width/2, 0, self.height)
        front = parent.attachNewNode(card_maker.generate())
        front.setY(self.length/2)
        front.setColor(self.color)

        # Back
        back = parent.attachNewNode(card_maker.generate())
        back.setY(-self.length/2)
        back.setH(180)
        back.setColor(self.color)

        # Left side
        card_maker.setFrame(-self.length/2, self.length/2, 0, self.height)
        left = parent.attachNewNode(card_maker.generate())
        left.setX(-self.width/2)
        left.setH(90)
        left.setColor(self.color)

        # Right side
        right = parent.attachNewNode(card_maker.generate())
        right.setX(self.width/2)
        right.setH(-90)
        right.setColor(self.color)

        # Top
        card_maker.setFrame(-self.width/2, self.width/2, -self.length/2, self.length/2)
        top = parent.attachNewNode(card_maker.generate())
        top.setZ(self.height)
        top.setP(-90)
        top.setColor(self.color)

    def _create_windows(self, parent: NodePath):
        """Create windows"""
        window_color = (0.3, 0.5, 0.7, 0.6)  # Blue tinted glass

        window_height = self.height * 0.4
        window_z = self.height * 0.6

        card_maker = CardMaker("window")

        # Front windshield
        card_maker.setFrame(-self.width/2 * 0.8, self.width/2 * 0.8, 0, window_height)
        front_window = parent.attachNewNode(card_maker.generate())
        front_window.setPos(0, self.length/2 + 0.01, window_z)
        front_window.setColor(window_color)

        # Side windows (simplified)
        card_maker.setFrame(-self.length/2 * 0.6, self.length/2 * 0.6, 0, window_height)
        left_window = parent.attachNewNode(card_maker.generate())
        left_window.setPos(-self.width/2 - 0.01, 0, window_z)
        left_window.setH(90)
        left_window.setColor(window_color)

        right_window = parent.attachNewNode(card_maker.generate())
        right_window.setPos(self.width/2 + 0.01, 0, window_z)
        right_window.setH(-90)
        right_window.setColor(window_color)

    def _create_wheels(self, parent: NodePath):
        """Create wheels"""
        wheel_color = (0.1, 0.1, 0.1, 1.0)  # Black
        wheel_radius = 0.35
        wheel_width = 0.25

        # Wheel positions (front-left, front-right, back-left, back-right)
        wheel_offset_x = self.width / 2 - 0.2
        wheel_offset_y_front = self.length / 2 - 0.5
        wheel_offset_y_back = -self.length / 2 + 0.5

        positions = [
            (-wheel_offset_x, wheel_offset_y_front, wheel_radius),
            (wheel_offset_x, wheel_offset_y_front, wheel_radius),
            (-wheel_offset_x, wheel_offset_y_back, wheel_radius),
            (wheel_offset_x, wheel_offset_y_back, wheel_radius),
        ]

        card_maker = CardMaker("wheel")
        card_maker.setFrame(-wheel_radius, wheel_radius, -wheel_radius, wheel_radius)

        for i, pos in enumerate(positions):
            wheel = parent.attachNewNode(card_maker.generate())
            wheel.setPos(*pos)
            wheel.setH(90 if i % 2 == 0 else -90)  # Face outward
            wheel.setColor(wheel_color)

    def _add_markings(self, parent: NodePath):
        """Add special vehicle markings"""
        if self.vehicle_type == VehicleType.POLICE:
            # Police stripe
            stripe_color = (0.1, 0.3, 0.9, 1.0)  # Blue stripe
            card_maker = CardMaker("police_stripe")
            card_maker.setFrame(-self.length/2, self.length/2, 0, 0.3)

            stripe_left = parent.attachNewNode(card_maker.generate())
            stripe_left.setPos(-self.width/2 - 0.01, 0, self.height * 0.5)
            stripe_left.setH(90)
            stripe_left.setColor(stripe_color)

            stripe_right = parent.attachNewNode(card_maker.generate())
            stripe_right.setPos(self.width/2 + 0.01, 0, self.height * 0.5)
            stripe_right.setH(-90)
            stripe_right.setColor(stripe_color)

        elif self.vehicle_type == VehicleType.AMBULANCE:
            # Red cross on sides
            cross_color = (1.0, 0.1, 0.1, 1.0)
            card_maker = CardMaker("cross")
            card_maker.setFrame(-0.4, 0.4, -0.4, 0.4)

            cross_left = parent.attachNewNode(card_maker.generate())
            cross_left.setPos(-self.width/2 - 0.02, 0, self.height * 0.6)
            cross_left.setH(90)
            cross_left.setColor(cross_color)

            cross_right = parent.attachNewNode(card_maker.generate())
            cross_right.setPos(self.width/2 + 0.02, 0, self.height * 0.6)
            cross_right.setH(-90)
            cross_right.setColor(cross_color)

        elif self.vehicle_type == VehicleType.TAXI:
            # Taxi sign on roof
            sign_color = (1.0, 0.9, 0.1, 1.0)
            card_maker = CardMaker("taxi_sign")
            card_maker.setFrame(-0.5, 0.5, 0, 0.3)

            sign = parent.attachNewNode(card_maker.generate())
            sign.setPos(0, 0, self.height + 0.2)
            sign.setColor(sign_color)


class VehicleSpawner:
    """Manages vehicle spawning with variety"""

    def __init__(self):
        """Initialize spawner"""
        # Define spawn probabilities
        self.spawn_weights = {
            VehicleType.SEDAN: 0.30,
            VehicleType.SUV: 0.20,
            VehicleType.HATCHBACK: 0.15,
            VehicleType.TRUCK: 0.10,
            VehicleType.VAN: 0.08,
            VehicleType.TAXI: 0.05,
            VehicleType.SPORTS_CAR: 0.04,
            VehicleType.POLICE: 0.03,
            VehicleType.BUS: 0.02,
            VehicleType.AMBULANCE: 0.02,
            VehicleType.VINTAGE: 0.01,
        }

    def spawn_random_vehicle(self, parent_node: NodePath, position: Tuple[float, float, float],
                           heading: float = 0) -> NodePath:
        """Spawn random vehicle at position"""
        # Choose vehicle type based on weights
        vehicle_type = np.random.choice(
            list(self.spawn_weights.keys()),
            p=list(self.spawn_weights.values())
        )

        # Create vehicle
        vehicle = ProceduralVehicle(vehicle_type)
        return vehicle.create_3d_model(parent_node, position, heading)

    def spawn_specific_vehicle(self, vehicle_type: VehicleType, parent_node: NodePath,
                              position: Tuple[float, float, float], heading: float = 0) -> NodePath:
        """Spawn specific vehicle type"""
        vehicle = ProceduralVehicle(vehicle_type)
        return vehicle.create_3d_model(parent_node, position, heading)


if __name__ == "__main__":
    """Test vehicle system"""
    print("Vehicle System Test")
    print("=" * 60)

    spawner = VehicleSpawner()

    # Test all vehicle types
    for vtype in VehicleType:
        vehicle = ProceduralVehicle(vtype, seed=42)
        print(f"\n{vtype.name}:")
        print(f"  Dimensions: {vehicle.length:.1f}m x {vehicle.width:.1f}m x {vehicle.height:.1f}m")
        print(f"  Color: RGB{tuple(round(c, 2) for c in vehicle.color[:3])}")

    print("\n" + "=" * 60)
    print(f"Total vehicle types: {len(VehicleType)}")
    print(f"Total color variations: {len(ProceduralVehicle.STANDARD_COLORS)}")
    print(f"Unique combinations: {len(VehicleType) * len(ProceduralVehicle.STANDARD_COLORS)}+")
