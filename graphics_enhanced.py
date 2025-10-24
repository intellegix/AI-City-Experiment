"""
Enhanced Graphics System for Realistic Rendering
Advanced visual effects, shading, and textures
"""
import pygame
import numpy as np
from typing import Tuple, Optional
import colorsys


class ColorPalette:
    """
    Realistic color palettes based on real-world references.
    Uses physically-based color theory for natural appearance.
    """

    # Terrain colors (inspired by real satellite imagery)
    DEEP_WATER = (25, 42, 86)
    SHALLOW_WATER = (65, 105, 225)
    WATER_HIGHLIGHT = (135, 206, 250)
    BEACH_SAND = (238, 214, 175)
    SAND_SHADOW = (210, 180, 140)
    GRASS_DARK = (76, 115, 47)
    GRASS_LIGHT = (124, 165, 75)
    GRASS_HIGHLIGHT = (152, 198, 90)
    FOREST_DARK = (34, 68, 34)
    FOREST_MID = (54, 94, 54)
    FOREST_LIGHT = (74, 114, 74)
    MOUNTAIN_DARK = (119, 117, 117)
    MOUNTAIN_MID = (149, 147, 147)
    MOUNTAIN_SNOW = (240, 240, 245)

    # Urban colors (realistic building materials)
    CONCRETE_DARK = (120, 120, 130)
    CONCRETE_LIGHT = (180, 180, 190)
    BRICK_RED = (156, 102, 82)
    BRICK_ORANGE = (180, 120, 90)
    GLASS_BLUE = (140, 180, 220)
    GLASS_GREEN = (160, 200, 180)
    METAL_STEEL = (160, 165, 175)
    ASPHALT = (45, 45, 50)
    ASPHALT_WORN = (65, 65, 70)

    # Residential colors (varied housing)
    HOUSE_BEIGE = (222, 214, 188)
    HOUSE_WHITE = (245, 245, 250)
    HOUSE_CREAM = (255, 245, 220)
    HOUSE_TAN = (210, 180, 140)
    ROOF_RED = (140, 70, 50)
    ROOF_GRAY = (90, 90, 95)
    ROOF_BROWN = (101, 67, 33)

    # Lighting colors
    SHADOW = (0, 0, 0)
    AMBIENT_LIGHT = (255, 250, 240)
    SUNLIGHT = (255, 248, 220)
    STREET_LIGHT = (255, 220, 180)


class RealisticShader:
    """
    Shader system for realistic lighting and shadows.
    Simulates ambient occlusion, directional lighting, and atmospheric effects.
    """

    @staticmethod
    def apply_ambient_occlusion(
        base_color: Tuple[int, int, int],
        occlusion: float
    ) -> Tuple[int, int, int]:
        """
        Apply ambient occlusion darkening.

        Args:
            base_color: RGB color
            occlusion: 0.0 (full light) to 1.0 (full shadow)

        Returns:
            Darkened color
        """
        factor = 1.0 - (occlusion * 0.6)  # Max 60% darkening
        return (
            int(base_color[0] * factor),
            int(base_color[1] * factor),
            int(base_color[2] * factor)
        )

    @staticmethod
    def apply_directional_light(
        base_color: Tuple[int, int, int],
        normal: Tuple[float, float],
        light_dir: Tuple[float, float] = (0.7, -0.7)
    ) -> Tuple[int, int, int]:
        """
        Apply directional lighting (sun).

        Args:
            base_color: RGB color
            normal: Surface normal (2D)
            light_dir: Light direction vector

        Returns:
            Lit color
        """
        # Calculate dot product (lambert shading)
        dot = max(0, normal[0] * light_dir[0] + normal[1] * light_dir[1])

        # Apply lighting with ambient term
        ambient = 0.4
        diffuse = 0.6
        intensity = ambient + diffuse * dot

        return (
            min(255, int(base_color[0] * intensity)),
            min(255, int(base_color[1] * intensity)),
            min(255, int(base_color[2] * intensity))
        )

    @staticmethod
    def apply_distance_fog(
        base_color: Tuple[int, int, int],
        distance: float,
        fog_start: float = 200.0,
        fog_end: float = 500.0,
        fog_color: Tuple[int, int, int] = (200, 210, 220)
    ) -> Tuple[int, int, int]:
        """
        Apply atmospheric fog based on distance.

        Args:
            base_color: RGB color
            distance: Distance from camera
            fog_start: Distance where fog begins
            fog_end: Distance where fog is maximum
            fog_color: Color of fog

        Returns:
            Fogged color
        """
        if distance < fog_start:
            return base_color

        # Calculate fog factor
        fog_factor = min(1.0, (distance - fog_start) / (fog_end - fog_start))

        # Blend base color with fog color
        return (
            int(base_color[0] * (1 - fog_factor) + fog_color[0] * fog_factor),
            int(base_color[1] * (1 - fog_factor) + fog_color[1] * fog_factor),
            int(base_color[2] * (1 - fog_factor) + fog_color[2] * fog_factor)
        )

    @staticmethod
    def add_specular_highlight(
        base_color: Tuple[int, int, int],
        view_dir: Tuple[float, float],
        normal: Tuple[float, float],
        light_dir: Tuple[float, float],
        shininess: float = 32.0
    ) -> Tuple[int, int, int]:
        """
        Add specular highlights (Blinn-Phong).

        Args:
            base_color: RGB color
            view_dir: View direction vector
            normal: Surface normal
            light_dir: Light direction
            shininess: Specular exponent

        Returns:
            Color with specular highlight
        """
        # Calculate halfway vector
        h_x = (view_dir[0] + light_dir[0]) / 2
        h_y = (view_dir[1] + light_dir[1]) / 2
        h_len = np.sqrt(h_x**2 + h_y**2)
        if h_len > 0:
            h_x /= h_len
            h_y /= h_len

        # Calculate specular term
        spec = max(0, normal[0] * h_x + normal[1] * h_y)
        spec = spec ** shininess

        # Add specular highlight
        return (
            min(255, int(base_color[0] + spec * 50)),
            min(255, int(base_color[1] + spec * 50)),
            min(255, int(base_color[2] + spec * 50))
        )


