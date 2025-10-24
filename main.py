"""
AI City Simulation - Main Application
Complete procedural city simulation with emergent AI NPCs

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
See LICENSE and NOTICE files for details.

Based on the comprehensive blueprint for AI-powered game development.
All phases implemented:
- Phase 1: Environment Setup & Configuration
- Phase 2: Terrain & World Generation
- Phase 3: City Layout & Asset Placement
- Phase 4: NPC Framework & Emergent AI
- Phase 5: Polish, Testing & Debug

Crafted by Intellegix - https://intellegix.ai
"""
import pygame
import numpy as np
import argparse
import sys
import time

from config import Config, PERFORMANCE, NPC
from terrain_generator import TerrainGenerator
from city_generator import CityLayoutGenerator
from npc_system import NPCManager, NPCType
from renderer import CityRenderer


class CitySimulation:
    """
    Main simulation controller.
    Manages world generation, NPC updates, and rendering.
    """

    def __init__(self, seed: int = None, npc_count: int = 100, grid_size: int = 512):
        """
        Initialize simulation.

        Args:
            seed: Random seed for reproducibility
            npc_count: Number of NPCs to spawn
            grid_size: Size of world grid
        """
        print("=" * 80)
        print("AI CITY SIMULATION")
        print("Crafted by Intellegix")
        print("=" * 80)
        print()

        # Set random seed
        if seed is not None:
            Config.set_seed(seed)
            print(f"Random seed: {seed}")
        else:
            seed = np.random.randint(0, 1000000)
            Config.set_seed(seed)
            print(f"Generated random seed: {seed}")

        self.seed = seed
        self.grid_size = grid_size

        # World components
        self.terrain: TerrainGenerator = None
        self.city: CityLayoutGenerator = None
        self.npc_manager: NPCManager = None
        self.renderer: CityRenderer = None

        # Simulation state
        self.running = False
        self.paused = False
        self.simulation_time = 0.0

        # Performance tracking
        self.frame_count = 0
        self.start_time = 0

        # Generate world
        self._generate_world(npc_count)

    def _generate_world(self, npc_count: int):
        """Generate the complete world"""
        print("\n" + "=" * 80)
        print("WORLD GENERATION")
        print("=" * 80)

        # Phase 2: Terrain Generation
        print("\n[Phase 2: Terrain & World Generation]")
        start = time.time()
        self.terrain = TerrainGenerator(size=self.grid_size, seed=self.seed)
        self.terrain.generate()
        print(f"[OK] Terrain generated in {time.time() - start:.2f}s")

        # Phase 3: City Layout
        print("\n[Phase 3: City Layout & Asset Placement]")
        start = time.time()
        self.city = CityLayoutGenerator(self.terrain, seed=self.seed)
        self.city.generate()
        print(f"[OK] City layout generated in {time.time() - start:.2f}s")

        # Phase 4: NPC System
        print("\n[Phase 4: NPC Framework & Emergent AI]")
        start = time.time()
        self.npc_manager = NPCManager(self.city)
        self.npc_manager.spawn_random_npcs(min(npc_count, PERFORMANCE.MAX_NPC_COUNT))
        print(f"[OK] {len(self.npc_manager.npcs)} NPCs spawned in {time.time() - start:.2f}s")

        # Phase 5: Rendering Setup
        print("\n[Phase 5: Rendering & Visualization]")
        start = time.time()
        self.renderer = CityRenderer()
        self.renderer.set_world(self.terrain, self.city, self.npc_manager)
        print(f"[OK] Renderer initialized in {time.time() - start:.2f}s")

        print("\n" + "=" * 80)
        print("WORLD GENERATION COMPLETE")
        print("=" * 80)
        print()

        self._print_world_stats()

    def _print_world_stats(self):
        """Print statistics about the generated world"""
        print("\nWorld Statistics:")
        print(f"  Grid Size: {self.grid_size}x{self.grid_size}")
        print(f"  Terrain Seed: {self.seed}")
        print(f"  Buildings: {len(self.city.buildings)}")
        print(f"  Road Coverage: {np.sum(self.city.road_grid) / (self.grid_size ** 2) * 100:.1f}%")
        print(f"  NPCs: {len(self.npc_manager.npcs)}")

        npc_stats = self.npc_manager.get_npc_stats()
        if npc_stats:
            print(f"\nNPC Distribution:")
            for npc_type, count in npc_stats['by_type'].items():
                if count > 0:
                    print(f"    {npc_type}: {count}")

        print()

    def run(self):
        """Main simulation loop"""
        self.running = True
        self.start_time = time.time()

        print("=" * 80)
        print("SIMULATION STARTED")
        print("=" * 80)
        print("\nControls:")
        print("  WASD     - Move camera")
        print("  Q/E      - Zoom in/out")
        print("  Space    - Pause/Resume")
        print("  D        - Toggle debug info")
        print("  ESC      - Quit")
        print()

        last_time = time.time()
        last_stats_time = time.time()

        while self.running:
            # Calculate delta time
            current_time = time.time()
            dt = current_time - last_time
            last_time = current_time

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        self.running = False
                    elif event.key == pygame.K_SPACE:
                        self.paused = not self.paused
                        print(f"Simulation {'paused' if self.paused else 'resumed'}")

            # Handle input
            self.renderer.handle_input(events)

            # Update simulation
            if not self.paused:
                self.npc_manager.update_all(dt)
                self.simulation_time += dt

            # Render
            self.renderer.render_frame(dt)
            self.renderer.tick()

            self.frame_count += 1

            # Print stats every 5 seconds
            if current_time - last_stats_time > 5.0:
                self._print_performance_stats()
                last_stats_time = current_time

        self.shutdown()

    def _print_performance_stats(self):
        """Print performance statistics"""
        elapsed = time.time() - self.start_time
        avg_fps = self.frame_count / elapsed if elapsed > 0 else 0

        npc_stats = self.npc_manager.get_npc_stats()

        print(f"\n[Stats] FPS: {avg_fps:.1f} | NPCs: {npc_stats.get('total', 0)} | "
              f"Simulation Time: {self.simulation_time:.1f}s")

        # Check performance targets
        if avg_fps < PERFORMANCE.MIN_FPS:
            print(f"  [WARNING] FPS below target ({PERFORMANCE.MIN_FPS})")

    def shutdown(self):
        """Clean shutdown"""
        print("\n" + "=" * 80)
        print("SIMULATION ENDED")
        print("=" * 80)

        elapsed = time.time() - self.start_time
        avg_fps = self.frame_count / elapsed if elapsed > 0 else 0

        print(f"\nFinal Statistics:")
        print(f"  Total Runtime: {elapsed:.1f}s")
        print(f"  Simulation Time: {self.simulation_time:.1f}s")
        print(f"  Total Frames: {self.frame_count}")
        print(f"  Average FPS: {avg_fps:.1f}")

        npc_stats = self.npc_manager.get_npc_stats()
        print(f"\nNPC Final State:")
        print(f"  Total NPCs: {npc_stats.get('total', 0)}")
        print(f"  Avg Hunger: {npc_stats.get('avg_hunger', 0):.1f}%")
        print(f"  Avg Energy: {npc_stats.get('avg_energy', 0):.1f}%")
        print(f"  Avg Social: {npc_stats.get('avg_social', 0):.1f}%")

        print("\nThank you for using AI City Simulation!")
        print()

        pygame.quit()


