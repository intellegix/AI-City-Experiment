"""
Configuration and constants for AI City Simulation
Based on technical specifications from the blueprint

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class PerformanceConfig:
    """Performance targets optimized for AMD Radeon 780M"""
    TARGET_FPS: int = 60
    MIN_FPS: int = 45  # Higher minimum for better experience
    MAX_DRAW_CALLS: int = 300  # REDUCED: 500→300 for integrated GPU
    MAX_VRAM_GB: int = 4  # REDUCED: AMD 780M shares 16GB RAM with CPU
    MAX_NPC_COUNT: int = 150  # CRITICAL: Reduced from 500 for AMD 780M performance
    CITY_SIZE_KM: float = 3.0  # REDUCED: Smaller city for better performance
    MAX_LOADING_TIME_SEC: int = 30


@dataclass
class TerrainConfig:
    """Terrain generation parameters"""
    SIZE: int = 512  # Grid size (512x512)
    SCALE: float = 100.0  # Perlin noise scale
    OCTAVES: int = 6  # Detail levels
    PERSISTENCE: float = 0.5
    LACUNARITY: float = 2.0
    SEED: int = None  # Random if None

    # Biome thresholds
    WATER_LEVEL: float = 0.3
    SAND_LEVEL: float = 0.35
    GRASS_LEVEL: float = 0.6
    FOREST_LEVEL: float = 0.75
    MOUNTAIN_LEVEL: float = 0.85


@dataclass
class CityConfig:
    """City layout configuration"""
    GRID_SIZE: int = 512
    BLOCK_SIZE: int = 40  # Average city block size
    ROAD_WIDTH: int = 4
    MAIN_ROAD_WIDTH: int = 6
    NUM_MAIN_ROADS: int = 8

    # Zones
    URBAN_CENTER_RADIUS: float = 0.25  # Fraction of city size
    SUBURBAN_RADIUS: float = 0.5

    # Building parameters
    MIN_BUILDING_SIZE: int = 8
    MAX_BUILDING_SIZE: int = 30
    BUILDING_DENSITY: float = 0.6  # Probability of building in valid space


@dataclass
class NPCConfig:
    """NPC AI configuration (AMD 780M optimized)"""
    INITIAL_NPC_COUNT: int = 10  # Start small for faster loading
    MAX_NPC_COUNT: int = 150  # REDUCED: Match PerformanceConfig for consistency

    # Perception
    PERCEPTION_RADIUS: float = 50.0
    INTERACTION_RADIUS: float = 10.0

    # Behavior parameters
    WALK_SPEED: float = 2.0
    RUN_SPEED: float = 5.0
    IDLE_TIME_RANGE: Tuple[float, float] = (2.0, 8.0)

    # Memory
    MEMORY_DECAY_RATE: float = 0.1  # Per second
    MAX_MEMORY_SIZE: int = 20

    # Needs (for emergent behavior)
    HUNGER_INCREASE_RATE: float = 0.05
    ENERGY_DECREASE_RATE: float = 0.03
    SOCIAL_DECREASE_RATE: float = 0.02


@dataclass
class RenderConfig:
    """Rendering configuration"""
    WINDOW_WIDTH: int = 1280
    WINDOW_HEIGHT: int = 720
    CAMERA_SPEED: float = 5.0
    ZOOM_SPEED: float = 0.1
    MIN_ZOOM: float = 0.5
    MAX_ZOOM: float = 3.0

    # LOD distances (REDUCED by 30% for AMD 780M integrated GPU)
    LOD_HIGH_DISTANCE: float = 60.0   # Was 100.0
    LOD_MED_DISTANCE: float = 150.0   # Was 300.0
    LOD_LOW_DISTANCE: float = 400.0   # Was 800.0
    LOD_CULL_DISTANCE: float = 600.0  # NEW: Cull objects beyond this distance

    # Colors (RGB)
    WATER_COLOR: Tuple[int, int, int] = (70, 130, 180)
    SAND_COLOR: Tuple[int, int, int] = (238, 214, 175)
    GRASS_COLOR: Tuple[int, int, int] = (124, 252, 0)
    FOREST_COLOR: Tuple[int, int, int] = (34, 139, 34)
    MOUNTAIN_COLOR: Tuple[int, int, int] = (139, 137, 137)
    ROAD_COLOR: Tuple[int, int, int] = (50, 50, 50)
    BUILDING_COLOR: Tuple[int, int, int] = (180, 180, 200)
    NPC_COLOR: Tuple[int, int, int] = (255, 100, 100)


@dataclass
class UIConfig:
    """UI/HUD configuration for professional gamer HUD"""
    HUD_OPACITY: float = 0.9
    FPS_COLOR_GREEN_THRESHOLD: int = 50  # Green for 50+ FPS
    FPS_COLOR_YELLOW_THRESHOLD: int = 30  # Yellow for 30-50 FPS
    SHOW_DEBUG_INFO: bool = True  # Show position/heading debug info


# Global configuration instances
PERFORMANCE = PerformanceConfig()
TERRAIN = TerrainConfig()
CITY = CityConfig()
NPC = NPCConfig()
RENDER = RenderConfig()
UI = UIConfig()


class Config:
    """Main configuration access point"""
    performance = PERFORMANCE
    terrain = TERRAIN
    city = CITY
    npc = NPC
    render = RENDER
    ui = UI

    @staticmethod
    def set_seed(seed: int):
        """Set random seed for reproducibility"""
        np.random.seed(seed)
        if TERRAIN.SEED is None:
            TERRAIN.SEED = seed
