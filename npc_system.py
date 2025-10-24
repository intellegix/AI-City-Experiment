"""
Advanced NPC System with Emergent AI Behaviors
Implements Phase 4: NPC Framework & Emergent AI

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import time

from config import NPC as NPC_CONFIG, Config
from ai_behavior import (
    BehaviorTree, Blackboard, Sequence, Selector, Action,
    Condition, NodeStatus, UtilityAI
)
from pathfinding import AStar, PathSmoother
from city_generator import CityLayoutGenerator, Building, ZoneType


class NPCType(Enum):
    """NPC character types"""
    CIVILIAN = 0
    SHOPKEEPER = 1
    GUARD = 2
    VENDOR = 3
    CHILD = 4


class NPCState(Enum):
    """High-level NPC states"""
    IDLE = 0
    WALKING = 1
    RUNNING = 2
    WORKING = 3
    SOCIALIZING = 4
    EATING = 5
    FLEEING = 6


@dataclass
class NPCNeeds:
    """Internal needs driving emergent behavior"""
    hunger: float = 0.0      # 0-100
    energy: float = 100.0    # 0-100
    social: float = 50.0     # 0-100
    safety: float = 100.0    # 0-100

    def update(self, dt: float):
        """Update needs over time"""
        self.hunger = min(100.0, self.hunger + NPC_CONFIG.HUNGER_INCREASE_RATE * dt)
        self.energy = max(0.0, self.energy - NPC_CONFIG.ENERGY_DECREASE_RATE * dt)
        self.social = max(0.0, self.social - NPC_CONFIG.SOCIAL_DECREASE_RATE * dt)

    def get_most_critical(self) -> str:
        """Get the most critical need"""
        needs = {
            'hunger': self.hunger,
            'energy': 100 - self.energy,
            'social': 100 - self.social,
            'safety': 100 - self.safety
        }
        return max(needs, key=needs.get)


@dataclass
class NPCMemory:
    """Memory system for NPCs"""
    events: List[Dict[str, Any]] = field(default_factory=list)
    known_locations: Dict[str, Tuple[int, int]] = field(default_factory=dict)
    relationships: Dict[int, float] = field(default_factory=dict)  # NPC_ID -> relationship value

    def remember_event(self, event_type: str, data: Any, timestamp: float):
        """Store an event in memory"""
        self.events.append({
            'type': event_type,
            'data': data,
            'timestamp': timestamp
        })

        # Limit memory size
        if len(self.events) > NPC_CONFIG.MAX_MEMORY_SIZE:
            self.events.pop(0)

    def decay_memories(self, dt: float):
        """Fade old memories"""
        current_time = time.time()
        self.events = [
            event for event in self.events
            if current_time - event['timestamp'] < 300  # 5 minutes
        ]

    def get_recent_events(self, event_type: str = None, limit: int = 5) -> List[Dict]:
        """Retrieve recent events"""
        events = self.events if event_type is None else [
            e for e in self.events if e['type'] == event_type
        ]
        return events[-limit:]


class NPC:
    """
    Advanced NPC agent with emergent AI behavior.

    Features:
    - Behavior tree-driven decision making
    - Utility AI for action selection
    - Memory system for learning
    - Need-based motivation
    - Pathfinding and navigation
    - Perception system
    """

    _id_counter = 0

    def __init__(
        self,
        position: Tuple[int, int],
        npc_type: NPCType = NPCType.CIVILIAN,
        city: Optional[CityLayoutGenerator] = None
    ):
        # Identification
        self.id = NPC._id_counter
        NPC._id_counter += 1
        self.npc_type = npc_type

        # Position and movement
        self.position = np.array(position, dtype=np.float32)
        self.velocity = np.array([0.0, 0.0], dtype=np.float32)
        self.target_position: Optional[np.ndarray] = None
        self.path: Optional[List[Tuple[int, int]]] = None
        self.path_index = 0

        # State
        self.state = NPCState.IDLE
        self.facing_direction = 0.0  # Radians

        # Internal systems
        self.needs = NPCNeeds()
        self.memory = NPCMemory()
        self.blackboard = Blackboard()

        # Perception
        self.perceived_npcs: List['NPC'] = []
        self.perceived_buildings: List[Building] = []

        # City reference
        self.city = city
        self.home_location: Optional[Tuple[int, int]] = None
        self.work_location: Optional[Tuple[int, int]] = None

        # AI systems
        self.behavior_tree = self._create_behavior_tree()
        self.utility_ai = self._create_utility_ai()

        # Timing
        self.idle_timer = 0.0
        self.idle_duration = np.random.uniform(*NPC_CONFIG.IDLE_TIME_RANGE)

        # Initialize blackboard
        self._update_blackboard()

        print(f"NPC {self.id} ({npc_type.name}) created at {position}")

    def update(self, dt: float, all_npcs: List['NPC'] = None):
        """
        Update NPC state.

        Args:
            dt: Delta time in seconds
            all_npcs: List of all NPCs for perception
        """
        # Update needs
        self.needs.update(dt)

        # Update perception
        if all_npcs:
            self._update_perception(all_npcs)

        # Update blackboard with current state
        self._update_blackboard()

        # Execute behavior tree
        self.behavior_tree.tick()

        # Update movement
        self._update_movement(dt)

        # Decay memories
        self.memory.decay_memories(dt)

    def _update_perception(self, all_npcs: List['NPC']):
        """Update what NPC can perceive"""
        self.perceived_npcs = []

        for other in all_npcs:
            if other.id == self.id:
                continue

            distance = np.linalg.norm(self.position - other.position)
            if distance < NPC_CONFIG.PERCEPTION_RADIUS:
                self.perceived_npcs.append(other)

    def _update_blackboard(self):
        """Update blackboard with current state"""
        self.blackboard.update({
            'npc_id': self.id,
            'position': self.position.copy(),
            'velocity': self.velocity.copy(),
            'state': self.state,
            'hunger': self.needs.hunger,
            'energy': self.needs.energy,
            'social': self.needs.social,
            'safety': self.needs.safety,
            'perceived_npcs': self.perceived_npcs,
            'has_path': self.path is not None,
            'at_target': self._is_at_target()
        })

    def _update_movement(self, dt: float):
        """Update movement based on current path"""
        if self.path and self.path_index < len(self.path):
            # Get next waypoint
            target = self.path[self.path_index]
            target_pos = np.array(target, dtype=np.float32)

            # Calculate direction
            direction = target_pos - self.position
            distance = np.linalg.norm(direction)

            if distance < 1.0:
                # Reached waypoint, move to next
                self.path_index += 1
                if self.path_index >= len(self.path):
                    # Reached end of path
                    self.path = None
                    self.path_index = 0
                    self.state = NPCState.IDLE
                    self.velocity = np.array([0.0, 0.0])
                return

            # Move toward waypoint
            direction /= distance  # Normalize

            # Set velocity based on state
            speed = NPC_CONFIG.WALK_SPEED if self.state == NPCState.WALKING else NPC_CONFIG.RUN_SPEED
            self.velocity = direction * speed

            # Update position
            self.position += self.velocity * dt

            # Update facing direction
            self.facing_direction = np.arctan2(direction[1], direction[0])

        else:
            # No path, decelerate
            self.velocity *= 0.9
            if np.linalg.norm(self.velocity) < 0.1:
                self.velocity = np.array([0.0, 0.0])

    def _is_at_target(self) -> bool:
        """Check if NPC has reached target"""
        if self.target_position is None:
            return False
        distance = np.linalg.norm(self.position - self.target_position)
        return distance < 2.0

    def set_destination(self, target: Tuple[int, int], running: bool = False):
        """
        Set navigation destination.

        Args:
            target: Target position
            running: Whether to run instead of walk
        """
        if self.city is None:
            return

        # Find path
        start = (int(self.position[0]), int(self.position[1]))

        # Create walkable grid (roads + some surrounding area)
        walkable = self.city.road_grid.copy()

        # Find path using A*
        path = AStar.find_path(start, target, walkable, allow_diagonal=True)

        if path:
            # Smooth path
            self.path = PathSmoother.smooth_path(path, walkable)
            self.path_index = 0
            self.target_position = np.array(target, dtype=np.float32)
            self.state = NPCState.RUNNING if running else NPCState.WALKING
        else:
            # No path found, try to move to nearest road
            nearest_road = self.city.get_nearest_road(target[0], target[1])
            if nearest_road:
                path = AStar.find_path(start, nearest_road, walkable, allow_diagonal=True)
                if path:
                    self.path = PathSmoother.smooth_path(path, walkable)
                    self.path_index = 0
                    self.target_position = np.array(nearest_road, dtype=np.float32)
                    self.state = NPCState.RUNNING if running else NPCState.WALKING

    def interact_with(self, other: 'NPC'):
        """Interact with another NPC"""
        # Update relationship
        if other.id not in self.memory.relationships:
            self.memory.relationships[other.id] = 0.0

        # Increase relationship
        self.memory.relationships[other.id] += 1.0

        # Satisfy social need
        self.needs.social = min(100.0, self.needs.social + 10.0)

        # Remember interaction
        self.memory.remember_event(
            'interaction',
            {'npc_id': other.id, 'type': 'conversation'},
            time.time()
        )

        # Change state
        self.state = NPCState.SOCIALIZING

    # ==================== BEHAVIOR TREE CREATION ====================

    def _create_behavior_tree(self) -> BehaviorTree:
        """Create behavior tree for this NPC"""

        # Define actions
        def wander_action(bb: Blackboard) -> NodeStatus:
            """Wander to random location"""
            if self.path is None and self.city:
                # Pick random road location
                road_cells = np.argwhere(self.city.road_grid)
                if len(road_cells) > 0:
                    target_idx = np.random.randint(0, len(road_cells))
                    target = tuple(road_cells[target_idx][::-1])  # y,x -> x,y
                    self.set_destination(target)
            return NodeStatus.SUCCESS

        def find_food_action(bb: Blackboard) -> NodeStatus:
            """Find and move to food source"""
            if self.city and self.city.buildings:
                # Find commercial buildings (restaurants)
                restaurants = [
                    b for b in self.city.buildings
                    if b.zone_type in [ZoneType.COMMERCIAL, ZoneType.MIXED]
                ]
                if restaurants:
                    target_building = np.random.choice(restaurants)
                    self.set_destination((target_building.x, target_building.y))
                    return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        def eat_action(bb: Blackboard) -> NodeStatus:
            """Eat to reduce hunger"""
            if self._is_at_target():
                self.needs.hunger = max(0.0, self.needs.hunger - 50.0)
                self.state = NPCState.EATING
                return NodeStatus.SUCCESS
            return NodeStatus.RUNNING

        def rest_action(bb: Blackboard) -> NodeStatus:
            """Rest to restore energy"""
            self.needs.energy = min(100.0, self.needs.energy + 20.0)
            self.state = NPCState.IDLE
            return NodeStatus.SUCCESS

        def socialize_action(bb: Blackboard) -> NodeStatus:
            """Find and interact with nearby NPC"""
            if self.perceived_npcs:
                other = self.perceived_npcs[0]
                self.interact_with(other)
                return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        def flee_action(bb: Blackboard) -> NodeStatus:
            """Flee from danger"""
            if self.city:
                # Move away from current position
                flee_distance = 50
                angle = np.random.uniform(0, 2 * np.pi)
                offset_x = int(flee_distance * np.cos(angle))
                offset_y = int(flee_distance * np.sin(angle))
                target = (
                    int(self.position[0] + offset_x),
                    int(self.position[1] + offset_y)
                )
                self.set_destination(target, running=True)
            return NodeStatus.SUCCESS

        # Build behavior tree
        root = Selector("NPCBehavior", [
            # Priority 1: Survival
            Sequence("HandleDanger", [
                Condition("InDanger", lambda bb: bb.get('safety', 100) < 50),
                Action("Flee", flee_action)
            ]),

            # Priority 2: Critical needs
            Sequence("SatisfyHunger", [
                Condition("VeryHungry", lambda bb: bb.get('hunger', 0) > 70),
                Action("FindFood", find_food_action),
                Action("Eat", eat_action)
            ]),

            Sequence("RestIfTired", [
                Condition("VeryTired", lambda bb: bb.get('energy', 100) < 30),
                Action("Rest", rest_action)
            ]),

            # Priority 3: Social needs
            Sequence("Socialize", [
                Condition("NeedsSocial", lambda bb: bb.get('social', 0) < 40),
                Condition("NPCsNearby", lambda bb: len(bb.get('perceived_npcs', [])) > 0),
                Action("Interact", socialize_action)
            ]),

            # Default: Wander
            Action("Wander", wander_action)
        ])

        return BehaviorTree(root, self.blackboard)

    def _create_utility_ai(self) -> UtilityAI:
        """Create utility AI for action selection"""
        utility = UtilityAI()

        # Add utility options
        utility.add_option(
            "eat",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: bb.get('hunger', 0) / 100.0
        )

        utility.add_option(
            "rest",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: (100 - bb.get('energy', 100)) / 100.0
        )

        utility.add_option(
            "socialize",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: (100 - bb.get('social', 50)) / 100.0 if bb.get('perceived_npcs', []) else 0.0
        )

        return utility


class NPCManager:
    """
    Manager for all NPCs in the simulation.
    Handles updates, spawning, and inter-NPC interactions.
    """

    def __init__(self, city: CityLayoutGenerator):
        self.city = city
        self.npcs: List[NPC] = []

    def spawn_npc(self, position: Tuple[int, int], npc_type: NPCType = NPCType.CIVILIAN) -> NPC:
        """Spawn a new NPC"""
        npc = NPC(position, npc_type, self.city)
        self.npcs.append(npc)
        return npc

    def spawn_random_npcs(self, count: int):
        """Spawn NPCs at random road locations"""
        road_cells = np.argwhere(self.city.road_grid)

        for _ in range(min(count, len(road_cells))):
            idx = np.random.randint(0, len(road_cells))
            pos = tuple(road_cells[idx][::-1])  # y,x -> x,y

            # Random NPC type
            npc_type = np.random.choice(list(NPCType))
            self.spawn_npc(pos, npc_type)

    def update_all(self, dt: float):
        """Update all NPCs"""
        for npc in self.npcs:
            npc.update(dt, self.npcs)

    def get_npc_stats(self) -> Dict[str, Any]:
        """Get statistics about NPCs"""
        if not self.npcs:
            return {}

        return {
            'total': len(self.npcs),
            'by_state': {
                state.name: sum(1 for n in self.npcs if n.state == state)
                for state in NPCState
            },
            'by_type': {
                npc_type.name: sum(1 for n in self.npcs if n.npc_type == npc_type)
                for npc_type in NPCType
            },
            'avg_hunger': np.mean([n.needs.hunger for n in self.npcs]),
            'avg_energy': np.mean([n.needs.energy for n in self.npcs]),
            'avg_social': np.mean([n.needs.social for n in self.npcs])
        }


if __name__ == "__main__":
    # Test NPC system
    print("Testing NPC system...")

    # Create simple mock city
    class MockCity:
        def __init__(self):
            self.size = 100
            self.road_grid = np.ones((100, 100), dtype=bool)
            self.buildings = []

        def get_nearest_road(self, x, y):
            return (x, y)

    city = MockCity()

    # Create NPC manager
    manager = NPCManager(city)
    manager.spawn_random_npcs(10)

    # Simulate
    for i in range(5):
        manager.update_all(1.0)
        stats = manager.get_npc_stats()
        print(f"\nTick {i + 1}: {stats['total']} NPCs")
        print(f"  States: {stats['by_state']}")
