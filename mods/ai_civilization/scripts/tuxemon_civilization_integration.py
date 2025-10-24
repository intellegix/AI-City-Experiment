"""
Tuxemon AI Civilization Integration
Spawns AI citizens as Tuxemon NPCs on a map
"""
import sys
import os
import json
import random
from typing import Dict, List, Optional

# Add paths
script_dir = os.path.dirname(__file__)
tuxemon_path = os.path.join(script_dir, '..', '..', '..', 'Tuxemon')
if tuxemon_path not in sys.path:
    sys.path.insert(0, tuxemon_path)

from ai_citizen_npc import AICitizenNPC
from npc_registrar import AICitizenNPCRegistrar


class TuxemonCivilizationManager:
    """
    Manages AI civilization within Tuxemon

    Handles:
    - Loading citizen profiles
    - Creating NPC database entries
    - Spawning citizens on maps
    - Sprite assignment based on archetypes
    """

    def __init__(self, session, use_llm: bool = False):
        """
        Initialize the civilization manager

        Args:
            session: Tuxemon game session
            use_llm: Whether to use LLM for citizen decision-making
        """
        self.session = session
        self.use_llm = use_llm
        self.citizens: List[AICitizenNPC] = []

        # Load configurations
        self.config_dir = os.path.join(script_dir, '..', 'config')
        self.sprite_mapping = self._load_sprite_mapping()

        # Create NPC registrar
        self.registrar = AICitizenNPCRegistrar(self.sprite_mapping)

        # Load citizen profiles
        self.profiles_path = os.path.join(
            script_dir, '..', 'db', 'citizen_profiles_from_csv.json'
        )
        self.citizen_profiles = self._load_citizen_profiles()

        print(f"TuxemonCivilizationManager initialized with {len(self.citizen_profiles)} citizen profiles")

    def _load_sprite_mapping(self) -> Dict:
        """Load sprite-to-archetype mapping"""
        mapping_path = os.path.join(self.config_dir, 'sprite_mapping.json')
        try:
            with open(mapping_path, 'r') as f:
                return json.load(f)
        except FileNotFoundError:
            print(f"Warning: Sprite mapping not found at {mapping_path}, using defaults")
            return {
                "archetype_sprites": {"default": ["adventurer", "villager", "bob"]},
                "color_variants": {}
            }

    def _load_citizen_profiles(self) -> List[Dict]:
        """Load citizen profiles from JSON"""
        try:
            with open(self.profiles_path, 'r') as f:
                data = json.load(f)
                # Handle both list and dict formats
                if isinstance(data, list):
                    return data
                elif isinstance(data, dict) and 'profiles' in data:
                    return data['profiles']
                elif isinstance(data, dict) and 'citizens' in data:
                    return data['citizens']
                else:
                    print(f"Warning: Unexpected citizen profile format - expected 'profiles' or 'citizens' key")
                    print(f"Available keys: {list(data.keys())}")
                    return []
        except FileNotFoundError:
            print(f"Warning: Citizen profiles not found at {self.profiles_path}")
            return []
        except Exception as e:
            print(f"Error loading citizen profiles: {e}")
            return []

    def get_sprite_for_citizen(self, profile: Dict) -> str:
        """
        Select an appropriate sprite based on citizen archetype

        Args:
            profile: Citizen profile dictionary

        Returns:
            Sprite name to use for this citizen
        """
        archetype = profile.get('archetype', 'default')

        # Get possible sprites for this archetype
        archetype_sprites = self.sprite_mapping.get('archetype_sprites', {})
        sprite_options = archetype_sprites.get(archetype, archetype_sprites.get('default', ['adventurer']))

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

    def create_npc_slug(self, profile: Dict) -> str:
        """
        Create a unique NPC slug for this citizen

        Args:
            profile: Citizen profile

        Returns:
            NPC slug string
        """
        citizen_id = profile.get('id', 'citizen_unknown')
        # NPC slugs must be unique
        return f"ai_civ_{citizen_id}"

    def spawn_citizens(self, num_citizens: int = 20, map_name: Optional[str] = None) -> None:
        """
        Spawn AI citizens as NPCs on the current map

        Args:
            num_citizens: Number of citizens to spawn
            map_name: Name of the map to spawn on (None = current map)
        """
        if not self.citizen_profiles:
            print("Error: No citizen profiles loaded!")
            return

        # Sample citizens from the pool
        num_to_spawn = min(num_citizens, len(self.citizen_profiles))
        selected_profiles = random.sample(self.citizen_profiles, num_to_spawn)

        print(f"Spawning {num_to_spawn} AI citizens on map...")

        for i, profile in enumerate(selected_profiles):
            self._spawn_citizen(profile, i, num_to_spawn)

        print(f"Successfully spawned {len(self.citizens)} AI citizens")

    def _spawn_citizen(self, profile: Dict, index: int, total_citizens: int) -> None:
        """
        Spawn a single citizen as a Tuxemon NPC

        Args:
            profile: Citizen profile
            index: Spawn index (for positioning)
            total_citizens: Total number of citizens being spawned
        """
        try:
            # Register citizen in Tuxemon's NPC database
            npc_slug = self.registrar.register_citizen(profile)

            # Get sprite name for logging
            sprite_name = self.get_sprite_for_citizen(profile)

            # Create the AI Citizen NPC (now that it's registered in DB)
            citizen_npc = AICitizenNPC(
                npc_slug=npc_slug,
                session=self.session,
                citizen_profile=profile,
                use_llm=self.use_llm
            )

            # Position the citizen on the map
            # Use a grid pattern to avoid overlap
            grid_size = int(total_citizens ** 0.5) + 1
            x = (index % grid_size) * 3 + 5  # Spread out on X axis
            y = (index // grid_size) * 3 + 5  # Spread out on Y axis

            citizen_npc.set_position((x, y, 0))

            # CRITICAL: Load sprites (makes NPC visible)
            # FIXED: Convert dict to NpcTemplateModel before passing to load_sprites()
            # The registrar stores raw dicts, but load_sprites() expects a Pydantic model
            from tuxemon.db import db, NpcTemplateModel
            npc_data_dict = db.database['npc'][npc_slug]

            # Convert the template dict to NpcTemplateModel object
            template_dict = npc_data_dict['template']
            template_model = NpcTemplateModel(**template_dict)

            # NOW safe to pass to load_sprites (expects NpcTemplateModel)
            citizen_npc.sprite_controller.load_sprites(template_model)

            # Add to NPC manager
            self.session.client.npc_manager.add_npc(citizen_npc)

            # Track our citizens
            self.citizens.append(citizen_npc)

            print(f"  Spawned: {profile.get('id', 'unknown')} as {sprite_name} at ({x}, {y})")

        except Exception as e:
            print(f"  Error spawning citizen {profile.get('id', 'unknown')}: {e}")

    def update(self, dt: float) -> None:
        """
        Update all AI citizens

        Args:
            dt: Time delta in seconds
        """
        # Citizens are updated automatically by Tuxemon's NPC manager
        # This method is for any civilization-level logic
        pass

    def get_citizen_stats(self) -> Dict:
        """
        Get statistics about the civilization

        Returns:
            Dictionary with stats
        """
        if not self.citizens:
            return {"total": 0}

        archetypes = {}
        total_wealth = 0

        for citizen in self.citizens:
            archetype = citizen.citizen_archetype
            archetypes[archetype] = archetypes.get(archetype, 0) + 1
            total_wealth += citizen.citizen_money

        return {
            "total": len(self.citizens),
            "archetypes": archetypes,
            "total_wealth": total_wealth,
            "avg_wealth": total_wealth / len(self.citizens) if self.citizens else 0
        }
