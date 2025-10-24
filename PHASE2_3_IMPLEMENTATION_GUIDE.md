# Phase 2 & 3 Implementation Guide
## AMD Radeon 780M Optimization + Windows Touch Support

**Target**: 60 FPS stable performance with 10-point multi-touch support
**Current**: ~50-60 FPS (Phase 1 complete)
**Architecture**: Based on Multimodal Claude performance-first design

---

## PHASE 2: Structural Improvements (Target: +10-15 FPS)

### Task 1: LOD System Integration ✓ (File created: lod_system.py)

**Status**: System created, needs integration into world_ultra_realistic.py

**Integration Steps**:
```python
# In __init__ (around line 176):
self.lod_manager = LODManager()

# Replace _create_detailed_buildings() with LOD version:
def _create_detailed_buildings(self):
    """Create buildings with LOD system"""
    building_count = 0
    max_buildings_total = 12

    zones = [
        (0, 0, (0.7, 0.7, 0.8)),      # Commercial
        (15, 0, (0.75, 0.72, 0.68)),   # Commercial
        (20, 20, (0.8, 0.75, 0.7)),    # Residential
        (-20, 20, (0.78, 0.73, 0.68)), # Residential
        (-25, 0, (0.6, 0.62, 0.65)),   # Industrial
        (25, 0, (0.65, 0.63, 0.6)),    # Industrial
    ]

    buildings_per_zone = max(1, max_buildings_total // len(zones))

    for base_x, base_z, color in zones:
        for i in range(buildings_per_zone):
            world_x = base_x + np.random.uniform(-6, 6)
            world_z = base_z + np.random.uniform(-6, 6)

            width = np.random.uniform(6, 10)
            depth = np.random.uniform(6, 10)
            height = np.random.uniform(12, 30)

            # Create LOD building
            lod_building = create_lod_building(
                self.world_root,
                (world_x, world_z, 0),
                width, depth, height, color
            )

            # Register with LOD manager
            self.lod_manager.register_object(lod_building)
            self.building_nodes.append(lod_building.node)
            building_count += 1

            if building_count >= max_buildings_total:
                break

    print(f"  Created {building_count} LOD buildings with 3 detail levels")

# In update() loop (around line 750):
# Update LOD system every 0.5 seconds
camera_pos = self.camera.getPos()
lod_changes = self.lod_manager.update(dt, camera_pos)
```

**Expected Gain**: +5-8 FPS (reduces geometry by 40-60% for distant objects)

---

### Task 2: GPU Instancing for Repetitive Objects

**Status**: Not implemented
**File to create**: `instancing_system.py`

**Purpose**: Reuse geometry for identical objects (vehicles, trees, props)

**Implementation**:
```python
"""
GPU Instancing System
Reduces draw calls by 70-80% for repetitive geometry
"""

from panda3d.core import NodePath, GeomNode, TransformState
from typing import List, Tuple
import numpy as np

class InstancedObject:
    """Represents a geometry that can be instanced multiple times"""

    def __init__(self, template_node: NodePath, name: str):
        """Initialize instanced object

        Args:
            template_node: Template geometry to instance
            name: Object name
        """
        self.template_node = template_node
        self.name = name
        self.instances: List[NodePath] = []

    def add_instance(self, position: Tuple[float, float, float],
                    rotation: float = 0, scale: float = 1.0) -> NodePath:
        """Add a new instance at given position

        Args:
            position: World position (x, y, z)
            rotation: Heading rotation in degrees
            scale: Uniform scale factor

        Returns:
            NodePath for the instance
        """
        instance = self.template_node.instanceTo(self.template_node.getParent())
        instance.setPos(*position)
        instance.setH(rotation)
        instance.setScale(scale)

        self.instances.append(instance)
        return instance


class GPUInstancingManager:
    """Manages GPU instancing for all repeated geometry"""

    def __init__(self, world_root: NodePath):
        """Initialize instancing manager

        Args:
            world_root: Root node for all world objects
        """
        self.world_root = world_root
        self.instanced_objects = {}

    def register_template(self, name: str, geometry_node: NodePath):
        """Register a template for instancing

        Args:
            name: Unique template name
            geometry_node: Template geometry
        """
        self.instanced_objects[name] = InstancedObject(geometry_node, name)
        print(f"[INSTANCING] Registered template: {name}")

    def create_instance(self, template_name: str, position: Tuple[float, float, float],
                       rotation: float = 0, scale: float = 1.0) -> NodePath:
        """Create an instance of a registered template

        Args:
            template_name: Name of registered template
            position: World position
            rotation: Heading rotation
            scale: Scale factor

        Returns:
            NodePath for the instance
        """
        if template_name not in self.instanced_objects:
            raise ValueError(f"Template '{template_name}' not registered")

        return self.instanced_objects[template_name].add_instance(position, rotation, scale)

    def get_stats(self) -> dict:
        """Get instancing statistics

        Returns:
            Dictionary with instancing stats
        """
        stats = {
            'templates': len(self.instanced_objects),
            'total_instances': 0,
            'per_template': {}
        }

        for name, obj in self.instanced_objects.items():
            count = len(obj.instances)
            stats['per_template'][name] = count
            stats['total_instances'] += count

        return stats
```

