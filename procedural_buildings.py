"""
Procedural Building System - Infinite Variety
Creates unique buildings through procedural generation

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
from direct.showbase.ShowBase import ShowBase
import numpy as np
from typing import Tuple, List, Dict
from enum import Enum
from city_generator import ZoneType


class BuildingStyle(Enum):
    """Architectural styles for buildings"""
    MODERN = 0
    CLASSIC = 1
    INDUSTRIAL = 2
    RESIDENTIAL = 3
    SKYSCRAPER = 4


class WindowPattern(Enum):
    """Window arrangement patterns"""
    GRID = 0
    HORIZONTAL_STRIPS = 1
    VERTICAL_STRIPS = 2
    RANDOM = 3
    CORNER_WINDOWS = 4


class ProceduralBuilding:
    """
    Advanced procedural building generator.

    Creates unique buildings with:
    - Variable heights (3-50 floors)
    - Different window patterns
    - Varied architectural styles
    - Color schemes by zone type
    - Rooftop variations
    - Facade details
    """

    def __init__(self, zone_type: ZoneType, seed: int = None):
        """Initialize building generator"""
        self.zone_type = zone_type
        self.seed = seed or np.random.randint(0, 1000000)
        np.random.seed(self.seed)

        # Building parameters
        self.style = self._determine_style()
        self.floors = self._determine_floors()
        self.width = self._determine_width()
        self.depth = self._determine_depth()
        self.floor_height = 3.0  # meters per floor

        # Visual parameters
        self.base_color = self._determine_base_color()
        self.accent_color = self._determine_accent_color()
        self.window_pattern = self._determine_window_pattern()
        self.has_rooftop_detail = np.random.random() > 0.5

    def _determine_style(self) -> BuildingStyle:
        """Determine architectural style based on zone"""
        if self.zone_type == ZoneType.COMMERCIAL:
            styles = [BuildingStyle.MODERN, BuildingStyle.SKYSCRAPER]
            weights = [0.6, 0.4]
        elif self.zone_type == ZoneType.RESIDENTIAL:
            styles = [BuildingStyle.RESIDENTIAL, BuildingStyle.CLASSIC]
            weights = [0.7, 0.3]
        elif self.zone_type == ZoneType.INDUSTRIAL:
            styles = [BuildingStyle.INDUSTRIAL]
            weights = [1.0]
        else:
            styles = [BuildingStyle.MODERN, BuildingStyle.CLASSIC]
            weights = [0.5, 0.5]

        return np.random.choice(styles, p=weights)

    def _determine_floors(self) -> int:
        """Determine number of floors based on style"""
        if self.style == BuildingStyle.SKYSCRAPER:
            return np.random.randint(20, 51)
        elif self.style == BuildingStyle.MODERN:
            return np.random.randint(8, 20)
        elif self.style == BuildingStyle.INDUSTRIAL:
            return np.random.randint(3, 8)
        elif self.style == BuildingStyle.RESIDENTIAL:
            return np.random.randint(4, 12)
        else:  # CLASSIC
            return np.random.randint(5, 15)

    def _determine_width(self) -> float:
        """Determine building width"""
        if self.style == BuildingStyle.SKYSCRAPER:
            return np.random.uniform(20, 40)
        elif self.style == BuildingStyle.RESIDENTIAL:
            return np.random.uniform(12, 25)
        else:
            return np.random.uniform(15, 35)

    def _determine_depth(self) -> float:
        """Determine building depth"""
        return np.random.uniform(15, 30)

    def _determine_base_color(self) -> Tuple[float, float, float, float]:
        """Determine base color based on zone and style"""
        if self.style == BuildingStyle.SKYSCRAPER:
            # Modern glass and steel
            colors = [
                (0.5, 0.6, 0.7, 1.0),   # Blue-gray glass
                (0.6, 0.65, 0.75, 1.0), # Light blue glass
                (0.55, 0.55, 0.6, 1.0), # Steel gray
            ]
        elif self.style == BuildingStyle.MODERN:
            # Clean modern materials
            colors = [
                (0.85, 0.85, 0.9, 1.0), # White concrete
                (0.7, 0.7, 0.75, 1.0),  # Light gray
                (0.6, 0.65, 0.7, 1.0),  # Medium gray
            ]
        elif self.style == BuildingStyle.RESIDENTIAL:
            # Warm residential colors
            colors = [
                (0.9, 0.85, 0.75, 1.0),  # Cream
                (0.85, 0.8, 0.7, 1.0),   # Beige
                (0.95, 0.9, 0.85, 1.0),  # Off-white
                (0.75, 0.65, 0.55, 1.0), # Tan
            ]
        elif self.style == BuildingStyle.INDUSTRIAL:
            # Industrial materials
            colors = [
                (0.5, 0.52, 0.55, 1.0), # Dark concrete
                (0.6, 0.58, 0.56, 1.0), # Weathered concrete
                (0.45, 0.47, 0.5, 1.0), # Industrial gray
            ]
        else:  # CLASSIC
            # Classic building materials
            colors = [
                (0.65, 0.5, 0.4, 1.0),  # Brick red
                (0.7, 0.6, 0.5, 1.0),   # Brick orange
                (0.8, 0.75, 0.65, 1.0), # Limestone
            ]

        return colors[np.random.randint(0, len(colors))]

    def _determine_accent_color(self) -> Tuple[float, float, float, float]:
        """Determine accent color for trim/details"""
        base_bright = sum(self.base_color[:3]) / 3
        if base_bright > 0.6:
            # Dark accents for light buildings
            return (0.2, 0.2, 0.25, 1.0)
        else:
            # Light accents for dark buildings
            return (0.9, 0.9, 0.95, 1.0)

    def _determine_window_pattern(self) -> WindowPattern:
        """Determine window arrangement pattern"""
        if self.style == BuildingStyle.SKYSCRAPER:
            patterns = [WindowPattern.GRID, WindowPattern.HORIZONTAL_STRIPS]
            weights = [0.7, 0.3]
        elif self.style == BuildingStyle.MODERN:
            patterns = [WindowPattern.GRID, WindowPattern.VERTICAL_STRIPS]
            weights = [0.6, 0.4]
        else:
            patterns = [WindowPattern.GRID, WindowPattern.RANDOM]
            weights = [0.8, 0.2]

        return np.random.choice(patterns, p=weights)

    def create_3d_model(self, parent_node: NodePath, position: Tuple[float, float, float]) -> NodePath:
        """Create 3D building geometry"""
        height = self.floors * self.floor_height

        # Create main building node
        building_node = parent_node.attachNewNode(f"building_{self.seed}")
        building_node.setPos(*position)

        # Create building base (main structure)
        self._create_base_structure(building_node, height)

        # Add windows
        self._add_windows(building_node, height)

        # Add rooftop detail
        if self.has_rooftop_detail:
            self._add_rooftop(building_node, height)

        # Add entrance (ground floor detail)
        self._add_entrance(building_node)

        return building_node

    def _create_base_structure(self, parent: NodePath, height: float):
        """Create main building structure"""
        card_maker = CardMaker("building_base")

        # Front face
        card_maker.setFrame(-self.width/2, self.width/2, 0, height)
        front = parent.attachNewNode(card_maker.generate())
        front.setY(-self.depth/2)
        front.setColor(self.base_color)

        # Back face
        back = parent.attachNewNode(card_maker.generate())
        back.setY(self.depth/2)
        back.setH(180)
        back.setColor(self.base_color)

        # Left face
        card_maker.setFrame(-self.depth/2, self.depth/2, 0, height)
        left = parent.attachNewNode(card_maker.generate())
        left.setX(-self.width/2)
        left.setH(90)
        left.setColor(self.base_color)

        # Right face
        right = parent.attachNewNode(card_maker.generate())
        right.setX(self.width/2)
        right.setH(-90)
        right.setColor(self.base_color)

        # Roof
        card_maker.setFrame(-self.width/2, self.width/2, -self.depth/2, self.depth/2)
        roof = parent.attachNewNode(card_maker.generate())
        roof.setZ(height)
        roof.setP(-90)
        roof.setColor(self._get_roof_color())

    def _add_windows(self, parent: NodePath, height: float):
        """Add windows based on pattern"""
        window_color = (0.2, 0.3, 0.4, 0.8)  # Dark blue glass
        window_size = 1.5

        if self.window_pattern == WindowPattern.GRID:
            # Regular grid pattern
            windows_per_floor_w = int(self.width / 3)
            windows_per_floor_d = int(self.depth / 3)

            for floor in range(1, self.floors):  # Skip ground floor
                floor_z = floor * self.floor_height + 1.0

                # Front and back windows
                for i in range(windows_per_floor_w):
                    x_offset = -self.width/2 + (i + 0.5) * (self.width / windows_per_floor_w)
                    self._create_window(parent, x_offset, -self.depth/2 - 0.01, floor_z, window_size, window_color, 0)
                    self._create_window(parent, x_offset, self.depth/2 + 0.01, floor_z, window_size, window_color, 180)

                # Side windows
                for i in range(windows_per_floor_d):
                    y_offset = -self.depth/2 + (i + 0.5) * (self.depth / windows_per_floor_d)
                    self._create_window(parent, -self.width/2 - 0.01, y_offset, floor_z, window_size, window_color, 90)
                    self._create_window(parent, self.width/2 + 0.01, y_offset, floor_z, window_size, window_color, -90)

        elif self.window_pattern == WindowPattern.HORIZONTAL_STRIPS:
            # Horizontal window bands
            for floor in range(1, self.floors, 2):  # Every other floor
                floor_z = floor * self.floor_height + 1.0
                self._create_window_strip(parent, -self.depth/2 - 0.01, floor_z, self.width, 2.0, window_color, 0)
                self._create_window_strip(parent, self.depth/2 + 0.01, floor_z, self.width, 2.0, window_color, 180)

    def _create_window(self, parent: NodePath, x: float, y: float, z: float, size: float, color: Tuple, heading: float):
        """Create single window"""
        card_maker = CardMaker("window")
        card_maker.setFrame(-size/2, size/2, -size/2, size/2)

        window = parent.attachNewNode(card_maker.generate())
        window.setPos(x, y, z)
        window.setH(heading)
        window.setColor(color)

        # Add window frame (accent color)
        frame_size = size + 0.2
        card_maker.setFrame(-frame_size/2, -frame_size/2 + 0.1, -frame_size/2, frame_size/2)
        frame = parent.attachNewNode(card_maker.generate())
        frame.setPos(x, y, z)
        frame.setH(heading)
        frame.setColor(self.accent_color)

    def _create_window_strip(self, parent: NodePath, y: float, z: float, width: float, height: float, color: Tuple, heading: float):
        """Create horizontal window strip"""
        card_maker = CardMaker("window_strip")
        card_maker.setFrame(-width/2, width/2, -height/2, height/2)

        strip = parent.attachNewNode(card_maker.generate())
        strip.setPos(0, y, z)
        strip.setH(heading)
        strip.setColor(color)

    def _add_rooftop(self, parent: NodePath, height: float):
        """Add rooftop details (AC units, antennas, etc.)"""
        # Simple rooftop structure
        card_maker = CardMaker("rooftop_detail")
        detail_height = np.random.uniform(2, 5)
        detail_width = min(self.width, self.depth) * 0.3

        card_maker.setFrame(-detail_width/2, detail_width/2, 0, detail_height)

        # Front
        front = parent.attachNewNode(card_maker.generate())
        front.setPos(0, -detail_width/2, height)
        front.setColor(self.accent_color)

        # Back
        back = parent.attachNewNode(card_maker.generate())
        back.setPos(0, detail_width/2, height)
        back.setH(180)
        back.setColor(self.accent_color)

        # Sides
        card_maker.setFrame(-detail_width/2, detail_width/2, 0, detail_height)
        left = parent.attachNewNode(card_maker.generate())
        left.setPos(-detail_width/2, 0, height)
        left.setH(90)
        left.setColor(self.accent_color)

        right = parent.attachNewNode(card_maker.generate())
        right.setPos(detail_width/2, 0, height)
        right.setH(-90)
        right.setColor(self.accent_color)

    def _add_entrance(self, parent: NodePath):
        """Add entrance detail at ground level"""
        # Create entrance overhang/canopy
        card_maker = CardMaker("entrance")
        entrance_width = min(self.width * 0.4, 8.0)
        entrance_depth = 2.0

        card_maker.setFrame(-entrance_width/2, entrance_width/2, -entrance_depth/2, entrance_depth/2)
        canopy = parent.attachNewNode(card_maker.generate())
        canopy.setPos(0, -self.depth/2 - entrance_depth/2, 3.0)
        canopy.setP(-90)
        canopy.setColor(self.accent_color)

    def _get_roof_color(self) -> Tuple[float, float, float, float]:
        """Get roof color (darker than base)"""
        base_r, base_g, base_b, _ = self.base_color
        return (base_r * 0.7, base_g * 0.7, base_b * 0.7, 1.0)

    def get_specs(self) -> Dict:
        """Get building specifications"""
        return {
            'style': self.style.name,
            'floors': self.floors,
            'height': self.floors * self.floor_height,
            'width': self.width,
            'depth': self.depth,
            'window_pattern': self.window_pattern.name,
            'base_color': self.base_color,
            'has_rooftop': self.has_rooftop_detail
        }


if __name__ == "__main__":
    """Test procedural building generation"""
    print("Procedural Building System Test")
    print("=" * 60)

    # Create sample buildings
    for i in range(5):
        for zone in [ZoneType.COMMERCIAL, ZoneType.RESIDENTIAL, ZoneType.INDUSTRIAL]:
            building = ProceduralBuilding(zone, seed=i * 100 + zone.value)
            specs = building.get_specs()

            print(f"\nBuilding {i+1} ({zone.name}):")
            print(f"  Style: {specs['style']}")
            print(f"  Floors: {specs['floors']}")
            print(f"  Dimensions: {specs['width']:.1f}m x {specs['depth']:.1f}m x {specs['height']:.1f}m")
            print(f"  Windows: {specs['window_pattern']}")
            print(f"  Rooftop detail: {specs['has_rooftop']}")

    print("\n" + "=" * 60)
    print("Procedural buildings can generate infinite unique variations!")
