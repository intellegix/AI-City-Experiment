"""
Procedural City Layout Generator with Road Networks
Implements Phase 3 of the blueprint: City Layout & Asset Placement

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
import networkx as nx
from typing import List, Tuple, Dict, Set, Optional
from dataclasses import dataclass
from enum import Enum
from config import CITY, Config
from terrain_generator import TerrainGenerator


class ZoneType(Enum):
    """City zone types"""
    COMMERCIAL = 0
    RESIDENTIAL = 1
    INDUSTRIAL = 2
    PARK = 3
    MIXED = 4


@dataclass
class Road:
    """Road segment"""
    start: Tuple[int, int]
    end: Tuple[int, int]
    width: int
    is_main: bool = False


@dataclass
class Building:
    """Building structure"""
    x: int
    y: int
    width: int
    height: int
    zone_type: ZoneType
    floors: int = 1


class CityLayoutGenerator:
    """
    Advanced procedural city generator with organic road networks.
    Features:
    - Main arterial roads radiating from center
    - Grid-based secondary streets
    - Zone-based building placement
    - Terrain-aware layout (avoids water, steep slopes)
    - Optimized for pathfinding with NetworkX graph
    """

    def __init__(self, terrain: TerrainGenerator, seed: int = None):
        """
        Initialize city generator.

        Args:
            terrain: TerrainGenerator instance for terrain awareness
            seed: Random seed
        """
        self.terrain = terrain
        self.size = terrain.size
        self.seed = seed or np.random.randint(0, 10000)
        np.random.seed(self.seed)

        # City data structures
        self.road_grid = np.zeros((self.size, self.size), dtype=bool)
        self.zone_map = np.zeros((self.size, self.size), dtype=np.int32)
        self.buildings: List[Building] = []
        self.roads: List[Road] = []

        # Road network graph for pathfinding
        self.road_graph = nx.Graph()

        # Center of city
        self.center = (self.size // 2, self.size // 2)

        print(f"CityLayoutGenerator initialized: {self.size}x{self.size}, seed={self.seed}")

    def generate(self) -> Tuple[np.ndarray, np.ndarray, List[Building]]:
        """
        Generate complete city layout.

        Returns:
            Tuple of (road_grid, zone_map, buildings)
        """
        print("Generating city layout...")

        # Generate road network
        self._generate_road_network()

        # Define city zones
        self._generate_zones()

        # Place buildings procedurally
        self._place_buildings()

        # Build road graph for pathfinding
        self._build_road_graph()

        print(f"City layout generated successfully!")
        print(f"  Roads: {len(self.roads)} segments")
        print(f"  Buildings: {len(self.buildings)}")
        print(f"  Road graph nodes: {self.road_graph.number_of_nodes()}")
        print(f"  Zone distribution: {self._get_zone_stats()}")

        return self.road_grid, self.zone_map, self.buildings

    def _generate_road_network(self):
        """
        Generate road network with main arterials and grid streets.
        Uses radial + grid hybrid pattern for organic yet navigable layout.
        """
        print("  Generating road network...")

        # 1. Create main arterial roads radiating from center
        self._create_radial_roads()

        # 2. Create ring roads at different radii
        self._create_ring_roads()

        # 3. Fill in grid pattern for secondary streets
        self._create_grid_roads()

        # 4. Smooth and connect roads
        self._smooth_roads()

    def _create_radial_roads(self):
        """Create main roads radiating from city center"""
        num_radials = CITY.NUM_MAIN_ROADS
        angles = np.linspace(0, 2 * np.pi, num_radials, endpoint=False)

        for angle in angles:
            # Calculate direction
            dx = np.cos(angle)
            dy = np.sin(angle)

            # Trace road from center to edge
            road_points = []
            for distance in range(0, self.size // 2, 2):
                x = int(self.center[0] + dx * distance)
                y = int(self.center[1] + dy * distance)

                if not (0 <= x < self.size and 0 <= y < self.size):
                    break

                # Check if terrain is suitable
                if not self.terrain.is_buildable(x, y):
                    continue

                road_points.append((x, y))

                # Draw road with width
                self._draw_road(x, y, CITY.MAIN_ROAD_WIDTH)

            # Store road segment
            if len(road_points) > 1:
                self.roads.append(Road(
                    start=road_points[0],
                    end=road_points[-1],
                    width=CITY.MAIN_ROAD_WIDTH,
                    is_main=True
                ))

    def _create_ring_roads(self):
        """Create circular ring roads at different radii"""
        ring_radii = [self.size // 6, self.size // 3, self.size // 2 - 20]

        for radius in ring_radii:
            circumference = int(2 * np.pi * radius)
            angles = np.linspace(0, 2 * np.pi, circumference // 3, endpoint=False)

            prev_point = None
            for angle in angles:
                x = int(self.center[0] + radius * np.cos(angle))
                y = int(self.center[1] + radius * np.sin(angle))

                if 0 <= x < self.size and 0 <= y < self.size:
                    if self.terrain.is_buildable(x, y):
                        self._draw_road(x, y, CITY.ROAD_WIDTH)

                        if prev_point:
                            self.roads.append(Road(
                                start=prev_point,
                                end=(x, y),
                                width=CITY.ROAD_WIDTH
                            ))
                        prev_point = (x, y)

    def _create_grid_roads(self):
        """Fill in grid pattern for secondary streets"""
        block_size = CITY.BLOCK_SIZE

        # Vertical streets
        for x in range(0, self.size, block_size):
            road_points = []
            for y in range(self.size):
                if self.terrain.is_buildable(x, y) and not self.road_grid[y, x]:
                    self._draw_road(x, y, CITY.ROAD_WIDTH)
                    road_points.append((x, y))
                elif len(road_points) > block_size:
                    self.roads.append(Road(
                        start=road_points[0],
                        end=road_points[-1],
                        width=CITY.ROAD_WIDTH
                    ))
                    road_points = []

        # Horizontal streets
        for y in range(0, self.size, block_size):
            road_points = []
            for x in range(self.size):
                if self.terrain.is_buildable(x, y) and not self.road_grid[y, x]:
                    self._draw_road(x, y, CITY.ROAD_WIDTH)
                    road_points.append((x, y))
                elif len(road_points) > block_size:
                    self.roads.append(Road(
                        start=road_points[0],
                        end=road_points[-1],
                        width=CITY.ROAD_WIDTH
                    ))
                    road_points = []

    def _draw_road(self, x: int, y: int, width: int):
        """Draw road segment with specified width"""
        half_width = width // 2
        for dy in range(-half_width, half_width + 1):
            for dx in range(-half_width, half_width + 1):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    self.road_grid[ny, nx] = True

    def _smooth_roads(self):
        """Apply smoothing to road network for better appearance"""
        # Simple morphological closing to connect nearby road segments
        from scipy.ndimage import binary_dilation, binary_erosion

        # Dilate then erode to close small gaps
        self.road_grid = binary_dilation(self.road_grid, iterations=1)
        self.road_grid = binary_erosion(self.road_grid, iterations=1)

    def _generate_zones(self):
        """
        Define city zones: commercial center, residential, industrial, parks.
        Uses distance from center and terrain features.
        """
        print("  Generating city zones...")

        center_x, center_y = self.center

        for y in range(self.size):
            for x in range(self.size):
                # Skip roads and unbuildable terrain
                if self.road_grid[y, x] or not self.terrain.is_buildable(x, y):
                    continue

                # Calculate distance from center (normalized)
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                norm_distance = distance / (self.size / 2)

                # Determine zone based on distance
                if norm_distance < CITY.URBAN_CENTER_RADIUS:
                    # Urban center: commercial/mixed
                    self.zone_map[y, x] = ZoneType.COMMERCIAL.value if np.random.random() > 0.3 else ZoneType.MIXED.value

                elif norm_distance < CITY.SUBURBAN_RADIUS:
                    # Suburbs: mostly residential with some commercial
                    rand = np.random.random()
                    if rand < 0.7:
                        self.zone_map[y, x] = ZoneType.RESIDENTIAL.value
                    elif rand < 0.85:
                        self.zone_map[y, x] = ZoneType.COMMERCIAL.value
                    else:
                        self.zone_map[y, x] = ZoneType.PARK.value

                else:
                    # Outskirts: industrial, parks, some residential
                    rand = np.random.random()
                    if rand < 0.4:
                        self.zone_map[y, x] = ZoneType.INDUSTRIAL.value
                    elif rand < 0.6:
                        self.zone_map[y, x] = ZoneType.PARK.value
                    else:
                        self.zone_map[y, x] = ZoneType.RESIDENTIAL.value

    def _place_buildings(self):
        """
        Procedurally place buildings in zoned areas.
        Uses grammar-based rules for realistic city layout.
        """
        print("  Placing buildings...")

        # Scan grid for building opportunities
        visited = np.zeros((self.size, self.size), dtype=bool)

        for y in range(0, self.size, 2):  # Sample every 2 cells for performance
            for x in range(0, self.size, 2):
                if visited[y, x] or self.road_grid[y, x]:
                    continue

                if not self.terrain.is_buildable(x, y):
                    continue

                # Random chance to place building based on density
                if np.random.random() > CITY.BUILDING_DENSITY:
                    continue

                # Determine building size based on zone
                zone_type = ZoneType(self.zone_map[y, x])
                building = self._create_building(x, y, zone_type)

                if building and self._can_place_building(building, visited):
                    self.buildings.append(building)

                    # Mark area as occupied
                    for by in range(building.y, min(building.y + building.height, self.size)):
                        for bx in range(building.x, min(building.x + building.width, self.size)):
                            visited[by, bx] = True

    def _create_building(self, x: int, y: int, zone_type: ZoneType) -> Optional[Building]:
        """Create building based on zone type"""
        # Building size varies by zone
        if zone_type == ZoneType.COMMERCIAL:
            width = np.random.randint(15, CITY.MAX_BUILDING_SIZE)
            height = np.random.randint(15, CITY.MAX_BUILDING_SIZE)
            floors = np.random.randint(3, 10)

        elif zone_type == ZoneType.RESIDENTIAL:
            width = np.random.randint(CITY.MIN_BUILDING_SIZE, 20)
            height = np.random.randint(CITY.MIN_BUILDING_SIZE, 20)
            floors = np.random.randint(1, 5)

        elif zone_type == ZoneType.INDUSTRIAL:
            width = np.random.randint(20, CITY.MAX_BUILDING_SIZE + 10)
            height = np.random.randint(15, 25)
            floors = np.random.randint(1, 3)

        elif zone_type == ZoneType.PARK:
            # Parks don't have buildings
            return None

        elif zone_type == ZoneType.MIXED:
            width = np.random.randint(CITY.MIN_BUILDING_SIZE, 25)
            height = np.random.randint(CITY.MIN_BUILDING_SIZE, 25)
            floors = np.random.randint(2, 8)

        else:
            return None

        return Building(x=x, y=y, width=width, height=height, zone_type=zone_type, floors=floors)

    def _can_place_building(self, building: Building, visited: np.ndarray) -> bool:
        """Check if building can be placed without overlapping roads or other buildings"""
        for by in range(building.y, min(building.y + building.height, self.size)):
            for bx in range(building.x, min(building.x + building.width, self.size)):
                if (bx >= self.size or by >= self.size or
                    self.road_grid[by, bx] or visited[by, bx] or
                    not self.terrain.is_buildable(bx, by)):
                    return False
        return True

    def _build_road_graph(self):
        """Build NetworkX graph from road network for pathfinding"""
        print("  Building road graph for pathfinding...")

        # Find all road cells and add as nodes
        road_cells = np.argwhere(self.road_grid)

        # Add nodes
        for y, x in road_cells:
            self.road_graph.add_node((x, y))

        # Add edges between adjacent road cells
        for y, x in road_cells:
            # Check 4-connected neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.road_grid[ny, nx]:
                        self.road_graph.add_edge((x, y), (nx, ny), weight=1.0)

    def _get_zone_stats(self) -> str:
        """Get zone distribution statistics"""
        unique, counts = np.unique(self.zone_map, return_counts=True)
        buildable_cells = np.sum(self.zone_map > 0)

        if buildable_cells == 0:
            return "No zones"

        stats = []
        zone_names = {
            ZoneType.COMMERCIAL.value: "Commercial",
            ZoneType.RESIDENTIAL.value: "Residential",
            ZoneType.INDUSTRIAL.value: "Industrial",
            ZoneType.PARK.value: "Park",
            ZoneType.MIXED.value: "Mixed"
        }

        for zone_id, count in zip(unique, counts):
            if zone_id > 0:  # Skip empty zones
                percentage = (count / buildable_cells) * 100
                name = zone_names.get(zone_id, "Unknown")
                stats.append(f"{name}: {percentage:.1f}%")

        return ", ".join(stats)

    def get_nearest_road(self, x: int, y: int) -> Optional[Tuple[int, int]]:
        """Find nearest road cell to given position"""
        min_dist = float('inf')
        nearest = None

        # Search in expanding radius
        search_radius = 50
        for dy in range(-search_radius, search_radius):
            for dx in range(-search_radius, search_radius):
                nx, ny = x + dx, y + dy
                if 0 <= nx < self.size and 0 <= ny < self.size:
                    if self.road_grid[ny, nx]:
                        dist = dx*dx + dy*dy
                        if dist < min_dist:
                            min_dist = dist
                            nearest = (nx, ny)

        return nearest


if __name__ == "__main__":
    # Test city generation
    from terrain_generator import TerrainGenerator

    terrain = TerrainGenerator(size=256, seed=42)
    terrain.generate()

    city = CityLayoutGenerator(terrain, seed=42)
    road_grid, zone_map, buildings = city.generate()

    print(f"\nGenerated {len(buildings)} buildings")
    print(f"Road coverage: {np.sum(road_grid) / (256 * 256) * 100:.1f}%")