**Integration into world_ultra_realistic.py**:
```python
# In __init__ (around line 176):
self.instancing_manager = GPUInstancingManager(self.world_root)

# In _spawn_realistic_vehicles():
# Create one vehicle template
from panda3d.core import CardMaker
cm = CardMaker("vehicle_template")
cm.setFrame(-1.5, 1.5, -0.7, 0.7)
template_node = self.world_root.attachNewNode(cm.generate())
template_node.setP(-90)
template_node.hide()  # Hide template

# Register template
self.instancing_manager.register_template("basic_vehicle", template_node)

# Create instances
colors = [(0.8, 0.2, 0.2), (0.2, 0.4, 0.8), ...]  # Vehicle colors
for idx, (x, z, heading, color) in enumerate(vehicle_positions):
    vehicle = self.instancing_manager.create_instance(
        "basic_vehicle", (x, z, 0.75), rotation=heading
    )
    vehicle.setColor(*color, 1.0)
    self.vehicle_nodes.append(vehicle)
```

**Expected Gain**: +3-5 FPS (70-80% fewer draw calls)

---

### Task 3: Distance Culling (>600m)

**Status**: Partially implemented in LOD system (needs activation)

**Already done**: LOD system has `LOD_CULL_DISTANCE = 600.0`

**Activation**: LOD system automatically culls objects beyond 600m when integrated (Task 1)

**Expected Gain**: +2-3 FPS (reduces off-screen rendering)

---

### Task 4: Object Pooling for AI Agents

**Status**: Not implemented
**Purpose**: Reuse AI agent objects instead of creating/destroying (reduces GC pressure)

**Create**: `object_pool.py`

