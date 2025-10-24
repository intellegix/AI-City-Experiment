"""
AI Citizen NPC Registrar
Dynamically registers AI citizens in Tuxemon's NPC database at runtime
"""
import sys
import os
import json
import random
from typing import Dict, Optional

# Add Tuxemon to path
script_dir = os.path.dirname(__file__)
tuxemon_path = os.path.join(script_dir, '..', '..', '..', 'Tuxemon')
if tuxemon_path not in sys.path:
    sys.path.insert(0, tuxemon_path)

from tuxemon.db import db


class AICitizenNPCRegistrar:
    """
    Dynamically registers AI citizens as Tuxemon NPCs at runtime
    """

    def __init__(self, sprite_mapping: Dict):
        """
        Initialize the registrar

        Args:
            sprite_mapping: Mapping of archetypes to sprites
        """
        self.sprite_mapping = sprite_mapping
        self.registered_citizens = set()

    def register_citizen(self, citizen_profile: Dict) -> str:
        """
        Register a single AI citizen in Tuxemon's NPC database

        Args:
            citizen_profile: Citizen profile from AI system

        Returns:
            NPC slug for the registered citizen
        """
        citizen_id = citizen_profile.get('id', 'citizen_unknown')
        npc_slug = f"ai_civ_{citizen_id}"

        # Skip if already registered
        if npc_slug in self.registered_citizens:
            return npc_slug

        # Get sprite for this citizen
        sprite_name = self._get_sprite_for_archetype(
            citizen_profile.get('archetype', 'default')
        )

        # Create NPC data structure matching Tuxemon's format
        npc_data = {
            "slug": npc_slug,
            "speech": {
                "profile": {
                    "default": {}  # Empty profile for now
                }
            },
            "combat": {
                "forfeit": True,
                "switch_logic": "random"
            },
            "template": {
                "sprite_name": sprite_name,
                "combat_front": sprite_name,
                "slug": "noclass"
            },
            "monsters": [],
            "items": []
        }

        # Dynamically add to Tuxemon's database
        # This bypasses the need for JSON files
        try:
            # Add entry without validation (since we don't have translation files)
            db.database['npc'][npc_slug] = npc_data
            self.registered_citizens.add(npc_slug)
            print(f"  Registered NPC in database: {npc_slug} ({sprite_name})")
            return npc_slug

        except Exception as e:
            print(f"  Error registering NPC {npc_slug}: {e}")
            raise

    def _get_sprite_for_archetype(self, archetype: str) -> str:
        """
        Select an appropriate sprite based on citizen archetype

        Args:
            archetype: Citizen archetype

        Returns:
            Sprite name to use for this citizen
        """
        archetype_sprites = self.sprite_mapping.get('archetype_sprites', {})
        sprite_options = archetype_sprites.get(
            archetype,
            archetype_sprites.get('default', ['adventurer'])
        )

        # Pick a base sprite
        base_sprite = random.choice(sprite_options)

        # Try to add color variation
        color_variants = self.sprite_mapping.get('color_variants', {})
        if base_sprite in color_variants:
            all_variants = color_variants[base_sprite]
            selected_sprite = random.choice(all_variants)
        else:
            selected_sprite = base_sprite

        return selected_sprite
