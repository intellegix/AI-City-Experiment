"""
AI Citizen NPC - Tuxemon Integration
Extends Tuxemon's NPC class with AI citizen behavior
"""
import sys
import os
import json
import random
from typing import Dict, List, Optional, Tuple, TYPE_CHECKING

# Add Tuxemon to path
tuxemon_path = os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Tuxemon')
if tuxemon_path not in sys.path:
    sys.path.insert(0, tuxemon_path)

from tuxemon.npc import NPC
from tuxemon.db import Direction

# Import our AI citizen logic
from ai_citizen import AICitizen

if TYPE_CHECKING:
    from tuxemon.session import Session


class AICitizenNPC(NPC):
    """
    Tuxemon NPC with AI citizen decision-making

    This class bridges Tuxemon's visual NPC system with our custom
    AI citizen behavior (needs, personality, memory, relationships).
    """

    def __init__(
        self,
        npc_slug: str,
        *,
        session: 'Session',
        citizen_profile: Dict,
        use_llm: bool = False
    ):
        """
        Initialize an AI citizen NPC

        Args:
            npc_slug: Tuxemon NPC slug identifier
            session: Tuxemon game session
            citizen_profile: AI citizen profile data (from CSV)
            use_llm: Whether to use LLM for decision-making
        """
        # Initialize Tuxemon NPC base class
        super().__init__(npc_slug=npc_slug, session=session)

        # Create our AI citizen with the profile
        self.ai_citizen = AICitizen(
            profile=citizen_profile,
            position=(0, 0),  # Position will be set on map
            use_llm=use_llm
        )

        # Set the NPC name to match citizen name
        if 'name' in citizen_profile:
            self.name = citizen_profile['name']
        elif 'id' in citizen_profile:
            self.name = citizen_profile['id'].replace('_', ' ').title()

        # Wandering behavior
        self.behavior = "wander"
        self.wander_cooldown = 0.0
        self.wander_interval = random.uniform(2.0, 5.0)

        # AI update timing
        self.ai_update_accumulator = 0.0
        self.ai_update_interval = 1.0  # Update AI once per second

    def update(self, time_delta: float) -> None:
        """
        Update both Tuxemon NPC and AI citizen logic

        Args:
            time_delta: Time elapsed since last update (seconds)
        """
        # Update Tuxemon NPC (movement, animations, etc.)
        super().update(time_delta)

        # Update AI citizen decision-making
        self.ai_update_accumulator += time_delta
        if self.ai_update_accumulator >= self.ai_update_interval:
            self.ai_update_accumulator = 0.0
            self._update_ai_citizen(self.ai_update_interval)

        # Handle autonomous wandering when not moving
        if self.behavior == "wander" and not self.moving:
            self.wander_cooldown -= time_delta
            if self.wander_cooldown <= 0:
                self._wander()
                self.wander_cooldown = self.wander_interval

    def _update_ai_citizen(self, dt: float) -> None:
        """
        Update AI citizen decision-making

        This synchronizes the citizen's position with Tuxemon coordinates
        and processes AI behavior.
        """
        # Sync position from Tuxemon to AI citizen
        self.ai_citizen.position = (
            self.position.x,
            self.position.y
        )

        # Update AI citizen logic
        # Note: We don't pass other citizens here yet - could be added
        # for more sophisticated social interactions
        self.ai_citizen.update(dt, all_citizens=[])

        # Sync some state back (future: could influence wandering based on needs)
        # For now, AI runs in parallel to basic wandering

    def _wander(self) -> None:
        """
        Make the NPC wander in a random direction

        Uses Tuxemon's pathfinding to move to a nearby tile.
        """
        if random.random() < 0.3:  # 30% chance to stand still
            return

        # Pick a random direction
        directions = [Direction.up, Direction.down, Direction.left, Direction.right]
        direction = random.choice(directions)

        # Move one tile in that direction
        self.move_one_tile(direction)

    def get_dialog_text(self) -> str:
        """
        Generate dialog text based on AI citizen state

        Returns:
            Dialog string to display when player interacts
        """
        # Use citizen's needs and personality to generate dialog
        citizen = self.ai_citizen

        # Simple dialog based on highest need
        needs = citizen.needs
        max_need = max(needs, key=needs.get)

        greetings = [
            f"Hello! I'm {self.name}.",
            f"Hi there! Name's {self.name}.",
            f"Greetings! I'm {self.name}."
        ]

        need_statements = {
            "hunger": [
                "I'm feeling quite hungry...",
                "Do you know where I can find some food?",
                "I could really use a meal right now."
            ],
            "energy": [
                "I'm exhausted...",
                "I need to rest soon.",
                "I'm running on empty here."
            ],
            "social": [
                "It's nice to meet someone new!",
                "I enjoy talking to people.",
                "Always happy to make a new friend!"
            ],
            "wealth": [
                "I'm trying to save up some money.",
                "Times are tough financially...",
                "I wish I had more resources."
            ]
        }

        greeting = random.choice(greetings)

        if needs[max_need] > 70:  # High need
            statement = random.choice(need_statements.get(max_need, ["I'm doing alright."]))
            return f"{greeting} {statement}"
        else:
            return f"{greeting} I'm doing well, thanks for asking!"

    @property
    def citizen_id(self) -> str:
        """Get the citizen's unique ID"""
        return self.ai_citizen.id

    @property
    def citizen_archetype(self) -> str:
        """Get the citizen's archetype"""
        return self.ai_citizen.archetype

    @property
    def citizen_money(self) -> int:
        """Get the citizen's money"""
        return int(self.ai_citizen.money)