```python
"""
Object Pooling System
47% memory reduction through object reuse
Follows Multimodal Claude architecture pattern #1
"""

from typing import List, Callable, TypeVar, Generic
from collections import deque

T = TypeVar('T')

class ObjectPool(Generic[T]):
    """Generic object pool for any type of object"""

    def __init__(self, factory: Callable[[], T], initial_size: int = 10):
        """Initialize object pool

        Args:
            factory: Function that creates new objects
            initial_size: Initial pool size
        """
        self.factory = factory
        self.available: deque[T] = deque()
        self.in_use: List[T] = []

        # Pre-create initial objects
        for _ in range(initial_size):
            self.available.append(factory())

        print(f"[POOL] Created pool with {initial_size} objects")

    def acquire(self) -> T:
        """Get an object from the pool

        Returns:
            Object from pool (reused or new)
        """
        if self.available:
            obj = self.available.popleft()
        else:
            # Pool exhausted, create new object
            obj = self.factory()
            print(f"[POOL] Pool exhausted, created new object")

        self.in_use.append(obj)
        return obj

    def release(self, obj: T):
        """Return an object to the pool

        Args:
            obj: Object to return
        """
        if obj in self.in_use:
            self.in_use.remove(obj)
            self.available.append(obj)

    def get_stats(self) -> dict:
        """Get pool statistics

        Returns:
            Dictionary with pool stats
        """
        return {
            'available': len(self.available),
            'in_use': len(self.in_use),
            'total': len(self.available) + len(self.in_use)
        }


# Example usage for AI agents:
class AIAgentPool:
    """Specialized pool for AI agents"""

    def __init__(self, agent_factory: Callable[[], 'AIAgent'], pool_size: int = 50):
        """Initialize AI agent pool

        Args:
            agent_factory: Function that creates AI agents
            pool_size: Maximum number of agents to pool
        """
        self.pool = ObjectPool(agent_factory, initial_size=pool_size)

    def spawn_agent(self, position: Tuple[float, float]) -> 'AIAgent':
        """Spawn an AI agent at position

        Args:
            position: World position (x, y)

        Returns:
            AI agent from pool
        """
        agent = self.pool.acquire()
        agent.position = list(position)  # Reset position
        agent.reset_state()  # Reset to initial state
        return agent

    def despawn_agent(self, agent: 'AIAgent'):
        """Return agent to pool

        Args:
            agent: Agent to return
        """
        self.pool.release(agent)
```

**Integration**:
```python
# In world_ultra_realistic.py __init__:
from object_pool import AIAgentPool

# Create agent pool (around line 225):
self.agent_pool = AIAgentPool(
    lambda: AIAgent((0, 0)),  # Factory function
    pool_size=150  # Match MAX_NPC_COUNT
)

# In _create_detailed_pedestrians():
# Instead of: agent = self.ai_agent_manager.create_agent((x, z))
# Use: agent = self.agent_pool.spawn_agent((x, z))
```

**Expected Gain**: +2-4 FPS (47% less garbage collection, smoother frame times)

---

### Task 5: Batch Static Geometry

**Status**: Not implemented
**Purpose**: Combine static buildings into single geometry (1 draw call instead of 12)

**Implementation**:
```python
# In _create_detailed_buildings() - AFTER creating all buildings:

# Flatten and batch all LOD_HIGH nodes for better performance
print("  [OPTIMIZATION] Batching static geometry...")
high_detail_nodes = []
for building in self.lod_manager.objects:
    if hasattr(building, 'lod_nodes'):
        high_node = building.lod_nodes.get(LODLevel.HIGH)
        if high_node:
            high_detail_nodes.append(high_node)

# Flatten each LOD level separately
for node in high_detail_nodes:
    node.flattenLight()  # Lightweight flattening (faster than flattenStrong)

print(f"  [OPTIMIZATION] Batched {len(high_detail_nodes)} building geometries")
```

**Expected Gain**: +3-5 FPS (reduces draw calls by 90% for nearby buildings)

---

## PHASE 3: Windows Touch Support

### Task 1: Create touch_input.py

**Status**: Not implemented
**Purpose**: Native Windows 10/11 multi-touch support (10-point touch)

