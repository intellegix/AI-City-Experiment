"""
Enhanced 3D World - GTA Style with Procedural Systems
Integrates all modular systems for maximum variety

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
import numpy as np
from typing import List, Tuple, Optional, Dict
import sys
import pygame  # For Xbox controller support

from terrain_generator import TerrainGenerator
from city_generator import CityLayoutGenerator, Building, ZoneType
from npc_system import NPCManager, NPC, NPCState
from controller_input import XboxController, ControllerManager
from procedural_buildings import ProceduralBuilding
from vehicle_system import VehicleSpawner, VehicleType


class EnhancedGTAWorld(ShowBase):
    """
    Enhanced GTA-style 3D world with full modular systems.

    Features:
    - Procedural buildings (12,000+ combinations)
    - 11 vehicle types (165+ variations)
    - Third-person GTA camera
    - Xbox controller support
    - Realistic lighting and shadows
    - AI-driven NPCs
    """

    def __init__(self, grid_size: int = 64, seed: int = None):
        """Initialize the enhanced 3D world"""
        ShowBase.__init__(self)

        print("=" * 80)
        print("AI CITY SIMULATION - ENHANCED 3D GTA STYLE")
        print("Crafted by Intellegix")
        print("=" * 80)
        print()
        print("Features:")
        print("  - Procedural buildings with infinite variety")
        print("  - 11 vehicle types with color variations")
        print("  - Xbox controller support")
        print("  - Third-person GTA camera")
        print("  - Realistic lighting & shadows")
        print()

        self.grid_size = grid_size
        self.seed = seed or np.random.randint(0, 1000000)

        # World components
        self.terrain: Optional[TerrainGenerator] = None
        self.city: Optional[CityLayoutGenerator] = None
        self.npc_manager: Optional[NPCManager] = None

        # Enhanced systems
        self.vehicle_spawner = VehicleSpawner()

        # 3D scene nodes
        self.world_root = self.render.attachNewNode("world")
        self.building_nodes: List[NodePath] = []
        self.vehicle_nodes: List[NodePath] = []
        self.npc_nodes: Dict[int, NodePath] = {}
        self.player_node: Optional[NodePath] = None

        # Camera state
        self.camera_distance = 15.0
        self.camera_height = 8.0
        self.camera_angle = 45.0  # degrees
        self.follow_target_pos = LVector3(0, 0, 0)

        # Xbox Controller support
        pygame.init()
        pygame.joystick.init()
        self.controller_manager = ControllerManager()
        self.controller = None
        if self.controller_manager.controllers:
            self.controller = self.controller_manager.controllers[0]
            print(f"[Controller] {self.controller.name} connected!")
        else:
            print("[Controller] No Xbox controller detected - using keyboard")

        # Setup the 3D world
        self._setup_lighting()
        self._setup_camera()
        self._generate_world()
        self._create_enhanced_scene()
        self._setup_controls()

        # Start update loop
        self.taskMgr.add(self.update_task, "update_world")

        print("\n" + "=" * 80)
        print("ENHANCED 3D WORLD READY!")
        print("=" * 80)
        print("\nControls:")
        print("  WASD / Left Stick  - Move player")
        print("  Q/E / Right Stick  - Rotate camera")
        print("  Triggers/Bumpers   - Zoom")
        print("  ESC                - Exit")
        print()

    def _setup_lighting(self):
        """Setup realistic GTA-style lighting"""
        print("Setting up realistic lighting...")

        # Ambient light
        ambient = AmbientLight("ambient")
        ambient.setColor((0.3, 0.3, 0.35, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        # Directional sun light
        sun = DirectionalLight("sun")
        sun.setColor((1.0, 0.95, 0.8, 1))
        sun.setShadowCaster(True, 2048, 2048)
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(-60, -45, 0)
        self.render.setLight(sun_np)

        # Sky blue fill light
        fill = DirectionalLight("fill")
        fill.setColor((0.2, 0.25, 0.35, 1))
        fill_np = self.render.attachNewNode(fill)
        fill_np.setHpr(120, -30, 0)
        self.render.setLight(fill_np)

        # Enable shadows
        self.render.setShaderAuto()

        # Fog for atmosphere
        fog = Fog("distance_fog")
        fog.setColor(0.7, 0.75, 0.8)
        fog.setExpDensity(0.005)
        self.render.setFog(fog)

        print("[OK] Lighting system initialized")

    def _setup_camera(self):
        """Setup third-person GTA-style camera"""
        print("Setting up third-person camera...")
        self.disableMouse()
        self.camera.setPos(0, -self.camera_distance, self.camera_height)
        self.camera.lookAt(0, 0, 2)
        print("[OK] Camera system ready")

    def _generate_world(self):
        """Generate the procedural world"""
        print("\nGenerating enhanced 3D world...")
        print(f"Grid size: {self.grid_size}x{self.grid_size}")
        print(f"Seed: {self.seed}")

        # Generate terrain
        print("\n[Phase 1: Terrain Generation]")
        self.terrain = TerrainGenerator(size=self.grid_size, seed=self.seed)
        self.terrain.generate()
        print("[OK] Terrain generated")

        # Generate city layout
        print("\n[Phase 2: City Layout]")
        self.city = CityLayoutGenerator(self.terrain, seed=self.seed)
        self.city.generate()
        print(f"[OK] City layout generated")

        # Spawn NPCs
        print("\n[Phase 3: NPCs]")
        self.npc_manager = NPCManager(self.city)
        self.npc_manager.spawn_random_npcs(10)
        print(f"[OK] {len(self.npc_manager.npcs)} NPCs spawned")

    def _create_enhanced_scene(self):
        """Create the enhanced 3D scene with procedural systems"""
        print("\n[Phase 4: Building Enhanced 3D Scene]")

        # Create ground
        self._create_ground()

        # Create procedural buildings
        self._create_procedural_buildings()

        # Create roads
        self._create_roads()

        # Spawn vehicles
        self._spawn_vehicles()

        # Create NPCs
        self._create_npcs()

        # Create player
        self._create_player()

        print("[OK] Enhanced 3D scene constructed")

    def _create_ground(self):
        """Create terrain ground plane"""
        card_maker = CardMaker("ground")
        size = self.grid_size * 2.0

        card_maker.setFrame(-size, size, -size, size)
        ground = self.world_root.attachNewNode(card_maker.generate())
        ground.setP(-90)
        ground.setZ(-0.1)
        ground.setColor(0.3, 0.5, 0.3, 1)  # Green grass

    def _create_procedural_buildings(self):
        """Create buildings using procedural system"""
        print("Creating procedural buildings...")

        # Get buildable positions from city
        building_count = 0
        max_buildings = 50  # Limit for performance

        # Generate buildings in zones around center
        zones = [
            (0, 0, ZoneType.COMMERCIAL),
            (30, 30, ZoneType.RESIDENTIAL),
            (-30, 30, ZoneType.RESIDENTIAL),
            (30, -30, ZoneType.INDUSTRIAL),
            (-30, -30, ZoneType.RESIDENTIAL),
        ]

        for base_x, base_z, zone_type in zones:
            for i in range(int(max_buildings / len(zones))):
                # Random position in zone
                offset_x = np.random.uniform(-20, 20)
                offset_z = np.random.uniform(-20, 20)

                world_x = base_x + offset_x
                world_z = base_z + offset_z

                # Create procedural building
                building_seed = self.seed + building_count
                building = ProceduralBuilding(zone_type, seed=building_seed)

                # Create 3D model
                building_node = building.create_3d_model(
                    self.world_root,
                    (world_x, world_z, 0)
                )

                self.building_nodes.append(building_node)
                building_count += 1

        print(f"[OK] Created {len(self.building_nodes)} procedural buildings")

    def _create_roads(self):
        """Create road network"""
        print("Creating road network...")

        card_maker = CardMaker("road")
        road_node = self.world_root.attachNewNode("roads")

        # Create main roads
        road_width = 12
        road_length = self.grid_size * 2.0

        # Horizontal road
        card_maker.setFrame(-road_length, road_length, -road_width/2, road_width/2)
        h_road = road_node.attachNewNode(card_maker.generate())
        h_road.setP(-90)
        h_road.setZ(0.01)
        h_road.setColor(0.15, 0.15, 0.17, 1.0)  # Asphalt

        # Vertical road
        card_maker.setFrame(-road_width/2, road_width/2, -road_length, road_length)
        v_road = road_node.attachNewNode(card_maker.generate())
        v_road.setP(-90)
        v_road.setZ(0.01)
        v_road.setColor(0.15, 0.15, 0.17, 1.0)

        print("[OK] Road network created")

    def _spawn_vehicles(self):
        """Spawn vehicles using vehicle system"""
        print("Spawning vehicles...")

        vehicle_count = 30  # Number of parked vehicles

        for i in range(vehicle_count):
            # Random parking spot along roads
            if np.random.random() > 0.5:
                # Horizontal road parking
                x = np.random.uniform(-self.grid_size, self.grid_size)
                z = 8 if np.random.random() > 0.5 else -8
                heading = 90 if z > 0 else -90
            else:
                # Vertical road parking
                x = 8 if np.random.random() > 0.5 else -8
                z = np.random.uniform(-self.grid_size, self.grid_size)
                heading = 0 if x > 0 else 180

            # Spawn random vehicle
            vehicle = self.vehicle_spawner.spawn_random_vehicle(
                self.world_root,
                (x, z, 0),
                heading
            )

            self.vehicle_nodes.append(vehicle)

        print(f"[OK] Spawned {len(self.vehicle_nodes)} vehicles")

    def _create_npcs(self):
        """Create 3D NPC characters"""
        print("Creating 3D NPCs...")

        for npc in self.npc_manager.npcs:
            # Create simple character model
            card_maker = CardMaker("npc")
            card_maker.setFrame(-0.3, 0.3, 0, 1.8)  # Human height

            npc_node = self.world_root.attachNewNode(f"npc_{npc.id}")

            # Front
            front = npc_node.attachNewNode(card_maker.generate())
            front.setY(-0.15)
            front.setColor(0.2, 0.4, 0.8, 1.0)

            # Back
            back = npc_node.attachNewNode(card_maker.generate())
            back.setY(0.15)
            back.setH(180)
            back.setColor(0.2, 0.4, 0.8, 1.0)

            # Position NPC
            world_x = (npc.position[0] - self.grid_size / 2) * 2.0
            world_z = (npc.position[1] - self.grid_size / 2) * 2.0
            npc_node.setPos(world_x, world_z, 0)

            self.npc_nodes[npc.id] = npc_node

        print(f"[OK] Created {len(self.npc_nodes)} NPC models")

    def _create_player(self):
        """Create player character"""
        card_maker = CardMaker("player")
        card_maker.setFrame(-0.4, 0.4, 0, 1.8)

        self.player_node = self.world_root.attachNewNode("player")

        # Front
        front = self.player_node.attachNewNode(card_maker.generate())
        front.setY(-0.2)
        front.setColor(1.0, 0.3, 0.3, 1.0)  # Red player

        # Back
        back = self.player_node.attachNewNode(card_maker.generate())
        back.setY(0.2)
        back.setH(180)
        back.setColor(1.0, 0.3, 0.3, 1.0)

        self.player_node.setPos(0, 0, 0)
        self.follow_target_pos = self.player_node.getPos()

    def _setup_controls(self):
        """Setup keyboard and mouse controls"""
        # Movement keys
        self.accept("w", self.set_key, ["forward", True])
        self.accept("w-up", self.set_key, ["forward", False])
        self.accept("s", self.set_key, ["backward", True])
        self.accept("s-up", self.set_key, ["backward", False])
        self.accept("a", self.set_key, ["left", True])
        self.accept("a-up", self.set_key, ["left", False])
        self.accept("d", self.set_key, ["right", True])
        self.accept("d-up", self.set_key, ["right", False])

        # Camera keys
        self.accept("q", self.set_key, ["cam_left", True])
        self.accept("q-up", self.set_key, ["cam_left", False])
        self.accept("e", self.set_key, ["cam_right", True])
        self.accept("e-up", self.set_key, ["cam_right", False])

        # Zoom
        self.accept("wheel_up", self.zoom_camera, [-2])
        self.accept("wheel_down", self.zoom_camera, [2])

        # Exit
        self.accept("escape", sys.exit)

        # Key state
        self.keys = {
            "forward": False,
            "backward": False,
            "left": False,
            "right": False,
            "cam_left": False,
            "cam_right": False,
        }

    def set_key(self, key: str, value: bool):
        """Set key state"""
        self.keys[key] = value

    def zoom_camera(self, delta: float):
        """Zoom camera in/out"""
        self.camera_distance = max(5.0, min(30.0, self.camera_distance + delta))

    def update_task(self, task):
        """Main update loop"""
        dt = globalClock.getDt()

        # Poll Xbox controller input
        if self.controller:
            pygame.event.pump()
            self.controller_manager.update_all()

        # Update player movement
        self._update_player(dt)

        # Update NPCs
        if self.npc_manager:
            self.npc_manager.update_all(dt)
            self._update_npc_positions()

        # Update camera
        self._update_camera(dt)

        return Task.cont

    def _update_player(self, dt: float):
        """Update player position based on input"""
        if not self.player_node:
            return

        speed = 10.0 * dt
        pos = self.player_node.getPos()

        # Calculate movement based on camera angle
        angle_rad = np.radians(self.camera_angle)

        # Keyboard movement
        if self.keys["forward"]:
            pos.x += speed * np.sin(angle_rad)
            pos.y += speed * np.cos(angle_rad)
        if self.keys["backward"]:
            pos.x -= speed * np.sin(angle_rad)
            pos.y -= speed * np.cos(angle_rad)
        if self.keys["left"]:
            pos.x -= speed * np.cos(angle_rad)
            pos.y += speed * np.sin(angle_rad)
        if self.keys["right"]:
            pos.x += speed * np.cos(angle_rad)
            pos.y -= speed * np.sin(angle_rad)

        # Xbox Controller movement
        if self.controller and self.controller.connected:
            state = self.controller.state
            stick_x = state.left_stick_x
            stick_y = -state.left_stick_y

            if abs(stick_x) > 0.01 or abs(stick_y) > 0.01:
                pos.x += speed * (stick_y * np.sin(angle_rad) + stick_x * np.cos(angle_rad)) * 1.5
                pos.y += speed * (stick_y * np.cos(angle_rad) - stick_x * np.sin(angle_rad)) * 1.5

        self.player_node.setPos(pos)
        self.follow_target_pos = pos

    def _update_camera(self, dt: float):
        """Update third-person camera position"""
        # Keyboard camera rotation
        if self.keys["cam_left"]:
            self.camera_angle += 90 * dt
        if self.keys["cam_right"]:
            self.camera_angle -= 90 * dt

        # Xbox Controller camera control
        if self.controller and self.controller.connected:
            state = self.controller.state

            # Right stick for camera
            stick_x = state.right_stick_x
            if abs(stick_x) > 0.01:
                self.camera_angle -= stick_x * 120 * dt

            # Triggers for zoom
            if state.left_trigger > 0.1:
                self.camera_distance = min(30.0, self.camera_distance + state.left_trigger * 10 * dt)
            if state.right_trigger > 0.1:
                self.camera_distance = max(5.0, self.camera_distance - state.right_trigger * 10 * dt)

        # Calculate camera position
        angle_rad = np.radians(self.camera_angle)
        cam_x = self.follow_target_pos.x - self.camera_distance * np.sin(angle_rad)
        cam_y = self.follow_target_pos.y - self.camera_distance * np.cos(angle_rad)
        cam_z = self.follow_target_pos.z + self.camera_height

        # Smooth camera movement
        current_pos = self.camera.getPos()
        new_pos = LVector3(cam_x, cam_y, cam_z)
        lerp_pos = current_pos + (new_pos - current_pos) * min(1.0, dt * 5.0)

        self.camera.setPos(lerp_pos)
        self.camera.lookAt(self.follow_target_pos.x, self.follow_target_pos.y,
                          self.follow_target_pos.z + 2)

    def _update_npc_positions(self):
        """Update NPC 3D positions from simulation"""
        for npc in self.npc_manager.npcs:
            if npc.id in self.npc_nodes:
                node = self.npc_nodes[npc.id]
                world_x = (npc.position[0] - self.grid_size / 2) * 2.0
                world_z = (npc.position[1] - self.grid_size / 2) * 2.0
                node.setPos(world_x, world_z, 0)


if __name__ == "__main__":
    """Launch enhanced 3D GTA-style world"""
    import argparse

    parser = argparse.ArgumentParser(description="AI City Simulation - Enhanced 3D GTA Style")
    parser.add_argument("--size", type=int, default=64, choices=[32, 64, 128],
                       help="World size (default: 64)")
    parser.add_argument("--seed", type=int, default=None,
                       help="Random seed")

    args = parser.parse_args()

    # Create and run enhanced 3D world
    world = EnhancedGTAWorld(grid_size=args.size, seed=args.seed)
    world.run()
