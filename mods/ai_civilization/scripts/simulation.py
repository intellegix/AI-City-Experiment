"""
AI Civilization Simulation - Main Entry Point
Supports both real-time visualization and headless background execution

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
import pygame
import json
import sys
import time
import argparse
from pathlib import Path
from typing import Optional
from civilization_manager import CivilizationManager, CitizenState
from ai_citizen import AICitizen


class SimulationVisualizer:
    """Real-time visualization of the AI civilization"""

    def __init__(self, manager: CivilizationManager, width: int = 1280, height: int = 720):
        pygame.init()
        self.manager = manager
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("AI Civilization Experiment")

        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 20)
        self.large_font = pygame.font.Font(None, 36)

        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'citizen': (50, 50, 200),
            'idle': (100, 100, 255),
            'working': (255, 150, 50),
            'socializing': (50, 255, 50),
            'trading': (255, 215, 0),
            'resting': (150, 150, 200),
            'seeking': (255, 100, 100),
            'traveling': (100, 200, 255),
            'text': (0, 0, 0),
            'relationship_positive': (0, 200, 0),
            'relationship_negative': (200, 0, 0),
            'relationship_neutral': (150, 150, 150)
        }

        # State colors mapping
        self.state_colors = {
            CitizenState.IDLE: self.colors['idle'],
            CitizenState.WORKING: self.colors['working'],
            CitizenState.SOCIALIZING: self.colors['socializing'],
            CitizenState.TRADING: self.colors['trading'],
            CitizenState.RESTING: self.colors['resting'],
            CitizenState.SEEKING_RESOURCES: self.colors['seeking'],
            CitizenState.TRAVELING: self.colors['traveling']
        }

        self.show_relationships = False
        self.show_stats = True
        self.paused = False

    def render(self):
        """Render the simulation"""
        self.screen.fill(self.colors['background'])

        # Draw relationships first (as lines)
        if self.show_relationships:
            self._draw_relationships()

        # Draw citizens
        self._draw_citizens()

        # Draw UI
        if self.show_stats:
            self._draw_stats()

        # Draw controls
        self._draw_controls()

        pygame.display.flip()

    def _draw_citizens(self):
        """Draw all citizens as colored circles"""
        for citizen in self.manager.citizens:
            # Get color based on state
            color = self.state_colors.get(citizen.state, self.colors['citizen'])

            # Scale position to screen
            x = int(citizen.position[0])
            y = int(citizen.position[1])

            # Draw citizen circle
            pygame.draw.circle(self.screen, color, (x, y), 8)

            # Draw border based on wealth
            border_thickness = max(1, int(citizen.money / 100))
            pygame.draw.circle(self.screen, (0, 0, 0), (x, y), 8, border_thickness)

            # Draw archetype label
            label = self.font.render(citizen.archetype[:4], True, self.colors['text'])
            self.screen.blit(label, (x - 15, y - 25))

    def _draw_relationships(self):
        """Draw relationship lines between citizens"""
        for citizen in self.manager.citizens:
            for other_id, relationship in citizen.memory.relationships.items():
                if abs(relationship) > 20:  # Only show significant relationships
                    other = self.manager.get_citizen(other_id)
                    if other:
                        # Determine color based on relationship
                        if relationship > 50:
                            color = self.colors['relationship_positive']
                        elif relationship < -50:
                            color = self.colors['relationship_negative']
                        else:
                            color = self.colors['relationship_neutral']

                        # Draw line
                        start = (int(citizen.position[0]), int(citizen.position[1]))
                        end = (int(other.position[0]), int(other.position[1]))
                        thickness = max(1, int(abs(relationship) / 30))
                        pygame.draw.line(self.screen, color, start, end, thickness)

    def _draw_stats(self):
        """Draw statistics panel"""
        stats = self.manager.get_stats()

        # Background panel
        panel_rect = pygame.Rect(10, 10, 350, 280)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect, 2)

        # Title
        title = self.large_font.render("Civilization Stats", True, self.colors['text'])
        self.screen.blit(title, (20, 15))

        # Stats
        y_offset = 55
        stats_text = [
            f"Tick: {stats['tick']} ({stats['simulation_time']:.1f}s)",
            f"Citizens: {stats['total_citizens']}",
            f"Interactions: {stats['total_interactions']}",
            f"Trades: {stats['total_trades']}",
            f"Total Wealth: ${stats['total_wealth']:.0f}",
            f"Avg Money: ${stats['avg_money']:.0f}",
            f"Wealth Inequality (Gini): {stats['wealth_gini']:.3f}",
            f"Avg Relationship: {stats['avg_relationship']:.1f}",
            f"",
            f"Avg Hunger: {stats['avg_hunger']:.2f}",
            f"Avg Energy: {stats['avg_energy']:.2f}",
            f"Avg Social: {stats['avg_social']:.2f}"
        ]

        for text in stats_text:
            surf = self.font.render(text, True, self.colors['text'])
            self.screen.blit(surf, (20, y_offset))
            y_offset += 20

    def _draw_controls(self):
        """Draw control instructions"""
        y_offset = 300
        controls = [
            "Controls:",
            "SPACE - Pause/Resume",
            "S - Toggle Stats",
            "R - Toggle Relationships",
            "Q - Quit",
            "",
            f"Status: {'PAUSED' if self.paused else 'RUNNING'}"
        ]

        panel_rect = pygame.Rect(10, y_offset, 350, 160)
        pygame.draw.rect(self.screen, (255, 255, 255), panel_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), panel_rect, 2)

        for text in controls:
            surf = self.font.render(text, True, self.colors['text'])
            self.screen.blit(surf, (20, y_offset + 10))
            y_offset += 20

    def handle_events(self) -> bool:
        """Handle user input. Returns False if should quit."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    return False
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key == pygame.K_s:
                    self.show_stats = not self.show_stats
                elif event.key == pygame.K_r:
                    self.show_relationships = not self.show_relationships

        return True


