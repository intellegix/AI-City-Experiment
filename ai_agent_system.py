"""
Advanced AI Agent System for Social Experiments
Implements autonomous agent behaviors for realistic city simulation

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
from enum import Enum
from typing import Tuple, List, Optional
from dataclasses import dataclass
import random


class AgentState(Enum):
    """AI Agent behavioral states"""
    WALKING = "walking"           # Moving towards destination
    STOPPED = "stopped"           # Standing still (temporary pause)
    WAITING = "waiting"           # Waiting at location (longer duration)
    WANDERING = "wandering"       # Random exploration
    FOLLOWING_ROAD = "following_road"  # Following road network


@dataclass
class AgentPersonality:
    """Personality traits affecting agent behavior"""
    walking_speed: float = 1.0    # Speed multiplier (0.5 = slow, 2.0 = fast)
    social: float = 0.5           # Tendency to group with others (0-1)
    exploratory: float = 0.5      # Tendency to wander vs follow roads (0-1)
    stop_frequency: float = 0.3   # How often agent stops (0-1)
    patience: float = 0.5         # How long agent waits (0-1)


class AIAgent:
    """
    Autonomous AI agent with sophisticated behaviors.

    Features:
    - Pathfinding along road network
    - Collision avoidance with other agents
    - Destination-based movement
    - Personality-driven behaviors
    - Social grouping tendencies
    """

    def __init__(self, agent_id: int, position: Tuple[float, float],
                 roads: List[Tuple[float, float, float, float]],
                 buildings: List[Tuple[float, float]]):
        """
        Initialize AI agent.

        Args:
            agent_id: Unique identifier for agent
            position: Initial (x, y) position
            roads: List of road segments [(x1, y1, x2, y2), ...]
            buildings: List of building positions [(x, y), ...]
        """
        self.id = agent_id
        self.position = np.array(position, dtype=float)
        self.heading = random.uniform(0, 360)

        # World knowledge
        self.roads = roads
        self.buildings = buildings
        self.world_bounds = 32.0  # Half of world size (64/2)

        # Behavioral state
        self.state = AgentState.WANDERING
        self.state_timer = 0.0  # Time in current state

        # Movement
        self.velocity = np.array([0.0, 0.0])
        self.destination = None
        self.current_road = None

        # Personality (randomized for variety)
        self.personality = AgentPersonality(
            walking_speed=random.uniform(0.7, 1.3),
            social=random.uniform(0.2, 0.8),
            exploratory=random.uniform(0.3, 0.9),
            stop_frequency=random.uniform(0.1, 0.5),
            patience=random.uniform(0.3, 0.8)
        )

        # Social awareness
        self.nearby_agents = []
        self.personal_space = 2.0  # Minimum distance from others

        # Decision making
        self.decision_cooldown = 0.0  # Time until next major decision

    def update(self, dt: float, all_agents: List['AIAgent']):
        """
        Update agent behavior.

        Args:
            dt: Delta time since last update
            all_agents: List of all agents in simulation (for collision avoidance)
        """
        self.state_timer += dt
        self.decision_cooldown -= dt

        # Update nearby agents for collision avoidance
        self._update_nearby_agents(all_agents)

        # State machine
        if self.state == AgentState.WALKING:
            self._behavior_walk_to_destination(dt)
        elif self.state == AgentState.WANDERING:
            self._behavior_wander(dt)
        elif self.state == AgentState.STOPPED:
            self._behavior_stopped(dt)
        elif self.state == AgentState.WAITING:
            self._behavior_waiting(dt)
        elif self.state == AgentState.FOLLOWING_ROAD:
            self._behavior_follow_road(dt)

        # Apply collision avoidance
        self._apply_collision_avoidance(dt)

        # Apply movement
        self._apply_movement(dt)

        # Boundary checking
        self._check_boundaries()

        # Make decisions periodically
        if self.decision_cooldown <= 0:
            self._make_decision()
            self.decision_cooldown = random.uniform(2.0, 5.0)

    def _update_nearby_agents(self, all_agents: List['AIAgent']):
        """Update list of nearby agents for collision avoidance"""
        self.nearby_agents = []
        for agent in all_agents:
            if agent.id != self.id:
                dist = np.linalg.norm(self.position - agent.position)
                if dist < self.personal_space * 3:  # Detection radius
                    self.nearby_agents.append(agent)

    def _behavior_walk_to_destination(self, dt: float):
        """Walk towards destination"""
        if self.destination is None:
            self.state = AgentState.WANDERING
            return

        # Calculate direction to destination
        direction = self.destination - self.position
        distance = np.linalg.norm(direction)

        # Reached destination?
        if distance < 1.0:
            self.state = AgentState.STOPPED
            self.state_timer = 0.0
            self.destination = None
            return

        # Move towards destination
        direction = direction / distance  # Normalize
        speed = 2.0 * self.personality.walking_speed
        self.velocity = direction * speed
        self.heading = np.degrees(np.arctan2(direction[0], direction[1]))

        # Random chance to stop
        if random.random() < self.personality.stop_frequency * 0.01:
            self.state = AgentState.STOPPED
            self.state_timer = 0.0

    def _behavior_wander(self, dt: float):
        """Random wandering behavior"""
        # Pick random direction and walk
        if self.state_timer == 0 or random.random() < 0.02:
            self.heading = random.uniform(0, 360)

        # Move forward
        speed = 1.5 * self.personality.walking_speed
        heading_rad = np.radians(self.heading)
        self.velocity = np.array([
            speed * np.sin(heading_rad),
            speed * np.cos(heading_rad)
        ])

        # Occasionally switch to road following or pick destination
        if random.random() < 0.005:
            if random.random() < self.personality.exploratory:
                self._pick_destination()
            else:
                self.state = AgentState.FOLLOWING_ROAD
                self.state_timer = 0.0

    def _behavior_stopped(self, dt: float):
        """Standing still temporarily"""
        self.velocity = np.array([0.0, 0.0])

        # Resume movement after brief pause
        wait_time = 1.0 + self.personality.patience * 3.0
        if self.state_timer > wait_time:
            if random.random() < 0.5:
                self.state = AgentState.WANDERING
            else:
                self._pick_destination()
            self.state_timer = 0.0

    def _behavior_waiting(self, dt: float):
        """Waiting at location for longer duration"""
        self.velocity = np.array([0.0, 0.0])

        # Resume movement after longer wait
        wait_time = 5.0 + self.personality.patience * 10.0
        if self.state_timer > wait_time:
            self.state = AgentState.WANDERING
            self.state_timer = 0.0

    def _behavior_follow_road(self, dt: float):
        """Follow nearest road"""
        if not self.roads:
            self.state = AgentState.WANDERING
            return

        # Find nearest road if we don't have one
        if self.current_road is None:
            self.current_road = self._find_nearest_road()

        if self.current_road is None:
            self.state = AgentState.WANDERING
            return

        # Get road direction
        x1, y1, x2, y2 = self.current_road
        road_direction = np.array([x2 - x1, y2 - y1])
        road_direction = road_direction / (np.linalg.norm(road_direction) + 1e-6)

        # Move along road
        speed = 2.0 * self.personality.walking_speed
        self.velocity = road_direction * speed
        self.heading = np.degrees(np.arctan2(road_direction[0], road_direction[1]))

        # Check if we've gone past the road end
        to_end = np.array([x2, y2]) - self.position
        if np.dot(to_end, road_direction) < 0:
            # Pick next road or destination
            self.current_road = None
            if random.random() < 0.3:
                self.state = AgentState.STOPPED
            else:
                self._pick_destination()

    def _apply_collision_avoidance(self, dt: float):
        """Avoid colliding with nearby agents"""
        if not self.nearby_agents:
            return

        avoidance_force = np.array([0.0, 0.0])

        for agent in self.nearby_agents:
            to_other = agent.position - self.position
            distance = np.linalg.norm(to_other)

            if distance < self.personal_space and distance > 0.1:
                # Repulsion force (stronger when closer)
                strength = (self.personal_space - distance) / self.personal_space
                avoidance_force -= to_other / distance * strength * 3.0

        # Apply avoidance
        self.velocity += avoidance_force

    def _apply_movement(self, dt: float):
        """Apply velocity to position"""
        # Limit velocity magnitude
        speed = np.linalg.norm(self.velocity)
        max_speed = 3.0 * self.personality.walking_speed
        if speed > max_speed:
            self.velocity = self.velocity / speed * max_speed

        # Update position
        self.position += self.velocity * dt

    def _check_boundaries(self):
        """Keep agent within world bounds"""
        if abs(self.position[0]) > self.world_bounds:
            self.position[0] = np.clip(self.position[0], -self.world_bounds, self.world_bounds)
            self.heading = (self.heading + 180) % 360
            self.velocity[0] *= -1

        if abs(self.position[1]) > self.world_bounds:
            self.position[1] = np.clip(self.position[1], -self.world_bounds, self.world_bounds)
            self.heading = (self.heading + 180) % 360
            self.velocity[1] *= -1

    def _make_decision(self):
        """Make high-level behavioral decision"""
        rand = random.random()

        if self.state == AgentState.WANDERING:
            if rand < 0.3:
                self._pick_destination()
            elif rand < 0.6:
                self.state = AgentState.FOLLOWING_ROAD
                self.current_road = None

        elif self.state == AgentState.WALKING:
            if rand < 0.1:
                self.state = AgentState.STOPPED
                self.destination = None

        elif self.state == AgentState.FOLLOWING_ROAD:
            if rand < 0.2:
                self._pick_destination()

    def _pick_destination(self):
        """Pick a random destination (building)"""
        if not self.buildings:
            self.state = AgentState.WANDERING
            return

        # Pick random building
        building_pos = random.choice(self.buildings)
        self.destination = np.array(building_pos, dtype=float)
        self.state = AgentState.WALKING
        self.state_timer = 0.0

    def _find_nearest_road(self) -> Optional[Tuple[float, float, float, float]]:
        """Find nearest road to current position"""
        if not self.roads:
            return None

        nearest_road = None
        min_distance = float('inf')

        for road in self.roads:
            x1, y1, x2, y2 = road
            road_center = np.array([(x1 + x2) / 2, (y1 + y2) / 2])
            dist = np.linalg.norm(self.position - road_center)

            if dist < min_distance:
                min_distance = dist
                nearest_road = road

        return nearest_road

    def get_state_info(self) -> dict:
        """Get current state information for debugging"""
        return {
            'id': self.id,
            'position': self.position.tolist(),
            'heading': self.heading,
            'state': self.state.value,
            'velocity': self.velocity.tolist(),
            'nearby_agents': len(self.nearby_agents),
            'has_destination': self.destination is not None
        }


class AIAgentManager:
    """
    Manager for all AI agents in simulation.

    Handles:
    - Agent creation and removal
    - Batch updates for all agents
    - Social interactions between agents
    - Performance optimization
    """

    def __init__(self, roads: List[Tuple[float, float, float, float]],
                 buildings: List[Tuple[float, float]]):
        """
        Initialize agent manager.

        Args:
            roads: List of road segments
            buildings: List of building positions
        """
        self.agents: List[AIAgent] = []
        self.roads = roads
        self.buildings = buildings
        self.next_agent_id = 0

    def create_agent(self, position: Tuple[float, float]) -> AIAgent:
        """Create new agent at position"""
        agent = AIAgent(
            agent_id=self.next_agent_id,
            position=position,
            roads=self.roads,
            buildings=self.buildings
        )
        self.agents.append(agent)
        self.next_agent_id += 1
        return agent

    def update_all(self, dt: float):
        """Update all agents"""
        for agent in self.agents:
            agent.update(dt, self.agents)

    def get_agent_positions(self) -> List[Tuple[float, float, float]]:
        """Get all agent positions and headings for rendering"""
        return [(agent.position[0], agent.position[1], agent.heading)
                for agent in self.agents]

    def get_statistics(self) -> dict:
        """Get statistics about agent behaviors"""
        if not self.agents:
            return {'total_agents': 0}

        state_counts = {}
        for agent in self.agents:
            state = agent.state.value
            state_counts[state] = state_counts.get(state, 0) + 1

        return {
            'total_agents': len(self.agents),
            'state_distribution': state_counts,
            'average_speed': np.mean([np.linalg.norm(a.velocity) for a in self.agents])
        }