def parse_arguments():
    """Parse command line arguments"""
    parser = argparse.ArgumentParser(
        description="AI City Simulation - Procedural city with emergent AI NPCs\nCrafted by Intellegix",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python main.py                          # Run with default settings
  python main.py --seed 42 --npcs 200     # Custom seed and NPC count
  python main.py --size 1024 --npcs 500   # Larger world with more NPCs

Performance Notes:
  - Grid sizes: 256 (fast), 512 (default), 1024 (slow)
  - NPC counts: 50-500 recommended depending on hardware
  - Use smaller grids for lower-end hardware

License:
  Copyright 2025 Intellegix
  Licensed under the Apache License, Version 2.0
  See LICENSE and NOTICE files for details.
        """
    )

    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for world generation (default: random)'
    )

    parser.add_argument(
        '--npcs',
        type=int,
        default=100,
        help=f'Number of NPCs to spawn (default: 100, max: {PERFORMANCE.MAX_NPC_COUNT})'
    )

    parser.add_argument(
        '--size',
        type=int,
        default=512,
        choices=[256, 512, 1024],
        help='World grid size (default: 512)'
    )

    return parser.parse_args()


def main():
    """Main entry point"""
    # Parse arguments
    args = parse_arguments()

    # Validate NPC count
    npc_count = min(args.npcs, PERFORMANCE.MAX_NPC_COUNT)
    if args.npcs > PERFORMANCE.MAX_NPC_COUNT:
        print(f"Warning: NPC count capped at {PERFORMANCE.MAX_NPC_COUNT}")

    try:
        # Create and run simulation
        simulation = CitySimulation(
            seed=args.seed,
            npc_count=npc_count,
            grid_size=args.size
        )

        simulation.run()

    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user")
        sys.exit(0)

    except Exception as e:
        print(f"\n\nError during simulation: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()