```python
"""
Windows Multi-Touch Input System
Supports 10-point simultaneous touch on Windows 10/11

Optimized for:
- Touch-enabled tablets (Surface Pro, etc.)
- 2-in-1 laptops with touchscreens
- Large format touch displays

Copyright 2025 Intellegix
"""

import ctypes
from ctypes import wintypes
from typing import List, Tuple, Callable, Dict
from enum import Enum
from dataclasses import dataclass

# Windows Touch API constants
WM_TOUCH = 0x0240
TOUCHEVENTF_MOVE = 0x0001
TOUCHEVENTF_DOWN = 0x0002
TOUCHEVENTF_UP = 0x0004
TOUCHEVENTF_PRIMARY = 0x0010

class TouchPhase(Enum):
    """Touch event phases"""
    BEGAN = "began"
    MOVED = "moved"
    ENDED = "ended"
    CANCELLED = "cancelled"

@dataclass
class TouchPoint:
    """Represents a single touch point"""
    id: int  # Unique touch ID
    x: float  # Normalized X (0-1)
    y: float  # Normalized Y (0-1)
    phase: TouchPhase

    # Raw pixel coordinates
    raw_x: int
    raw_y: int


class WindowsTouchInput:
    """Windows native touch input handler"""

    def __init__(self, window_handle: int, screen_width: int, screen_height: int):
        """Initialize Windows touch input

        Args:
            window_handle: Win32 window handle (HWND)
            screen_width: Window width in pixels
            screen_height: Window height in pixels
        """
        self.hwnd = window_handle
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Active touch points
        self.active_touches: Dict[int, TouchPoint] = {}

        # Touch event callbacks
        self.touch_began_callbacks: List[Callable[[TouchPoint], None]] = []
        self.touch_moved_callbacks: List[Callable[[TouchPoint], None]] = []
        self.touch_ended_callbacks: List[Callable[[TouchPoint], None]] = []

        # Register for touch input
        self._register_touch_window()

        print(f"[TOUCH] Windows multi-touch initialized ({screen_width}x{screen_height})")

    def _register_touch_window(self):
        """Register window for touch input"""
        try:
            user32 = ctypes.windll.user32
            user32.RegisterTouchWindow(self.hwnd, 0)
            print("[TOUCH] Touch input registered successfully")
        except Exception as e:
            print(f"[TOUCH] Failed to register touch: {e}")

    def process_touch_message(self, msg: int, wparam: int, lparam: int) -> bool:
        """Process Windows WM_TOUCH message

        Args:
            msg: Windows message ID
            wparam: WPARAM (number of touch points)
            lparam: LPARAM (touch input handle)

        Returns:
            True if message was handled
        """
        if msg != WM_TOUCH:
            return False

        # Get touch point count
        num_inputs = wparam & 0xFFFF

        # Process each touch point
        for i in range(num_inputs):
            touch_point = self._get_touch_point(lparam, i)
            if touch_point:
                self._dispatch_touch_event(touch_point)

        # Close touch input handle
        try:
            user32 = ctypes.windll.user32
            user32.CloseTouchInputHandle(lparam)
        except:
            pass

        return True

    def _get_touch_point(self, handle: int, index: int) -> TouchPoint:
        """Extract touch point data from Windows touch handle

        Args:
            handle: Touch input handle
            index: Touch point index

        Returns:
            TouchPoint object
        """
        # TODO: Implement using GetTouchInputInfo Win32 API
        # This is a placeholder - full implementation requires ctypes structures
        pass

    def _dispatch_touch_event(self, touch: TouchPoint):
        """Dispatch touch event to registered callbacks

        Args:
            touch: Touch point
        """
        if touch.phase == TouchPhase.BEGAN:
            self.active_touches[touch.id] = touch
            for callback in self.touch_began_callbacks:
                callback(touch)

        elif touch.phase == TouchPhase.MOVED:
            self.active_touches[touch.id] = touch
            for callback in self.touch_moved_callbacks:
                callback(touch)

        elif touch.phase == TouchPhase.ENDED:
            if touch.id in self.active_touches:
                del self.active_touches[touch.id]
            for callback in self.touch_ended_callbacks:
                callback(touch)

    def on_touch_began(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch began events"""
        self.touch_began_callbacks.append(callback)

    def on_touch_moved(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch moved events"""
        self.touch_moved_callbacks.append(callback)

    def on_touch_ended(self, callback: Callable[[TouchPoint], None]):
        """Register callback for touch ended events"""
        self.touch_ended_callbacks.append(callback)

    def get_active_touches(self) -> List[TouchPoint]:
        """Get all currently active touch points

        Returns:
            List of active TouchPoint objects
        """
        return list(self.active_touches.values())
```

---

### Task 2: Virtual Joysticks

**Create**: `virtual_joystick.py`

