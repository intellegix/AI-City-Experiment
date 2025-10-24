"""
Android/Termux optimized configuration for AI City Simulation
Reduces resource requirements for mobile devices

Copyright 2025 Intellegix
Licensed under the Apache License, Version 2.0
"""
from dataclasses import dataclass
from typing import Tuple
import numpy as np


@dataclass
class PerformanceConfig:
    """Performance targets optimized for Android/Termux"""
    TARGET_FPS: int = 30  # Lower FPS for mobile
    MIN_FPS: int = 20
    MAX_DRAW_CALLS: int = 150  # Reduced for mobile
    MAX_VRAM_GB: int = 2  # Mobile memory constraint
    MAX_NPC_COUNT: int = 50  # Significantly reduced for mobile
    CITY_SIZE_KM: float = 1.5  # Smaller city for mobile
    MAX_LOADING_TIME_SEC: int = 60  # Allow more time on mobile


@dataclass
class TerrainConfig:
    """Terrain generation parameters - optimized for mobile"""
    SIZE: int = 256  # Reduced from 512 for mobile
    SCALE: float = 50.0  # Adjusted for smaller size
    OCTAVES: int = 4  # Reduced detail levels for performance
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
    """City layout configuration - optimized for mobile"""
    GRID_SIZE: int = 256  # Reduced from 512
    BLOCK_SIZE: int = 30  # Smaller blocks
    ROAD_WIDTH: int = 3  # Narrower roads
    MAIN_ROAD_WIDTH: int = 5
    NUM_MAIN_ROADS: int = 6  # Fewer roads

    # Zones
    URBAN_CENTER_RADIUS: float = 0.25
    SUBURBAN_RADIUS: float = 0.5

    # Building parameters
    MIN_BUILDING_SIZE: int = 6  # Smaller buildings
    MAX_BUILDING_SIZE: int = 20
    BUILDING_DENSITY: float = 0.5  # Less dense


@dataclass
class NPCConfig:
    """NPC AI configuration - heavily optimized for mobile"""
    INITIAL_NPC_COUNT: int = 5  # Start very small
    MAX_NPC_COUNT: int = 50  # Maximum 50 NPCs

    # Perception
    PERCEPTION_RADIUS: float = 30.0  # Reduced
    INTERACTION_RADIUS: float = 8.0

    # Behavior parameters
    WALK_SPEED: float = 2.0
    RUN_SPEED: float = 4.0  # Reduced
    IDLE_TIME_RANGE: Tuple[float, float] = (2.0, 8.0)

    # Memory
    MEMORY_DECAY_RATE: float = 0.1
    MAX_MEMORY_SIZE: int = 10  # Reduced memory

    # Needs (for emergent behavior)
    HUNGER_INCREASE_RATE: float = 0.05
    ENERGY_DECREASE_RATE: float = 0.03
    SOCIAL_DECREASE_RATE: float = 0.02


@dataclass
class RenderConfig:
    """Rendering configuration - mobile optimized"""
    WINDOW_WIDTH: int = 800  # Smaller window for mobile
    WINDOW_HEIGHT: int = 600
    CAMERA_SPEED: float = 3.0  # Slower camera
    ZOOM_SPEED: float = 0.1
    MIN_ZOOM: float = 0.5
    MAX_ZOOM: float = 2.0

    # LOD distances - heavily reduced for mobile
    LOD_HIGH_DISTANCE: float = 40.0
    LOD_MED_DISTANCE: float = 80.0
    LOD_LOW_DISTANCE: float = 150.0
    LOD_CULL_DISTANCE: float = 200.0  # Aggressive culling

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
    """UI/HUD configuration for mobile"""
    HUD_OPACITY: float = 0.8  # Slightly more transparent
    FPS_COLOR_GREEN_THRESHOLD: int = 25  # Adjusted for 30 FPS target
    FPS_COLOR_YELLOW_THRESHOLD: int = 15
    SHOW_DEBUG_INFO: bool = True


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
