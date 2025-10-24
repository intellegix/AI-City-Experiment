"""
Civilization Manager - Coordinates AI citizens and tracks emergent behaviors

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import json
import time
import random
import numpy as np
import os
from pathlib import Path
from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass, field
from ai_citizen import AICitizen, CitizenState


@dataclass
class TradeProposal:
    """Represents a trade proposal between citizens"""
    proposer_id: str
    recipient_id: str
    offer_items: List[str] = field(default_factory=list)
    offer_money: float = 0.0
    request_items: List[str] = field(default_factory=list)
    request_money: float = 0.0
    timestamp: float = field(default_factory=time.time)


@dataclass
class SocialEvent:
    """Represents a social event in the civilization"""
    event_type: str  # 'trade', 'interaction', 'conflict', 'cooperation'
    participants: List[str]
    outcome: str
    timestamp: float = field(default_factory=time.time)
    data: Dict = field(default_factory=dict)


class CivilizationManager:
    """
    Manages the AI civilization simulation.

    Features:
    - Citizen spawning and management
    - Social dynamics tracking
    - Economic system (trading, wealth distribution)
    - Event logging for analysis
    - Emergent behavior metrics
    """

    def __init__(self, world_size: Tuple[int, int] = (800, 600), use_llm: bool = False):
        self.world_size = world_size
        self.citizens: List[AICitizen] = []
        self.tick_count = 0
        self.simulation_time = 0.0
        self.use_llm = use_llm
        self.llm = None

        # Initialize LLM if requested
        if use_llm:
            try:
                from llm_integration import get_llm
                self.llm = get_llm()
                if self.llm.is_available():
                    print("LLM mode enabled - citizens will use Qwen 1.5B for decisions")
                else:
                    print("LLM failed to load - falling back to behavior trees")
                    self.use_llm = False
            except ImportError:
                print("LLM module not available - using behavior trees")
                self.use_llm = False

        # Event tracking
        self.events: List[SocialEvent] = []
        self.trade_proposals: List[TradeProposal] = []

        # Load citizen profiles (prefer CSV infrastructure if available)
        script_dir = os.path.dirname(__file__)
        csv_profiles_file = os.path.join(script_dir, '../db/citizen_profiles_from_csv.json')
        fallback_profiles_file = os.path.join(script_dir, '../db/citizen_profiles.json')

        if os.path.exists(csv_profiles_file):
            profiles_file = csv_profiles_file
            print("Loading 1000 citizens from CSV infrastructure...")
        else:
            profiles_file = fallback_profiles_file
            print("Loading default citizen profiles...")

        with open(profiles_file, 'r') as f:
            self.profiles_data = json.load(f)

        # Civilization metrics
        self.metrics = {
            'total_interactions': 0,
            'total_trades': 0,
            'total_wealth': 0,
            'wealth_gini': 0.0,
            'avg_relationship': 0.0,
            'conflict_count': 0,
            'cooperation_count': 0
        }

    def spawn_citizens(self, count: int = 20, profiles: List[str] = None):
        """
        Spawn citizens with diverse backgrounds.

        Args:
            count: Number of citizens to spawn
            profiles: Optional list of profile IDs to use. If None, random selection.
        """
        available_profiles = self.profiles_data['profiles']

        for i in range(count):
            # Select profile
            if profiles and i < len(profiles):
                profile_id = profiles[i]
                profile = next((p for p in available_profiles if p['id'] == profile_id), None)
            else:
                profile = random.choice(available_profiles)

            if profile is None:
                profile = random.choice(available_profiles)

            # Random starting position
            position = (
                random.randint(50, self.world_size[0] - 50),
                random.randint(50, self.world_size[1] - 50)
            )

            # Create citizen (with LLM if enabled)
            citizen = AICitizen(profile, position, use_llm=self.use_llm)
            self.citizens.append(citizen)

            print(f"Spawned {citizen.id} ({citizen.archetype}) at {position} with ${citizen.money}")

    def update(self, dt: float):
        """
        Update simulation by one tick.

        Args:
            dt: Delta time in seconds
        """
        self.tick_count += 1
        self.simulation_time += dt

        # Update all citizens (pass LLM if using)
        for citizen in self.citizens:
            citizen.update(dt, self.citizens, llm=self.llm)

        # Process social dynamics
        self._process_social_dynamics()

        # Process economic interactions
        self._process_economic_interactions()

        # Update metrics every 10 ticks
        if self.tick_count % 10 == 0:
            self._update_metrics()

        # Cleanup old events (keep last 1000)
        if len(self.events) > 1000:
            self.events = self.events[-1000:]

    def _process_social_dynamics(self):
        """Process emergent social interactions"""
        # Randomly trigger interactions between nearby citizens
        for citizen in self.citizens:
            if citizen.state != CitizenState.SOCIALIZING and len(citizen.perceived_citizens) > 0:
                # Extraverts more likely to initiate interaction
                if random.random() < citizen.personality['extraversion'] * 0.1:
                    other = random.choice(citizen.perceived_citizens)

                    # Check relationship - friends interact more
                    relationship = citizen.memory.get_relationship(other.id)
                    if relationship > -50:  # Not enemies
                        citizen.interact_with(other)

                        # Log event
                        self.events.append(SocialEvent(
                            event_type='interaction',
                            participants=[citizen.id, other.id],
                            outcome='success',
                            data={'relationship_before': relationship}
                        ))

                        self.metrics['total_interactions'] += 1

    def _process_economic_interactions(self):
        """Process trading and economic behaviors"""
        # Process pending trade proposals
        for proposal in self.trade_proposals[:]:
            proposer = self.get_citizen(proposal.proposer_id)
            recipient = self.get_citizen(proposal.recipient_id)

            if proposer and recipient:
                # Evaluate trade
                if recipient.evaluate_trade(
                    proposal.request_items, proposal.offer_items,
                    proposal.request_money, proposal.offer_money,
                    proposer
                ):
                    # Execute trade
                    self._execute_trade(proposer, recipient, proposal)
                    self.trade_proposals.remove(proposal)
                else:
                    # Trade rejected - small relationship penalty
                    proposer.memory.update_relationship(recipient.id, -1.0)
                    recipient.memory.update_relationship(proposer.id, -0.5)
                    self.trade_proposals.remove(proposal)

        # Spontaneous trading between nearby citizens
        for citizen in self.citizens:
            if citizen.state == CitizenState.SEEKING_RESOURCES and len(citizen.perceived_citizens) > 0:
                # Try to initiate trade
                if random.random() < 0.05:  # 5% chance per tick
                    other = random.choice(citizen.perceived_citizens)
                    self._attempt_spontaneous_trade(citizen, other)

    def _attempt_spontaneous_trade(self, citizen1: AICitizen, citizen2: AICitizen):
        """Attempt a spontaneous trade between two citizens"""
        # Simple trade: citizen1 wants items, offers money
        if not citizen2.items or citizen1.money < 10:
            return

        # Pick a random item from citizen2
        item = random.choice(citizen2.items)
        value = citizen2._value_item(item)

        # Citizen1 offers money for item
        offer_price = value * random.uniform(0.8, 1.2)  # 80-120% of value

        if citizen1.can_afford(offer_price):
            # Create proposal
            proposal = TradeProposal(
                proposer_id=citizen1.id,
                recipient_id=citizen2.id,
                offer_items=[],
                offer_money=offer_price,
                request_items=[item],
                request_money=0.0
            )
            self.trade_proposals.append(proposal)

    def _execute_trade(self, proposer: AICitizen, recipient: AICitizen, proposal: TradeProposal):
        """Execute a trade between two citizens"""
        # Transfer items from proposer to recipient
        for item in proposal.offer_items:
            if item in proposer.items:
                proposer.items.remove(item)
                recipient.items.append(item)
                proposer.stats['items_given'] += 1
                recipient.stats['items_received'] += 1

        # Transfer items from recipient to proposer
        for item in proposal.request_items:
            if item in recipient.items:
                recipient.items.remove(item)
                proposer.items.append(item)
                recipient.stats['items_given'] += 1
                proposer.stats['items_received'] += 1

        # Transfer money
        if proposal.offer_money > 0:
            proposer.money -= proposal.offer_money
            recipient.money += proposal.offer_money
            proposer.stats['money_spent'] += proposal.offer_money
            recipient.stats['money_earned'] += proposal.offer_money

        if proposal.request_money > 0:
            recipient.money -= proposal.request_money
            proposer.money += proposal.request_money
            recipient.stats['money_spent'] += proposal.request_money
            proposer.stats['money_earned'] += proposal.request_money

        # Update relationship (successful trade = positive)
        proposer.memory.update_relationship(recipient.id, 5.0)
        recipient.memory.update_relationship(proposer.id, 5.0)

        # Update stats
        proposer.stats['trades_completed'] += 1
        recipient.stats['trades_completed'] += 1

        # Log event
        self.events.append(SocialEvent(
            event_type='trade',
            participants=[proposer.id, recipient.id],
            outcome='success',
            data={
                'offer_items': proposal.offer_items,
                'offer_money': proposal.offer_money,
                'request_items': proposal.request_items,
                'request_money': proposal.request_money
            }
        ))

        self.metrics['total_trades'] += 1

    def _update_metrics(self):
        """Update civilization-level metrics"""
        if not self.citizens:
            return

        # Total wealth
        self.metrics['total_wealth'] = sum(c.money for c in self.citizens)

        # Wealth inequality (Gini coefficient)
        self.metrics['wealth_gini'] = self._calculate_gini_coefficient([c.money for c in self.citizens])

        # Average relationship
        all_relationships = []
        for citizen in self.citizens:
            all_relationships.extend(citizen.memory.relationships.values())

        if all_relationships:
            self.metrics['avg_relationship'] = np.mean(all_relationships)
        else:
            self.metrics['avg_relationship'] = 0.0

    def _calculate_gini_coefficient(self, values: List[float]) -> float:
        """Calculate Gini coefficient for wealth inequality (0 = perfect equality, 1 = perfect inequality)"""
        if not values or len(values) < 2:
            return 0.0

        sorted_values = sorted(values)
        n = len(sorted_values)
        index = np.arange(1, n + 1)
        return (2 * np.sum(index * sorted_values)) / (n * np.sum(sorted_values)) - (n + 1) / n

    def get_citizen(self, citizen_id: str) -> Optional[AICitizen]:
        """Get citizen by ID"""
        return next((c for c in self.citizens if c.id == citizen_id), None)

    def get_stats(self) -> Dict[str, Any]:
        """Get civilization statistics"""
        if not self.citizens:
            return {'error': 'No citizens'}

        return {
            'tick': self.tick_count,
            'simulation_time': self.simulation_time,
            'total_citizens': len(self.citizens),
            'total_interactions': self.metrics['total_interactions'],
            'total_trades': self.metrics['total_trades'],
            'total_wealth': self.metrics['total_wealth'],
            'wealth_gini': self.metrics['wealth_gini'],
            'avg_relationship': self.metrics['avg_relationship'],
            'avg_money': np.mean([c.money for c in self.citizens]),
            'avg_hunger': np.mean([c.needs.hunger for c in self.citizens]),
            'avg_energy': np.mean([c.needs.energy for c in self.citizens]),
            'avg_social': np.mean([c.needs.social for c in self.citizens]),
            'states': {
                state.name: sum(1 for c in self.citizens if c.state == state)
                for state in CitizenState
            },
            'recent_events': len([e for e in self.events if time.time() - e.timestamp < 60])
        }

    def export_data(self) -> Dict[str, Any]:
        """Export full simulation data for analysis"""
        return {
            'tick': self.tick_count,
            'simulation_time': self.simulation_time,
            'citizens': [c.to_dict() for c in self.citizens],
            'events': [
                {
                    'type': e.event_type,
                    'participants': e.participants,
                    'outcome': e.outcome,
                    'timestamp': e.timestamp,
                    'data': e.data
                }
                for e in self.events[-100:]  # Last 100 events
            ],
            'metrics': self.metrics.copy()
        }


if __name__ == "__main__":
    # Test civilization manager
    print("Testing Civilization Manager...")

    manager = CivilizationManager()
    manager.spawn_citizens(10)

    print(f"\nSpawned {len(manager.citizens)} citizens")

    # Simulate for 10 ticks
    for i in range(10):
        manager.update(1.0)
        stats = manager.get_stats()
        print(f"\nTick {stats['tick']}: "
              f"{stats['total_interactions']} interactions, "
              f"{stats['total_trades']} trades, "
              f"Gini: {stats['wealth_gini']:.3f}")