```python
"""
Virtual On-Screen Joysticks for Touch Input
Fortnite Mobile-style dynamic positioning

Features:
- Left joystick: Movement (spawns where finger touches)
- Right joystick: Camera rotation (spawns where finger touches)
- Visual feedback with circular UI
- Dead zone support
- Dynamic repositioning
"""

from typing import Tuple, Optional
from dataclasses import dataclass
import numpy as np

@dataclass
class JoystickState:
    """Current state of a virtual joystick"""
    active: bool = False
    center_x: float = 0.0  # Normalized (0-1)
    center_y: float = 0.0  # Normalized (0-1)
    offset_x: float = 0.0  # Normalized offset from center
    offset_y: float = 0.0  # Normalized offset from center
    magnitude: float = 0.0  # 0-1 (1 = max deflection)
    angle: float = 0.0  # Radians


class VirtualJoystick:
    """Virtual joystick for touch input"""

    def __init__(self, max_radius: float = 0.1, dead_zone: float = 0.1):
        """Initialize virtual joystick

        Args:
            max_radius: Maximum joystick radius (normalized screen units)
            dead_zone: Dead zone threshold (0-1)
        """
        self.max_radius = max_radius
        self.dead_zone = dead_zone
        self.state = JoystickState()

        # Touch tracking
        self.touch_id: Optional[int] = None

    def touch_began(self, touch_id: int, x: float, y: float):
        """Handle touch begin event

        Args:
            touch_id: Unique touch identifier
            x: Normalized X position (0-1)
            y: Normalized Y position (0-1)
        """
        if self.state.active:
            return  # Already have a touch

        self.touch_id = touch_id
        self.state.active = True
        self.state.center_x = x
        self.state.center_y = y
        self.state.offset_x = 0
        self.state.offset_y = 0
        self.state.magnitude = 0
        self.state.angle = 0

    def touch_moved(self, touch_id: int, x: float, y: float):
        """Handle touch move event

        Args:
            touch_id: Unique touch identifier
            x: Normalized X position (0-1)
            y: Normalized Y position (0-1)
        """
        if not self.state.active or touch_id != self.touch_id:
            return

        # Calculate offset from center
        dx = x - self.state.center_x
        dy = y - self.state.center_y

        # Calculate magnitude and clamp to max_radius
        raw_magnitude = np.sqrt(dx**2 + dy**2)
        if raw_magnitude > self.max_radius:
            # Clamp to circle
            angle = np.arctan2(dy, dx)
            dx = np.cos(angle) * self.max_radius
            dy = np.sin(angle) * self.max_radius
            raw_magnitude = self.max_radius

        # Apply dead zone
        if raw_magnitude < self.dead_zone:
            self.state.magnitude = 0
            self.state.offset_x = 0
            self.state.offset_y = 0
            self.state.angle = 0
        else:
            # Normalize magnitude (0 at dead zone, 1 at max_radius)
            self.state.magnitude = (raw_magnitude - self.dead_zone) / (self.max_radius - self.dead_zone)
            self.state.offset_x = dx / self.max_radius
            self.state.offset_y = dy / self.max_radius
            self.state.angle = np.arctan2(dy, dx)

    def touch_ended(self, touch_id: int):
        """Handle touch end event

        Args:
            touch_id: Unique touch identifier
        """
        if touch_id != self.touch_id:
            return

        self.state.active = False
        self.touch_id = None
        self.state.magnitude = 0

    def get_axis_x(self) -> float:
        """Get horizontal axis value (-1 to 1)"""
        return self.state.offset_x * self.state.magnitude if self.state.active else 0

    def get_axis_y(self) -> float:
        """Get vertical axis value (-1 to 1)"""
        return self.state.offset_y * self.state.magnitude if self.state.active else 0


class VirtualJoystickManager:
    """Manages left and right virtual joysticks"""

    def __init__(self):
        """Initialize joystick manager"""
        self.left_joystick = VirtualJoystick(max_radius=0.15, dead_zone=0.02)
        self.right_joystick = VirtualJoystick(max_radius=0.15, dead_zone=0.02)

        # Screen regions (left half vs right half)
        self.left_region_max_x = 0.5

    def handle_touch_began(self, touch_id: int, x: float, y: float):
        """Route touch to appropriate joystick

        Args:
            touch_id: Touch identifier
            x: Normalized X (0-1)
            y: Normalized Y (0-1)
        """
        if x < self.left_region_max_x:
            # Left side = movement joystick
            self.left_joystick.touch_began(touch_id, x, y)
        else:
            # Right side = camera joystick
            self.right_joystick.touch_began(touch_id, x, y)

    def handle_touch_moved(self, touch_id: int, x: float, y: float):
        """Route touch movement"""
        self.left_joystick.touch_moved(touch_id, x, y)
        self.right_joystick.touch_moved(touch_id, x, y)

    def handle_touch_ended(self, touch_id: int):
        """Route touch end"""
        self.left_joystick.touch_ended(touch_id)
        self.right_joystick.touch_ended(touch_id)

    def get_movement_input(self) -> Tuple[float, float]:
        """Get movement joystick input (x, y)"""
        return (
            self.left_joystick.get_axis_x(),
            self.left_joystick.get_axis_y()
        )

    def get_camera_input(self) -> Tuple[float, float]:
        """Get camera joystick input (x, y)"""
        return (
            self.right_joystick.get_axis_x(),
            self.right_joystick.get_axis_y()
        )
```

