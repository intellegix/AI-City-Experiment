"""
Detailed Vehicle System - Photorealistic Car Models
Creates realistic vehicles with proper geometry and details

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
    DELIVERY_TRUCK = 11


class DetailedVehicle:
    """
    Photorealistic vehicle generator with detailed geometry.

    Features:
    - Proper car body shape (hood, cabin, trunk)
    - Detailed wheels with rims and tires
    - Headlights and taillights
    - Side mirrors
    - Door panels and handles
    - Windows with proper depth
    - License plates
    - Undercarriage
    - Exhaust pipes
    - Windshield wipers
    - Grill and bumpers
    """

    STANDARD_COLORS = [
        (0.08, 0.08, 0.08, 1.0),     # Black
        (0.95, 0.95, 0.95, 1.0),     # White
        (0.50, 0.50, 0.52, 1.0),     # Gray
        (0.75, 0.08, 0.08, 1.0),     # Red
        (0.08, 0.20, 0.65, 1.0),     # Blue
        (0.15, 0.55, 0.20, 1.0),     # Green
        (0.85, 0.75, 0.10, 1.0),     # Yellow
        (0.65, 0.35, 0.12, 1.0),     # Brown
        (0.72, 0.72, 0.78, 1.0),     # Silver
        (0.12, 0.18, 0.28, 1.0),     # Dark blue
        (0.55, 0.10, 0.10, 1.0),     # Maroon
        (0.08, 0.45, 0.52, 1.0),     # Teal
        (0.20, 0.55, 0.75, 1.0),     # Light blue
        (0.85, 0.45, 0.12, 1.0),     # Orange
        (0.45, 0.12, 0.58, 1.0),     # Purple
    ]

    def __init__(self, vehicle_type: VehicleType, seed: int = None):
        """Initialize detailed vehicle"""
        self.vehicle_type = vehicle_type
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

        # Get dimensions
        self.length, self.width, self.height = self._get_dimensions()

        # Get colors
        self.body_color = self._get_body_color()
        self.window_color = (0.15, 0.20, 0.30, 0.6)  # Dark tinted glass
        self.chrome_color = (0.85, 0.87, 0.90, 1.0)  # Chrome/metal

        # Body proportions
        self._calculate_proportions()

    def _get_dimensions(self) -> Tuple[float, float, float]:
        """Get vehicle dimensions"""
        dims = {
            VehicleType.SEDAN: (4.7, 1.8, 1.45),
            VehicleType.SUV: (4.9, 2.0, 1.85),
            VehicleType.TRUCK: (5.8, 2.2, 1.95),
            VehicleType.VAN: (5.2, 2.0, 2.3),
            VehicleType.BUS: (12.0, 2.55, 3.2),
            VehicleType.TAXI: (4.7, 1.8, 1.45),
            VehicleType.POLICE: (4.8, 1.9, 1.5),
            VehicleType.AMBULANCE: (5.8, 2.2, 2.5),
            VehicleType.SPORTS_CAR: (4.3, 1.95, 1.15),
            VehicleType.VINTAGE: (4.2, 1.75, 1.65),
            VehicleType.HATCHBACK: (4.0, 1.75, 1.5),
            VehicleType.DELIVERY_TRUCK: (6.5, 2.3, 2.8),
        }
        return dims[self.vehicle_type]

    def _calculate_proportions(self):
        """Calculate vehicle body proportions"""
        # Hood, cabin, trunk proportions
        if self.vehicle_type == VehicleType.SPORTS_CAR:
            self.hood_length = self.length * 0.45
            self.cabin_length = self.length * 0.35
            self.trunk_length = self.length * 0.20
        elif self.vehicle_type in [VehicleType.BUS, VehicleType.VAN, VehicleType.DELIVERY_TRUCK]:
            self.hood_length = self.length * 0.20
            self.cabin_length = self.length * 0.80
            self.trunk_length = 0
        elif self.vehicle_type == VehicleType.TRUCK:
            self.hood_length = self.length * 0.35
            self.cabin_length = self.length * 0.35
            self.trunk_length = self.length * 0.30  # Bed
        else:  # Sedan, SUV, etc.
            self.hood_length = self.length * 0.35
            self.cabin_length = self.length * 0.40
            self.trunk_length = self.length * 0.25

        # Heights
        self.body_height = self.height * 0.6  # Lower body
        self.cabin_height = self.height * 0.4  # Upper cabin/windows
        self.wheel_radius = 0.38
        self.wheel_width = 0.25

    def _get_body_color(self) -> Tuple[float, float, float, float]:
        """Get vehicle body color"""
        if self.vehicle_type == VehicleType.TAXI:
            return (1.0, 0.92, 0.10, 1.0)  # Yellow
        elif self.vehicle_type == VehicleType.POLICE:
            return (0.05, 0.05, 0.10, 1.0)  # Dark blue/black
        elif self.vehicle_type == VehicleType.AMBULANCE:
            return (0.95, 0.95, 0.95, 1.0)  # White
        elif self.vehicle_type == VehicleType.BUS:
            return (0.92, 0.55, 0.12, 1.0)  # Orange
        elif self.vehicle_type == VehicleType.DELIVERY_TRUCK:
            return (0.88, 0.88, 0.90, 1.0)  # White/light gray
        else:
            return self.STANDARD_COLORS[np.random.randint(0, len(self.STANDARD_COLORS))]

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float],
                       heading: float = 0) -> NodePath:
        """Create detailed 3D vehicle"""
        vehicle_node = parent_node.attachNewNode(f"vehicle_{self.vehicle_type.name}_{self.seed}")
        vehicle_node.setPos(*position)
        vehicle_node.setH(heading)

        # 1. Undercarriage (chassis)
        self._create_undercarriage(vehicle_node)

        # 2. Lower body (hood, trunk, sides)
        self._create_lower_body(vehicle_node)

        # 3. Upper cabin (windshield, roof, windows)
        self._create_upper_cabin(vehicle_node)

        # 4. Detailed wheels with rims
        self._create_detailed_wheels(vehicle_node)

        # 5. Lights (headlights, taillights)
        self._create_lights(vehicle_node)

        # 6. Details (mirrors, door handles, grill)
        self._create_details(vehicle_node)

        # 7. Special markings
        if self.vehicle_type in [VehicleType.POLICE, VehicleType.AMBULANCE, VehicleType.TAXI]:
            self._add_special_markings(vehicle_node)

        return vehicle_node

    def _create_undercarriage(self, parent: NodePath):
        """Create vehicle undercarriage/chassis"""
        card_maker = CardMaker("chassis")
        chassis_color = (0.15, 0.15, 0.15, 1.0)  # Dark gray/black
        chassis_height = 0.25

        # Bottom plate
        card_maker.setFrame(-self.width/2 + 0.2, self.width/2 - 0.2,
                           -self.length/2 + 0.3, self.length/2 - 0.3)
        chassis = parent.attachNewNode(card_maker.generate())
        chassis.setZ(chassis_height)
        chassis.setP(-90)
        chassis.setColor(chassis_color)

    def _create_lower_body(self, parent: NodePath):
        """Create lower body (hood, sides, trunk)"""
        card_maker = CardMaker("body")
        body_z = self.wheel_radius + 0.1

        # Hood section
        hood_start = self.length/2
        hood_end = self.length/2 - self.hood_length

        # Front (hood/bumper)
        card_maker.setFrame(-self.width/2, self.width/2, 0, self.body_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, hood_start, body_z)
        front.setColor(self.body_color)

        # Hood top (slopes slightly)
        card_maker.setFrame(-self.width/2, self.width/2, hood_end, hood_start)
        hood_top = parent.attachNewNode(card_maker.generate())
        hood_top.setZ(body_z + self.body_height)
        hood_top.setP(-85)  # Slight slope
        hood_top.setColor(self.body_color)

        # Trunk section
        trunk_start = hood_end - self.cabin_length
        trunk_end = -self.length/2

        if self.trunk_length > 0:
            # Rear (trunk/bumper)
            card_maker.setFrame(-self.width/2, self.width/2, 0, self.body_height)
            rear = parent.attachNewNode(card_maker.generate())
            rear.setPos(0, trunk_end, body_z)
            rear.setH(180)
            rear.setColor(self.body_color)

            # Trunk top (slopes slightly)
            card_maker.setFrame(-self.width/2, self.width/2, trunk_end, trunk_start)
            trunk_top = parent.attachNewNode(card_maker.generate())
            trunk_top.setZ(body_z + self.body_height)
            trunk_top.setP(-95)  # Slight slope
            trunk_top.setColor(self.body_color)

        # Side panels
        card_maker.setFrame(-self.length/2, self.length/2, 0, self.body_height)

        # Left side
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-self.width/2, 0, body_z)
        left.setH(90)
        left.setColor(self.body_color)

        # Right side
        right = parent.attachNewNode(card_maker.generate())
        right.setPos(self.width/2, 0, body_z)
        right.setH(-90)
        right.setColor(self.body_color)

        # Add door panels and handles
        self._create_doors(parent, body_z)

    def _create_doors(self, parent: NodePath, body_z: float):
        """Create door panels with handles"""
        card_maker = CardMaker("door")
        door_height = self.body_height * 0.8
        door_length = self.cabin_length * 0.45
        door_z = body_z + self.body_height * 0.1

        # Door outline (slightly darker)
        door_outline_color = (self.body_color[0] * 0.85, self.body_color[1] * 0.85,
                              self.body_color[2] * 0.85, 1.0)

        # Left front door
        card_maker.setFrame(-door_length/2, door_length/2, 0, door_height)
        left_front = parent.attachNewNode(card_maker.generate())
        left_front.setPos(-self.width/2 - 0.02, self.cabin_length/4, door_z)
        left_front.setH(90)
        left_front.setColor(door_outline_color)

        # Right front door
        right_front = parent.attachNewNode(card_maker.generate())
        right_front.setPos(self.width/2 + 0.02, self.cabin_length/4, door_z)
        right_front.setH(-90)
        right_front.setColor(door_outline_color)

        # Door handles (chrome)
        handle_size = 0.15
        handle_z = door_z + door_height * 0.5

        for side_x, heading in [(-self.width/2 - 0.03, 90), (self.width/2 + 0.03, -90)]:
            card_maker.setFrame(-handle_size, handle_size, -handle_size/2, handle_size/2)
            handle = parent.attachNewNode(card_maker.generate())
            handle.setPos(side_x, self.cabin_length/4, handle_z)
            handle.setH(heading)
            handle.setColor(self.chrome_color)

    def _create_upper_cabin(self, parent: NodePath):
        """Create upper cabin with windshield and windows"""
        card_maker = CardMaker("cabin")
        cabin_z = self.wheel_radius + 0.1 + self.body_height
        cabin_start = self.length/2 - self.hood_length
        cabin_end = cabin_start - self.cabin_length

        # Windshield (front, angled)
        windshield_height = self.cabin_height * 0.9
        card_maker.setFrame(-self.width/2 + 0.15, self.width/2 - 0.15, 0, windshield_height)
        windshield = parent.attachNewNode(card_maker.generate())
        windshield.setPos(0, cabin_start - 0.1, cabin_z)
        windshield.setP(25)  # Angled back
        windshield.setColor(self.window_color)
        windshield.setTransparency(TransparencyAttrib.MAlpha)

        # Rear window (angled)
        if self.trunk_length > 0:
            card_maker.setFrame(-self.width/2 + 0.15, self.width/2 - 0.15, 0, windshield_height * 0.8)
            rear_window = parent.attachNewNode(card_maker.generate())
            rear_window.setPos(0, cabin_end + 0.1, cabin_z)
            rear_window.setP(-25)  # Angled back
            rear_window.setH(180)
            rear_window.setColor(self.window_color)
            rear_window.setTransparency(TransparencyAttrib.MAlpha)

        # Side windows
        window_height = self.cabin_height * 0.7
        window_length = self.cabin_length * 0.85

        card_maker.setFrame(cabin_end + 0.2, cabin_start - 0.2, 0, window_height)

        # Left windows
        left_windows = parent.attachNewNode(card_maker.generate())
        left_windows.setPos(-self.width/2 - 0.02, 0, cabin_z + 0.1)
        left_windows.setH(90)
        left_windows.setColor(self.window_color)
        left_windows.setTransparency(TransparencyAttrib.MAlpha)

        # Right windows
        right_windows = parent.attachNewNode(card_maker.generate())
        right_windows.setPos(self.width/2 + 0.02, 0, cabin_z + 0.1)
        right_windows.setH(-90)
        right_windows.setColor(self.window_color)
        right_windows.setTransparency(TransparencyAttrib.MAlpha)

        # Roof
        card_maker.setFrame(-self.width/2, self.width/2, cabin_end, cabin_start)
        roof = parent.attachNewNode(card_maker.generate())
        roof.setZ(cabin_z + self.cabin_height)
        roof.setP(-90)
        roof.setColor(self.body_color)

        # Roof pillars (A, B, C pillars)
        self._create_roof_pillars(parent, cabin_z, cabin_start, cabin_end)

    def _create_roof_pillars(self, parent: NodePath, cabin_z: float, front_y: float, rear_y: float):
        """Create roof support pillars"""
        pillar_width = 0.12
        pillar_color = (self.body_color[0] * 0.7, self.body_color[1] * 0.7,
                       self.body_color[2] * 0.7, 1.0)

        card_maker = CardMaker("pillar")
        card_maker.setFrame(-pillar_width/2, pillar_width/2, 0, self.cabin_height)

        # A-pillars (front)
        for x in [-self.width/2 + 0.15, self.width/2 - 0.15]:
            pillar = parent.attachNewNode(card_maker.generate())
            pillar.setPos(x, front_y - 0.2, cabin_z)
            pillar.setColor(pillar_color)

        # B-pillars (middle)
        mid_y = (front_y + rear_y) / 2
        for x in [-self.width/2 + 0.15, self.width/2 - 0.15]:
            pillar = parent.attachNewNode(card_maker.generate())
            pillar.setPos(x, mid_y, cabin_z)
            pillar.setColor(pillar_color)

        # C-pillars (rear) - if has trunk
        if self.trunk_length > 0:
            for x in [-self.width/2 + 0.15, self.width/2 - 0.15]:
                pillar = parent.attachNewNode(card_maker.generate())
                pillar.setPos(x, rear_y + 0.2, cabin_z)
                pillar.setColor(pillar_color)

    def _create_detailed_wheels(self, parent: NodePath):
        """Create detailed wheels with rims and tires"""
        # Wheel positions
        if self.vehicle_type == VehicleType.BUS:
            # Bus has more wheels
            positions = [
                (-self.width/2 - 0.15, self.length/2 - 1.5, self.wheel_radius),  # Front left
                (self.width/2 + 0.15, self.length/2 - 1.5, self.wheel_radius),   # Front right
                (-self.width/2 - 0.15, -self.length/2 + 2.5, self.wheel_radius), # Rear left 1
                (self.width/2 + 0.15, -self.length/2 + 2.5, self.wheel_radius),  # Rear right 1
                (-self.width/2 - 0.15, -self.length/2 + 1.0, self.wheel_radius), # Rear left 2
                (self.width/2 + 0.15, -self.length/2 + 1.0, self.wheel_radius),  # Rear right 2
            ]
        else:
            front_offset = self.length/2 - self.hood_length * 0.8
            rear_offset = -self.length/2 + self.trunk_length * 0.5 if self.trunk_length > 0 else -self.length/2 + 0.8

            positions = [
                (-self.width/2 - 0.1, front_offset, self.wheel_radius),  # Front left
                (self.width/2 + 0.1, front_offset, self.wheel_radius),   # Front right
                (-self.width/2 - 0.1, rear_offset, self.wheel_radius),   # Rear left
                (self.width/2 + 0.1, rear_offset, self.wheel_radius),    # Rear right
            ]

        for i, pos in enumerate(positions):
            self._create_single_wheel(parent, pos, i % 2 == 0)

    def _create_single_wheel(self, parent: NodePath, pos: Tuple[float, float, float], is_left: bool):
        """Create single detailed wheel with tire and rim"""
        card_maker = CardMaker("wheel")

        # Tire (black, outer part)
        tire_color = (0.08, 0.08, 0.08, 1.0)
        card_maker.setFrame(-self.wheel_radius, self.wheel_radius,
                           -self.wheel_radius, self.wheel_radius)
        tire = parent.attachNewNode(card_maker.generate())
        tire.setPos(*pos)
        tire.setH(90 if is_left else -90)
        tire.setColor(tire_color)

        # Rim (chrome/silver, inner part)
        rim_radius = self.wheel_radius * 0.65
        card_maker.setFrame(-rim_radius, rim_radius, -rim_radius, rim_radius)
        rim = parent.attachNewNode(card_maker.generate())
        rim.setPos(pos[0] + (0.01 if is_left else -0.01), pos[1], pos[2])
        rim.setH(90 if is_left else -90)
        rim.setColor(self.chrome_color)

        # Brake disc (visible through rim)
        brake_radius = rim_radius * 0.75
        brake_color = (0.35, 0.32, 0.30, 1.0)  # Dark metal
        card_maker.setFrame(-brake_radius, brake_radius, -brake_radius, brake_radius)
        brake = parent.attachNewNode(card_maker.generate())
        brake.setPos(pos[0] + (0.02 if is_left else -0.02), pos[1], pos[2])
        brake.setH(90 if is_left else -90)
        brake.setColor(brake_color)

        # Wheel well/fender
        self._create_wheel_well(parent, pos, is_left)

    def _create_wheel_well(self, parent: NodePath, wheel_pos: Tuple[float, float, float], is_left: bool):
        """Create wheel well/fender around wheel"""
        card_maker = CardMaker("fender")
        fender_color = self.body_color

        # Curved fender over wheel
        fender_width = self.wheel_radius * 2.2
        fender_height = self.wheel_radius * 0.5

        card_maker.setFrame(-fender_width/2, fender_width/2, 0, fender_height)
        fender = parent.attachNewNode(card_maker.generate())
        fender.setPos(wheel_pos[0], wheel_pos[1], wheel_pos[2] + self.wheel_radius)
        fender.setP(-90)
        fender.setH(90 if is_left else -90)
        fender.setColor(fender_color)

    def _create_lights(self, parent: NodePath):
        """Create headlights and taillights"""
        card_maker = CardMaker("light")

        # Headlights (front, white/yellow)
        headlight_color = (0.95, 0.95, 0.88, 1.0)  # Warm white
        headlight_size = 0.25

        for x in [-self.width/2 + 0.4, self.width/2 - 0.4]:
            # Main headlight
            card_maker.setFrame(-headlight_size, headlight_size,
                               -headlight_size, headlight_size)
            headlight = parent.attachNewNode(card_maker.generate())
            headlight.setPos(x, self.length/2 + 0.02, self.wheel_radius + self.body_height * 0.5)
            headlight.setColor(headlight_color)

        # Taillights (rear, red)
        taillight_color = (0.85, 0.08, 0.08, 1.0)  # Bright red

        for x in [-self.width/2 + 0.4, self.width/2 - 0.4]:
            card_maker.setFrame(-headlight_size, headlight_size,
                               -headlight_size * 0.8, headlight_size * 0.8)
            taillight = parent.attachNewNode(card_maker.generate())
            taillight.setPos(x, -self.length/2 - 0.02, self.wheel_radius + self.body_height * 0.4)
            taillight.setH(180)
            taillight.setColor(taillight_color)

        # Brake lights (center rear)
        card_maker.setFrame(-self.width * 0.15, self.width * 0.15,
                           -headlight_size/2, headlight_size/2)
        brake_light = parent.attachNewNode(card_maker.generate())
        brake_light.setPos(0, -self.length/2 - 0.02, self.wheel_radius + self.body_height * 0.7)
        brake_light.setH(180)
        brake_light.setColor(taillight_color)

    def _create_details(self, parent: NodePath):
        """Create additional details (mirrors, grill, etc.)"""
        # Side mirrors
        self._create_side_mirrors(parent)

        # Front grill
        self._create_front_grill(parent)

        # License plates
        self._create_license_plates(parent)

        # Windshield wipers
        if self.vehicle_type not in [VehicleType.BUS, VehicleType.DELIVERY_TRUCK]:
            self._create_wipers(parent)

        # Exhaust pipe
        self._create_exhaust(parent)

    def _create_side_mirrors(self, parent: NodePath):
        """Create side mirrors"""
        card_maker = CardMaker("mirror")
        mirror_size = 0.18
        mirror_z = self.wheel_radius + self.body_height + self.cabin_height * 0.5

        # Mirror housing (body color)
        card_maker.setFrame(-mirror_size, mirror_size, -mirror_size/2, mirror_size/2)

        # Left mirror
        left_mirror = parent.attachNewNode(card_maker.generate())
        left_mirror.setPos(-self.width/2 - 0.25, self.cabin_length/2, mirror_z)
        left_mirror.setH(90)
        left_mirror.setColor(self.body_color)

        # Right mirror
        right_mirror = parent.attachNewNode(card_maker.generate())
        right_mirror.setPos(self.width/2 + 0.25, self.cabin_length/2, mirror_z)
        right_mirror.setH(-90)
        right_mirror.setColor(self.body_color)

        # Mirror glass (reflective, slightly smaller)
        card_maker.setFrame(-mirror_size * 0.8, mirror_size * 0.8,
                           -mirror_size/2 * 0.8, mirror_size/2 * 0.8)

        left_glass = parent.attachNewNode(card_maker.generate())
        left_glass.setPos(-self.width/2 - 0.26, self.cabin_length/2, mirror_z)
        left_glass.setH(90)
        left_glass.setColor(self.chrome_color)

        right_glass = parent.attachNewNode(card_maker.generate())
        right_glass.setPos(self.width/2 + 0.26, self.cabin_length/2, mirror_z)
        right_glass.setH(-90)
        right_glass.setColor(self.chrome_color)

    def _create_front_grill(self, parent: NodePath):
        """Create front grill"""
        card_maker = CardMaker("grill")
        grill_width = self.width * 0.6
        grill_height = self.body_height * 0.3
        grill_color = (0.10, 0.10, 0.12, 1.0)  # Dark grill

        card_maker.setFrame(-grill_width/2, grill_width/2, 0, grill_height)
        grill = parent.attachNewNode(card_maker.generate())
        grill.setPos(0, self.length/2 + 0.01, self.wheel_radius + self.body_height * 0.25)
        grill.setColor(grill_color)

        # Grill bars (chrome)
        num_bars = 5
        for i in range(num_bars):
            bar_y = grill_height * (i + 1) / (num_bars + 1)
            card_maker.setFrame(-grill_width/2, grill_width/2, -0.03, 0.03)
            bar = parent.attachNewNode(card_maker.generate())
            bar.setPos(0, self.length/2 + 0.02, self.wheel_radius + self.body_height * 0.25 + bar_y)
            bar.setColor(self.chrome_color)

    def _create_license_plates(self, parent: NodePath):
        """Create license plates"""
        card_maker = CardMaker("license_plate")
        plate_width = 0.5
        plate_height = 0.15
        plate_color = (0.95, 0.95, 0.88, 1.0)  # Off-white

        # Front plate
        card_maker.setFrame(-plate_width/2, plate_width/2, -plate_height/2, plate_height/2)
        front_plate = parent.attachNewNode(card_maker.generate())
        front_plate.setPos(0, self.length/2 + 0.03, self.wheel_radius + 0.3)
        front_plate.setColor(plate_color)

        # Rear plate
        rear_plate = parent.attachNewNode(card_maker.generate())
        rear_plate.setPos(0, -self.length/2 - 0.03, self.wheel_radius + 0.3)
        rear_plate.setH(180)
        rear_plate.setColor(plate_color)

    def _create_wipers(self, parent: NodePath):
        """Create windshield wipers"""
        card_maker = CardMaker("wiper")
        wiper_length = self.width * 0.35
        wiper_thickness = 0.03
        wiper_color = (0.08, 0.08, 0.08, 1.0)

        windshield_base_z = self.wheel_radius + self.body_height + 0.1

        # Driver side wiper
        card_maker.setFrame(0, wiper_length, -wiper_thickness/2, wiper_thickness/2)
        wiper = parent.attachNewNode(card_maker.generate())
        wiper.setPos(-self.width/4, self.length/2 - self.hood_length - 0.2, windshield_base_z)
        wiper.setP(-90)
        wiper.setColor(wiper_color)

    def _create_exhaust(self, parent: NodePath):
        """Create exhaust pipe"""
        card_maker = CardMaker("exhaust")
        exhaust_radius = 0.08
        exhaust_color = (0.25, 0.25, 0.28, 1.0)  # Dark metal

        # Single or dual exhaust based on vehicle type
        if self.vehicle_type in [VehicleType.SPORTS_CAR, VehicleType.TRUCK]:
            # Dual exhaust
            for x in [-self.width/3, self.width/3]:
                card_maker.setFrame(-exhaust_radius, exhaust_radius,
                                   -exhaust_radius, exhaust_radius)
                exhaust = parent.attachNewNode(card_maker.generate())
                exhaust.setPos(x, -self.length/2 - 0.05, self.wheel_radius + 0.2)
                exhaust.setH(180)
                exhaust.setColor(exhaust_color)
        else:
            # Single exhaust (right side)
            card_maker.setFrame(-exhaust_radius, exhaust_radius,
                               -exhaust_radius, exhaust_radius)
            exhaust = parent.attachNewNode(card_maker.generate())
            exhaust.setPos(self.width/3, -self.length/2 - 0.05, self.wheel_radius + 0.2)
            exhaust.setH(180)
            exhaust.setColor(exhaust_color)

    def _add_special_markings(self, parent: NodePath):
        """Add special vehicle markings"""
        card_maker = CardMaker("marking")

        if self.vehicle_type == VehicleType.POLICE:
            # Police stripes and lightbar
            stripe_color = (0.10, 0.35, 0.95, 1.0)  # Blue

            # Side stripes
            card_maker.setFrame(-self.length/2 + 1, self.length/2 - 1, 0, 0.25)
            for x in [-self.width/2 - 0.01, self.width/2 + 0.01]:
                stripe = parent.attachNewNode(card_maker.generate())
                stripe.setPos(x, 0, self.wheel_radius + self.body_height * 0.55)
                stripe.setH(90 if x < 0 else -90)
                stripe.setColor(stripe_color)

            # Roof lightbar
            lightbar_color = (0.85, 0.10, 0.10, 1.0)  # Red
            card_maker.setFrame(-self.width * 0.4, self.width * 0.4, -0.15, 0.15)
            lightbar = parent.attachNewNode(card_maker.generate())
            lightbar.setZ(self.wheel_radius + self.body_height + self.cabin_height + 0.15)
            lightbar.setP(-90)
            lightbar.setColor(lightbar_color)

        elif self.vehicle_type == VehicleType.AMBULANCE:
            # Red cross on sides and rear
            cross_color = (0.95, 0.08, 0.08, 1.0)
            cross_size = 0.6

            # Side crosses
            card_maker.setFrame(-cross_size/2, cross_size/2, -cross_size/2, cross_size/2)
            for x in [-self.width/2 - 0.03, self.width/2 + 0.03]:
                cross = parent.attachNewNode(card_maker.generate())
                cross.setPos(x, 0, self.wheel_radius + self.body_height + self.cabin_height * 0.5)
                cross.setH(90 if x < 0 else -90)
                cross.setColor(cross_color)

            # Roof lightbar
            lightbar_color = (0.10, 0.35, 0.95, 1.0)  # Blue
            card_maker.setFrame(-self.width * 0.4, self.width * 0.4, -0.15, 0.15)
            lightbar = parent.attachNewNode(card_maker.generate())
            lightbar.setZ(self.wheel_radius + self.body_height + self.cabin_height + 0.15)
            lightbar.setP(-90)
            lightbar.setColor(lightbar_color)

        elif self.vehicle_type == VehicleType.TAXI:
            # Roof taxi sign
            sign_color = (1.0, 0.92, 0.10, 1.0)  # Yellow
            card_maker.setFrame(-0.6, 0.6, -0.25, 0.25)
            sign = parent.attachNewNode(card_maker.generate())
            sign.setZ(self.wheel_radius + self.body_height + self.cabin_height + 0.15)
            sign.setP(-90)
            sign.setColor(sign_color)


class DetailedVehicleSpawner:
    """Spawner for detailed vehicles"""

    def __init__(self):
        """Initialize spawner"""
        self.spawn_weights = {
            VehicleType.SEDAN: 0.28,
            VehicleType.SUV: 0.18,
            VehicleType.HATCHBACK: 0.14,
            VehicleType.TRUCK: 0.10,
            VehicleType.VAN: 0.08,
            VehicleType.DELIVERY_TRUCK: 0.06,
            VehicleType.TAXI: 0.05,
            VehicleType.SPORTS_CAR: 0.04,
            VehicleType.POLICE: 0.03,
            VehicleType.BUS: 0.02,
            VehicleType.AMBULANCE: 0.01,
            VehicleType.VINTAGE: 0.01,
        }

    def spawn_random_vehicle(self, parent_node: NodePath,
                           position: Tuple[float, float, float],
                           heading: float = 0) -> NodePath:
        """Spawn random detailed vehicle"""
        vehicle_type = np.random.choice(
            list(self.spawn_weights.keys()),
            p=list(self.spawn_weights.values())
        )

        vehicle = DetailedVehicle(vehicle_type)
        return vehicle.create_3d_model(parent_node, position, heading)

    def spawn_specific_vehicle(self, vehicle_type: VehicleType, parent_node: NodePath,
                              position: Tuple[float, float, float],
                              heading: float = 0) -> NodePath:
        """Spawn specific vehicle type"""
        vehicle = DetailedVehicle(vehicle_type)
        return vehicle.create_3d_model(parent_node, position, heading)


if __name__ == "__main__":
    """Test detailed vehicle system"""
    print("Detailed Vehicle System Test")
    print("=" * 70)

    for vtype in VehicleType:
        vehicle = DetailedVehicle(vtype, seed=42)
        print(f"\n{vtype.name}:")
        print(f"  Dimensions: {vehicle.length:.2f}m x {vehicle.width:.2f}m x {vehicle.height:.2f}m")
        print(f"  Body proportions: Hood={vehicle.hood_length:.2f}m, "
              f"Cabin={vehicle.cabin_length:.2f}m, Trunk={vehicle.trunk_length:.2f}m")
        print(f"  Color: RGB{tuple(round(c, 2) for c in vehicle.body_color[:3])}")

    print("\n" + "=" * 70)
    print(f"Total vehicle types: {len(VehicleType)}")
    print("Photorealistic vehicles with detailed geometry!")
