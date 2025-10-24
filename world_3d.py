"""
3D World Rendering Engine - GTA Style
Implements realistic 3D graphics with Panda3D

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from direct.showbase.ShowBase import ShowBase
from panda3d.core import *
from direct.task import Task
from direct.actor.Actor import Actor
from direct.interval.IntervalGlobal import *
import numpy as np
from typing import List, Tuple, Optional, Dict
import sys
import pygame  # For Xbox controller support

from terrain_generator import TerrainGenerator
from city_generator import CityLayoutGenerator, Building, ZoneType
from npc_system import NPCManager, NPC, NPCState
from controller_input import XboxController, ControllerManager


class GTAStyleWorld(ShowBase):
    """
    GTA-style 3D world with realistic graphics.

    Features:
    - Third-person camera system
    - Procedural 3D city blocks
    - Realistic lighting and shadows
    - 3D NPC characters
    - Textured buildings and roads
    """

    def __init__(self, grid_size: int = 64, seed: int = None):
        """Initialize the 3D world"""
        ShowBase.__init__(self)

        print("=" * 80)
        print("AI CITY SIMULATION - 3D GTA STYLE")
        print("Crafted by Intellegix")
        print("=" * 80)
        print()

        self.grid_size = grid_size
        self.seed = seed or np.random.randint(0, 1000000)

        # World components
        self.terrain: Optional[TerrainGenerator] = None
        self.city: Optional[CityLayoutGenerator] = None
        self.npc_manager: Optional[NPCManager] = None

        # 3D scene nodes
        self.world_root = self.render.attachNewNode("world")
        self.building_nodes: List[NodePath] = []
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
            print(f"\n[Controller] {self.controller.name} connected!")
        else:
            print("\n[Controller] No Xbox controller detected - using keyboard")

        # Setup the 3D world
        self._setup_lighting()
        self._setup_camera()
        self._generate_world()
        self._create_3d_scene()
        self._setup_controls()

        # Start update loop
        self.taskMgr.add(self.update_task, "update_world")

        print("\n3D World ready! Use WASD or Xbox Controller to move")
        print("Press ESC to exit")

    def _setup_lighting(self):
        """Setup realistic GTA-style lighting"""
        print("Setting up realistic lighting...")

        # Ambient light (soft global illumination)
        ambient = AmbientLight("ambient")
        ambient.setColor((0.3, 0.3, 0.35, 1))
        ambient_np = self.render.attachNewNode(ambient)
        self.render.setLight(ambient_np)

        # Directional sun light (key light)
        sun = DirectionalLight("sun")
        sun.setColor((1.0, 0.95, 0.8, 1))  # Warm sunlight
        sun.setShadowCaster(True, 2048, 2048)  # Enable shadows
        sun_np = self.render.attachNewNode(sun)
        sun_np.setHpr(-60, -45, 0)  # Sun angle
        self.render.setLight(sun_np)

        # Sky blue fill light
        fill = DirectionalLight("fill")
        fill.setColor((0.2, 0.25, 0.35, 1))  # Blue sky bounce
        fill_np = self.render.attachNewNode(fill)
        fill_np.setHpr(120, -30, 0)
        self.render.setLight(fill_np)

        # Enable shadows
        self.render.setShaderAuto()

        # Fog for atmosphere (like GTA)
        fog = Fog("distance_fog")
        fog.setColor(0.7, 0.75, 0.8)
        fog.setExpDensity(0.005)
        self.render.setFog(fog)

        print("[OK] Lighting system initialized")

    def _setup_camera(self):
        """Setup third-person GTA-style camera"""
        print("Setting up third-person camera...")

        # Disable default camera control
        self.disableMouse()

        # Set initial camera position
        self.camera.setPos(0, -self.camera_distance, self.camera_height)
        self.camera.lookAt(0, 0, 2)

        print("[OK] Camera system ready")

    def _generate_world(self):
        """Generate the procedural world"""
        print("\nGenerating 3D world...")
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
        print(f"[OK] City generated ({len(self.city.buildings)} buildings)")

        # Spawn NPCs
        print("\n[Phase 3: NPCs]")
        self.npc_manager = NPCManager(self.city)
        self.npc_manager.spawn_random_npcs(10)  # Start with fewer NPCs for 3D
        print(f"[OK] {len(self.npc_manager.npcs)} NPCs spawned")

    def _create_3d_scene(self):
        """Create the 3D scene from generated data"""
        print("\n[Phase 4: Building 3D Scene]")

        # Create ground plane
        self._create_ground()

        # Create buildings
        self._create_buildings()

        # Create roads
        self._create_roads()

        # Create NPCs
        self._create_npcs()

        # Create player representation
        self._create_player()

        print("[OK] 3D scene constructed")

    def _create_ground(self):
        """Create terrain ground plane"""
        # Create a simple ground plane
        ground = self.loader.loadModel("models/misc/smiley")  # Placeholder
        if ground:
            ground.reparentTo(self.world_root)
            ground.setScale(self.grid_size * 0.5)
            ground.setPos(0, 0, -1)
            ground.setColor(0.3, 0.5, 0.3, 1)  # Green grass

    def _create_buildings(self):
        """Create 3D buildings procedurally"""
        print("Creating 3D buildings...")

        card_maker = CardMaker("building")

        for i, building in enumerate(self.city.buildings[:50]):  # Limit for performance
            # Convert grid coordinates to 3D world coordinates
            x = (building.x - self.grid_size / 2) * 2.0
            y = (building.y - self.grid_size / 2) * 2.0

            # Create building geometry
            height = building.height * 2.0
            width = building.width * 1.5
            depth = building.depth * 1.5

            # Create box for building
            building_node = self.world_root.attachNewNode(f"building_{i}")
            building_node.setPos(x, y, height / 2)

            # Front face
            card_maker.setFrame(-width/2, width/2, -height/2, height/2)
            front = building_node.attachNewNode(card_maker.generate())
            front.setY(-depth/2)
            front.setColor(self._get_building_color(building))

            # Back face
            back = building_node.attachNewNode(card_maker.generate())
            back.setY(depth/2)
            back.setH(180)
            back.setColor(self._get_building_color(building))

            # Left face
            card_maker.setFrame(-depth/2, depth/2, -height/2, height/2)
            left = building_node.attachNewNode(card_maker.generate())
            left.setX(-width/2)
            left.setH(90)
            left.setColor(self._get_building_color(building))

            # Right face
            right = building_node.attachNewNode(card_maker.generate())
            right.setX(width/2)
            right.setH(-90)
            right.setColor(self._get_building_color(building))

            # Top face (roof)
            card_maker.setFrame(-width/2, width/2, -depth/2, depth/2)
            top = building_node.attachNewNode(card_maker.generate())
            top.setZ(height/2)
            top.setP(-90)
            top.setColor(self._get_roof_color(building))

            self.building_nodes.append(building_node)

        print(f"[OK] Created {len(self.building_nodes)} buildings")

    def _get_building_color(self, building: Building) -> Tuple[float, float, float, float]:
        """Get realistic building color based on zone type"""
        if building.zone_type == ZoneType.COMMERCIAL:
            # Glass and steel - blue tinted
            return (0.6, 0.65, 0.75, 1.0)
        elif building.zone_type == ZoneType.RESIDENTIAL:
            # Warm beige/tan
            colors = [
                (0.85, 0.8, 0.7, 1.0),
                (0.9, 0.85, 0.75, 1.0),
                (0.8, 0.75, 0.65, 1.0),
            ]
            return colors[building.id % len(colors)]
        elif building.zone_type == ZoneType.INDUSTRIAL:
            # Gray concrete
            return (0.5, 0.52, 0.55, 1.0)
        else:
            # Default
            return (0.7, 0.7, 0.7, 1.0)

    def _get_roof_color(self, building: Building) -> Tuple[float, float, float, float]:
        """Get roof color"""
        return (0.3, 0.3, 0.35, 1.0)  # Dark roof

    def _create_roads(self):
        """Create road system"""
        print("Creating road network...")

        card_maker = CardMaker("road")
        road_node = self.world_root.attachNewNode("roads")

        # Create roads from road grid
        road_cells = np.argwhere(self.city.road_grid)

        for i, (y, x) in enumerate(road_cells[::4]):  # Sample every 4th for performance
            world_x = (x - self.grid_size / 2) * 2.0
            world_y = (y - self.grid_size / 2) * 2.0

            card_maker.setFrame(-1, 1, -1, 1)
            road_segment = road_node.attachNewNode(card_maker.generate())
            road_segment.setPos(world_x, world_y, 0.01)
            road_segment.setP(-90)
            road_segment.setColor(0.15, 0.15, 0.17, 1.0)  # Asphalt

        print("[OK] Road network created")

    def _create_npcs(self):
        """Create 3D NPC characters"""
        print("Creating 3D NPCs...")

        for npc in self.npc_manager.npcs:
            # Create simple box character
            npc_node = self.loader.loadModel("models/misc/smiley")  # Placeholder
            if npc_node:
                npc_node.reparentTo(self.world_root)
                npc_node.setScale(0.5, 0.5, 1.0)  # Human proportions
                npc_node.setColor(0.2, 0.4, 0.8, 1.0)  # Blue character

                # Position NPC
                world_x = (npc.position[0] - self.grid_size / 2) * 2.0
                world_y = (npc.position[1] - self.grid_size / 2) * 2.0
                npc_node.setPos(world_x, world_y, 0.5)

                self.npc_nodes[npc.id] = npc_node

        print(f"[OK] Created {len(self.npc_nodes)} NPC models")

    def _create_player(self):
        """Create player character (camera follow target)"""
        # Create a simple player indicator
        self.player_node = self.loader.loadModel("models/misc/smiley")
        if self.player_node:
            self.player_node.reparentTo(self.world_root)
            self.player_node.setScale(0.7, 0.7, 1.5)
            self.player_node.setColor(1.0, 0.3, 0.3, 1.0)  # Red player
            self.player_node.setPos(0, 0, 0.75)

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
            pygame.event.pump()  # Process pygame events
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
        """Update player position based on input (keyboard + controller)"""
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

        # Xbox Controller movement (Left Stick)
        if self.controller and self.controller.connected:
            state = self.controller.state

            # Left stick for movement (GTA style)
            stick_x = state.left_stick_x
            stick_y = -state.left_stick_y  # Invert Y for forward/back

            if abs(stick_x) > 0.01 or abs(stick_y) > 0.01:
                # Move relative to camera angle
                pos.x += speed * (stick_y * np.sin(angle_rad) + stick_x * np.cos(angle_rad)) * 1.5
                pos.y += speed * (stick_y * np.cos(angle_rad) - stick_x * np.sin(angle_rad)) * 1.5

        self.player_node.setPos(pos)
        self.follow_target_pos = pos

    def _update_camera(self, dt: float):
        """Update third-person camera position (keyboard + controller)"""
        # Keyboard camera rotation
        if self.keys["cam_left"]:
            self.camera_angle += 90 * dt
        if self.keys["cam_right"]:
            self.camera_angle -= 90 * dt

        # Xbox Controller camera control
        if self.controller and self.controller.connected:
            state = self.controller.state

            # Right stick horizontal for camera rotation (like GTA)
            stick_x = state.right_stick_x
            if abs(stick_x) > 0.01:
                self.camera_angle -= stick_x * 120 * dt  # Smooth rotation

            # Right stick vertical for zoom (or triggers)
            stick_y = state.right_stick_y
            if abs(stick_y) > 0.01:
                zoom_delta = -stick_y * 15 * dt
                self.camera_distance = max(5.0, min(30.0, self.camera_distance + zoom_delta))

            # Triggers for zoom (LT = zoom out, RT = zoom in)
            if state.left_trigger > 0.1:
                self.camera_distance = min(30.0, self.camera_distance + state.left_trigger * 10 * dt)
            if state.right_trigger > 0.1:
                self.camera_distance = max(5.0, self.camera_distance - state.right_trigger * 10 * dt)

            # Bumpers for discrete zoom
            if state.left_bumper:
                self.zoom_camera(3 * dt * 60)  # Zoom out
            if state.right_bumper:
                self.zoom_camera(-3 * dt * 60)  # Zoom in

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
                world_y = (npc.position[1] - self.grid_size / 2) * 2.0
                node.setPos(world_x, world_y, 0.5)


if __name__ == "__main__":
    """Launch 3D GTA-style world"""
    import argparse

    parser = argparse.ArgumentParser(description="AI City Simulation - 3D GTA Style")
    parser.add_argument("--size", type=int, default=64, choices=[32, 64, 128],
                       help="World size (default: 64)")
    parser.add_argument("--seed", type=int, default=None,
                       help="Random seed")

    args = parser.parse_args()

    # Create and run 3D world
    world = GTAStyleWorld(grid_size=args.size, seed=args.seed)
    world.run()