class ProceduralTexture:
    """
    Procedural texture generation for realistic surfaces.
    """

    @staticmethod
    def generate_noise_texture(
        width: int,
        height: int,
        scale: float = 10.0,
        seed: int = 0
    ) -> np.ndarray:
        """Generate Perlin-like noise texture"""
        np.random.seed(seed)
        noise = np.random.rand(height // 4, width // 4)

        # Upscale with bilinear interpolation
        from scipy.ndimage import zoom
        noise = zoom(noise, 4, order=1)

        # Normalize
        noise = (noise - noise.min()) / (noise.max() - noise.min())

        return noise[:height, :width]

    @staticmethod
    def apply_texture_variation(
        base_color: Tuple[int, int, int],
        noise_value: float,
        variation: float = 0.15
    ) -> Tuple[int, int, int]:
        """
        Apply texture variation to color.

        Args:
            base_color: Base RGB color
            noise_value: Noise value 0-1
            variation: Amount of variation (0-1)

        Returns:
            Varied color
        """
        # Convert noise to variation factor (-variation to +variation)
        factor = 1.0 + (noise_value - 0.5) * variation * 2

        return (
            min(255, max(0, int(base_color[0] * factor))),
            min(255, max(0, int(base_color[1] * factor))),
            min(255, max(0, int(base_color[2] * factor)))
        )


class RealisticBuildingRenderer:
    """
    Advanced building renderer with realistic details.
    """

    @staticmethod
    def draw_building_3d(
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        floors: int,
        base_color: Tuple[int, int, int],
        lighting_dir: Tuple[float, float] = (0.7, -0.7)
    ):
        """
        Draw building with 3D perspective and details.

        Args:
            surface: Pygame surface to draw on
            x, y: Position
            width, height: Dimensions
            floors: Number of floors
            base_color: Building color
            lighting_dir: Light direction for shading
        """
        if width < 4 or height < 4:
            # Too small for details, draw simple rectangle
            pygame.draw.rect(surface, base_color, (x, y, width, height))
            return

        # Calculate 3D offset for isometric effect
        iso_offset_x = int(height * 0.15)
        iso_offset_y = int(height * 0.15)

        # Draw shadow
        shadow_color = (50, 50, 55, 128)
        shadow_points = [
            (x + width, y + height),
            (x + width + iso_offset_x, y + height - iso_offset_y),
            (x + iso_offset_x, y + height - iso_offset_y),
            (x, y + height)
        ]
        pygame.draw.polygon(surface, (50, 50, 50), shadow_points)

        # Front face (lighter)
        front_color = RealisticShader.apply_directional_light(
            base_color,
            (0, 1),  # Normal facing down-right
            lighting_dir
        )
        pygame.draw.rect(surface, front_color, (x, y, width, height))

        # Right face (darker)
        right_color = tuple(int(c * 0.7) for c in base_color)
        right_points = [
            (x + width, y),
            (x + width + iso_offset_x, y - iso_offset_y),
            (x + width + iso_offset_x, y + height - iso_offset_y),
            (x + width, y + height)
        ]
        if iso_offset_x > 0 and iso_offset_y > 0:
            pygame.draw.polygon(surface, right_color, right_points)

        # Top face (medium)
        top_color = tuple(int(c * 0.85) for c in base_color)
        top_points = [
            (x, y),
            (x + iso_offset_x, y - iso_offset_y),
            (x + width + iso_offset_x, y - iso_offset_y),
            (x + width, y)
        ]
        if iso_offset_x > 0 and iso_offset_y > 0:
            pygame.draw.polygon(surface, top_color, top_points)

        # Draw windows if large enough
        if width > 10 and height > 15:
            RealisticBuildingRenderer._draw_windows(
                surface, x, y, width, height, floors
            )

        # Building outline
        pygame.draw.rect(surface, (0, 0, 0), (x, y, width, height), 1)

    @staticmethod
    def _draw_windows(
        surface: pygame.Surface,
        x: int,
        y: int,
        width: int,
        height: int,
        floors: int
    ):
        """Draw windows on building"""
        window_color = (100, 150, 200)  # Glass blue
        window_dark = (50, 75, 100)

        floor_height = height // max(1, floors)

        for floor in range(floors):
            floor_y = y + floor * floor_height + 2

            # Draw windows across width
            num_windows = max(1, width // 8)
            window_width = max(2, (width - 4) // num_windows - 2)

            for i in range(num_windows):
                window_x = x + 2 + i * (window_width + 2)
                window_height = max(2, floor_height - 4)

                if window_height > 0 and window_width > 0:
                    # Randomize window lighting (some lit, some dark)
                    if np.random.random() > 0.3:
                        color = window_color
                    else:
                        color = window_dark

                    pygame.draw.rect(
                        surface,
                        color,
                        (window_x, floor_y, window_width, window_height)
                    )


class ParticleSystem:
    """
    Particle system for ambient effects (birds, leaves, etc.)
    """

    def __init__(self):
        self.particles = []

    def emit(self, x: float, y: float, particle_type: str = "ambient"):
        """Emit a particle"""
        self.particles.append({
            'x': x,
            'y': y,
            'vx': np.random.uniform(-0.5, 0.5),
            'vy': np.random.uniform(-0.5, 0.5),
            'life': 100,
            'type': particle_type
        })

    def update(self, dt: float):
        """Update all particles"""
        for particle in self.particles[:]:
            particle['x'] += particle['vx']
            particle['y'] += particle['vy']
            particle['life'] -= 1

            if particle['life'] <= 0:
                self.particles.remove(particle)

    def render(self, surface: pygame.Surface, camera):
        """Render particles"""
        for particle in self.particles:
            screen_x, screen_y = camera.world_to_screen(particle['x'], particle['y'])

            alpha = int((particle['life'] / 100) * 255)
            color = (200, 200, 200, alpha)

            pygame.draw.circle(surface, color[:3], (screen_x, screen_y), 1)


def generate_height_shading(heightmap: np.ndarray) -> np.ndarray:
    """
    Generate realistic shading from heightmap.

    Args:
        heightmap: 2D array of heights

    Returns:
        Shading intensity map
    """
    # Calculate gradients (surface normals)
    gradient_x = np.zeros_like(heightmap)
    gradient_y = np.zeros_like(heightmap)

    gradient_x[:, :-1] = heightmap[:, 1:] - heightmap[:, :-1]
    gradient_y[:-1, :] = heightmap[1:, :] - heightmap[:-1, :]

    # Calculate lighting intensity
    light_dir = np.array([0.7, 0.7])  # 45-degree light
    intensity = gradient_x * light_dir[0] + gradient_y * light_dir[1]

    # Normalize and apply
    intensity = (intensity - intensity.min()) / (intensity.max() - intensity.min() + 0.001)

    return intensity


def apply_realistic_terrain_colors(
    biome_map: np.ndarray,
    heightmap: np.ndarray,
    moisture_map: np.ndarray
) -> np.ndarray:
    """
    Apply realistic colors to terrain based on multiple factors.

    Args:
        biome_map: Biome type for each cell
        heightmap: Elevation data
        moisture_map: Moisture data

    Returns:
        RGB color array
    """
    height, width = biome_map.shape
    colors = np.zeros((height, width, 3), dtype=np.uint8)

    # Generate lighting from heightmap
    shading = generate_height_shading(heightmap)

    for y in range(height):
        for x in range(width):
            biome = biome_map[y, x]
            elevation = heightmap[y, x]
            moisture = moisture_map[y, x]
            shade = shading[y, x]

            # Select base color based on biome
            if biome == 0:  # Water
                if elevation < 0.25:
                    base_color = ColorPalette.DEEP_WATER
                elif elevation < 0.28:
                    base_color = ColorPalette.SHALLOW_WATER
                else:
                    base_color = ColorPalette.WATER_HIGHLIGHT
            elif biome == 1:  # Sand
                base_color = ColorPalette.BEACH_SAND if moisture > 0.4 else ColorPalette.SAND_SHADOW
            elif biome == 2:  # Grass
                if moisture > 0.6:
                    base_color = ColorPalette.GRASS_DARK
                elif moisture > 0.4:
                    base_color = ColorPalette.GRASS_LIGHT
                else:
                    base_color = ColorPalette.GRASS_HIGHLIGHT
            elif biome == 3:  # Forest
                base_color = ColorPalette.FOREST_DARK if moisture > 0.5 else ColorPalette.FOREST_MID
            else:  # Mountain
                if elevation > 0.9:
                    base_color = ColorPalette.MOUNTAIN_SNOW
                elif elevation > 0.87:
                    base_color = ColorPalette.MOUNTAIN_MID
                else:
                    base_color = ColorPalette.MOUNTAIN_DARK

            # Apply shading
            shade_factor = 0.7 + shade * 0.6  # Range: 0.7 to 1.3
            colors[y, x] = [
                min(255, int(base_color[0] * shade_factor)),
                min(255, int(base_color[1] * shade_factor)),
                min(255, int(base_color[2] * shade_factor))
            ]

    return colors
