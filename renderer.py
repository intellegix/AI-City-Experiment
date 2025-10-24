"""
Advanced Pygame Renderer with LOD System
Implements Phase 5: Polish, Testing & Debug (Visualization)

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import pygame
import numpy as np
from typing import Tuple, Optional, List
import time

from config import RENDER, TERRAIN, Config
from terrain_generator import TerrainGenerator, BiomeType
from city_generator import CityLayoutGenerator, Building, ZoneType
from npc_system import NPCManager, NPCState, NPC as NPCAgent
from graphics_enhanced import (
    ColorPalette, RealisticShader, RealisticBuildingRenderer,
    apply_realistic_terrain_colors, ParticleSystem
)
from controller_input import ControllerManager, XboxController, ControllerButton


class Camera:
    """
    2D camera with smooth movement and zoom.
    """

    def __init__(self, width: int, height: int, world_size: int):
        self.width = width
        self.height = height
        self.world_size = world_size

        # Camera position (center)
        self.x = world_size // 2
        self.y = world_size // 2

        # Zoom level
        self.zoom = 1.0

        # Velocity for smooth movement
        self.vx = 0.0
        self.vy = 0.0

    def update(self, dt: float):
        """Update camera position"""
        self.x += self.vx * dt
        self.y += self.vy * dt

        # Clamp to world bounds
        half_view_x = (self.width / self.zoom) / 2
        half_view_y = (self.height / self.zoom) / 2

        self.x = max(half_view_x, min(self.world_size - half_view_x, self.x))
        self.y = max(half_view_y, min(self.world_size - half_view_y, self.y))

    def world_to_screen(self, world_x: float, world_y: float) -> Tuple[int, int]:
        """Convert world coordinates to screen coordinates"""
        # Relative to camera
        rel_x = world_x - self.x
        rel_y = world_y - self.y

        # Apply zoom
        screen_x = (rel_x * self.zoom) + (self.width / 2)
        screen_y = (rel_y * self.zoom) + (self.height / 2)

        return (int(screen_x), int(screen_y))

    def screen_to_world(self, screen_x: int, screen_y: int) -> Tuple[float, float]:
        """Convert screen coordinates to world coordinates"""
        # Relative to screen center
        rel_x = screen_x - (self.width / 2)
        rel_y = screen_y - (self.height / 2)

        # Remove zoom
        world_x = (rel_x / self.zoom) + self.x
        world_y = (rel_y / self.zoom) + self.y

        return (world_x, world_y)

    def get_visible_bounds(self) -> Tuple[int, int, int, int]:
        """Get visible world bounds (min_x, min_y, max_x, max_y)"""
        half_view_x = (self.width / self.zoom) / 2
        half_view_y = (self.height / self.zoom) / 2

        min_x = max(0, int(self.x - half_view_x))
        min_y = max(0, int(self.y - half_view_y))
        max_x = min(self.world_size, int(self.x + half_view_x) + 1)
        max_y = min(self.world_size, int(self.y + half_view_y) + 1)

        return (min_x, min_y, max_x, max_y)


class LODSystem:
    """
    Level of Detail system for performance optimization.
    Adjusts rendering detail based on distance from camera.
    """

    @staticmethod
    def get_lod_level(distance: float) -> int:
        """
        Get LOD level based on distance.

        Returns:
            0 = High detail
            1 = Medium detail
            2 = Low detail
            3 = Culled (don't render)
        """
        if distance < RENDER.LOD_HIGH_DISTANCE:
            return 0
        elif distance < RENDER.LOD_MED_DISTANCE:
            return 1
        elif distance < RENDER.LOD_LOW_DISTANCE:
            return 2
        else:
            return 3


class CityRenderer:
    """
    Main renderer for the city simulation.

    Features:
    - Multi-layer rendering (terrain -> roads -> buildings -> NPCs)
    - LOD system for performance
    - Camera system with zoom
    - FPS counter and debug info
    """

    def __init__(
        self,
        width: int = RENDER.WINDOW_WIDTH,
        height: int = RENDER.WINDOW_HEIGHT
    ):
        pygame.init()

        self.width = width
        self.height = height

        # Create window
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI City Simulation")

        # Clock for FPS
        self.clock = pygame.time.Clock()
        self.fps = 60

        # Font for UI
        self.font = pygame.font.Font(None, 24)
        self.small_font = pygame.font.Font(None, 18)

        # Rendering flags
        self.show_debug = True
        self.show_paths = False
        self.paused = False

        # Performance tracking
        self.frame_times: List[float] = []
        self.draw_calls = 0

        # World references (set later)
        self.terrain: Optional[TerrainGenerator] = None
        self.city: Optional[CityLayoutGenerator] = None
        self.npc_manager: Optional[NPCManager] = None
        self.camera: Optional[Camera] = None

        # Cached surfaces for performance
        self.terrain_surface: Optional[pygame.Surface] = None
        self.city_surface: Optional[pygame.Surface] = None

        # Controller support
        self.controller_manager = ControllerManager()
        self.controller: Optional[XboxController] = None
        self._update_controller_status()

    def set_world(
        self,
        terrain: TerrainGenerator,
        city: CityLayoutGenerator,
        npc_manager: NPCManager
    ):
        """Set world references and initialize camera"""
        self.terrain = terrain
        self.city = city
        self.npc_manager = npc_manager

        # Create camera
        self.camera = Camera(self.width, self.height, terrain.size)

        # Pre-render static layers
        self._cache_terrain()
        self._cache_city()

    def _cache_terrain(self):
        """Pre-render terrain to surface with realistic colors and shading"""
        if not self.terrain:
            return

        size = self.terrain.size
        self.terrain_surface = pygame.Surface((size, size))

        # Generate realistic terrain colors with shading
        print("Generating realistic terrain colors...")
        color_array = apply_realistic_terrain_colors(
            self.terrain.biomemap,
            self.terrain.heightmap,
            self.terrain.moisture_map
        )

        # Apply colors to surface
        pygame.surfarray.blit_array(
            self.terrain_surface,
            np.transpose(color_array, (1, 0, 2))
        )

        print("Terrain cached to surface with realistic graphics")

    def _cache_city(self):
        """Pre-render city roads to surface with realistic asphalt texture"""
        if not self.city:
            return

        size = self.city.size
        self.city_surface = pygame.Surface((size, size))
        self.city_surface.set_colorkey((0, 0, 0))  # Transparent
        self.city_surface.fill((0, 0, 0))

        # Generate noise for road texture variation
        road_noise = np.random.rand(size, size) * 0.1 + 0.95  # 95-105% variation

        # Render roads with texture
        road_cells = np.argwhere(self.city.road_grid)
        for y, x in road_cells:
            # Apply texture variation to asphalt color
            base = ColorPalette.ASPHALT if np.random.random() > 0.2 else ColorPalette.ASPHALT_WORN
            noise = road_noise[y, x]
            color = tuple(int(c * noise) for c in base)
            self.city_surface.set_at((x, y), color)

        print("City roads cached to surface with realistic textures")

    def _get_biome_color(self, biome: BiomeType) -> Tuple[int, int, int]:
        """Get color for biome type"""
        color_map = {
            BiomeType.WATER: RENDER.WATER_COLOR,
            BiomeType.SAND: RENDER.SAND_COLOR,
            BiomeType.GRASS: RENDER.GRASS_COLOR,
            BiomeType.FOREST: RENDER.FOREST_COLOR,
            BiomeType.MOUNTAIN: RENDER.MOUNTAIN_COLOR
        }
        return color_map.get(biome, (0, 0, 0))

    def render_frame(self, dt: float):
        """Render one frame"""
        frame_start = time.time()
        self.draw_calls = 0

        # Clear screen
        self.screen.fill((0, 0, 0))

        if not self.camera:
            return

        # Update camera
        self.camera.update(dt)

        # Get visible bounds for culling
        min_x, min_y, max_x, max_y = self.camera.get_visible_bounds()

        # Render layers
        self._render_terrain(min_x, min_y, max_x, max_y)
        self._render_roads(min_x, min_y, max_x, max_y)
        self._render_buildings(min_x, min_y, max_x, max_y)
        self._render_npcs()

        # Render UI
        self._render_ui(dt)

        # Update display
        pygame.display.flip()

        # Track frame time
        frame_time = time.time() - frame_start
        self.frame_times.append(frame_time)
        if len(self.frame_times) > 60:
            self.frame_times.pop(0)

    def _render_terrain(self, min_x: int, min_y: int, max_x: int, max_y: int):
        """Render terrain layer"""
        if not self.terrain_surface or not self.camera:
            return

        # Calculate zoom scale
        scale = max(1, int(self.camera.zoom))

        # Get visible portion of terrain
        visible_terrain = self.terrain_surface.subsurface(
            (min_x, min_y, max_x - min_x, max_y - min_y)
        )

        # Scale based on zoom
        if scale != 1:
            new_width = int((max_x - min_x) * scale)
            new_height = int((max_y - min_y) * scale)
            if new_width > 0 and new_height > 0:
                visible_terrain = pygame.transform.scale(
                    visible_terrain,
                    (new_width, new_height)
                )

        # Calculate screen position
        screen_x, screen_y = self.camera.world_to_screen(min_x, min_y)

        # Blit to screen
        self.screen.blit(visible_terrain, (screen_x, screen_y))
        self.draw_calls += 1

    def _render_roads(self, min_x: int, min_y: int, max_x: int, max_y: int):
        """Render road layer"""
        if not self.city_surface or not self.camera:
            return

        # Calculate zoom scale
        scale = max(1, int(self.camera.zoom))

        # Get visible portion of city
        visible_city = self.city_surface.subsurface(
            (min_x, min_y, max_x - min_x, max_y - min_y)
        )

        # Scale based on zoom
        if scale != 1:
            new_width = int((max_x - min_x) * scale)
            new_height = int((max_y - min_y) * scale)
            if new_width > 0 and new_height > 0:
                visible_city = pygame.transform.scale(
                    visible_city,
                    (new_width, new_height)
                )

        # Calculate screen position
        screen_x, screen_y = self.camera.world_to_screen(min_x, min_y)

        # Blit to screen
        self.screen.blit(visible_city, (screen_x, screen_y))
        self.draw_calls += 1

    def _render_buildings(self, min_x: int, min_y: int, max_x: int, max_y: int):
        """Render buildings with LOD"""
        if not self.city or not self.camera:
            return

        camera_pos = (self.camera.x, self.camera.y)

        for building in self.city.buildings:
            # Frustum culling
            if not (min_x <= building.x < max_x and min_y <= building.y < max_y):
                continue

            # Calculate distance from camera
            distance = np.sqrt(
                (building.x - camera_pos[0])**2 +
                (building.y - camera_pos[1])**2
            )

            # Get LOD level
            lod = LODSystem.get_lod_level(distance)

            if lod == 3:  # Culled
                continue

            # Convert to screen coordinates
            screen_x, screen_y = self.camera.world_to_screen(building.x, building.y)

            # Calculate screen size
            width = int(building.width * self.camera.zoom)
            height = int(building.height * self.camera.zoom)

            if width < 1 or height < 1:
                continue

            # Choose rendering detail based on LOD
            color = self._get_zone_color(building.zone_type)

            if lod == 0:
                # High detail: 3D building with windows and shading
                RealisticBuildingRenderer.draw_building_3d(
                    self.screen,
                    screen_x, screen_y,
                    width, height,
                    building.floors,
                    color
                )
            elif lod == 1:
                # Medium detail: simple 3D effect
                # Front face
                pygame.draw.rect(
                    self.screen,
                    color,
                    (screen_x, screen_y, width, height)
                )
                # Simple shadow
                shadow_color = tuple(int(c * 0.6) for c in color)
                shadow_offset = max(1, int(height * 0.1))
                if shadow_offset > 0:
                    pygame.draw.polygon(
                        self.screen,
                        shadow_color,
                        [(screen_x + width, screen_y),
                         (screen_x + width + shadow_offset, screen_y - shadow_offset),
                         (screen_x + width + shadow_offset, screen_y + height - shadow_offset),
                         (screen_x + width, screen_y + height)]
                    )
                # Outline
                pygame.draw.rect(self.screen, (0, 0, 0), (screen_x, screen_y, width, height), 1)
            else:
                # Low detail: single pixel with color
                pygame.draw.circle(
                    self.screen,
                    color,
                    (screen_x, screen_y),
                    2
                )

            self.draw_calls += 1

    def _render_npcs(self):
        """Render NPCs"""
        if not self.npc_manager or not self.camera:
            return

        for npc in self.npc_manager.npcs:
            # Convert to screen coordinates
            screen_x, screen_y = self.camera.world_to_screen(
                npc.position[0],
                npc.position[1]
            )

            # Check if on screen
            if not (0 <= screen_x < self.width and 0 <= screen_y < self.height):
                continue

            # Size based on zoom
            radius = max(2, int(3 * self.camera.zoom))

            # Color based on state
            color = self._get_npc_state_color(npc.state)

            # Draw NPC
            pygame.draw.circle(
                self.screen,
                color,
                (screen_x, screen_y),
                radius
            )

            # Draw direction indicator
            if np.linalg.norm(npc.velocity) > 0.1:
                end_x = screen_x + int(np.cos(npc.facing_direction) * radius * 2)
                end_y = screen_y + int(np.sin(npc.facing_direction) * radius * 2)
                pygame.draw.line(
                    self.screen,
                    (255, 255, 255),
                    (screen_x, screen_y),
                    (end_x, end_y),
                    1
                )

            self.draw_calls += 1

    def _get_zone_color(self, zone_type: ZoneType) -> Tuple[int, int, int]:
        """Get realistic color for zone type with variation"""
        # Use realistic building colors based on zone
        if zone_type == ZoneType.COMMERCIAL:
            # Commercial: glass and steel
            colors = [ColorPalette.GLASS_BLUE, ColorPalette.GLASS_GREEN,
                     ColorPalette.CONCRETE_LIGHT, ColorPalette.METAL_STEEL]
        elif zone_type == ZoneType.RESIDENTIAL:
            # Residential: varied housing colors
            colors = [ColorPalette.HOUSE_BEIGE, ColorPalette.HOUSE_WHITE,
                     ColorPalette.HOUSE_CREAM, ColorPalette.HOUSE_TAN,
                     ColorPalette.BRICK_RED]
        elif zone_type == ZoneType.INDUSTRIAL:
            # Industrial: concrete and metal
            colors = [ColorPalette.CONCRETE_DARK, ColorPalette.CONCRETE_LIGHT,
                     ColorPalette.METAL_STEEL]
        elif zone_type == ZoneType.PARK:
            # Parks: green
            colors = [ColorPalette.GRASS_LIGHT, ColorPalette.FOREST_LIGHT]
        else:  # MIXED
            # Mixed: combination
            colors = [ColorPalette.BRICK_ORANGE, ColorPalette.CONCRETE_LIGHT,
                     ColorPalette.HOUSE_BEIGE]

        # Random selection for variety
        return colors[np.random.randint(0, len(colors))]

    def _get_npc_state_color(self, state: NPCState) -> Tuple[int, int, int]:
        """Get color for NPC state"""
        color_map = {
            NPCState.IDLE: (100, 100, 255),
            NPCState.WALKING: (100, 255, 100),
            NPCState.RUNNING: (255, 200, 100),
            NPCState.WORKING: (200, 200, 200),
            NPCState.SOCIALIZING: (255, 100, 255),
            NPCState.EATING: (255, 255, 100),
            NPCState.FLEEING: (255, 50, 50)
        }
        return color_map.get(state, RENDER.NPC_COLOR)

    def _render_ui(self, dt: float):
        """Render UI overlay"""
        if not self.show_debug:
            return

        # FPS
        fps_text = self.font.render(f"FPS: {int(self.clock.get_fps())}", True, (255, 255, 255))
        self.screen.blit(fps_text, (10, 10))

        # Draw calls
        dc_text = self.small_font.render(f"Draw Calls: {self.draw_calls}", True, (255, 255, 255))
        self.screen.blit(dc_text, (10, 35))

        # Camera info
        cam_text = self.small_font.render(
            f"Camera: ({int(self.camera.x)}, {int(self.camera.y)}) Zoom: {self.camera.zoom:.2f}",
            True,
            (255, 255, 255)
        )
        self.screen.blit(cam_text, (10, 55))

        # NPC stats
        if self.npc_manager:
            stats = self.npc_manager.get_npc_stats()
            npc_text = self.small_font.render(f"NPCs: {stats.get('total', 0)}", True, (255, 255, 255))
            self.screen.blit(npc_text, (10, 75))

        # Controller status
        if self.controller and self.controller.connected:
            controller_name = self.controller.joystick.get_name() if self.controller.joystick else "Xbox Controller"
            controller_text = self.small_font.render(
                f"Controller: {controller_name[:30]}",
                True,
                (100, 255, 100)  # Green for connected
            )
            self.screen.blit(controller_text, (10, 95))

        # Controls hint
        if self.controller and self.controller.connected:
            controls = [
                "Controls:",
                "WASD / Left Stick - Move",
                "Q/E / Bumpers - Zoom",
                "Space / Start - Pause",
                "D / Y - Toggle Debug",
                "Right Stick - Zoom",
                "Triggers - Zoom In/Out",
                "ESC - Quit"
            ]
        else:
            controls = [
                "Controls:",
                "WASD - Move Camera",
                "Q/E - Zoom",
                "Space - Pause",
                "D - Toggle Debug",
                "ESC - Quit",
                "",
                "Connect Xbox Controller",
                "for gamepad support"
            ]

        y_offset = self.height - (len(controls) * 20 + 10)
        for i, line in enumerate(controls):
            text = self.small_font.render(line, True, (200, 200, 200))
            self.screen.blit(text, (10, y_offset + i * 20))

        # Attribution (bottom right corner)
        attribution_text = self.small_font.render("Crafted by Intellegix", True, (150, 150, 150))
        attr_width = attribution_text.get_width()
        self.screen.blit(attribution_text, (self.width - attr_width - 10, self.height - 20))

    def _update_controller_status(self):
        """Update controller connection status"""
        self.controller = self.controller_manager.get_primary_controller()

    def handle_input(self, events: List[pygame.event.Event]):
        """Handle input events from keyboard and Xbox controller"""
        if not self.camera:
            return

        # Update controller
        self.controller_manager.update_all()
        self._update_controller_status()

        # Handle keyboard/mouse events
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_d:
                    self.show_debug = not self.show_debug

            elif event.type == pygame.MOUSEWHEEL:
                # Zoom with mouse wheel
                self.camera.zoom += event.y * RENDER.ZOOM_SPEED
                self.camera.zoom = max(RENDER.MIN_ZOOM, min(RENDER.MAX_ZOOM, self.camera.zoom))

            # Controller connection/disconnection
            elif event.type == pygame.JOYDEVICEADDED:
                print(f"Controller connected!")
                self.controller_manager.scan_controllers()
                self._update_controller_status()

            elif event.type == pygame.JOYDEVICEREMOVED:
                print(f"Controller disconnected!")
                self._update_controller_status()

        # Handle keyboard input
        keys = pygame.key.get_pressed()
        camera_speed = RENDER.CAMERA_SPEED / self.camera.zoom

        # Keyboard camera movement
        keyboard_vx = 0
        keyboard_vy = 0

        if keys[pygame.K_w]:
            keyboard_vy = -camera_speed
        elif keys[pygame.K_s]:
            keyboard_vy = camera_speed

        if keys[pygame.K_a]:
            keyboard_vx = -camera_speed
        elif keys[pygame.K_d]:
            keyboard_vx = camera_speed

        # Keyboard zoom
        if keys[pygame.K_q]:
            self.camera.zoom = max(RENDER.MIN_ZOOM, self.camera.zoom - RENDER.ZOOM_SPEED)
        elif keys[pygame.K_e]:
            self.camera.zoom = min(RENDER.MAX_ZOOM, self.camera.zoom + RENDER.ZOOM_SPEED)

        # Handle controller input
        controller_vx = 0
        controller_vy = 0

        if self.controller and self.controller.connected:
            state = self.controller.state

            # Left stick for camera movement
            if abs(state.left_stick_x) > 0.1 or abs(state.left_stick_y) > 0.1:
                controller_vx = state.left_stick_x * camera_speed * 1.5  # Slightly faster for analog
                controller_vy = state.left_stick_y * camera_speed * 1.5

            # Right stick for zoom (vertical axis)
            if abs(state.right_stick_y) > 0.1:
                zoom_change = -state.right_stick_y * RENDER.ZOOM_SPEED * 2.0
                self.camera.zoom += zoom_change
                self.camera.zoom = max(RENDER.MIN_ZOOM, min(RENDER.MAX_ZOOM, self.camera.zoom))

            # Triggers for zoom
            if state.right_trigger > 0.1:
                self.camera.zoom += state.right_trigger * RENDER.ZOOM_SPEED * 0.5
                self.camera.zoom = min(RENDER.MAX_ZOOM, self.camera.zoom)

            if state.left_trigger > 0.1:
                self.camera.zoom -= state.left_trigger * RENDER.ZOOM_SPEED * 0.5
                self.camera.zoom = max(RENDER.MIN_ZOOM, self.camera.zoom)

            # D-pad for camera movement (discrete)
            if state.dpad_x != 0 or state.dpad_y != 0:
                controller_vx += state.dpad_x * camera_speed
                controller_vy += state.dpad_y * camera_speed

            # Button controls
            if state.button_start:
                self.paused = not self.paused

            if self.controller.is_button_pressed(ControllerButton.Y):
                self.show_debug = not self.show_debug

            # Bumpers for zoom
            if state.button_lb:
                self.camera.zoom = max(RENDER.MIN_ZOOM, self.camera.zoom - RENDER.ZOOM_SPEED)
            if state.button_rb:
                self.camera.zoom = min(RENDER.MAX_ZOOM, self.camera.zoom + RENDER.ZOOM_SPEED)

        # Combine keyboard and controller input (controller takes priority if both active)
        if abs(controller_vx) > 0.1 or abs(controller_vy) > 0.1:
            self.camera.vx = controller_vx
            self.camera.vy = controller_vy
        else:
            self.camera.vx = keyboard_vx
            self.camera.vy = keyboard_vy

    def tick(self) -> int:
        """Tick the clock and return FPS"""
        return self.clock.tick(self.fps)
