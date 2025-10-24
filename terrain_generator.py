"""
Procedural Terrain Generation using Perlin Noise
Implements Phase 2 of the blueprint: Terrain & World Generation

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
from typing import Tuple, Optional
from config import TERRAIN, Config
from enum import Enum


class PerlinNoise:
    """
    Pure NumPy implementation of 2D Perlin noise.
    Compatible with all Python versions without C extensions.
    """

    def __init__(self, seed: int = 0):
        """Initialize with random permutation table based on seed"""
        self.seed = seed
        np.random.seed(seed)

        # Create permutation table
        self.p = np.arange(256, dtype=int)
        np.random.shuffle(self.p)
        self.p = np.concatenate([self.p, self.p])  # Duplicate for overflow

    def fade(self, t: np.ndarray) -> np.ndarray:
        """Fade function: 6t^5 - 15t^4 + 10t^3"""
        return t * t * t * (t * (t * 6 - 15) + 10)

    def lerp(self, a: float, b: float, t: np.ndarray) -> np.ndarray:
        """Linear interpolation"""
        return a + t * (b - a)

    def grad(self, hash_val: int, x: float, y: float) -> float:
        """Gradient function - converts hash to gradient vector"""
        h = hash_val & 3
        if h == 0:
            return x + y
        elif h == 1:
            return -x + y
        elif h == 2:
            return x - y
        else:
            return -x - y

    def noise(self, x: float, y: float) -> float:
        """
        Generate 2D Perlin noise value at coordinates (x, y)
        Returns value in approximate range [-1, 1]
        """
        # Find grid cell coordinates
        X = int(np.floor(x)) & 255
        Y = int(np.floor(y)) & 255

        # Relative coordinates within cell
        x -= np.floor(x)
        y -= np.floor(y)

        # Fade curves
        u = self.fade(x)
        v = self.fade(y)

        # Hash coordinates of 4 corners
        a = self.p[X] + Y
        aa = self.p[a]
        ab = self.p[a + 1]
        b = self.p[X + 1] + Y
        ba = self.p[b]
        bb = self.p[b + 1]

        # Blend results from 4 corners
        res = self.lerp(
            self.lerp(self.grad(self.p[aa], x, y),
                     self.grad(self.p[ba], x - 1, y),
                     u),
            self.lerp(self.grad(self.p[ab], x, y - 1),
                     self.grad(self.p[bb], x - 1, y - 1),
                     u),
            v
        )

        return res


class BiomeType(Enum):
    """Terrain biome types"""
    WATER = 0
    SAND = 1
    GRASS = 2
    FOREST = 3
    MOUNTAIN = 4


class TerrainGenerator:
    """
    Advanced procedural terrain generation system using multi-octave Perlin noise.
    Features:
    - Multiple biome types with smooth transitions
    - Adjustable detail through octaves
    - Deterministic generation with seeds
    - Optimized for large-scale terrain (5km x 5km equivalent)
    """

    def __init__(self, size: int = None, seed: int = None):
        """
        Initialize terrain generator.

        Args:
            size: Grid size (default from config)
            seed: Random seed for reproducibility
        """
        self.size = size or TERRAIN.SIZE
        self.seed = seed or TERRAIN.SEED or np.random.randint(0, 10000)
        np.random.seed(self.seed)

        # Initialize Perlin noise generator
        self.noise_gen = PerlinNoise(seed=self.seed)

        # Terrain data
        self.heightmap: Optional[np.ndarray] = None
        self.biomemap: Optional[np.ndarray] = None
        self.moisture_map: Optional[np.ndarray] = None

        print(f"TerrainGenerator initialized: {self.size}x{self.size}, seed={self.seed}")

    def generate(self) -> Tuple[np.ndarray, np.ndarray]:
        """
        Generate complete terrain with heightmap and biomes.

        Returns:
            Tuple of (heightmap, biomemap)
        """
        print("Generating terrain...")

        # Generate base heightmap using Perlin noise
        self.heightmap = self._generate_heightmap()

        # Generate moisture map for richer biomes
        self.moisture_map = self._generate_moisture_map()

        # Determine biomes based on height and moisture
        self.biomemap = self._generate_biomes()

        # Apply erosion simulation for realism
        self._apply_erosion()

        print(f"Terrain generated successfully! Stats:")
        print(f"  Height range: {self.heightmap.min():.2f} - {self.heightmap.max():.2f}")
        print(f"  Biome distribution: {self._get_biome_stats()}")

        return self.heightmap, self.biomemap

    def _generate_heightmap(self) -> np.ndarray:
        """
        Generate heightmap using multi-octave Perlin noise.
        This creates realistic terrain with varying levels of detail.
        """
        heightmap = np.zeros((self.size, self.size))

        # Pre-create noise generators for each octave (performance optimization)
        octave_noise_generators = [PerlinNoise(seed=self.seed + i) for i in range(TERRAIN.OCTAVES)]

        # Multi-octave Perlin noise for realistic terrain
        for y in range(self.size):
            for x in range(self.size):
                # Normalize coordinates
                nx = x / self.size - 0.5
                ny = y / self.size - 0.5

                # Sample Perlin noise with multiple octaves
                elevation = 0
                amplitude = 1.0
                frequency = 1.0

                for octave in range(TERRAIN.OCTAVES):
                    sample_x = nx * frequency * TERRAIN.SCALE
                    sample_y = ny * frequency * TERRAIN.SCALE

                    # Perlin noise value
                    perlin_value = octave_noise_generators[octave].noise(sample_x, sample_y)

                    elevation += perlin_value * amplitude

                    amplitude *= TERRAIN.PERSISTENCE
                    frequency *= TERRAIN.LACUNARITY

                # Normalize to [0, 1]
                heightmap[y, x] = elevation

        # Normalize heightmap
        heightmap = (heightmap - heightmap.min()) / (heightmap.max() - heightmap.min())

        # Apply island effect (optional - makes edges lower)
        heightmap = self._apply_island_effect(heightmap)

        return heightmap

    def _generate_moisture_map(self) -> np.ndarray:
        """Generate moisture map for more diverse biomes"""
        moisture = np.zeros((self.size, self.size))

        # Pre-create noise generators for moisture octaves (performance optimization)
        moisture_noise_generators = [PerlinNoise(seed=self.seed + 1000 + i) for i in range(3)]

        for y in range(self.size):
            for x in range(self.size):
                nx = x / self.size
                ny = y / self.size

                # Different noise pattern for moisture using multiple octaves
                moisture_value = 0
                amplitude = 1.0
                frequency = 1.0

                for octave in range(3):
                    sample_x = nx * 50 * frequency
                    sample_y = ny * 50 * frequency
                    noise_val = moisture_noise_generators[octave].noise(sample_x, sample_y)
                    moisture_value += noise_val * amplitude

                    amplitude *= 0.5
                    frequency *= 2.0

                moisture[y, x] = moisture_value

        # Normalize
        moisture = (moisture - moisture.min()) / (moisture.max() - moisture.min())

        return moisture

    def _apply_island_effect(self, heightmap: np.ndarray, strength: float = 0.5) -> np.ndarray:
        """
        Apply radial gradient to create island-like terrain.
        Makes edges lower than center for more interesting cities.
        """
        center_x, center_y = self.size // 2, self.size // 2
        max_distance = np.sqrt(center_x**2 + center_y**2)

        for y in range(self.size):
            for x in range(self.size):
                distance = np.sqrt((x - center_x)**2 + (y - center_y)**2)
                gradient = 1.0 - (distance / max_distance) * strength
                heightmap[y, x] *= gradient

        return heightmap

    def _generate_biomes(self) -> np.ndarray:
        """
        Determine biome type for each cell based on elevation and moisture.
        Creates distinct zones: urban center (flat), suburbs, and nature.
        """
        biomemap = np.zeros((self.size, self.size), dtype=np.int32)

        for y in range(self.size):
            for x in range(self.size):
                height = self.heightmap[y, x]
                moisture = self.moisture_map[y, x]

                # Determine biome based on thresholds
                if height < TERRAIN.WATER_LEVEL:
                    biomemap[y, x] = BiomeType.WATER.value
                elif height < TERRAIN.SAND_LEVEL:
                    biomemap[y, x] = BiomeType.SAND.value
                elif height < TERRAIN.GRASS_LEVEL:
                    # Grass or forest based on moisture
                    if moisture > 0.6:
                        biomemap[y, x] = BiomeType.FOREST.value
                    else:
                        biomemap[y, x] = BiomeType.GRASS.value
                elif height < TERRAIN.MOUNTAIN_LEVEL:
                    biomemap[y, x] = BiomeType.FOREST.value if moisture > 0.4 else BiomeType.GRASS.value
                else:
                    biomemap[y, x] = BiomeType.MOUNTAIN.value

        return biomemap

    def _apply_erosion(self, iterations: int = 3):
        """
        Simple erosion simulation for more realistic terrain.
        Simulates water flow and sediment transport.
        """
        for _ in range(iterations):
            # Calculate gradient
            gradient_x = np.zeros_like(self.heightmap)
            gradient_y = np.zeros_like(self.heightmap)

            gradient_x[:, :-1] = self.heightmap[:, 1:] - self.heightmap[:, :-1]
            gradient_y[:-1, :] = self.heightmap[1:, :] - self.heightmap[:-1, :]

            # Simple erosion: lower high gradients slightly
            erosion_strength = 0.01
            self.heightmap -= erosion_strength * (np.abs(gradient_x) + np.abs(gradient_y))

        # Re-normalize
        self.heightmap = np.clip(self.heightmap, 0, 1)

    def _get_biome_stats(self) -> str:
        """Get biome distribution statistics"""
        unique, counts = np.unique(self.biomemap, return_counts=True)
        total = self.size * self.size
        stats = []

        biome_names = {
            BiomeType.WATER.value: "Water",
            BiomeType.SAND.value: "Sand",
            BiomeType.GRASS.value: "Grass",
            BiomeType.FOREST.value: "Forest",
            BiomeType.MOUNTAIN.value: "Mountain"
        }

        for biome_id, count in zip(unique, counts):
            percentage = (count / total) * 100
            name = biome_names.get(biome_id, "Unknown")
            stats.append(f"{name}: {percentage:.1f}%")

        return ", ".join(stats)

    def is_buildable(self, x: int, y: int) -> bool:
        """
        Check if a location is suitable for building placement.

        Args:
            x, y: Grid coordinates

        Returns:
            True if location is buildable
        """
        if not (0 <= x < self.size and 0 <= y < self.size):
            return False

        biome = self.biomemap[y, x]
        height = self.heightmap[y, x]

        # Can only build on grass/sand, not too steep
        return (biome in [BiomeType.GRASS.value, BiomeType.SAND.value] and
                TERRAIN.SAND_LEVEL < height < TERRAIN.FOREST_LEVEL)

    def get_elevation(self, x: int, y: int) -> float:
        """Get elevation at specific coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return self.heightmap[y, x]
        return 0.0

    def get_biome(self, x: int, y: int) -> BiomeType:
        """Get biome type at specific coordinates"""
        if 0 <= x < self.size and 0 <= y < self.size:
            return BiomeType(self.biomemap[y, x])
        return BiomeType.WATER


if __name__ == "__main__":
    # Test terrain generation
    import matplotlib.pyplot as plt

    terrain = TerrainGenerator(size=256, seed=42)
    heightmap, biomemap = terrain.generate()

    # Visualize
    fig, axes = plt.subplots(1, 2, figsize=(12, 5))

    axes[0].imshow(heightmap, cmap='terrain')
    axes[0].set_title('Heightmap')
    axes[0].axis('off')

    axes[1].imshow(biomemap, cmap='tab10')
    axes[1].set_title('Biome Map')
    axes[1].axis('off')

    plt.tight_layout()
    plt.savefig('terrain_preview.png')
    print("Terrain preview saved to terrain_preview.png")
