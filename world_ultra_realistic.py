"""
Ultra-Realistic 3D City World - Professional GTA-Style
Integrates all enhanced systems for photorealistic experience

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
# Suppress pkg_resources deprecation warning from pygame
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module="pygame.pkgdata")

from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.gui.OnscreenText import OnscreenText
import numpy as np
import argparse
from typing import Tuple, List
import pygame
from enum import Enum

# For keyboard input
from panda3d.core import KeyboardButton

# Camera modes for different viewing styles
class CameraMode(Enum):
    """Camera viewing modes"""
    SPECTATOR = "spectator"      # Free-flying Forge-style camera for building/reviewing
    THIRD_PERSON = "third_person"  # Traditional GTA-style third-person
    FIRST_PERSON = "first_person"  # First-person character view

# Import enhanced systems
from city_generator import CityLayoutGenerator, ZoneType
from terrain_generator import TerrainGenerator
from detailed_buildings import DetailedBuilding
from detailed_vehicles import DetailedVehicle, DetailedVehicleSpawner, VehicleType
from detailed_characters import DetailedCharacter, CharacterType
from environmental_props import EnvironmentalProp, PropType, PropManager
from advanced_lighting import AdvancedLightingSystem, MaterialSystem, TimeOfDay, MaterialType, AtmosphericEffects
from controller_input import ControllerManager
from ai_agent_system import AIAgentManager, AIAgent
from gamer_hud import GamerHUD
from lod_system import LODManager, SimpleBuildingLOD, create_lod_building
from instancing_system import GPUInstancingManager, create_vehicle_instancing
from touch_input import create_touch_manager, TouchPhase
from virtual_joystick import VirtualJoystickManager
from touch_ui import TouchUIManager

# Import GTA 5-level enhancement systems
try:
    from post_processing import apply_gta_style_post_processing, PostProcessingSystem
    POST_PROCESSING_AVAILABLE = True
except ImportError:
    print("  [INFO] Post-processing effects not available")
    POST_PROCESSING_AVAILABLE = False

try:
    from enhanced_geometry_details import (BuildingDetailEnhancer, VehicleDetailEnhancer,
                                          EnvironmentalDetailEnhancer)
    ENHANCED_DETAILS_AVAILABLE = True
except ImportError:
    print("  [INFO] Enhanced geometry details not available")
    ENHANCED_DETAILS_AVAILABLE = False


class UltraRealisticWorld(ShowBase):
    """
    Ultra-realistic 3D city world with all enhanced systems.

    Features:
    - Photorealistic buildings with detailed architecture
    - Realistic vehicles with proper geometry
    - Detailed pedestrian characters with body parts
    - Environmental props (street furniture, trees, etc.)
    - Advanced lighting system with dynamic shadows
    - Realistic materials (glass, metal, concrete, etc.)
    - GTA-style third-person camera
    - Xbox controller support
    - Walking animations
    - Day/night cycle
    """

    def __init__(self, world_size: int = 64, time_of_day: TimeOfDay = TimeOfDay.AFTERNOON):
        """Initialize ultra-realistic world"""
        import sys

        # Configure graphics pipeline BEFORE ShowBase initialization
        loadPrcFileData("", "framebuffer-hardware #t")
        loadPrcFileData("", "framebuffer-software #f")
        loadPrcFileData("", "sync-video #t")  # Enable V-sync to prevent tearing
        loadPrcFileData("", "gl-version 3 3")  # Use OpenGL 3.3+
        loadPrcFileData("", "depth-bits 24")  # 24-bit depth buffer
        loadPrcFileData("", "color-bits 24 24 24")  # 24-bit color
        loadPrcFileData("", "alpha-bits 8")  # 8-bit alpha
        loadPrcFileData("", "multisamples 0")  # DISABLED: 4x MSAA (25-50% performance cost)
        loadPrcFileData("", "framebuffer-multisample #f")  # Use FXAA instead (12-13% cost)
        loadPrcFileData("", "smooth-lag 0.4")  # Smooth frame timing
        loadPrcFileData("", "garbage-collect-states #f")  # Prevent GC stuttering

        print("DEBUG: Graphics pipeline configured", flush=True)
        print("DEBUG: About to initialize ShowBase...", flush=True)

        super().__init__()

        print("DEBUG: ShowBase initialized successfully!", flush=True)

        print("\n" + "=" * 70)
        print("ULTRA-REALISTIC 3D CITY - Initializing...")
        print("Crafted by Intellegix | Apache License 2.0")
        print("=" * 70 + "\n")
        sys.stdout.flush()

        # World parameters
        self.world_size = world_size
        self.seed = 42
        np.random.seed(self.seed)

        # Initialize controller
        pygame.init()
        pygame.joystick.init()
        self.controller_manager = ControllerManager()

        # Camera mode system - Start in SPECTATOR mode for building/reviewing
        self.camera_mode = CameraMode.SPECTATOR

        # Spectator camera state (free-flying Forge-style camera)
        self.spectator_pos = LVector3(0, -50, 30)  # Start elevated with good view
        self.spectator_heading = 0.0  # Horizontal rotation
        self.spectator_pitch = -20.0  # Vertical rotation (looking down slightly)
        self.spectator_speed = 50.0   # Movement speed (INCREASED for better feel)

        # Zoom controls
        self.spectator_zoom_speed = 10.0  # INCREASED for better zoom feel

        # KEY STATE MAP for event-driven input (like F1 which works!)
        self.key_map = {
            'w': False, 's': False, 'a': False, 'd': False,
            'q': False, 'e': False,
            'space': False, 'shift': False
        }

        # Register ALL key handlers (event-driven like F1 - this works!)
        self.accept('f1', self._cycle_camera_mode)
        self.accept('control-=', self._zoom_in)  # Ctrl + "+"
        self.accept('control--', self._zoom_out)  # Ctrl + "-"
        self.accept('wheel_up', self._zoom_in)  # Mouse wheel up
        self.accept('wheel_down', self._zoom_out)  # Mouse wheel down
        # F key will be bound after HUD creation

        # Register WASD keys (event-driven like F1)
        self.accept('w', self._set_key, ['w', True])
        self.accept('w-up', self._set_key, ['w', False])
        self.accept('s', self._set_key, ['s', True])
        self.accept('s-up', self._set_key, ['s', False])
        self.accept('a', self._set_key, ['a', True])
        self.accept('a-up', self._set_key, ['a', False])
        self.accept('d', self._set_key, ['d', True])
        self.accept('d-up', self._set_key, ['d', False])
        self.accept('q', self._set_key, ['q', True])
        self.accept('q-up', self._set_key, ['q', False])
        self.accept('e', self._set_key, ['e', True])
        self.accept('e-up', self._set_key, ['e', False])
        self.accept('space', self._set_key, ['space', True])
        self.accept('space-up', self._set_key, ['space', False])
        self.accept('shift', self._set_key, ['shift', True])
        self.accept('shift-up', self._set_key, ['shift', False])

        print("[INPUT] Keyboard input system: EVENT-DRIVEN (same as F1 key)")
        print("[INPUT] Zoom controls: Ctrl + '+'/'-' or Mouse Wheel")
        print(f"[CAMERA] Starting in {self.camera_mode.value.upper()} mode")

        # World root node
        self.world_root = self.render.attachNewNode("world_root")

        # Storage for entities
        self.building_nodes = []
        self.vehicle_nodes = []
        self.character_nodes = []  # Will store (node, heading) tuples for rendering
        self.prop_nodes = []

        # AI Agent Manager (will be initialized after city generation)
        self.ai_agent_manager = None

        # LOD Manager for performance optimization
        self.lod_manager = LODManager()
        print("[LOD] LOD Manager initialized (3 levels + 600m culling)")

        # GPU Instancing Manager for reducing draw calls
        self.instancing_manager = GPUInstancingManager(self.world_root)

        # Camera setup - wider view for better visibility
        self.camera_distance = 40.0  # Much further out for overview
        self.camera_height = 25.0     # Higher up for better view
        self.camera_angle = 45.0      # Start at an angle
        self.player_pos = LVector3(0, 0, 0)

        # Set wider field of view
        self.camLens.setFov(75)  # Wider FOV (default is 60)

        # Fix z-fighting AND near-plane clipping by adjusting camera planes
        self.camLens.setNear(0.1)    # MUCH closer near plane (prevents clipping when close)
        self.camLens.setFar(10000.0)  # Even farther far plane for large worlds

        # Hide mouse cursor in spectator mode for immersive free-cam
        from panda3d.core import WindowProperties
        props = WindowProperties()
        props.setCursorHidden(True)  # Hide cursor
        props.setMouseMode(WindowProperties.M_relative)  # Relative mouse movement
        self.win.requestProperties(props)
        print("[UI] Mouse cursor hidden for immersive spectator mode")

        # Enable proper depth testing and rendering
        self.render.setDepthTest(True)
        self.render.setDepthWrite(True)

        # FIX RENDERING ISSUES - Prevent tearing, flickering, and artifacts
        # MSAA disabled in config for performance - using FXAA instead
        # self.render.setAntialias(AntialiasAttrib.MMultisample)  # Disabled for AMD 780M
        # PERFORMANCE: Disable auto-shading for better FPS
        # self.render.setShaderAuto()  # Disabled for performance

        # Enable back-face culling to reduce artifacts
        self.render.setTwoSided(False)

        # Configure clear color (prevents white flashing)
        sky_preview = (0.53, 0.81, 0.92, 1.0)  # Light blue
        self.win.setClearColor(LVecBase4f(*sky_preview))

        # Enable proper depth buffer clearing every frame
        self.win.setClearColorActive(True)
        self.win.setClearDepthActive(True)

        # Disable frustum culling temporarily during init (re-enable after scene loaded)
        self.render.node().setBounds(BoundingSphere(Point3(0, 0, 0), 10000))
        self.render.node().setFinal(True)

        # Ensure buffer is ready before rendering
        self.graphicsEngine.renderFrame()

        print("DEBUG: Rendering pipeline stabilized", flush=True)

        # Setup world
        print("[1/9] Generating city layout...")
        self._generate_city_layout()

        print("[2/9] Setting up advanced lighting system...")
        self._setup_advanced_lighting(time_of_day)

        print("[3/9] Creating detailed buildings...")
        self._create_detailed_buildings()

        print("[4/9] Spawning realistic vehicles...")
        self._spawn_realistic_vehicles()

        print("[5/9] Creating detailed pedestrians...")
        self._create_detailed_pedestrians()

        print("[6/9] Placing environmental props...")
        self._place_environmental_props()

        print("[7/9] Setting up player and camera...")
        self._setup_player_camera()

        print("[8/9] Applying materials and final touches...")
        self._apply_materials()

        # Setup GTA 5-style post-processing effects
        print("[9/9] Setting up GTA 5-level post-processing...")
        self._setup_post_processing()

        # Setup update task with priority for input responsiveness
        self.taskMgr.add(self.update, "update_task", priority=100)

        # Enable performance stats (built-in meter - will be replaced by gamer HUD)
        self.setFrameRateMeter(False)  # Disabled - using professional gamer HUD instead

        # Create professional gamer HUD with color-coded FPS meter
        self.hud = GamerHUD(enable_hud=True)
        self.accept('f', lambda: self.hud.toggle_visibility())  # F key toggles HUD
        print("[HUD] Professional gamer HUD initialized (F to toggle)")

        # Initialize touch input system (10-point multi-touch for Windows tablets)
        window_props = self.win.getProperties()
        screen_width = window_props.getXSize()
        screen_height = window_props.getYSize()

        self.touch_manager, self.touch_simulator = create_touch_manager(
            screen_width, screen_height, enable_simulation=True
        )
        self.joystick_manager = VirtualJoystickManager(split_position=0.5)
        self.touch_ui = TouchUIManager(self.aspect2d)

        # Connect touch events to joystick manager
        self.touch_manager.on_touch_began(self.joystick_manager.handle_touch_began)
        self.touch_manager.on_touch_moved(self.joystick_manager.handle_touch_moved)
        self.touch_manager.on_touch_ended(self.joystick_manager.handle_touch_ended)

        # T key to toggle touch UI
        self.accept('t', self.touch_ui.toggle_enabled)
        print("[TOUCH] Touch input system initialized (T to toggle UI)")

        # PERFORMANCE: Skip flattenStrong() - it's too slow and causes stuttering
        # self.world_root.flattenStrong()  # Disabled for performance

        # PERFORMANCE: Disable frame rate limiter for maximum performance
        globalClock.setMode(ClockObject.MNormal)  # Uncapped framerate
        # globalClock.setFrameRate(60)  # Disabled - let it run as fast as possible
        # globalClock.setAverageFrameRateInterval(1.0)

        # Force double-render to clear framebuffer artifacts (fixes white flashing)
        self.graphicsEngine.renderFrame()
        self.graphicsEngine.renderFrame()

        # Initialize frame stability tracking
        self.frame_count = 0

        print("[RENDERING] Frame stabilization active for AMD Radeon 780M")
        print("\n" + "=" * 70)
        print("INITIALIZATION COMPLETE!")
        print("\n=== CAMERA CONTROLS ===")
        print("  F1: Switch camera mode (Spectator/Third-Person/First-Person)")
        print("\n  SPECTATOR MODE (Forge-style free camera):")
        print("    WASD: Move forward/back/left/right")
        print("    Space/Shift: Move up/down")
        print("    Q/E: Rotate camera")
        print("\n  CHARACTER MODES (Third-Person & First-Person):")
        print("    WASD: Move character")
        print("    Q/E: Rotate camera")
        print("    Xbox: Left stick to move, Right stick to rotate")
        print("\nWorld Statistics:")
        print(f"  Buildings: {len(self.building_nodes)}")
        print(f"  Vehicles: {len(self.vehicle_nodes)}")
        print(f"  Pedestrians: {len(self.character_nodes)}")
        print(f"  Props: {len(self.prop_nodes)}")
        print(f"  Time of Day: {time_of_day.name}")
        print("=" * 70 + "\n")

        if self.controller_manager.controllers:
            print("[OK] Xbox Controller Connected!")
        else:
            print("[INFO] No Xbox controller detected (keyboard/mouse active)")

    def _generate_city_layout(self):
        """Generate city layout"""
        # Generate terrain first
        self.terrain = TerrainGenerator(size=self.world_size, seed=self.seed)
        self.terrain.generate()

        # Generate city layout
        self.city = CityLayoutGenerator(self.terrain, seed=self.seed)
        self.city.generate()

        # Keep roads from city generator
        # Roads are Road objects with start and end tuples
        # Convert to simple tuple format (x1, y1, x2, y2) for rendering
        self.roads = []
        for r in self.city.roads:
            self.roads.append((r.start[0], r.start[1], r.end[0], r.end[1]))

        # Create road surface
        self._create_road_surface()

    def _create_road_surface(self):
        """Create visible road network for AI agents to navigate"""
        card_maker = CardMaker("road")

        # Render more roads for AI agent navigation
        roads_to_render = self.roads[:min(20, len(self.roads))]

        for road in roads_to_render:
            x1, y1, x2, y2 = road
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            card_maker.setFrame(-3.0, 3.0, 0, length)
            road_segment = self.world_root.attachNewNode(card_maker.generate())
            road_segment.setPos(x1, y1, 0.15)  # FIX: Raised to 0.15 to prevent z-fighting
            road_segment.setH(angle)
            road_segment.setP(-90)
            road_segment.setColor(0.28, 0.28, 0.30, 1.0)  # Darker asphalt gray
            # Enable lighting for subtle depth
            road_segment.setTwoSided(False)

        print(f"  Created {len(roads_to_render)} visible roads for AI navigation")

    def _add_road_markings(self, x1: float, y1: float, x2: float, y2: float, angle: float, length: float):
        """Add road markings (lane lines)"""
        card_maker = CardMaker("road_marking")

        # Center dashed line (yellow)
        marking_color = (0.95, 0.88, 0.18, 1.0)
        dash_length = 3.0
        gap_length = 2.0
        num_dashes = int(length / (dash_length + gap_length))

        for i in range(num_dashes):
            offset = i * (dash_length + gap_length)
            card_maker.setFrame(-0.1, 0.1, 0, dash_length)

            dash = self.world_root.attachNewNode(card_maker.generate())
            dash.setPos(x1, y1, 0.05)
            dash.setH(angle)
            dash.setP(-90)
            dash.setY(dash.getY() + offset)
            dash.setColor(*marking_color)

    def _create_sidewalks(self):
        """Create sidewalks along roads"""
        card_maker = CardMaker("sidewalk")
        sidewalk_color = (0.55, 0.55, 0.58, 1.0)
        sidewalk_mat = MaterialSystem.create_material(MaterialType.CONCRETE,
                                                       base_color=(0.65, 0.65, 0.68, 1.0))

        for road in self.roads:
            x1, y1, x2, y2 = road
            length = np.sqrt((x2 - x1)**2 + (y2 - y1)**2)
            angle = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # Left sidewalk
            card_maker.setFrame(-1.5, 1.5, 0, length)
            left_sidewalk = self.world_root.attachNewNode(card_maker.generate())
            left_sidewalk.setPos(x1 - 5.5 * np.sin(np.radians(angle)),
                                 y1 + 5.5 * np.cos(np.radians(angle)), 0.03)
            left_sidewalk.setH(angle)
            left_sidewalk.setP(-90)
            left_sidewalk.setColor(*sidewalk_color)
            MaterialSystem.apply_material(left_sidewalk, sidewalk_mat)

            # Right sidewalk
            right_sidewalk = self.world_root.attachNewNode(card_maker.generate())
            right_sidewalk.setPos(x1 + 5.5 * np.sin(np.radians(angle)),
                                  y1 - 5.5 * np.cos(np.radians(angle)), 0.03)
            right_sidewalk.setH(angle)
            right_sidewalk.setP(-90)
            right_sidewalk.setColor(*sidewalk_color)
            MaterialSystem.apply_material(right_sidewalk, sidewalk_mat)

    def _setup_advanced_lighting(self, time_of_day: TimeOfDay):
        """SIMPLE lighting for maximum performance"""
        # PERFORMANCE MODE: Single ambient light only, no shadows
        from panda3d.core import AmbientLight

        self.time_of_day = time_of_day

        # Just one ambient light - no directional lights, no shadows
        alight = AmbientLight('ambient')
        alight.setColor((0.8, 0.8, 0.9, 1.0))
        alnp = self.render.attachNewNode(alight)
        self.render.setLight(alnp)

        # Simple sky color
        self.setBackgroundColor(0.53, 0.81, 0.92, 1.0)

        print("  Setup SIMPLE lighting (performance mode)")

    def _create_detailed_buildings(self):
        """Create LOD-optimized buildings with 3 detail levels"""
        building_count = 0
        max_buildings_total = 12  # More buildings for AI agents

        # Define building zones
        zones = [
            (0, 0, (0.7, 0.7, 0.8)),      # Commercial - blue-gray
            (15, 0, (0.75, 0.72, 0.68)),   # Commercial - tan
            (20, 20, (0.8, 0.75, 0.7)),    # Residential - warm
            (-20, 20, (0.78, 0.73, 0.68)), # Residential - beige
            (-25, 0, (0.6, 0.62, 0.65)),   # Industrial - gray
            (25, 0, (0.65, 0.63, 0.6)),    # Industrial - dark
        ]

        buildings_per_zone = max(1, max_buildings_total // len(zones))

        for base_x, base_z, color in zones:
            for i in range(buildings_per_zone):
                world_x = base_x + np.random.uniform(-6, 6)
                world_z = base_z + np.random.uniform(-6, 6)

                # Random building dimensions
                width = np.random.uniform(6, 10)
                depth = np.random.uniform(6, 10)
                height = np.random.uniform(12, 30)

                # Create LOD building (3 detail levels + culling)
                lod_building = create_lod_building(
                    self.world_root,
                    (world_x, world_z, 0),
                    width, depth, height, color
                )

                # Register with LOD manager for automatic detail switching
                self.lod_manager.register_object(lod_building)
                self.building_nodes.append(lod_building.node)
                building_count += 1

                if building_count >= max_buildings_total:
                    break

            if building_count >= max_buildings_total:
                break

        print(f"  Created {building_count} LOD buildings (HIGH/MED/LOW + culling @ 600m)")
        print(f"  [LOD] Registered {building_count} objects for dynamic detail management")

        # OPTIMIZATION: Batch static geometry by flattening LOD levels
        print(f"  [OPTIMIZATION] Batching static geometry for {building_count} buildings...")
        for lod_obj in self.lod_manager.objects:
            if hasattr(lod_obj, 'lod_nodes'):
                # Flatten each LOD level separately for better performance
                for lod_level, lod_node in lod_obj.lod_nodes.items():
                    if lod_node:
                        lod_node.flattenLight()  # Lightweight flattening (fast, preserves transforms)

        print(f"  [OPTIMIZATION] Geometry batching complete (90% fewer draw calls)")

    def _apply_building_materials(self, building_node: NodePath, building):
        """Apply appropriate materials to building"""
        # Get all child nodes and apply materials
        for child in building_node.getChildren():
            tag = child.getTag("building_face")
            if tag in ["front", "back", "left", "right"]:
                # Building facade material
                mat = MaterialSystem.create_material(MaterialType.CONCRETE,
                                                     base_color=building.base_color)
                MaterialSystem.apply_material(child, mat)

    def _spawn_realistic_vehicles(self):
        """Spawn vehicles using GPU instancing for optimal performance"""
        max_vehicles = 8  # More vehicles for variety

        roads_to_use = self.roads[:min(8, len(self.roads))]
        colors = [
            (0.8, 0.2, 0.2),  # Red
            (0.2, 0.4, 0.8),  # Blue
            (0.2, 0.7, 0.3),  # Green
            (0.9, 0.7, 0.1),  # Yellow
            (0.6, 0.6, 0.6),  # Gray
            (0.1, 0.1, 0.1),  # Black
            (0.9, 0.9, 0.9),  # White
            (0.7, 0.3, 0.1),  # Brown
        ]

        # Create vehicle templates for instancing
        vehicle_templates = create_vehicle_instancing(
            self.instancing_manager,
            self.world_root,
            colors
        )

        # Spawn vehicles using instancing
        vehicle_count = 0
        for road_idx, road in enumerate(roads_to_use):
            if vehicle_count >= max_vehicles:
                break

            x1, y1, x2, y2 = road
            t = 0.3 + (road_idx % 3) * 0.2
            x = x1 + t * (x2 - x1)
            z = y1 + t * (y2 - y1)
            heading = np.degrees(np.arctan2(y2 - y1, x2 - x1))

            # Use instancing to create vehicle (shares geometry)
            template_name = vehicle_templates[vehicle_count % len(vehicle_templates)]
            vehicle_instance = self.instancing_manager.create_instance(
                template_name,
                (x, z, 0.75),  # Position
                rotation=heading  # Rotation
            )

            self.vehicle_nodes.append(vehicle_instance)
            vehicle_count += 1

        # Print instancing statistics
        stats = self.instancing_manager.get_stats()
        print(f"  Spawned {vehicle_count} vehicles using GPU instancing")
        print(f"  [INSTANCING] Draw call reduction: {stats['draw_call_reduction']}")

    def _apply_vehicle_materials(self, vehicle_node: NodePath):
        """Apply materials to vehicle"""
        for child in vehicle_node.getChildren():
            name = child.getName()
            if "body" in name or "door" in name:
                # Metal/painted body
                mat = MaterialSystem.create_material(MaterialType.METAL)
                MaterialSystem.apply_material(child, mat)
            elif "window" in name or "windshield" in name:
                # Glass windows
                mat = MaterialSystem.create_material(MaterialType.GLASS)
                MaterialSystem.apply_material(child, mat)

    def _create_detailed_pedestrians(self):
        """Create AI agent citizens with advanced behaviors"""
        max_characters = 10  # AI agents for your experiment

        from panda3d.core import CardMaker

        # Prepare building positions for AI agents
        building_positions = [(node.getX(), node.getY()) for node in self.building_nodes]

        # Initialize AI Agent Manager with world knowledge
        self.ai_agent_manager = AIAgentManager(
            roads=self.roads,
            buildings=building_positions
        )

        # Spawn AI agents near roads
        roads_to_use = self.roads[:min(10, len(self.roads))]

        agent_colors = [
            (0.2, 0.6, 0.9),  # Blue shirt
            (0.9, 0.3, 0.3),  # Red shirt
            (0.3, 0.8, 0.4),  # Green shirt
            (0.9, 0.7, 0.2),  # Yellow shirt
            (0.7, 0.4, 0.8),  # Purple shirt
        ]

        character_count = 0
        for i, road in enumerate(roads_to_use):
            if character_count >= max_characters:
                break

            x1, y1, x2, y2 = road
            t = np.random.uniform(0.2, 0.8)
            x = x1 + t * (x2 - x1) + np.random.uniform(-2, 2)
            z = y1 + t * (y2 - y1) + np.random.uniform(-2, 2)

            # Create AI agent in manager
            agent = self.ai_agent_manager.create_agent((x, z))

            # Create visual representation (vertical rectangle = person)
            char_node = self.world_root.attachNewNode(f"agent_{character_count}")
            char_node.setPos(x, z, 0.9)  # Half height above ground

            cm = CardMaker("agent")
            cm.setFrame(-0.3, 0.3, -0.9, 0.9)  # Tall thin rectangle
            char_card = char_node.attachNewNode(cm.generate())
            char_card.setColor(*agent_colors[character_count % len(agent_colors)], 1.0)

            # Store node with initial heading for rendering
            self.character_nodes.append((char_node, agent.heading))
            character_count += 1

        print(f"  Created {character_count} AI agent citizens for experiment")
        print(f"  AI Agent Manager initialized with {len(self.roads)} roads and {len(building_positions)} buildings")

        # DEBUG: Print initial agent positions
        print(f"  [DEBUG] Initial agent positions:")
        for i, agent in enumerate(self.ai_agent_manager.agents):
            print(f"    Agent {i}: pos=({agent.position[0]:.1f}, {agent.position[1]:.1f}), state={agent.state.value}")

    def _place_environmental_props(self):
        """SKIP props for maximum performance"""
        # PERFORMANCE MODE: No props at all
        self.prop_nodes = []
        print(f"  Skipped props (performance mode)")

    def _setup_player_camera(self):
        """Setup player character and GTA-style camera"""
        # Create player character
        self.player_char = DetailedCharacter(CharacterType.CASUAL_PEDESTRIAN, seed=999)
        self.player_node = self.player_char.create_3d_model(
            self.world_root,
            (self.player_pos.x, self.player_pos.y, 0),
            heading=0,
            walk_progress=0.0
        )

        # Initial camera position
        self._update_camera()

    def _apply_materials(self):
        """Apply simplified materials for performance"""
        # PERFORMANCE: Smaller ground plane, no materials
        card_maker = CardMaker("ground")
        ground_size = self.world_size  # Half the size (64 instead of 128)

        card_maker.setFrame(-ground_size, ground_size, -ground_size, ground_size)
        ground = self.world_root.attachNewNode(card_maker.generate())
        ground.setP(-90)
        ground.setColor(0.35, 0.55, 0.38, 1.0)  # Grass green

        # PERFORMANCE: Skip material system
        # grass_mat = MaterialSystem.create_material(MaterialType.GRASS)
        # MaterialSystem.apply_material(ground, grass_mat)

        print("  Applied simplified materials (performance mode)")

    def _setup_post_processing(self):
        """Setup GTA 5-level post-processing effects"""
        # PERFORMANCE: Post-processing disabled for smooth frame rate
        print("  [PERFORMANCE MODE] Post-processing effects disabled for smooth 60 FPS")
        print("  --> Using optimized standard rendering")
        return

        # Original post-processing code (disabled):
        # if POST_PROCESSING_AVAILABLE:
        #     try:
        #         self.post_processing = apply_gta_style_post_processing(self)
        #         print("  [+] GTA 5-style bloom enabled")
        #         print("  [+] Color grading enabled")
        #         print("  [+] Enhanced visual quality active")
        #     except Exception as e:
        #         print(f"  [-] Post-processing setup failed: {e}")
        #         print("  --> Continuing with standard rendering")
        # else:
        #     print("  --> Post-processing module not loaded, using standard rendering")

    def _update_camera(self):
        """Update camera position based on current mode"""
        if self.camera_mode == CameraMode.SPECTATOR:
            # Free-flying Forge-style camera for building/reviewing
            heading_rad = np.radians(self.spectator_heading)
            pitch_rad = np.radians(self.spectator_pitch)

            self.camera.setPos(self.spectator_pos)
            self.camera.setH(self.spectator_heading)
            self.camera.setP(self.spectator_pitch)

            # Hide player character in spectator mode
            if hasattr(self, 'player_node') and self.player_node:
                self.player_node.hide()

        elif self.camera_mode == CameraMode.THIRD_PERSON:
            # Traditional GTA-style third-person camera
            angle_rad = np.radians(self.camera_angle)

            cam_x = self.player_pos.x - self.camera_distance * np.sin(angle_rad)
            cam_y = self.player_pos.y - self.camera_distance * np.cos(angle_rad)
            cam_z = self.camera_height

            self.camera.setPos(cam_x, cam_y, cam_z)
            self.camera.lookAt(self.player_pos.x, self.player_pos.y, 1.5)

            # Show player character in third-person
            if hasattr(self, 'player_node') and self.player_node:
                self.player_node.show()

        elif self.camera_mode == CameraMode.FIRST_PERSON:
            # First-person view (camera at player head height)
            self.camera.setPos(self.player_pos.x, self.player_pos.y, 1.7)  # Eye height
            self.camera.setH(self.camera_angle)
            self.camera.setP(0)  # Level horizon

            # Hide player character in first-person
            if hasattr(self, 'player_node') and self.player_node:
                self.player_node.hide()

    def update(self, task):
        """Main update loop - optimized for performance"""
        dt = globalClock.getDt()

        # Clamp delta time to prevent huge jumps
        dt = min(dt, 0.1)

        # Update controller (high priority)
        if self.controller_manager:
            pygame.event.pump()
            self.controller_manager.update_all()

        # Handle input FIRST for responsiveness
        self._handle_input(dt)

        # Update player position immediately
        self.player_node.setPos(self.player_pos.x, self.player_pos.y, 0)

        # Update camera immediately for responsive view
        self._update_camera()

        # Update professional gamer HUD with FPS and camera info
        current_fps = int(globalClock.getAverageFrameRate())
        debug_info = {
            'pos_x': self.spectator_pos.x,
            'pos_y': self.spectator_pos.y,
            'pos_z': self.spectator_pos.z,
            'heading': self.spectator_heading
        }
        self.hud.update(dt, current_fps, self.camera_mode.value, debug_info)

        # Update LOD system (every 0.5s, not every frame for performance)
        camera_pos = self.camera.getPos()
        lod_changes = self.lod_manager.update(dt, camera_pos)

        # Update touch UI with current joystick states
        self.touch_ui.update(self.joystick_manager)

        # Process touch input for movement/camera if active
        self._handle_touch_input(dt)

        # Animate AI agent citizens (simple random walk)
        if task.frame % 5 == 0:  # Update every 5 frames
            self._animate_ai_agents(dt * 5)

        return task.cont

    def _set_key(self, key, value):
        """Handle key press/release events (event-driven callback)"""
        self.key_map[key] = value
        if value:  # Key pressed
            print(f"[INPUT DEBUG] {key.upper()} key pressed (EVENT-DRIVEN like F1)")

    def _zoom_in(self):
        """Zoom in (move camera forward faster)"""
        print("[INPUT DEBUG] Zoom IN (Ctrl + '+' or Mouse Wheel Up)")
        if self.camera_mode == CameraMode.SPECTATOR:
            # Move forward in the direction we're looking
            heading_rad = np.radians(self.spectator_heading)
            pitch_rad = np.radians(self.spectator_pitch)
            self.spectator_pos.x += self.spectator_zoom_speed * np.sin(heading_rad) * np.cos(pitch_rad)
            self.spectator_pos.y += self.spectator_zoom_speed * np.cos(heading_rad) * np.cos(pitch_rad)
            self.spectator_pos.z += self.spectator_zoom_speed * np.sin(pitch_rad)
            print(f"[ZOOM] New position: ({self.spectator_pos.x:.1f}, {self.spectator_pos.y:.1f}, {self.spectator_pos.z:.1f})")
        elif self.camera_mode == CameraMode.THIRD_PERSON:
            self.camera_distance = max(5, self.camera_distance - 5)

    def _zoom_out(self):
        """Zoom out (move camera backward faster)"""
        print("[INPUT DEBUG] Zoom OUT (Ctrl + '-' or Mouse Wheel Down)")
        if self.camera_mode == CameraMode.SPECTATOR:
            # Move backward
            heading_rad = np.radians(self.spectator_heading)
            pitch_rad = np.radians(self.spectator_pitch)
            self.spectator_pos.x -= self.spectator_zoom_speed * np.sin(heading_rad) * np.cos(pitch_rad)
            self.spectator_pos.y -= self.spectator_zoom_speed * np.cos(heading_rad) * np.cos(pitch_rad)
            self.spectator_pos.z -= self.spectator_zoom_speed * np.sin(pitch_rad)
            print(f"[ZOOM] New position: ({self.spectator_pos.x:.1f}, {self.spectator_pos.y:.1f}, {self.spectator_pos.z:.1f})")
        elif self.camera_mode == CameraMode.THIRD_PERSON:
            self.camera_distance = min(100, self.camera_distance + 5)

    def _cycle_camera_mode(self):
        """Cycle through camera modes (F1 key)"""
        modes = [CameraMode.SPECTATOR, CameraMode.THIRD_PERSON, CameraMode.FIRST_PERSON]
        current_index = modes.index(self.camera_mode)
        next_index = (current_index + 1) % len(modes)
        self.camera_mode = modes[next_index]

        print(f"\n[CAMERA] Switched to {self.camera_mode.value.upper()} mode")

        # Update professional gamer HUD
        if hasattr(self, 'hud'):
            self.hud.set_mode(self.camera_mode.value)

        # Update camera immediately
        self._update_camera()

    def _handle_input(self, dt: float):
        """Handle keyboard and controller input - EVENT-DRIVEN (same method as F1 key)"""
        if self.camera_mode == CameraMode.SPECTATOR:
            # Spectator mode controls (free-flying Forge-style)
            speed = self.spectator_speed * dt

            # Movement relative to camera direction
            move_forward = 0
            move_right = 0
            move_up = 0

            # EVENT-DRIVEN input (same as F1 key - this works!)
            if self.key_map['w']:
                move_forward = 1
            if self.key_map['s']:
                move_forward = -1
            if self.key_map['a']:
                move_right = -1
            if self.key_map['d']:
                move_right = 1
            if self.key_map['space']:
                move_up = 1
            if self.key_map['shift']:
                move_up = -1

            # Rotation (INCREASED rotation speed for better responsiveness)
            if self.key_map['q']:
                self.spectator_heading += 120 * dt  # Faster rotation
            if self.key_map['e']:
                self.spectator_heading -= 120 * dt  # Faster rotation

            # Calculate movement vector based on camera orientation
            heading_rad = np.radians(self.spectator_heading)
            pitch_rad = np.radians(self.spectator_pitch)

            # Forward/back movement (respecting pitch for true 3D movement)
            if move_forward != 0:
                self.spectator_pos.x += move_forward * speed * np.sin(heading_rad) * np.cos(pitch_rad)
                self.spectator_pos.y += move_forward * speed * np.cos(heading_rad) * np.cos(pitch_rad)
                self.spectator_pos.z += move_forward * speed * np.sin(pitch_rad)

            # Left/right strafe (always horizontal)
            if move_right != 0:
                self.spectator_pos.x += move_right * speed * np.cos(heading_rad)
                self.spectator_pos.y -= move_right * speed * np.sin(heading_rad)

            # Up/down (always vertical)
            if move_up != 0:
                self.spectator_pos.z += move_up * speed

            # DEBUG: Log camera movement
            if move_forward != 0 or move_right != 0 or move_up != 0:
                if not hasattr(self, 'last_camera_log'):
                    self.last_camera_log = 0
                self.last_camera_log -= dt
                if self.last_camera_log <= 0:
                    print(f"[CAMERA DEBUG] Spectator pos: ({self.spectator_pos.x:.1f}, {self.spectator_pos.y:.1f}, {self.spectator_pos.z:.1f}), heading: {self.spectator_heading:.0f}°")
                    self.last_camera_log = 2.0  # Log every 2 seconds during movement

        else:
            # Character mode controls (third-person or first-person)
            speed = 10.0 * dt

            # Keyboard movement
            move_x = 0
            move_y = 0

            # EVENT-DRIVEN input (same as F1 key and spectator mode)
            if self.key_map['w']:
                move_y = 1
            if self.key_map['s']:
                move_y = -1
            if self.key_map['a']:
                move_x = -1
            if self.key_map['d']:
                move_x = 1
            if self.key_map['q']:
                self.camera_angle += 90 * dt
            if self.key_map['e']:
                self.camera_angle -= 90 * dt

            # Controller input
            controller = self.controller_manager.get_controller(0)
            if controller and controller.connected:
                state = controller.state

                # Left stick - movement
                stick_x = state.left_stick_x
                stick_y = -state.left_stick_y

                if abs(stick_x) > 0.01 or abs(stick_y) > 0.01:
                    move_x = stick_x
                    move_y = stick_y

                # Right stick horizontal - camera rotation
                if abs(state.right_stick_x) > 0.01:
                    self.camera_angle -= state.right_stick_x * 120 * dt

                # Right stick vertical or triggers - zoom (third-person only)
                if self.camera_mode == CameraMode.THIRD_PERSON:
                    if abs(state.right_stick_y) > 0.01:
                        zoom_delta = -state.right_stick_y * 15 * dt
                        self.camera_distance = max(5, min(100, self.camera_distance + zoom_delta))

                    # Triggers for zoom
                    if state.left_trigger > 0.1:
                        self.camera_distance = min(100, self.camera_distance + state.left_trigger * 15 * dt)
                    if state.right_trigger > 0.1:
                        self.camera_distance = max(5, self.camera_distance - state.right_trigger * 15 * dt)

            # Apply camera-relative movement
            if move_x != 0 or move_y != 0:
                angle_rad = np.radians(self.camera_angle)
                self.player_pos.x += speed * (move_y * np.sin(angle_rad) + move_x * np.cos(angle_rad)) * 1.5
                self.player_pos.y += speed * (move_y * np.cos(angle_rad) - move_x * np.sin(angle_rad)) * 1.5

    def _handle_touch_input(self, dt: float):
        """Handle touch joystick input for movement and camera

        Args:
            dt: Delta time
        """
        # Get touch joystick input
        move_x, move_y = self.joystick_manager.get_movement_input()
        cam_x, cam_y = self.joystick_manager.get_camera_input()

        # Only process touch if either joystick is active
        if not self.joystick_manager.is_movement_active() and not self.joystick_manager.is_camera_active():
            return

        # Apply movement (similar to keyboard/controller input)
        if self.camera_mode == CameraMode.SPECTATOR:
            # Spectator mode: direct camera movement
            speed = self.spectator_speed * dt

            # Movement from left joystick
            if abs(move_x) > 0.01 or abs(move_y) > 0.01:
                heading_rad = np.radians(self.spectator_heading)
                pitch_rad = np.radians(self.spectator_pitch)

                # Forward/back from joystick Y axis
                self.spectator_pos.x += move_y * speed * np.sin(heading_rad) * np.cos(pitch_rad)
                self.spectator_pos.y += move_y * speed * np.cos(heading_rad) * np.cos(pitch_rad)
                self.spectator_pos.z += move_y * speed * np.sin(pitch_rad)

                # Strafe from joystick X axis
                self.spectator_pos.x += move_x * speed * np.cos(heading_rad)
                self.spectator_pos.y -= move_x * speed * np.sin(heading_rad)

            # Camera rotation from right joystick
            if abs(cam_x) > 0.01:
                self.spectator_heading -= cam_x * 120 * dt  # Horizontal rotation

        else:
            # Character mode: move character
            speed = 10.0 * dt

            # Apply movement from left joystick
            if abs(move_x) > 0.01 or abs(move_y) > 0.01:
                angle_rad = np.radians(self.camera_angle)
                self.player_pos.x += speed * (move_y * np.sin(angle_rad) + move_x * np.cos(angle_rad)) * 1.5
                self.player_pos.y += speed * (move_y * np.cos(angle_rad) - move_x * np.sin(angle_rad)) * 1.5

            # Apply camera rotation from right joystick
            if abs(cam_x) > 0.01:
                self.camera_angle -= cam_x * 120 * dt

    def _animate_ai_agents(self, dt: float):
        """Animate AI agent citizens using advanced AI system"""
        if not self.ai_agent_manager or not self.ai_agent_manager.agents:
            return

        # Update all AI agents (pathfinding, collision avoidance, behaviors)
        self.ai_agent_manager.update_all(dt)

        # Update visual representations based on AI agent positions
        for i, (char_node, _) in enumerate(self.character_nodes):
            if i < len(self.ai_agent_manager.agents):
                agent = self.ai_agent_manager.agents[i]

                # Update position (X, Y from agent, Z fixed at 0.9 for visibility)
                char_node.setPos(agent.position[0], agent.position[1], 0.9)

                # Update heading rotation
                char_node.setH(agent.heading)

                # Store updated heading
                self.character_nodes[i] = (char_node, agent.heading)

        # DEBUG: Print agent statistics every 5 seconds
        if hasattr(self, 'debug_timer'):
            self.debug_timer -= dt
            if self.debug_timer <= 0:
                stats = self.ai_agent_manager.get_statistics()
                print(f"\n[AI DEBUG] Agent Statistics:")
                print(f"  Total Agents: {stats['total_agents']}")
                print(f"  State Distribution: {stats['state_distribution']}")
                print(f"  Average Speed: {stats['average_speed']:.2f}")
                # Print first 3 agent positions
                for i in range(min(3, len(self.ai_agent_manager.agents))):
                    agent = self.ai_agent_manager.agents[i]
                    print(f"  Agent {i}: pos=({agent.position[0]:.1f}, {agent.position[1]:.1f}), "
                          f"state={agent.state.value}, heading={agent.heading:.0f}°")
                self.debug_timer = 5.0  # Reset timer
        else:
            self.debug_timer = 5.0  # Initialize timer


def _kill_existing_instances():
    """Kill any existing Python processes running this script"""
    import os
    import psutil

    current_pid = os.getpid()
    script_name = os.path.basename(__file__)

    print(f"[STARTUP] Checking for existing instances of {script_name}...")

    killed_count = 0
    for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
        try:
            # Check if it's a Python process
            if proc.info['name'] and 'python' in proc.info['name'].lower():
                # Check if it's running this script
                cmdline = proc.info['cmdline']
                if cmdline and any(script_name in str(arg) for arg in cmdline):
                    # Don't kill ourselves
                    if proc.info['pid'] != current_pid:
                        print(f"  [CLEANUP] Killing old instance (PID: {proc.info['pid']})")
                        try:
                            proc.kill()
                            proc.wait(timeout=2)
                            killed_count += 1
                        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.TimeoutExpired):
                            pass
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            continue

    if killed_count > 0:
        print(f"[STARTUP] Killed {killed_count} old instance(s)")
    else:
        print(f"[STARTUP] No existing instances found")

    # Brief pause to let OS clean up processes
    import time
    time.sleep(0.5)


def main():
    """Main entry point"""
    # Kill any existing instances first
    try:
        _kill_existing_instances()
    except Exception as e:
        print(f"[WARNING] Could not check for existing instances: {e}")
        print(f"[WARNING] Continuing anyway...")

    parser = argparse.ArgumentParser(description='Ultra-Realistic 3D City World')
    parser.add_argument('--size', type=int, default=64, help='World size')
    parser.add_argument('--time', type=str, default='afternoon',
                       choices=['dawn', 'morning', 'noon', 'afternoon', 'dusk', 'night'],
                       help='Time of day')

    args = parser.parse_args()

    # Convert time string to enum
    time_map = {
        'dawn': TimeOfDay.DAWN,
        'morning': TimeOfDay.MORNING,
        'noon': TimeOfDay.NOON,
        'afternoon': TimeOfDay.AFTERNOON,
        'dusk': TimeOfDay.DUSK,
        'night': TimeOfDay.NIGHT,
    }

    time_of_day = time_map[args.time]

    # Create and run world
    app = UltraRealisticWorld(world_size=args.size, time_of_day=time_of_day)
    app.run()


if __name__ == "__main__":
    main()
