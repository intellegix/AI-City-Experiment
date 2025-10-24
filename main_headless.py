"""
AI City Simulation - Headless/Terminal Mode for Termux
Text-based simulation without graphics requirements

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import numpy as np
import argparse
import sys
import time
import os
from datetime import datetime

try:
    from config_android import Config, PERFORMANCE, NPC
except ImportError:
    from config import Config, PERFORMANCE, NPC

from terrain_generator import TerrainGenerator
from city_generator import CityLayoutGenerator
from npc_system import NPCManager, NPCType


class HeadlessCitySimulation:
    """
    Headless simulation controller for terminal/text mode.
    Runs simulation and outputs statistics without graphics.
    """

    def __init__(self, seed: int = None, npc_count: int = 10, grid_size: int = 256, duration: int = 60):
        """
        Initialize headless simulation.

        Args:
            seed: Random seed for reproducibility
            npc_count: Number of NPCs to spawn
            grid_size: Size of world grid
            duration: Simulation duration in seconds
        """
        print("=" * 80)
        print("AI CITY SIMULATION - HEADLESS MODE")
        print("Crafted by Intellegix - Optimized for Termux")
        print("=" * 80)
        print()

        if seed:
            Config.set_seed(seed)
            print(f"✓ Using seed: {seed}")

        self.grid_size = grid_size
        self.npc_count = min(npc_count, NPC.MAX_NPC_COUNT)
        self.duration = duration
        self.running = False
        self.start_time = None

        # Statistics
        self.stats = {
            'total_ticks': 0,
            'npc_actions': 0,
            'avg_tick_time': 0,
            'npc_states': {}
        }

        print(f"✓ Grid size: {grid_size}x{grid_size}")
        print(f"✓ NPC count: {self.npc_count}")
        print(f"✓ Duration: {duration}s")
        print()

        self._initialize_world()

    def _initialize_world(self):
        """Initialize the game world"""
        print("Initializing world...")
        print()

        # Generate terrain
        print("[1/4] Generating terrain...")
        self.terrain_gen = TerrainGenerator(size=self.grid_size)
        heightmap, biomemap = self.terrain_gen.generate()
        print(f"      ✓ Terrain generated ({self.grid_size}x{self.grid_size})")

        # Generate city
        print("[2/4] Generating city layout...")
        self.city_gen = CityLayoutGenerator(self.terrain_gen)
        self.roads, self.zones, self.buildings = self.city_gen.generate()
        print(f"      ✓ City layout complete")
        print(f"      ✓ Roads: {np.count_nonzero(self.roads)} cells")
        print(f"      ✓ Buildings: {len(self.buildings)} structures")

        # Initialize NPCs
        print("[3/4] Spawning NPCs...")
        self.npc_manager = NPCManager(self.city_gen)

        # Spawn NPCs
        self.npc_manager.spawn_random_npcs(self.npc_count)
        print(f"      ✓ {self.npc_count} NPCs spawned")

        # Final setup
        print("[4/4] Finalizing...")
        print()
        print("=" * 80)
        print("WORLD READY")
        print("=" * 80)
        print()

    def _print_status(self, elapsed):
        """Print current simulation status"""
        os.system('clear' if os.name != 'nt' else 'cls')

        print("=" * 80)
        print(f"AI CITY SIMULATION - {datetime.now().strftime('%H:%M:%S')}")
        print("=" * 80)
        print()
        print(f"Runtime: {elapsed:.1f}s / {self.duration}s")
        print(f"Progress: [{'#' * int(30 * elapsed / self.duration)}{'-' * int(30 * (1 - elapsed / self.duration))}]")
        print()

        # NPC Statistics
        print("NPC STATISTICS:")
        print("-" * 80)
        npc_states = {}
        for npc in self.npc_manager.npcs:
            state = npc.state if hasattr(npc, 'state') else 'Unknown'
            npc_states[state] = npc_states.get(state, 0) + 1

        for state, count in sorted(npc_states.items(), key=lambda x: str(x[0])):
            bar = '█' * count
            state_name = state.name if hasattr(state, 'name') else str(state)
            print(f"  {state_name:15s}: {bar} ({count})")

        print()
        print("PERFORMANCE:")
        print("-" * 80)
        print(f"  Total Ticks: {self.stats['total_ticks']}")
        print(f"  Avg Tick Time: {self.stats['avg_tick_time']:.4f}s")
        print(f"  Ticks/Second: {1/self.stats['avg_tick_time']:.1f}" if self.stats['avg_tick_time'] > 0 else "  Ticks/Second: N/A")
        print()

        # Sample NPC info
        if self.npc_manager.npcs:
            npc = self.npc_manager.npcs[0]
            print("SAMPLE NPC (ID: 0):")
            print("-" * 80)
            print(f"  Type: {npc.npc_type.name if hasattr(npc, 'npc_type') else 'Unknown'}")
            print(f"  Position: ({npc.position[0]:.1f}, {npc.position[1]:.1f})")
            print(f"  State: {npc.state.name if hasattr(npc, 'state') else 'Unknown'}")
            if hasattr(npc, 'needs'):
                print(f"  Hunger: {'█' * int(npc.needs.hunger / 10)}{'-' * (10 - int(npc.needs.hunger / 10))} {npc.needs.hunger:.1f}%")
                print(f"  Energy: {'█' * int(npc.needs.energy / 10)}{'-' * (10 - int(npc.needs.energy / 10))} {npc.needs.energy:.1f}%")
                print(f"  Social: {'█' * int(npc.needs.social / 10)}{'-' * (10 - int(npc.needs.social / 10))} {npc.needs.social:.1f}%")

        print()
        print("Press CTRL+C to stop simulation")
        print("=" * 80)

    def run(self):
        """Run the headless simulation"""
        self.running = True
        self.start_time = time.time()
        dt = 1.0 / 30  # 30 updates per second
        last_update = time.time()

        print("Starting simulation...")
        print("Press CTRL+C to stop")
        print()

        try:
            while self.running:
                current_time = time.time()
                elapsed = current_time - self.start_time

                # Check if duration exceeded
                if elapsed >= self.duration:
                    print("\nSimulation duration complete!")
                    break

                # Update simulation
                tick_start = time.time()
                self.npc_manager.update_all(dt)
                tick_time = time.time() - tick_start

                # Update statistics
                self.stats['total_ticks'] += 1
                self.stats['avg_tick_time'] = (
                    (self.stats['avg_tick_time'] * (self.stats['total_ticks'] - 1) + tick_time)
                    / self.stats['total_ticks']
                )

                # Print status every second
                if current_time - last_update >= 1.0:
                    self._print_status(elapsed)
                    last_update = current_time

                # Sleep to maintain update rate
                sleep_time = max(0, dt - (time.time() - current_time))
                if sleep_time > 0:
                    time.sleep(sleep_time)

        except KeyboardInterrupt:
            print("\n\nSimulation interrupted by user")

        finally:
            self.running = False
            self._print_final_stats()

    def _print_final_stats(self):
        """Print final simulation statistics"""
        elapsed = time.time() - self.start_time

        print()
        print("=" * 80)
        print("SIMULATION COMPLETE")
        print("=" * 80)
        print()
        print(f"Total Runtime: {elapsed:.1f}s")
        print(f"Total Ticks: {self.stats['total_ticks']}")
        print(f"Average Tick Time: {self.stats['avg_tick_time']:.4f}s")
        print(f"Average TPS: {self.stats['total_ticks'] / elapsed:.1f}")
        print()
        print("Thank you for using AI City Simulation!")
        print("=" * 80)


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(
        description='AI City Simulation - Headless Mode for Termux'
    )
    parser.add_argument(
        '--seed',
        type=int,
        default=None,
        help='Random seed for reproducibility'
    )
    parser.add_argument(
        '--npc-count',
        type=int,
        default=10,
        help=f'Number of NPCs (max {NPC.MAX_NPC_COUNT})'
    )
    parser.add_argument(
        '--grid-size',
        type=int,
        default=256,
        help='Size of world grid (default: 256)'
    )
    parser.add_argument(
        '--duration',
        type=int,
        default=60,
        help='Simulation duration in seconds (default: 60)'
    )

    args = parser.parse_args()

    # Create and run simulation
    sim = HeadlessCitySimulation(
        seed=args.seed,
        npc_count=args.npc_count,
        grid_size=args.grid_size,
        duration=args.duration
    )
    sim.run()

    return 0


if __name__ == '__main__':
    sys.exit(main())
