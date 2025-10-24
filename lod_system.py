"""
LOD (Level of Detail) System for Performance Optimization

Manages 3 LOD levels + distance culling to significantly improve FPS:
- LOD_HIGH (0-60m): Full detail, all geometry visible
- LOD_MED (60-150m): Medium detail, reduced geometry
- LOD_LOW (150-400m): Low detail, simple shapes only
- CULLED (>600m): Objects hidden completely

Optimized for AMD Radeon 780M integrated graphics.

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""

from enum import Enum
from typing import List, Tuple, Dict
from panda3d.core import NodePath, Vec3
import numpy as np


class LODLevel(Enum):
    """LOD detail levels"""
    HIGH = 0    # 0-60m: Full detail
    MED = 1     # 60-150m: Medium detail
    LOW = 2     # 150-400m: Low detail
    CULLED = 3  # >600m: Hidden


class LODConfig:
    """LOD distance thresholds (from config.py)"""
    LOD_HIGH_DISTANCE: float = 60.0   # Full detail up to 60m
    LOD_MED_DISTANCE: float = 150.0   # Medium detail 60-150m
    LOD_LOW_DISTANCE: float = 400.0   # Low detail 150-400m
    LOD_CULL_DISTANCE: float = 600.0  # Cull objects beyond 600m


class LODObject:
    """Represents an object with multiple LOD levels"""

    def __init__(self, node: NodePath, position: Tuple[float, float, float]):
        """Initialize LOD object

        Args:
            node: Root node containing all LOD levels
            position: World position (x, y, z)
        """
        self.node = node
        self.position = Vec3(*position)
        self.current_lod = LODLevel.CULLED

        # LOD nodes (to be set by subclasses)
        self.lod_nodes: Dict[LODLevel, NodePath] = {}

    def update_lod(self, camera_pos: Vec3) -> bool:
        """Update LOD based on distance from camera

        Args:
            camera_pos: Camera position

        Returns:
            True if LOD changed, False otherwise
        """
        distance = (self.position - camera_pos).length()

        # Determine LOD level based on distance
        if distance <= LODConfig.LOD_HIGH_DISTANCE:
            target_lod = LODLevel.HIGH
        elif distance <= LODConfig.LOD_MED_DISTANCE:
            target_lod = LODLevel.MED
        elif distance <= LODConfig.LOD_LOW_DISTANCE:
            target_lod = LODLevel.LOW
        elif distance <= LODConfig.LOD_CULL_DISTANCE:
            target_lod = LODLevel.LOW  # Keep showing low detail until cull distance
        else:
            target_lod = LODLevel.CULLED

        # Only update if LOD changed
        if target_lod != self.current_lod:
            self._switch_lod(target_lod)
            self.current_lod = target_lod
            return True

        return False

    def _switch_lod(self, new_lod: LODLevel):
        """Switch to a different LOD level

        Args:
            new_lod: Target LOD level
        """
        # Hide all LOD nodes first
        for lod_node in self.lod_nodes.values():
            if lod_node:
                lod_node.hide()

        # Show only the target LOD
        if new_lod in self.lod_nodes and self.lod_nodes[new_lod]:
            self.lod_nodes[new_lod].show()
        elif new_lod == LODLevel.CULLED:
            # All nodes hidden (culled)
            pass


class LODManager:
    """Manages LOD updates for all objects in the scene"""

    def __init__(self):
        """Initialize LOD manager"""
        self.objects: List[LODObject] = []
        self.update_interval = 0.5  # Update LOD every 0.5 seconds (not every frame)
        self.time_since_update = 0.0

        # Statistics
        self.stats = {
            'total_objects': 0,
            'lod_high': 0,
            'lod_med': 0,
            'lod_low': 0,
            'lod_culled': 0
        }

    def register_object(self, obj: LODObject):
        """Register an object for LOD management

        Args:
            obj: LOD object to manage
        """
        self.objects.append(obj)
        self.stats['total_objects'] = len(self.objects)

    def update(self, dt: float, camera_pos: Vec3) -> int:
        """Update LOD for all objects

        Args:
            dt: Delta time since last frame
            camera_pos: Camera position

        Returns:
            Number of objects that changed LOD this frame
        """
        self.time_since_update += dt

        # Only update every N seconds to reduce overhead
        if self.time_since_update < self.update_interval:
            return 0

        self.time_since_update = 0.0

        # Reset statistics
        self.stats['lod_high'] = 0
        self.stats['lod_med'] = 0
        self.stats['lod_low'] = 0
        self.stats['lod_culled'] = 0

        # Update all objects
        changed_count = 0
        for obj in self.objects:
            if obj.update_lod(camera_pos):
                changed_count += 1

            # Update statistics
            if obj.current_lod == LODLevel.HIGH:
                self.stats['lod_high'] += 1
            elif obj.current_lod == LODLevel.MED:
                self.stats['lod_med'] += 1
            elif obj.current_lod == LODLevel.LOW:
                self.stats['lod_low'] += 1
            else:
                self.stats['lod_culled'] += 1

        return changed_count

    def get_statistics(self) -> Dict[str, int]:
        """Get LOD statistics

        Returns:
            Dictionary with LOD statistics
        """
        return self.stats.copy()


class SimpleBuildingLOD(LODObject):
    """Building with 3 LOD levels"""

    def __init__(self, node: NodePath, position: Tuple[float, float, float],
                 width: float, depth: float, height: float, color: Tuple[float, float, float]):
        """Initialize building LOD

        Args:
            node: Root node for building
            position: World position
            width: Building width
            depth: Building depth
            height: Building height
            color: Building color (RGB)
        """
        super().__init__(node, position)

        # Create LOD nodes
        from panda3d.core import CardMaker

        # LOD HIGH: 4 walls (full detail)
        high_node = node.attachNewNode("lod_high")
        cm = CardMaker("wall")

        # Front wall
        cm.setFrame(-width/2, width/2, 0, height)
        front = high_node.attachNewNode(cm.generate())
        front.setY(depth/2)
        front.setColor(*color, 1.0)

        # Back wall
        back = high_node.attachNewNode(cm.generate())
        back.setY(-depth/2)
        back.setH(180)
        back.setColor(*color, 1.0)

        # Left wall
        cm.setFrame(-depth/2, depth/2, 0, height)
        left = high_node.attachNewNode(cm.generate())
        left.setX(-width/2)
        left.setH(90)
        left.setColor(*color, 1.0)

        # Right wall
        right = high_node.attachNewNode(cm.generate())
        right.setX(width/2)
        right.setH(-90)
        right.setColor(*color, 1.0)

        # LOD MED: 2 walls (front and back only)
        med_node = node.attachNewNode("lod_med")
        cm2 = CardMaker("wall_med")
        cm2.setFrame(-width/2, width/2, 0, height)

        front_med = med_node.attachNewNode(cm2.generate())
        front_med.setY(depth/2)
        front_med.setColor(*color, 1.0)

        back_med = med_node.attachNewNode(cm2.generate())
        back_med.setY(-depth/2)
        back_med.setH(180)
        back_med.setColor(*color, 1.0)

        # LOD LOW: 1 billboard (simple card facing camera)
        low_node = node.attachNewNode("lod_low")
        cm3 = CardMaker("billboard")
        cm3.setFrame(-width/2, width/2, 0, height * 0.8)  # Slightly shorter

        billboard = low_node.attachNewNode(cm3.generate())
        billboard.setColor(*color, 0.8)  # Slightly transparent
        billboard.setBillboardPointEye()  # Always face camera

        # Register LOD nodes
        self.lod_nodes = {
            LODLevel.HIGH: high_node,
            LODLevel.MED: med_node,
            LODLevel.LOW: low_node
        }

        # Start with all hidden
        for lod_node in self.lod_nodes.values():
            lod_node.hide()


# Utility function for easy integration
def create_lod_building(world_root: NodePath, position: Tuple[float, float, float],
                       width: float, depth: float, height: float,
                       color: Tuple[float, float, float]) -> SimpleBuildingLOD:
    """Create a building with LOD support

    Args:
        world_root: Parent node
        position: World position
        width: Building width
        depth: Building depth
        height: Building height
        color: Building color (RGB)

    Returns:
        SimpleBuildingLOD object
    """
    node = world_root.attachNewNode(f"building_lod_{position[0]}_{position[1]}")
    node.setPos(*position)

    return SimpleBuildingLOD(node, position, width, depth, height, color)