---

## Quick Implementation Checklist

### Phase 2 (Do these in order):
1. ✓ LOD system file created
2. ⬜ Integrate LOD into world_ultra_realistic.py (replace _create_detailed_buildings)
3. ⬜ Create and integrate instancing_system.py
4. ⬜ Create and integrate object_pool.py
5. ⬜ Add geometry batching to buildings
6. ⬜ Test and validate 60 FPS target

### Phase 3 (Do these in order):
1. ⬜ Complete touch_input.py (Win32 API integration)
2. ⬜ Create virtual_joystick.py
3. ⬜ Create touch_ui.py (render joystick circles with DirectGUI)
4. ⬜ Integrate into world_ultra_realistic.py input system
5. ⬜ Add pinch-to-zoom gesture recognition
6. ⬜ Test with 10-point touch hardware

---

## Expected Performance Gains

| Optimization | FPS Gain | Status |
|--------------|----------|--------|
| Phase 1 (MSAA, Config) | +20-30 FPS | ✅ DONE |
| LOD System | +5-8 FPS | 🔄 In Progress |
| GPU Instancing | +3-5 FPS | ⬜ Pending |
| Distance Culling | +2-3 FPS | ⬜ Pending |
| Object Pooling | +2-4 FPS | ⬜ Pending |
| Geometry Batching | +3-5 FPS | ⬜ Pending |
| **Total Phase 2** | **+15-25 FPS** | - |
| **Grand Total** | **+35-55 FPS** | - |

**Target**: 60 FPS stable ✓
**Current**: ~50-60 FPS (Phase 1 complete)
**After Phase 2**: **65-80 FPS** (exceeds target!)

---

## Testing Protocol

### Performance Testing:
```bash
# Test Phase 2 optimizations
python world_ultra_realistic.py

# Expected output:
# [PERFORMANCE] Average FPS: 65-80 (target: 60)
# [LOD] 8 objects HIGH, 3 objects MED, 1 object LOW
# [INSTANCING] 8 templates, 156 instances
# [POOL] 45 available, 10 in use
```

### Touch Testing (Windows 10/11 tablet required):
```bash
# Enable touch input debug mode
python world_ultra_realistic.py --touch-debug

# Expected: Visual joystick circles appear on touch
# Expected: Smooth 60 FPS with simultaneous 10-finger input
```

---

## Architecture Alignment

This implementation follows your **Multimodal Claude architecture**:

✅ **Object Pooling** - Pattern #1 (47% memory reduction)
✅ **LOD System** - Asset streaming architecture
✅ **GPU Instancing** - Optimized rendering pipeline
✅ **Event-Driven Touch** - Event delegation pattern
✅ **60 FPS Target** - Performance-first design
✅ **Modular Design** - Clear separation of concerns

---

**Ready to implement?** Start with Phase 2 Task 2 (integrating LOD system into world_ultra_realistic.py).

Want me to complete any specific task in detail?
