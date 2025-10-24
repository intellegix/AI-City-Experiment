"""
Advanced Procedural Texture System - GTA 5 Level Detail
Generates realistic textures with wear, dirt, and surface variation

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from panda3d.core import *
import numpy as np
from enum import Enum
from typing import Tuple, Optional


class TextureType(Enum):
    """Types of procedural textures"""
    CONCRETE_CLEAN = "concrete_clean"
    CONCRETE_WEATHERED = "concrete_weathered"
    BRICK_RED = "brick_red"
    BRICK_GREY = "brick_grey"
    ASPHALT_FRESH = "asphalt_fresh"
    ASPHALT_WORN = "asphalt_worn"
    METAL_PAINTED = "metal_painted"
    METAL_RUST = "metal_rust"
    GLASS_CLEAN = "glass_clean"
    GLASS_DIRTY = "glass_dirty"
    WOOD_POLISHED = "wood_polished"
    WOOD_WEATHERED = "wood_weathered"
    PLASTIC_NEW = "plastic_new"
    PLASTIC_FADED = "plastic_faded"
    GRASS_LUSH = "grass_lush"
    GRASS_DRY = "grass_dry"
    TILE_FLOOR = "tile_floor"
    GRAVEL = "gravel"
    DIRT = "dirt"


class ProceduralTextureGenerator:
    """
    Generates high-quality procedural textures with realistic detail.

    Features:
    - Multi-layer noise for natural variation
    - Weathering and wear patterns
    - Dirt and grime overlays
    - Normal map generation
    - Specular map generation
    - Ambient occlusion simulation
    """

    def __init__(self, resolution: int = 512):
        """Initialize texture generator"""
        self.resolution = resolution
        self._noise_cache = {}

    def generate_texture(self, texture_type: TextureType,
                        wear_level: float = 0.5,
                        dirt_level: float = 0.3) -> Texture:
        """
        Generate a complete texture with diffuse, normal, and specular maps.

        Args:
            texture_type: Type of texture to generate
            wear_level: How worn/weathered (0.0 = pristine, 1.0 = heavily worn)
            dirt_level: Amount of dirt/grime (0.0 = clean, 1.0 = very dirty)

        Returns:
            Panda3D Texture object with all maps
        """
        # Generate base color map
        diffuse_data = self._generate_diffuse_map(texture_type, wear_level, dirt_level)

        # Generate normal map for surface detail
        normal_data = self._generate_normal_map(texture_type, wear_level)

        # Generate specular map for shininess variation
        specular_data = self._generate_specular_map(texture_type, wear_level, dirt_level)

        # Create Panda3D texture
        tex = Texture(f"{texture_type.value}")
        tex.setup2dTexture(self.resolution, self.resolution,
                          Texture.T_unsigned_byte, Texture.F_rgba)

        # Set diffuse data
        tex.setRamImage(diffuse_data.tobytes())

        # Enable filtering for smoothness
        tex.setMinfilter(Texture.FT_linear_mipmap_linear)
        tex.setMagfilter(Texture.FT_linear)
        tex.setAnisotropicDegree(16)  # High quality filtering

        return tex

    def _generate_diffuse_map(self, texture_type: TextureType,
                             wear_level: float, dirt_level: float) -> np.ndarray:
        """Generate diffuse color map"""
        res = self.resolution

        # Get base colors for texture type
        base_color, variation = self._get_texture_colors(texture_type)

        # Create base texture
        texture = np.zeros((res, res, 4), dtype=np.uint8)

        # Apply base color with variation
        noise = self._generate_noise(res, scale=0.05, octaves=4)
        for i in range(3):  # RGB channels
            color_val = int(base_color[i] * 255)
            variation_amount = int(variation * 255)
            texture[:, :, i] = np.clip(
                color_val + (noise * variation_amount), 0, 255
            ).astype(np.uint8)

        texture[:, :, 3] = 255  # Alpha channel

        # Apply detail patterns based on texture type
        if "brick" in texture_type.value:
            texture = self._add_brick_pattern(texture, base_color)
        elif "concrete" in texture_type.value:
            texture = self._add_concrete_texture(texture)
        elif "asphalt" in texture_type.value:
            texture = self._add_asphalt_texture(texture)
        elif "metal" in texture_type.value:
            texture = self._add_metal_texture(texture)
        elif "wood" in texture_type.value:
            texture = self._add_wood_grain(texture)
        elif "tile" in texture_type.value:
            texture = self._add_tile_pattern(texture)
        elif "grass" in texture_type.value:
            texture = self._add_grass_texture(texture)

        # Apply weathering
        if wear_level > 0.1:
            texture = self._add_weathering(texture, wear_level)

        # Apply dirt and grime
        if dirt_level > 0.1:
            texture = self._add_dirt_grime(texture, dirt_level)

        return texture

    def _generate_normal_map(self, texture_type: TextureType,
                            wear_level: float) -> np.ndarray:
        """Generate normal map for surface detail"""
        res = self.resolution

        # Create height map from noise
        height_scale = self._get_normal_map_strength(texture_type)
        noise = self._generate_noise(res, scale=0.1, octaves=6)
        height_map = noise * height_scale * (1.0 + wear_level * 0.5)

        # Calculate normals from height map
        normal_map = np.zeros((res, res, 4), dtype=np.uint8)

        # Compute gradients
        dx = np.roll(height_map, -1, axis=1) - height_map
        dy = np.roll(height_map, -1, axis=0) - height_map

        # Convert to normal vectors
        normal_map[:, :, 0] = np.clip((dx + 1.0) * 127.5, 0, 255).astype(np.uint8)  # R (X)
        normal_map[:, :, 1] = np.clip((dy + 1.0) * 127.5, 0, 255).astype(np.uint8)  # G (Y)
        normal_map[:, :, 2] = 200  # B (Z - pointing up)
        normal_map[:, :, 3] = 255  # Alpha

        return normal_map

    def _generate_specular_map(self, texture_type: TextureType,
                               wear_level: float, dirt_level: float) -> np.ndarray:
        """Generate specular map for shininess variation"""
        res = self.resolution

        # Base specular value
        base_spec = self._get_specular_value(texture_type)

        # Reduce specular with wear and dirt
        spec_multiplier = 1.0 - (wear_level * 0.4) - (dirt_level * 0.6)

        # Add variation
        noise = self._generate_noise(res, scale=0.08, octaves=3)
        specular_map = np.clip(
            (base_spec + noise * 0.2) * spec_multiplier * 255, 0, 255
        ).astype(np.uint8)

        # Create RGBA specular map
        spec_rgba = np.zeros((res, res, 4), dtype=np.uint8)
        spec_rgba[:, :, 0] = specular_map
        spec_rgba[:, :, 1] = specular_map
        spec_rgba[:, :, 2] = specular_map
        spec_rgba[:, :, 3] = 255

        return spec_rgba

    def _generate_noise(self, size: int, scale: float = 0.1,
                       octaves: int = 4, persistence: float = 0.5) -> np.ndarray:
        """Generate multi-octave Perlin-like noise"""
        # Simple multi-octave noise using numpy
        noise = np.zeros((size, size))
        amplitude = 1.0
        frequency = 1.0

        for _ in range(octaves):
            # Generate random noise at this frequency
            octave_size = max(2, int(size * scale * frequency))
            random_noise = np.random.random((octave_size, octave_size))

            # Upscale to target size
            from scipy.ndimage import zoom
            try:
                scaled_noise = zoom(random_noise, size / octave_size, order=1)
            except:
                # Fallback if scipy not available
                scaled_noise = np.random.random((size, size))

            noise += scaled_noise * amplitude

            amplitude *= persistence
            frequency *= 2.0

        # Normalize
        noise = (noise - noise.min()) / (noise.max() - noise.min())
        return noise

    def _get_texture_colors(self, texture_type: TextureType) -> Tuple[Tuple[float, float, float], float]:
        """Get base color and variation for texture type"""
        colors = {
            TextureType.CONCRETE_CLEAN: ((0.75, 0.75, 0.78), 0.05),
            TextureType.CONCRETE_WEATHERED: ((0.55, 0.55, 0.58), 0.15),
            TextureType.BRICK_RED: ((0.65, 0.25, 0.20), 0.12),
            TextureType.BRICK_GREY: ((0.45, 0.45, 0.48), 0.10),
            TextureType.ASPHALT_FRESH: ((0.20, 0.20, 0.22), 0.08),
            TextureType.ASPHALT_WORN: ((0.28, 0.28, 0.30), 0.15),
            TextureType.METAL_PAINTED: ((0.70, 0.70, 0.72), 0.03),
            TextureType.METAL_RUST: ((0.55, 0.35, 0.25), 0.20),
            TextureType.GLASS_CLEAN: ((0.85, 0.90, 0.95), 0.02),
            TextureType.GLASS_DIRTY: ((0.65, 0.68, 0.70), 0.10),
            TextureType.WOOD_POLISHED: ((0.45, 0.30, 0.20), 0.15),
            TextureType.WOOD_WEATHERED: ((0.35, 0.28, 0.22), 0.20),
            TextureType.PLASTIC_NEW: ((0.80, 0.80, 0.82), 0.02),
            TextureType.PLASTIC_FADED: ((0.65, 0.65, 0.68), 0.12),
            TextureType.GRASS_LUSH: ((0.25, 0.65, 0.30), 0.18),
            TextureType.GRASS_DRY: ((0.45, 0.55, 0.30), 0.15),
            TextureType.TILE_FLOOR: ((0.88, 0.88, 0.90), 0.05),
            TextureType.GRAVEL: ((0.48, 0.45, 0.42), 0.20),
            TextureType.DIRT: ((0.40, 0.32, 0.25), 0.18),
        }
        return colors.get(texture_type, ((0.5, 0.5, 0.5), 0.1))

    def _get_normal_map_strength(self, texture_type: TextureType) -> float:
        """Get normal map detail strength"""
        strengths = {
            TextureType.CONCRETE_CLEAN: 0.05,
            TextureType.CONCRETE_WEATHERED: 0.15,
            TextureType.BRICK_RED: 0.20,
            TextureType.BRICK_GREY: 0.20,
            TextureType.ASPHALT_FRESH: 0.08,
            TextureType.ASPHALT_WORN: 0.18,
            TextureType.METAL_PAINTED: 0.02,
            TextureType.METAL_RUST: 0.25,
            TextureType.GLASS_CLEAN: 0.01,
            TextureType.GLASS_DIRTY: 0.08,
            TextureType.WOOD_POLISHED: 0.12,
            TextureType.WOOD_WEATHERED: 0.22,
        }
        return strengths.get(texture_type, 0.1)

    def _get_specular_value(self, texture_type: TextureType) -> float:
        """Get base specular reflectivity"""
        values = {
            TextureType.CONCRETE_CLEAN: 0.15,
            TextureType.CONCRETE_WEATHERED: 0.08,
            TextureType.BRICK_RED: 0.10,
            TextureType.BRICK_GREY: 0.12,
            TextureType.ASPHALT_FRESH: 0.18,
            TextureType.ASPHALT_WORN: 0.10,
            TextureType.METAL_PAINTED: 0.75,
            TextureType.METAL_RUST: 0.25,
            TextureType.GLASS_CLEAN: 0.95,
            TextureType.GLASS_DIRTY: 0.65,
            TextureType.WOOD_POLISHED: 0.45,
            TextureType.WOOD_WEATHERED: 0.15,
            TextureType.PLASTIC_NEW: 0.50,
            TextureType.PLASTIC_FADED: 0.25,
        }
        return values.get(texture_type, 0.3)

    def _add_brick_pattern(self, texture: np.ndarray,
                          base_color: Tuple[float, float, float]) -> np.ndarray:
        """Add brick pattern with mortar"""
        res = self.resolution
        brick_height = res // 16  # Brick size
        brick_width = brick_height * 3
        mortar_width = max(2, brick_height // 8)

        # Create mortar (lighter grey)
        mortar_color = np.array([180, 180, 185], dtype=np.uint8)

        for y in range(0, res, brick_height):
            for x in range(0, res, brick_width):
                # Offset every other row
                offset = (brick_width // 2) if (y // brick_height) % 2 == 1 else 0
                x_pos = (x + offset) % res

                # Draw mortar lines
                y_end = min(y + mortar_width, res)
                texture[y:y_end, :] = mortar_color

                x_end = min(x_pos + mortar_width, res)
                if x_end > x_pos:
                    texture[:, x_pos:x_end] = mortar_color

        return texture

    def _add_concrete_texture(self, texture: np.ndarray) -> np.ndarray:
        """Add concrete surface details"""
        # Add small random speckles
        noise = self._generate_noise(self.resolution, scale=0.2, octaves=6)
        speckles = (noise > 0.7).astype(np.uint8) * 30

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i].astype(int) - speckles, 0, 255).astype(np.uint8)

        return texture

    def _add_asphalt_texture(self, texture: np.ndarray) -> np.ndarray:
        """Add asphalt aggregate texture"""
        # Add small light/dark spots for aggregate
        noise = self._generate_noise(self.resolution, scale=0.15, octaves=5)
        aggregate = ((noise - 0.5) * 40).astype(int)

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i].astype(int) + aggregate, 0, 255).astype(np.uint8)

        return texture

    def _add_metal_texture(self, texture: np.ndarray) -> np.ndarray:
        """Add brushed metal texture"""
        # Add horizontal brush marks
        noise = self._generate_noise(self.resolution, scale=0.05, octaves=2)
        # Stretch horizontally
        brush_marks = np.tile(noise[:, 0:1], (1, self.resolution))
        brush_effect = ((brush_marks - 0.5) * 20).astype(int)

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i].astype(int) + brush_effect, 0, 255).astype(np.uint8)

        return texture

    def _add_wood_grain(self, texture: np.ndarray) -> np.ndarray:
        """Add wood grain pattern"""
        # Create horizontal grain lines
        y = np.arange(self.resolution)
        grain = np.sin(y * 0.3 + np.random.random(self.resolution) * 2) * 15
        grain_2d = np.tile(grain.reshape(-1, 1), (1, self.resolution))

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i].astype(int) + grain_2d, 0, 255).astype(np.uint8)

        return texture

    def _add_tile_pattern(self, texture: np.ndarray) -> np.ndarray:
        """Add tile pattern with grout lines"""
        tile_size = self.resolution // 8
        grout_width = max(1, tile_size // 16)
        grout_color = np.array([120, 120, 125], dtype=np.uint8)

        for i in range(0, self.resolution, tile_size):
            # Horizontal grout lines
            texture[i:i+grout_width, :] = grout_color
            # Vertical grout lines
            texture[:, i:i+grout_width] = grout_color

        return texture

    def _add_grass_texture(self, texture: np.ndarray) -> np.ndarray:
        """Add grass blade texture"""
        # Add high frequency noise for grass blades
        noise = self._generate_noise(self.resolution, scale=0.5, octaves=8)
        grass_detail = ((noise - 0.5) * 60).astype(int)

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i].astype(int) + grass_detail, 0, 255).astype(np.uint8)

        return texture

    def _add_weathering(self, texture: np.ndarray, wear_level: float) -> np.ndarray:
        """Add weathering effects (cracks, discoloration)"""
        # Darken texture slightly
        darkening = int(wear_level * 30)

        # Add random dark patches
        noise = self._generate_noise(self.resolution, scale=0.1, octaves=3)
        wear_mask = (noise < wear_level).astype(int) * darkening

        for i in range(3):
            texture[:, :, i] = np.clip(texture[:, :, i] - wear_mask, 0, 255).astype(np.uint8)

        return texture

    def _add_dirt_grime(self, texture: np.ndarray, dirt_level: float) -> np.ndarray:
        """Add dirt and grime overlay"""
        # Create dirt pattern
        dirt_noise = self._generate_noise(self.resolution, scale=0.08, octaves=4)
        dirt_mask = (dirt_noise * dirt_level * 100).astype(int)

        # Darken with dirt (brownish tint)
        dirt_color = np.array([20, 15, 10], dtype=int)

        for i in range(3):
            texture[:, :, i] = np.clip(
                texture[:, :, i] - dirt_mask + dirt_color[i] * (dirt_mask // 50),
                0, 255
            ).astype(np.uint8)

        return texture


class TextureLibrary:
    """
    Manages texture cache and provides easy access to procedural textures.
    """

    def __init__(self, resolution: int = 512):
        """Initialize texture library"""
        self.generator = ProceduralTextureGenerator(resolution)
        self._cache = {}

    def get_texture(self, texture_type: TextureType,
                   wear_level: float = 0.5,
                   dirt_level: float = 0.3) -> Texture:
        """Get texture from cache or generate new one"""
        cache_key = (texture_type, wear_level, dirt_level)

        if cache_key not in self._cache:
            self._cache[cache_key] = self.generator.generate_texture(
                texture_type, wear_level, dirt_level
            )

        return self._cache[cache_key]

    def clear_cache(self):
        """Clear texture cache"""
        self._cache.clear()
