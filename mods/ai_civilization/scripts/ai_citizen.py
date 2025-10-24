"""
AI Citizen for Civilization Experiment
Adapted from NPC system for social experiment framework

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
import json
import time
from typing import List, Tuple, Optional, Dict, Any
from dataclasses import dataclass, field
from enum import Enum
import sys
import os

# Add ai_systems to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../ai_systems'))

from ai_behavior import (
    BehaviorTree, Blackboard, Sequence, Selector, Action,
    Condition, NodeStatus, UtilityAI
)


class CitizenState(Enum):
    """High-level citizen states"""
    IDLE = 0
    TRAVELING = 1
    WORKING = 2
    SOCIALIZING = 3
    TRADING = 4
    RESTING = 5
    SEEKING_RESOURCES = 6


@dataclass
class CitizenNeeds:
    """Internal needs driving emergent behavior - normalized 0.0-1.0"""
    hunger: float = 0.5      # 0.0 (satisfied) - 1.0 (starving)
    energy: float = 0.5      # 0.0 (exhausted) - 1.0 (fully rested)
    social: float = 0.5      # 0.0 (lonely) - 1.0 (socially fulfilled)
    wealth: float = 0.5      # 0.0 (broke) - 1.0 (wealthy)
    safety: float = 1.0      # 0.0 (danger) - 1.0 (safe)
    achievement: float = 0.3 # 0.0 (unfulfilled) - 1.0 (accomplished)

    def update(self, dt: float):
        """Update needs over time - natural decay"""
        # Hunger increases over time
        self.hunger = min(1.0, self.hunger + 0.01 * dt)

        # Energy decreases when active
        self.energy = max(0.0, self.energy - 0.008 * dt)

        # Social need increases (loneliness)
        self.social = max(0.0, self.social - 0.005 * dt)

        # Achievement slowly decays
        self.achievement = max(0.0, self.achievement - 0.002 * dt)

    def get_most_critical(self) -> str:
        """Get the most critical unfulfilled need"""
        needs = {
            'hunger': self.hunger,
            'energy': 1.0 - self.energy,
            'social': 1.0 - self.social,
            'wealth': 1.0 - self.wealth,
            'safety': 1.0 - self.safety,
            'achievement': 1.0 - self.achievement
        }
        return max(needs, key=needs.get)


@dataclass
class CitizenMemory:
    """Memory system for citizens"""
    events: List[Dict[str, Any]] = field(default_factory=list)
    known_citizens: Dict[str, Dict] = field(default_factory=dict)
    relationships: Dict[str, float] = field(default_factory=dict)  # citizen_id -> -100 to +100
    known_locations: Dict[str, Tuple[int, int]] = field(default_factory=dict)

    def remember_event(self, event_type: str, data: Any):
        """Store an event in memory"""
        self.events.append({
            'type': event_type,
            'data': data,
            'timestamp': time.time()
        })

        # Limit memory size
        if len(self.events) > 100:
            self.events.pop(0)

    def update_relationship(self, citizen_id: str, delta: float):
        """Update relationship value"""
        if citizen_id not in self.relationships:
            self.relationships[citizen_id] = 0.0

        self.relationships[citizen_id] = np.clip(
            self.relationships[citizen_id] + delta,
            -100.0, 100.0
        )

    def get_relationship(self, citizen_id: str) -> float:
        """Get relationship value (-100 to +100)"""
        return self.relationships.get(citizen_id, 0.0)

    def decay_memories(self, dt: float):
        """Fade old memories and relationships"""
        current_time = time.time()

        # Remove events older than 10 minutes
        self.events = [
            event for event in self.events
            if current_time - event['timestamp'] < 600
        ]

        # Decay relationships toward neutral
        for citizen_id in self.relationships:
            if self.relationships[citizen_id] > 0:
                self.relationships[citizen_id] = max(0, self.relationships[citizen_id] - 0.1 * dt)
            elif self.relationships[citizen_id] < 0:
                self.relationships[citizen_id] = min(0, self.relationships[citizen_id] + 0.1 * dt)


class AICitizen:
    """
    AI Citizen for social experiment.

    Features:
    - Personality-driven behavior (Big Five traits)
    - Need-based decision making
    - Memory and relationship tracking
    - Emergent social behaviors
    - Economic decision making
    """

    _id_counter = 0

    def __init__(self, profile: Dict, position: Tuple[int, int] = (0, 0), use_llm: bool = False):
        # Identification
        self.id = f"citizen_{AICitizen._id_counter:04d}"
        AICitizen._id_counter += 1
        self.archetype = profile.get('archetype', 'civilian')
        self.profile_id = profile.get('id', 'unknown')

        # LLM mode
        self.use_llm = use_llm

        # Position
        self.position = np.array(position, dtype=np.float32)
        self.target_position: Optional[np.ndarray] = None

        # State
        self.state = CitizenState.IDLE

        # Personality (Big Five - 0.0 to 1.0)
        personality_seed = profile.get('personality_seed', {})
        self.personality = {
            'openness': personality_seed.get('openness', 0.5),
            'conscientiousness': personality_seed.get('conscientiousness', 0.5),
            'extraversion': personality_seed.get('extraversion', 0.5),
            'agreeableness': personality_seed.get('agreeableness', 0.5),
            'neuroticism': personality_seed.get('neuroticism', 0.5)
        }

        # Resources
        starting_resources = profile.get('starting_resources', {})
        self.money = starting_resources.get('money', 100)
        self.items = starting_resources.get('items', []).copy()

        # Internal systems
        self.needs = CitizenNeeds()
        self.memory = CitizenMemory()
        self.blackboard = Blackboard()

        # Perception
        self.perceived_citizens: List['AICitizen'] = []

        # AI systems
        self.behavior_tree = self._create_behavior_tree()
        self.utility_ai = self._create_utility_ai()

        # Statistics
        self.stats = {
            'interactions_count': 0,
            'trades_completed': 0,
            'items_given': 0,
            'items_received': 0,
            'money_earned': 0,
            'money_spent': 0,
            'total_distance_traveled': 0.0
        }

        # Initialize blackboard
        self._update_blackboard()

    def update(self, dt: float, all_citizens: List['AICitizen'] = None, llm=None):
        """
        Update citizen state.

        Args:
            dt: Delta time in seconds
            all_citizens: List of all citizens for perception
            llm: Optional LLM instance for decision-making
        """
        # Update needs
        self.needs.update(dt)

        # Update wealth need based on money
        self.needs.wealth = min(1.0, self.money / 1000.0)

        # Update perception
        if all_citizens:
            self._update_perception(all_citizens)

        # Update blackboard
        self._update_blackboard()

        # Decision making - LLM or behavior tree
        if self.use_llm and llm and llm.is_available():
            self._execute_llm_decision(llm)
        else:
            # Execute behavior tree (fallback)
            self.behavior_tree.tick()

        # Decay memories
        self.memory.decay_memories(dt)

    def _update_perception(self, all_citizens: List['AICitizen']):
        """Update what citizen can perceive"""
        self.perceived_citizens = []
        perception_radius = 50.0 + (self.personality['extraversion'] * 50.0)  # 50-100 based on extraversion

        for other in all_citizens:
            if other.id == self.id:
                continue

            distance = np.linalg.norm(self.position - other.position)
            if distance < perception_radius:
                self.perceived_citizens.append(other)

    def _update_blackboard(self):
        """Update blackboard with current state"""
        self.blackboard.update({
            'citizen_id': self.id,
            'position': self.position.copy(),
            'state': self.state,
            'money': self.money,
            'items': self.items.copy(),
            'personality': self.personality.copy(),

            # Needs
            'hunger': self.needs.hunger,
            'energy': self.needs.energy,
            'social': self.needs.social,
            'wealth': self.needs.wealth,
            'safety': self.needs.safety,
            'achievement': self.needs.achievement,

            # Perception
            'perceived_citizens': self.perceived_citizens,
            'num_nearby': len(self.perceived_citizens),

            # Memory
            'relationships': self.memory.relationships.copy()
        })

    # ==================== SOCIAL INTERACTIONS ====================

    def interact_with(self, other: 'AICitizen', interaction_type: str = 'chat'):
        """Interact with another citizen"""
        # Update relationship based on personality compatibility
        compatibility = self._calculate_compatibility(other)
        relationship_delta = compatibility * 2.0  # -2 to +2

        self.memory.update_relationship(other.id, relationship_delta)
        other.memory.update_relationship(self.id, relationship_delta)

        # Satisfy social need
        social_gain = 0.1 + (self.personality['extraversion'] * 0.1)
        self.needs.social = min(1.0, self.needs.social + social_gain)
        other.needs.social = min(1.0, other.needs.social + social_gain)

        # Remember interaction
        self.memory.remember_event('interaction', {
            'citizen_id': other.id,
            'type': interaction_type,
            'relationship_delta': relationship_delta
        })

        # Update stats
        self.stats['interactions_count'] += 1
        other.stats['interactions_count'] += 1

        # Change state
        self.state = CitizenState.SOCIALIZING
        other.state = CitizenState.SOCIALIZING

    def _calculate_compatibility(self, other: 'AICitizen') -> float:
        """Calculate personality compatibility (-1.0 to +1.0)"""
        # Simple compatibility based on personality similarity
        diff_sum = 0.0
        for trait in ['openness', 'conscientiousness', 'extraversion', 'agreeableness']:
            diff = abs(self.personality[trait] - other.personality[trait])
            diff_sum += diff

        # Average difference (0-1), invert to get compatibility
        avg_diff = diff_sum / 4.0
        compatibility = 1.0 - (avg_diff * 2.0)  # -1 to +1

        # Bonus for high agreeableness
        agreeableness_bonus = (self.personality['agreeableness'] + other.personality['agreeableness'] - 1.0) * 0.2

        return np.clip(compatibility + agreeableness_bonus, -1.0, 1.0)

    # ==================== ECONOMIC BEHAVIORS ====================

    def can_afford(self, cost: float) -> bool:
        """Check if citizen can afford cost"""
        return self.money >= cost

    def evaluate_trade(self, offer_items: List[str], request_items: List[str],
                      offer_money: float, request_money: float,
                      other_citizen: 'AICitizen') -> bool:
        """
        Evaluate if a trade is acceptable.
        Returns True if trade should be accepted.
        """
        # Calculate value of what we're giving
        giving_value = offer_money
        for item in offer_items:
            giving_value += self._value_item(item)

        # Calculate value of what we're receiving
        receiving_value = request_money
        for item in request_items:
            receiving_value += self._value_item(item)

        # Apply relationship modifier
        relationship = self.memory.get_relationship(other_citizen.id)
        if relationship > 50:
            # Friends - more generous (willing to lose up to 20% value)
            return receiving_value >= giving_value * 0.8
        elif relationship < -50:
            # Enemies - demand premium (want 130% value)
            return receiving_value >= giving_value * 1.3
        else:
            # Neutral - want fair trade (within 10%)
            return receiving_value >= giving_value * 0.9

    def _value_item(self, item_id: str) -> float:
        """Determine how much this citizen values an item"""
        # Load item data
        items_file = os.path.join(os.path.dirname(__file__), '../db/items.json')
        with open(items_file, 'r') as f:
            items_data = json.load(f)

        # Find item
        item_data = next((i for i in items_data['items'] if i['id'] == item_id), None)
        if not item_data:
            return 10.0  # Default value

        base_value = item_data.get('base_value', 10)

        # Modify based on current needs
        effect = item_data.get('effect', None)
        if effect == 'hunger' and self.needs.hunger > 0.7:
            base_value *= 2.0  # Hungry people value food more
        elif effect == 'energy' and self.needs.energy < 0.3:
            base_value *= 2.0  # Tired people value rest items more
        elif item_data.get('category') == 'tool' and self.personality['conscientiousness'] > 0.7:
            base_value *= 1.5  # Conscientious people value tools

        return base_value

    # ==================== BEHAVIOR TREE CREATION ====================

    def _create_behavior_tree(self) -> BehaviorTree:
        """Create behavior tree for this citizen"""

        # Define actions
        def seek_food_action(bb: Blackboard) -> NodeStatus:
            """Seek food to satisfy hunger"""
            # Look for citizens with food items
            for citizen in self.perceived_citizens:
                if any('water' in item or 'food' in item or 'snack' in item or 'coffee' in item
                       for item in citizen.items):
                    # Attempt to trade or request
                    self.state = CitizenState.SEEKING_RESOURCES
                    return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        def seek_social_action(bb: Blackboard) -> NodeStatus:
            """Seek social interaction"""
            if self.perceived_citizens:
                # Pick a citizen to interact with - prefer friends
                best_target = None
                best_relationship = -200

                for citizen in self.perceived_citizens:
                    rel = self.memory.get_relationship(citizen.id)
                    if rel > best_relationship:
                        best_relationship = rel
                        best_target = citizen

                if best_target:
                    self.interact_with(best_target, 'chat')
                    return NodeStatus.SUCCESS
            return NodeStatus.FAILURE

        def rest_action(bb: Blackboard) -> NodeStatus:
            """Rest to restore energy"""
            self.needs.energy = min(1.0, self.needs.energy + 0.2)
            self.state = CitizenState.RESTING
            return NodeStatus.SUCCESS

        def work_action(bb: Blackboard) -> NodeStatus:
            """Work to earn money"""
            # Earn based on archetype and conscientiousness
            base_earnings = 10 + (self.personality['conscientiousness'] * 20)
            self.money += base_earnings
            self.stats['money_earned'] += base_earnings

            # Working satisfies achievement but costs energy
            self.needs.achievement = min(1.0, self.needs.achievement + 0.1)
            self.needs.energy = max(0.0, self.needs.energy - 0.15)

            self.state = CitizenState.WORKING
            return NodeStatus.SUCCESS

        def idle_action(bb: Blackboard) -> NodeStatus:
            """Idle - slight energy recovery"""
            self.needs.energy = min(1.0, self.needs.energy + 0.05)
            self.state = CitizenState.IDLE
            return NodeStatus.SUCCESS

        # Build behavior tree based on personality
        root = Selector("CitizenBehavior", [
            # Priority 1: Critical needs
            Sequence("SatisfyHunger", [
                Condition("VeryHungry", lambda bb: bb.get('hunger', 0) > 0.8),
                Action("SeekFood", seek_food_action)
            ]),

            Sequence("RestIfExhausted", [
                Condition("VeryTired", lambda bb: bb.get('energy', 1.0) < 0.2),
                Action("Rest", rest_action)
            ]),

            # Priority 2: Social needs (higher priority for extraverts)
            Sequence("Socialize", [
                Condition("NeedsSocial", lambda bb: bb.get('social', 0) < 0.4),
                Condition("CitizensNearby", lambda bb: bb.get('num_nearby', 0) > 0),
                Condition("IsExtraverted", lambda bb: bb.get('personality', {}).get('extraversion', 0.5) > 0.5),
                Action("SeekInteraction", seek_social_action)
            ]),

            # Priority 3: Economic needs
            Sequence("EarnMoney", [
                Condition("LowWealth", lambda bb: bb.get('wealth', 0.5) < 0.3),
                Condition("HasEnergy", lambda bb: bb.get('energy', 0) > 0.3),
                Action("Work", work_action)
            ]),

            # Default: Idle
            Action("Idle", idle_action)
        ])

        return BehaviorTree(root, self.blackboard)

    def _create_utility_ai(self) -> UtilityAI:
        """Create utility AI for action selection"""
        utility = UtilityAI()

        # Add utility options based on personality and needs
        utility.add_option(
            "socialize",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: (1.0 - bb.get('social', 0.5)) * bb.get('personality', {}).get('extraversion', 0.5)
        )

        utility.add_option(
            "work",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: (1.0 - bb.get('wealth', 0.5)) * bb.get('personality', {}).get('conscientiousness', 0.5)
        )

        utility.add_option(
            "rest",
            lambda bb: NodeStatus.SUCCESS,
            lambda bb: (1.0 - bb.get('energy', 1.0))
        )

        return utility

    def _execute_llm_decision(self, llm):
        """Execute decision from LLM"""
        # Get citizen state for LLM
        citizen_state = {
            'archetype': self.archetype,
            'money': self.money,
            'items': self.items,
            'needs': {
                'hunger': self.needs.hunger,
                'energy': self.needs.energy,
                'social': self.needs.social,
                'wealth': self.needs.wealth,
                'safety': self.needs.safety,
                'achievement': self.needs.achievement
            },
            'personality': self.personality,
            'num_nearby': len(self.perceived_citizens)
        }

        # Get decision from LLM
        decision = llm.generate_decision(citizen_state)
        action = decision['action']

        # Execute action
        if action == 'work':
            base_earnings = 10 + (self.personality['conscientiousness'] * 20)
            self.money += base_earnings
            self.stats['money_earned'] += base_earnings
            self.needs.achievement = min(1.0, self.needs.achievement + 0.1)
            self.needs.energy = max(0.0, self.needs.energy - 0.15)
            self.state = CitizenState.WORKING

        elif action == 'rest':
            self.needs.energy = min(1.0, self.needs.energy + 0.2)
            self.state = CitizenState.RESTING

        elif action == 'socialize' and self.perceived_citizens:
            other = self.perceived_citizens[0]
            self.interact_with(other, 'chat')

        elif action == 'seek_food':
            self.state = CitizenState.SEEKING_RESOURCES

        elif action == 'trade' and self.perceived_citizens:
            # Simplified trading attempt
            self.state = CitizenState.TRADING

        else:  # idle
            self.needs.energy = min(1.0, self.needs.energy + 0.05)
            self.state = CitizenState.IDLE

    def to_dict(self) -> Dict:
        """Export citizen data for metrics"""
        return {
            'id': self.id,
            'archetype': self.archetype,
            'profile_id': self.profile_id,
            'position': self.position.tolist(),
            'state': self.state.name,
            'money': self.money,
            'items': self.items.copy(),
            'personality': self.personality.copy(),
            'needs': {
                'hunger': self.needs.hunger,
                'energy': self.needs.energy,
                'social': self.needs.social,
                'wealth': self.needs.wealth,
                'safety': self.needs.safety,
                'achievement': self.needs.achievement
            },
            'relationships': self.memory.relationships.copy(),
            'stats': self.stats.copy()
        }
