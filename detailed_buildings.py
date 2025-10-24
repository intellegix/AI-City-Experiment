"""
Detailed Building System - Extremely Realistic Architecture
Creates photorealistic buildings with advanced geometry and details

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from typing import Tuple, List, Dict
from enum import Enum
from city_generator import ZoneType


class BuildingStyle(Enum):
    """Architectural styles"""
    MODERN_GLASS = 0
    MODERN_CONCRETE = 1
    CLASSIC_BRICK = 2
    INDUSTRIAL_WAREHOUSE = 3
    LUXURY_RESIDENTIAL = 4
    OFFICE_TOWER = 5
    MIXED_USE = 6
    ART_DECO = 7


class DetailedBuilding:
    """
    Extremely detailed building generator with realistic architecture.

    Features:
    - Detailed window frames with depth
    - Balconies with railings
    - Building trim and molding
    - Rooftop structures (AC units, water towers, antennas)
    - Ground floor storefronts
    - Fire escapes (for older buildings)
    - Varied roof types
    - Building damage/weathering effects
    - Entrance awnings and canopies
    - Window ledges and sills
    """

    def __init__(self, zone_type: ZoneType, seed: int = None):
        """Initialize detailed building"""
        self.zone_type = zone_type
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

        # Building parameters
        self.style = self._determine_style()
        self.floors = self._determine_floors()
        self.width = self._determine_width()
        self.depth = self._determine_depth()
        self.floor_height = 3.2  # Slightly taller for realism

        # Visual parameters
        self.base_color = self._determine_base_color()
        self.accent_color = self._determine_accent_color()
        self.window_color = self._determine_window_color()
        self.has_balconies = self._should_have_balconies()
        self.has_fire_escape = self._should_have_fire_escape()
        self.has_rooftop_detail = True  # Always have rooftop details
        self.weathering = np.random.uniform(0.0, 0.3)  # Weathering amount

    def _determine_style(self) -> BuildingStyle:
        """Determine architectural style based on zone"""
        if self.zone_type == ZoneType.COMMERCIAL:
            styles = [BuildingStyle.MODERN_GLASS, BuildingStyle.OFFICE_TOWER,
                     BuildingStyle.MIXED_USE]
            weights = [0.5, 0.3, 0.2]
        elif self.zone_type == ZoneType.RESIDENTIAL:
            styles = [BuildingStyle.LUXURY_RESIDENTIAL, BuildingStyle.MODERN_CONCRETE,
                     BuildingStyle.CLASSIC_BRICK]
            weights = [0.4, 0.3, 0.3]
        elif self.zone_type == ZoneType.INDUSTRIAL:
            styles = [BuildingStyle.INDUSTRIAL_WAREHOUSE]
            weights = [1.0]
        else:
            styles = [BuildingStyle.MODERN_GLASS, BuildingStyle.ART_DECO]
            weights = [0.7, 0.3]

        return np.random.choice(styles, p=weights)

    def _determine_floors(self) -> int:
        """Determine number of floors"""
        if self.style == BuildingStyle.OFFICE_TOWER:
            return np.random.randint(25, 55)
        elif self.style == BuildingStyle.MODERN_GLASS:
            return np.random.randint(10, 25)
        elif self.style == BuildingStyle.INDUSTRIAL_WAREHOUSE:
            return np.random.randint(2, 6)
        elif self.style == BuildingStyle.LUXURY_RESIDENTIAL:
            return np.random.randint(6, 18)
        elif self.style == BuildingStyle.ART_DECO:
            return np.random.randint(15, 35)
        else:
            return np.random.randint(5, 15)

    def _determine_width(self) -> float:
        """Determine building width"""
        if self.style == BuildingStyle.OFFICE_TOWER:
            return np.random.uniform(25, 45)
        elif self.style == BuildingStyle.INDUSTRIAL_WAREHOUSE:
            return np.random.uniform(30, 60)
        else:
            return np.random.uniform(15, 35)

    def _determine_depth(self) -> float:
        """Determine building depth"""
        if self.style == BuildingStyle.INDUSTRIAL_WAREHOUSE:
            return np.random.uniform(40, 80)
        else:
            return np.random.uniform(20, 40)

    def _determine_base_color(self) -> Tuple[float, float, float, float]:
        """Determine base color with realistic materials"""
        if self.style == BuildingStyle.MODERN_GLASS:
            # Glass buildings - blue/green tinted glass
            colors = [
                (0.45, 0.55, 0.65, 1.0),  # Blue glass
                (0.50, 0.60, 0.70, 1.0),  # Light blue glass
                (0.48, 0.58, 0.55, 1.0),  # Green-tinted glass
            ]
        elif self.style == BuildingStyle.MODERN_CONCRETE:
            # Modern concrete - light grays and whites
            colors = [
                (0.88, 0.88, 0.92, 1.0),  # White concrete
                (0.75, 0.75, 0.80, 1.0),  # Light gray concrete
                (0.82, 0.85, 0.88, 1.0),  # Off-white
            ]
        elif self.style == BuildingStyle.CLASSIC_BRICK:
            # Brick buildings - warm reds and oranges
            colors = [
                (0.65, 0.42, 0.35, 1.0),  # Red brick
                (0.70, 0.50, 0.38, 1.0),  # Orange brick
                (0.58, 0.38, 0.30, 1.0),  # Dark brick
            ]
        elif self.style == BuildingStyle.INDUSTRIAL_WAREHOUSE:
            # Industrial - dark concrete and metal
            colors = [
                (0.45, 0.47, 0.50, 1.0),  # Industrial gray
                (0.50, 0.52, 0.55, 1.0),  # Light industrial
                (0.40, 0.42, 0.45, 1.0),  # Dark industrial
            ]
        elif self.style == BuildingStyle.LUXURY_RESIDENTIAL:
            # Upscale residences - creams and beiges
            colors = [
                (0.92, 0.88, 0.80, 1.0),  # Cream
                (0.88, 0.82, 0.72, 1.0),  # Beige
                (0.95, 0.92, 0.88, 1.0),  # Ivory
            ]
        elif self.style == BuildingStyle.OFFICE_TOWER:
            # Office towers - steel and glass
            colors = [
                (0.52, 0.58, 0.68, 1.0),  # Steel blue
                (0.48, 0.52, 0.60, 1.0),  # Dark steel
                (0.55, 0.60, 0.70, 1.0),  # Light steel
            ]
        elif self.style == BuildingStyle.ART_DECO:
            # Art Deco - elegant tones
            colors = [
                (0.85, 0.80, 0.70, 1.0),  # Limestone
                (0.75, 0.72, 0.65, 1.0),  # Sandstone
                (0.70, 0.65, 0.58, 1.0),  # Tan stone
            ]
        else:
            colors = [(0.70, 0.70, 0.75, 1.0)]

        return colors[np.random.randint(0, len(colors))]

    def _determine_accent_color(self) -> Tuple[float, float, float, float]:
        """Determine accent color for trim"""
        # Accent color contrasts with base
        base_bright = sum(self.base_color[:3]) / 3
        if base_bright > 0.65:
            # Dark accents for light buildings
            return (0.15, 0.15, 0.18, 1.0)
        else:
            # Light accents for dark buildings
            return (0.92, 0.92, 0.95, 1.0)

    def _determine_window_color(self) -> Tuple[float, float, float, float]:
        """Determine window glass color"""
        if self.style == BuildingStyle.MODERN_GLASS:
            # Reflective blue glass
            return (0.25, 0.35, 0.50, 0.7)
        elif self.style == BuildingStyle.OFFICE_TOWER:
            # Dark reflective glass
            return (0.20, 0.25, 0.35, 0.8)
        else:
            # Standard dark glass
            return (0.15, 0.20, 0.30, 0.75)

    def _should_have_balconies(self) -> bool:
        """Determine if building has balconies"""
        if self.style == BuildingStyle.LUXURY_RESIDENTIAL:
            return np.random.random() > 0.2  # 80% chance
        elif self.style == BuildingStyle.MODERN_CONCRETE:
            return np.random.random() > 0.5  # 50% chance
        else:
            return False

    def _should_have_fire_escape(self) -> bool:
        """Determine if building has fire escape"""
        if self.style in [BuildingStyle.CLASSIC_BRICK, BuildingStyle.INDUSTRIAL_WAREHOUSE]:
            return np.random.random() > 0.4  # 60% chance for older buildings
        else:
            return False

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float]) -> NodePath:
        """Create extremely detailed 3D building"""
        height = self.floors * self.floor_height

        building_node = parent_node.attachNewNode(f"detailed_building_{self.seed}")
        building_node.setPos(*position)

        # 1. Main structure
        self._create_main_structure(building_node, height)

        # 2. Detailed windows with frames
        self._create_detailed_windows(building_node, height)

        # 3. Balconies (if applicable)
        if self.has_balconies:
            self._create_balconies(building_node, height)

        # 4. Building trim and molding
        self._create_trim_molding(building_node, height)

        # 5. Ground floor storefront
        self._create_ground_floor_details(building_node)

        # 6. Fire escape (if applicable)
        if self.has_fire_escape:
            self._create_fire_escape(building_node, height)

        # 7. Rooftop structures
        self._create_detailed_rooftop(building_node, height)

        # 8. Entrance canopy
        self._create_entrance_canopy(building_node)

        # 9. Building details (AC units on walls, etc.)
        self._create_wall_details(building_node, height)

        return building_node

    def _create_main_structure(self, parent: NodePath, height: float):
        """Create main building structure"""
        card_maker = CardMaker("building_main")

        # Apply weathering to base color
        weathered_color = self._apply_weathering(self.base_color)

        # Front face
        card_maker.setFrame(-self.width/2, self.width/2, 0, height)
        front = parent.attachNewNode(card_maker.generate())
        front.setY(-self.depth/2)
        front.setColor(weathered_color)
        front.setTag("building_face", "front")

        # Back face
        back = parent.attachNewNode(card_maker.generate())
        back.setY(self.depth/2)
        back.setH(180)
        back.setColor(weathered_color)
        back.setTag("building_face", "back")

        # Left face
        card_maker.setFrame(-self.depth/2, self.depth/2, 0, height)
        left = parent.attachNewNode(card_maker.generate())
        left.setX(-self.width/2)
        left.setH(90)
        left.setColor(weathered_color)
        left.setTag("building_face", "left")

        # Right face
        right = parent.attachNewNode(card_maker.generate())
        right.setX(self.width/2)
        right.setH(-90)
        right.setColor(weathered_color)
        right.setTag("building_face", "right")

        # Roof
        self._create_detailed_roof(parent, height)

    def _create_detailed_roof(self, parent: NodePath, height: float):
        """Create detailed roof with proper geometry"""
        card_maker = CardMaker("roof")
        roof_color = self._get_roof_color()

        if self.style == BuildingStyle.ART_DECO:
            # Stepped pyramid roof
            levels = 3
            step_size = min(self.width, self.depth) * 0.1
            for i in range(levels):
                offset = i * step_size
                level_width = self.width - offset * 2
                level_depth = self.depth - offset * 2
                level_height = i * 2.0

                card_maker.setFrame(-level_width/2, level_width/2, -level_depth/2, level_depth/2)
                roof_level = parent.attachNewNode(card_maker.generate())
                roof_level.setZ(height + level_height)
                roof_level.setP(-90)
                roof_level.setColor(roof_color)
        else:
            # Flat roof with slight border
            card_maker.setFrame(-self.width/2, self.width/2, -self.depth/2, self.depth/2)
            roof = parent.attachNewNode(card_maker.generate())
            roof.setZ(height)
            roof.setP(-90)
            roof.setColor(roof_color)

            # Roof border/parapet
            self._create_roof_parapet(parent, height)

    def _create_roof_parapet(self, parent: NodePath, height: float):
        """Create roof parapet (low wall around roof edge)"""
        card_maker = CardMaker("parapet")
        parapet_height = 1.2
        parapet_thickness = 0.3

        # Front parapet
        card_maker.setFrame(-self.width/2, self.width/2, 0, parapet_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -self.depth/2, height)
        front.setColor(self.accent_color)

        # Back parapet
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, self.depth/2, height)
        back.setH(180)
        back.setColor(self.accent_color)

        # Left parapet
        card_maker.setFrame(-self.depth/2, self.depth/2, 0, parapet_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-self.width/2, 0, height)
        left.setH(90)
        left.setColor(self.accent_color)

        # Right parapet
        right = parent.attachNewNode(card_maker.generate())
        right.setPos(self.width/2, 0, height)
        right.setH(-90)
        right.setColor(self.accent_color)

    def _create_detailed_windows(self, parent: NodePath, height: float):
        """Create windows with frames, sills, and depth"""
        window_size = 1.4
        window_frame_width = 0.12
        window_sill_depth = 0.25

        windows_per_floor_w = max(2, int(self.width / 3.5))
        windows_per_floor_d = max(2, int(self.depth / 3.5))

        for floor in range(1, self.floors):
            floor_z = floor * self.floor_height + self.floor_height * 0.4

            # Front and back windows
            for i in range(windows_per_floor_w):
                x_offset = -self.width/2 + (i + 0.5) * (self.width / windows_per_floor_w)

                # Front - offset further to prevent z-fighting
                self._create_window_with_frame(parent, x_offset, -self.depth/2 - 0.15, floor_z,
                                               window_size, window_frame_width, window_sill_depth, 0)
                # Back
                self._create_window_with_frame(parent, x_offset, self.depth/2 + 0.15, floor_z,
                                               window_size, window_frame_width, window_sill_depth, 180)

            # Side windows
            for i in range(windows_per_floor_d):
                y_offset = -self.depth/2 + (i + 0.5) * (self.depth / windows_per_floor_d)

                # Left - offset further to prevent z-fighting
                self._create_window_with_frame(parent, -self.width/2 - 0.15, y_offset, floor_z,
                                               window_size, window_frame_width, window_sill_depth, 90)
                # Right
                self._create_window_with_frame(parent, self.width/2 + 0.15, y_offset, floor_z,
                                               window_size, window_frame_width, window_sill_depth, -90)

    def _create_window_with_frame(self, parent: NodePath, x: float, y: float, z: float,
                                   size: float, frame_width: float, sill_depth: float, heading: float):
        """Create detailed window with frame and sill"""
        card_maker = CardMaker("window")

        # Window glass
        card_maker.setFrame(-size/2, size/2, -size/2, size/2)
        window = parent.attachNewNode(card_maker.generate())
        window.setPos(x, y, z)
        window.setH(heading)
        window.setColor(self.window_color)
        window.setTransparency(TransparencyAttrib.MAlpha)

        # Window frame (4 sides)
        frame_color = self.accent_color

        # Top frame
        card_maker.setFrame(-size/2 - frame_width, size/2 + frame_width, size/2, size/2 + frame_width)
        top_frame = parent.attachNewNode(card_maker.generate())
        top_frame.setPos(x, y - 0.01 if heading == 0 else y + 0.01, z)
        top_frame.setH(heading)
        top_frame.setColor(frame_color)

        # Bottom frame (window sill - slightly deeper)
        card_maker.setFrame(-size/2 - frame_width, size/2 + frame_width,
                           -size/2 - sill_depth, -size/2)
        sill = parent.attachNewNode(card_maker.generate())
        sill.setPos(x, y - 0.01 if heading == 0 else y + 0.01, z)
        sill.setH(heading)
        sill.setColor(frame_color)

        # Left frame
        card_maker.setFrame(-size/2 - frame_width, -size/2, -size/2, size/2)
        left_frame = parent.attachNewNode(card_maker.generate())
        left_frame.setPos(x, y - 0.01 if heading == 0 else y + 0.01, z)
        left_frame.setH(heading)
        left_frame.setColor(frame_color)

        # Right frame
        card_maker.setFrame(size/2, size/2 + frame_width, -size/2, size/2)
        right_frame = parent.attachNewNode(card_maker.generate())
        right_frame.setPos(x, y - 0.01 if heading == 0 else y + 0.01, z)
        right_frame.setH(heading)
        right_frame.setColor(frame_color)

    def _create_balconies(self, parent: NodePath, height: float):
        """Create balconies with railings"""
        balcony_depth = 1.5
        balcony_width = min(self.width * 0.4, 6.0)
        balcony_height = 0.15
        railing_height = 1.0

        # Balconies on alternating floors
        for floor in range(2, self.floors, 2):
            floor_z = floor * self.floor_height

            # Front balconies (3-4 per floor)
            num_balconies = min(4, int(self.width / 8))
            for i in range(num_balconies):
                x_offset = -self.width/2 + (i + 0.5) * (self.width / num_balconies)
                self._create_single_balcony(parent, x_offset, -self.depth/2, floor_z,
                                           balcony_width, balcony_depth, balcony_height, railing_height, 0)

    def _create_single_balcony(self, parent: NodePath, x: float, y: float, z: float,
                               width: float, depth: float, height: float, railing_height: float, heading: float):
        """Create single balcony with railing"""
        card_maker = CardMaker("balcony")

        # Balcony floor
        card_maker.setFrame(-width/2, width/2, 0, depth)
        floor = parent.attachNewNode(card_maker.generate())
        floor.setPos(x, y, z)
        floor.setH(heading)
        floor.setP(-90)
        floor.setColor(self.accent_color)

        # Railing (front and sides)
        railing_color = (0.3, 0.3, 0.35, 1.0)  # Dark metal
        railing_thickness = 0.08

        # Front railing
        card_maker.setFrame(-width/2, width/2, 0, railing_height)
        front_rail = parent.attachNewNode(card_maker.generate())
        front_rail.setPos(x, y + depth, z + height)
        front_rail.setH(heading)
        front_rail.setColor(railing_color)

        # Left railing
        card_maker.setFrame(0, depth, 0, railing_height)
        left_rail = parent.attachNewNode(card_maker.generate())
        left_rail.setPos(x - width/2, y, z + height)
        left_rail.setH(heading + 90)
        left_rail.setColor(railing_color)

        # Right railing
        right_rail = parent.attachNewNode(card_maker.generate())
        right_rail.setPos(x + width/2, y, z + height)
        right_rail.setH(heading - 90)
        right_rail.setColor(railing_color)

    def _create_trim_molding(self, parent: NodePath, height: float):
        """Create decorative trim and molding"""
        if self.style in [BuildingStyle.CLASSIC_BRICK, BuildingStyle.ART_DECO, BuildingStyle.LUXURY_RESIDENTIAL]:
            # Horizontal trim every few floors
            trim_height = 0.25
            trim_depth = 0.15

            for floor in range(0, self.floors, 5):
                if floor == 0:
                    continue
                floor_z = floor * self.floor_height
                self._create_horizontal_trim(parent, floor_z, trim_height, trim_depth)

    def _create_horizontal_trim(self, parent: NodePath, z: float, trim_height: float, depth: float):
        """Create horizontal decorative trim around building"""
        card_maker = CardMaker("trim")

        # Front trim
        card_maker.setFrame(-self.width/2, self.width/2, 0, trim_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -self.depth/2 - depth, z)
        front.setColor(self.accent_color)

        # Back trim
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, self.depth/2 + depth, z)
        back.setH(180)
        back.setColor(self.accent_color)

        # Left trim
        card_maker.setFrame(-self.depth/2, self.depth/2, 0, trim_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-self.width/2 - depth, 0, z)
        left.setH(90)
        left.setColor(self.accent_color)

        # Right trim
        right = parent.attachNewNode(card_maker.generate())
        right.setPos(self.width/2 + depth, 0, z)
        right.setH(-90)
        right.setColor(self.accent_color)

    def _create_ground_floor_details(self, parent: NodePath):
        """Create ground floor storefront details"""
        if self.zone_type == ZoneType.COMMERCIAL or self.style == BuildingStyle.MIXED_USE:
            # Storefront windows (larger than regular windows)
            storefront_height = 2.5
            storefront_width = min(self.width * 0.8, 12.0)

            card_maker = CardMaker("storefront")
            card_maker.setFrame(-storefront_width/2, storefront_width/2, 0.5, storefront_height)

            storefront = parent.attachNewNode(card_maker.generate())
            storefront.setPos(0, -self.depth/2 - 0.1, 0)
            storefront.setColor((0.15, 0.18, 0.22, 0.6))  # Dark glass
            storefront.setTransparency(TransparencyAttrib.MAlpha)

            # Storefront frame
            card_maker.setFrame(-storefront_width/2 - 0.2, storefront_width/2 + 0.2, 0, 0.1)
            frame_top = parent.attachNewNode(card_maker.generate())
            frame_top.setPos(0, -self.depth/2 - 0.12, storefront_height)
            frame_top.setColor(self.accent_color)

    def _create_fire_escape(self, parent: NodePath, height: float):
        """Create external fire escape on side of building"""
        # Fire escape on right side
        escape_width = 1.0
        escape_color = (0.25, 0.15, 0.10, 1.0)  # Rusty metal

        # Vertical ladder/stairs
        for floor in range(1, self.floors - 1):
            floor_z = floor * self.floor_height

            # Platform
            card_maker = CardMaker("fire_escape_platform")
            card_maker.setFrame(0, escape_width, 0, escape_width)
            platform = parent.attachNewNode(card_maker.generate())
            platform.setPos(self.width/2 + 0.2, 0, floor_z)
            platform.setP(-90)
            platform.setColor(escape_color)

            # Railing
            card_maker.setFrame(0, escape_width, 0, 0.9)
            railing = parent.attachNewNode(card_maker.generate())
            railing.setPos(self.width/2 + 0.2, escape_width, floor_z)
            railing.setH(-90)
            railing.setColor(escape_color)

    def _create_detailed_rooftop(self, parent: NodePath, height: float):
        """Create detailed rooftop structures"""
        structures_added = 0
        max_structures = np.random.randint(3, 7)

        # AC units
        for i in range(max_structures // 2):
            size = np.random.uniform(1.5, 3.0)
            x = np.random.uniform(-self.width/3, self.width/3)
            y = np.random.uniform(-self.depth/3, self.depth/3)
            self._create_ac_unit(parent, x, y, height, size)
            structures_added += 1

        # Water tower (for older buildings)
        if self.style in [BuildingStyle.CLASSIC_BRICK, BuildingStyle.INDUSTRIAL_WAREHOUSE]:
            if np.random.random() > 0.5:
                self._create_water_tower(parent, 0, 0, height)
                structures_added += 1

        # Antenna/communications
        if structures_added < max_structures:
            x = np.random.uniform(-self.width/4, self.width/4)
            y = np.random.uniform(-self.depth/4, self.depth/4)
            self._create_antenna(parent, x, y, height)

    def _create_ac_unit(self, parent: NodePath, x: float, y: float, z: float, size: float):
        """Create air conditioning unit"""
        card_maker = CardMaker("ac_unit")
        ac_color = (0.60, 0.62, 0.65, 1.0)  # Metal gray
        ac_height = size * 0.6

        # AC box
        # Front
        card_maker.setFrame(-size/2, size/2, 0, ac_height)
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(x, y - size/2, z)
        front.setColor(ac_color)

        # Back
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(x, y + size/2, z)
        back.setH(180)
        back.setColor(ac_color)

        # Sides
        card_maker.setFrame(-size/2, size/2, 0, ac_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(x - size/2, y, z)
        left.setH(90)
        left.setColor(ac_color)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(x + size/2, y, z)
        right.setH(-90)
        right.setColor(ac_color)

        # Top
        card_maker.setFrame(-size/2, size/2, -size/2, size/2)
        top = parent.attachNewNode(card_maker.generate())
        top.setPos(x, y, z + ac_height)
        top.setP(-90)
        top.setColor(ac_color)

    def _create_water_tower(self, parent: NodePath, x: float, y: float, z: float):
        """Create water tower"""
        tower_radius = 2.5
        tower_height = 4.0
        support_height = 3.0

        # Cylindrical tank (represented as octagon)
        card_maker = CardMaker("water_tower")
        tower_color = (0.35, 0.30, 0.28, 1.0)  # Dark rusty metal

        sides = 8
        for i in range(sides):
            angle1 = (i / sides) * 360
            angle2 = ((i + 1) / sides) * 360

            x1 = tower_radius * np.cos(np.radians(angle1))
            y1 = tower_radius * np.sin(np.radians(angle1))
            x2 = tower_radius * np.cos(np.radians(angle2))
            y2 = tower_radius * np.sin(np.radians(angle2))

            card_maker.setFrame(0, np.sqrt((x2-x1)**2 + (y2-y1)**2), 0, tower_height)
            side = parent.attachNewNode(card_maker.generate())
            side.setPos(x + x1, y + y1, z + support_height)
            side.setH(angle1)
            side.setColor(tower_color)

        # Support legs
        leg_color = (0.25, 0.20, 0.18, 1.0)
        for i in range(4):
            angle = i * 90
            leg_x = tower_radius * 0.7 * np.cos(np.radians(angle))
            leg_y = tower_radius * 0.7 * np.sin(np.radians(angle))

            card_maker.setFrame(-0.2, 0.2, 0, support_height)
            leg = parent.attachNewNode(card_maker.generate())
            leg.setPos(x + leg_x, y + leg_y, z)
            leg.setColor(leg_color)

    def _create_antenna(self, parent: NodePath, x: float, y: float, z: float):
        """Create antenna or communications tower"""
        card_maker = CardMaker("antenna")
        antenna_height = np.random.uniform(4.0, 8.0)
        antenna_color = (0.70, 0.72, 0.75, 1.0)  # Light metal

        # Main pole
        card_maker.setFrame(-0.1, 0.1, 0, antenna_height)
        pole = parent.attachNewNode(card_maker.generate())
        pole.setPos(x, y, z)
        pole.setColor(antenna_color)

        # Cross pieces
        for i in range(3):
            cross_z = z + antenna_height * (0.3 + i * 0.25)
            card_maker.setFrame(-0.5, 0.5, -0.05, 0.05)
            cross = parent.attachNewNode(card_maker.generate())
            cross.setPos(x, y, cross_z)
            cross.setP(-90)
            cross.setColor(antenna_color)

    def _create_entrance_canopy(self, parent: NodePath):
        """Create entrance canopy/awning"""
        canopy_width = min(self.width * 0.5, 8.0)
        canopy_depth = 2.5
        canopy_height = 0.2

        card_maker = CardMaker("canopy")

        # Canopy surface
        card_maker.setFrame(-canopy_width/2, canopy_width/2, 0, canopy_depth)
        canopy = parent.attachNewNode(card_maker.generate())
        canopy.setPos(0, -self.depth/2, 3.5)
        canopy.setP(-90)
        canopy.setColor(self.accent_color)

        # Support posts
        post_color = (0.25, 0.25, 0.28, 1.0)
        for x_pos in [-canopy_width/2 + 0.5, canopy_width/2 - 0.5]:
            card_maker.setFrame(-0.15, 0.15, 0, 3.5)
            post = parent.attachNewNode(card_maker.generate())
            post.setPos(x_pos, -self.depth/2 + canopy_depth - 0.3, 0)
            post.setColor(post_color)

    def _create_wall_details(self, parent: NodePath, height: float):
        """Create wall-mounted details (AC units, vents, etc.)"""
        # Only add wall details if building has at least 3 floors
        if self.floors < 3:
            return

        # Random wall-mounted AC units
        num_units = np.random.randint(2, 5)
        for i in range(num_units):
            floor = np.random.randint(1, self.floors - 1)
            floor_z = floor * self.floor_height + 1.5
            x_offset = np.random.uniform(-self.width/3, self.width/3)

            # Small wall AC unit
            card_maker = CardMaker("wall_ac")
            card_maker.setFrame(-0.4, 0.4, -0.3, 0.3)
            ac = parent.attachNewNode(card_maker.generate())
            ac.setPos(x_offset, -self.depth/2 - 0.2, floor_z)
            ac.setColor((0.55, 0.57, 0.60, 1.0))

    def _apply_weathering(self, color: Tuple[float, float, float, float]) -> Tuple[float, float, float, float]:
        """Apply weathering effect to color"""
        r, g, b, a = color
        # Darken slightly based on weathering amount
        factor = 1.0 - (self.weathering * 0.2)
        return (r * factor, g * factor, b * factor, a)

    def _get_roof_color(self) -> Tuple[float, float, float, float]:
        """Get roof color"""
        if self.style == BuildingStyle.INDUSTRIAL_WAREHOUSE:
            return (0.35, 0.35, 0.38, 1.0)  # Dark industrial roof
        else:
            base_r, base_g, base_b, _ = self.base_color
            return (base_r * 0.6, base_g * 0.6, base_b * 0.6, 1.0)

    def get_specs(self) -> Dict:
        """Get building specifications"""
        return {
            'style': self.style.name,
            'floors': self.floors,
            'height': self.floors * self.floor_height,
            'width': self.width,
            'depth': self.depth,
            'has_balconies': self.has_balconies,
            'has_fire_escape': self.has_fire_escape,
            'weathering': self.weathering
        }


if __name__ == "__main__":
    """Test detailed building system"""
    print("Detailed Building System Test")
    print("=" * 60)

    for zone in [ZoneType.COMMERCIAL, ZoneType.RESIDENTIAL, ZoneType.INDUSTRIAL]:
        building = DetailedBuilding(zone, seed=42 + zone.value)
        specs = building.get_specs()

        print(f"\n{zone.name} Building:")
        print(f"  Style: {specs['style']}")
        print(f"  Floors: {specs['floors']}")
        print(f"  Dimensions: {specs['width']:.1f}m x {specs['depth']:.1f}m x {specs['height']:.1f}m")
        print(f"  Balconies: {specs['has_balconies']}")
        print(f"  Fire Escape: {specs['has_fire_escape']}")
        print(f"  Weathering: {specs['weathering']:.2f}")

    print("\n" + "=" * 60)
    print("Extremely detailed buildings with realistic architecture!")
