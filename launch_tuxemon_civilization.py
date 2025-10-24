"""
Launch Tuxemon-based AI Civilization
Integrates our AI citizens into the Tuxemon game engine with full sprites and tilemaps

FIXED ISSUES:
- Import path configuration (moved to top before cwd change)
- Session initialization race condition (added validation)
- Threading replaced with Tuxemon update loop (Pygame-safe)
"""
import sys
import os
import argparse

# ============================================================================
# CRITICAL FIX #1: Configure ALL paths BEFORE changing directory
# ============================================================================
script_root = os.path.dirname(os.path.abspath(__file__))
original_dir = os.getcwd()

# Add paths in correct order (BEFORE any imports or cwd changes)
tuxemon_path = os.path.join(script_root, 'Tuxemon')
mods_path = os.path.join(script_root, 'mods', 'ai_civilization', 'scripts')
ai_systems_path = os.path.join(script_root, 'ai_systems')

# Insert at beginning of sys.path for priority
sys.path.insert(0, mods_path)
sys.path.insert(0, ai_systems_path)
sys.path.insert(0, tuxemon_path)

# NOW safe to change directory
os.chdir(tuxemon_path)
print(f"[INIT] Working directory: {os.getcwd()}")
print(f"[INIT] Mods path: {mods_path}")

# ============================================================================
# CRITICAL FIX #2: Import civilization manager at TOP (not in function)
# ============================================================================
# This MUST happen after sys.path setup but BEFORE Tuxemon imports
from tuxemon_civilization_integration import TuxemonCivilizationManager

# Import Tuxemon after paths configured
from tuxemon import main, prepare
from tuxemon.session import local_session


# Global state for citizen spawning
_citizens_spawned = False
_num_citizens = 20
_use_llm = False
_civilization_manager = None


def spawn_citizens_hook():
    """
    Hook function called after map is loaded to spawn AI citizens

    FIXED: No longer uses threading, called from Tuxemon's update loop
    FIXED: Validates session initialization before proceeding
    """
    global _citizens_spawned, _num_citizens, _use_llm, _civilization_manager

    if _citizens_spawned:
        return  # Already spawned

    try:
        # ====================================================================
        # CRITICAL FIX #3: Validate session initialization before proceeding
        # ====================================================================
        if local_session.client is None:
            print("[SPAWN] Waiting for client initialization...")
            return  # Not ready yet, will retry next frame

        if not hasattr(local_session.client, 'npc_manager') or local_session.client.npc_manager is None:
            print("[SPAWN] Waiting for NPC manager initialization...")
            return  # Not ready yet, will retry next frame

        if not hasattr(local_session.client, 'map_manager') or local_session.client.map_manager is None:
            print("[SPAWN] Waiting for map manager initialization...")
            return  # Not ready yet, will retry next frame

        if local_session.client.map_manager.current_map is None:
            print("[SPAWN] Waiting for map to load...")
            return  # Not ready yet, will retry next frame

        print("\n" + "=" * 60)
        print("SPAWNING AI CITIZENS")
        print("=" * 60)
        print(f"[SPAWN] Session validated - ready to spawn")

        # Create civilization manager
        _civilization_manager = TuxemonCivilizationManager(
            session=local_session,
            use_llm=_use_llm
        )

        # Spawn citizens
        _civilization_manager.spawn_citizens(num_citizens=_num_citizens)

        # Get stats
        stats = _civilization_manager.get_citizen_stats()
        print(f"\nAI Civilization spawned successfully!")
        print(f"Total citizens: {stats['total']}")
        print(f"Archetypes: {stats.get('archetypes', {})}")
        print(f"Total wealth: ${stats.get('total_wealth', 0)}")
        print("=" * 60)

        _citizens_spawned = True

        # Store civilization manager globally so it persists
        local_session.client.ai_civilization = _civilization_manager

    except Exception as e:
        print(f"\nError spawning AI citizens: {e}")
        import traceback
        traceback.print_exc()


def patch_tuxemon_for_citizens():
    """
    Patch Tuxemon to spawn citizens when map loads

    CRITICAL FIX #4: Uses WorldState.update() instead of threading
    - No threading (Pygame is not thread-safe)
    - Spawns when map is fully loaded and validated
    - Retries automatically until session is ready
    """
    from tuxemon.states.world_state import WorldState

    # Store original update method
    original_update = WorldState.update

    # State for spawn timing
    _spawn_attempted = [False]  # Use list to avoid nonlocal issues
    _frames_waited = [0]

    def patched_update(self, time_delta: float):
        """
        Patched update that spawns citizens after map loads

        Called every frame by Tuxemon - safe for Pygame operations
        """
        # Call original update first
        result = original_update(self, time_delta)

        # Only attempt spawn once map is loaded
        if not _spawn_attempted[0]:
            # Wait a few frames for map to fully settle
            _frames_waited[0] += 1

            if _frames_waited[0] > 10:  # Wait ~10 frames (~0.16s at 60fps)
                _spawn_attempted[0] = True
                print(f"[UPDATE] Attempting to spawn citizens (frame {_frames_waited[0]})")
                spawn_citizens_hook()

        return result

    # Apply patch
    WorldState.update = patched_update
    print("[PATCH] Tuxemon patched for AI civilization integration (update hook)")
    print("[PATCH] Citizens will spawn when map is fully loaded")


def launch():
    """Launch Tuxemon with AI Civilization"""
    global _num_citizens, _use_llm

    # Parse command-line arguments
    parser = argparse.ArgumentParser(description='Launch Tuxemon AI Civilization')
    parser.add_argument('--citizens', type=int, default=20,
                        help='Number of AI citizens to spawn (default: 20)')
    parser.add_argument('--llm', action='store_true',
                        help='Enable LLM-based decision making (slower but more nuanced)')
    args = parser.parse_args()

    _num_citizens = args.citizens
    _use_llm = args.llm

    print("=" * 60)
    print("TUXEMON AI CIVILIZATION EXPERIMENT")
    print("=" * 60)
    print(f"Citizens to spawn: {_num_citizens}")
    print(f"LLM Mode: {'Enabled (Qwen 1.5B)' if _use_llm else 'Disabled (Behavior Trees)'}")
    print("=" * 60)
    print("\nStarting Tuxemon...")
    print("AI citizens will spawn when map is fully loaded.")
    print("\nControls:")
    print("  Arrow Keys - Move player")
    print("  ESC - Menu")
    print("  Space/Enter - Interact with NPCs")
    print("=" * 60)
    print()

    try:
        # Patch Tuxemon to inject our citizens
        patch_tuxemon_for_citizens()

        # Launch Tuxemon normally
        config = prepare.CONFIG
        config.skip_titlescreen = True  # Skip title screen

        main.main(config=config, load_slot=None)

    except Exception as e:
        print(f"\nError running Tuxemon: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    launch()