class Simulation:
    """Main simulation controller"""

    def __init__(self, num_citizens: int = 20, headless: bool = False,
                 target_fps: int = 30, output_dir: str = "experiments", use_llm: bool = False):
        self.num_citizens = num_citizens
        self.headless = headless
        self.target_fps = target_fps
        self.use_llm = use_llm

        # Create output directory
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(exist_ok=True)

        # Create experiment subdirectory with timestamp
        self.experiment_dir = self.output_dir / f"experiment_{int(time.time())}"
        self.experiment_dir.mkdir(exist_ok=True)

        # Create manager (with LLM if enabled)
        self.manager = CivilizationManager(use_llm=use_llm)
        self.manager.spawn_citizens(num_citizens)

        # Create visualizer if not headless
        self.visualizer: Optional[SimulationVisualizer] = None
        if not headless:
            self.visualizer = SimulationVisualizer(self.manager)

        # Metrics tracking
        self.metrics_history = []
        self.save_interval = 100  # Save every 100 ticks

    def run(self, max_ticks: Optional[int] = None):
        """
        Run the simulation.

        Args:
            max_ticks: Maximum number of ticks to run (None = infinite)
        """
        running = True
        last_save = 0

        print(f"Starting {'headless' if self.headless else 'visual'} simulation...")
        print(f"Citizens: {self.num_citizens}")
        print(f"Output: {self.experiment_dir}")

        while running:
            # Handle events (visual mode only)
            if self.visualizer:
                running = self.visualizer.handle_events()
                if not running:
                    break

                # Update if not paused
                if not self.visualizer.paused:
                    self.manager.update(1.0 / self.target_fps)

                # Render
                self.visualizer.render()
                self.visualizer.clock.tick(self.target_fps)

            else:
                # Headless mode - run as fast as possible
                self.manager.update(1.0)

                # Print stats every 100 ticks
                if self.manager.tick_count % 100 == 0:
                    stats = self.manager.get_stats()
                    print(f"Tick {stats['tick']}: "
                          f"{stats['total_interactions']} interactions, "
                          f"{stats['total_trades']} trades, "
                          f"Gini: {stats['wealth_gini']:.3f}, "
                          f"Avg Rel: {stats['avg_relationship']:.1f}")

            # Save metrics periodically
            if self.manager.tick_count - last_save >= self.save_interval:
                self._save_metrics()
                last_save = self.manager.tick_count

            # Check max ticks
            if max_ticks and self.manager.tick_count >= max_ticks:
                print(f"Reached max ticks ({max_ticks})")
                running = False

        # Final save
        self._save_metrics()
        self._save_final_data()

        if self.visualizer:
            pygame.quit()

        print(f"\nSimulation complete!")
        print(f"Total ticks: {self.manager.tick_count}")
        print(f"Data saved to: {self.experiment_dir}")

    def _save_metrics(self):
        """Save current metrics to history"""
        stats = self.manager.get_stats()
        self.metrics_history.append(stats)

        # Save metrics file
        metrics_file = self.experiment_dir / "metrics_history.json"
        with open(metrics_file, 'w') as f:
            json.dump(self.metrics_history, f, indent=2)

    def _save_final_data(self):
        """Save final simulation data"""
        # Export full data
        data = self.manager.export_data()

        # Save to JSON
        data_file = self.experiment_dir / "final_data.json"
        with open(data_file, 'w') as f:
            json.dump(data, f, indent=2)

        # Save summary
        summary = {
            'num_citizens': self.num_citizens,
            'total_ticks': self.manager.tick_count,
            'simulation_time': self.manager.simulation_time,
            'final_stats': self.manager.get_stats(),
            'experiment_dir': str(self.experiment_dir)
        }

        summary_file = self.experiment_dir / "summary.json"
        with open(summary_file, 'w') as f:
            json.dump(summary, f, indent=2)


def main():
    parser = argparse.ArgumentParser(description="AI Civilization Experiment")
    parser.add_argument('--citizens', type=int, default=20, help='Number of citizens (default: 20)')
    parser.add_argument('--headless', action='store_true', help='Run in headless mode (no visualization)')
    parser.add_argument('--max-ticks', type=int, default=None, help='Maximum ticks to run (default: infinite)')
    parser.add_argument('--fps', type=int, default=30, help='Target FPS for visual mode (default: 30)')
    parser.add_argument('--output', type=str, default='../../../experiments', help='Output directory for data')
    parser.add_argument('--use-llm', action='store_true', help='Use Qwen 1.5B LLM for citizen decisions')

    args = parser.parse_args()

    # Create and run simulation
    sim = Simulation(
        num_citizens=args.citizens,
        headless=args.headless,
        target_fps=args.fps,
        output_dir=args.output,
        use_llm=args.use_llm
    )

    sim.run(max_ticks=args.max_ticks)


if __name__ == "__main__":
    main()
