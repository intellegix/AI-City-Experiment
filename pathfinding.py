"""
Advanced Pathfinding System for NPC Navigation
Implements A* algorithm with optimizations for city navigation
"""
import numpy as np
from typing import List, Tuple, Optional, Set
from dataclasses import dataclass
import heapq
from collections import deque


@dataclass
class PathNode:
    """Node in pathfinding graph"""
    position: Tuple[int, int]
    g_cost: float  # Cost from start
    h_cost: float  # Heuristic cost to goal
    parent: Optional['PathNode'] = None

    @property
    def f_cost(self) -> float:
        """Total cost (g + h)"""
        return self.g_cost + self.h_cost

    def __lt__(self, other):
        """Compare based on f_cost for heap"""
        return self.f_cost < other.f_cost

    def __eq__(self, other):
        """Compare based on position"""
        return self.position == other.position

    def __hash__(self):
        """Hash based on position"""
        return hash(self.position)


class AStar:
    """
    A* pathfinding algorithm implementation.
    Optimized for grid-based navigation with obstacle avoidance.
    """

    @staticmethod
    def heuristic(a: Tuple[int, int], b: Tuple[int, int], metric: str = "manhattan") -> float:
        """
        Calculate heuristic distance between two points.

        Args:
            a, b: Coordinate tuples
            metric: "manhattan", "euclidean", or "diagonal"

        Returns:
            Estimated distance
        """
        if metric == "manhattan":
            return abs(a[0] - b[0]) + abs(a[1] - b[1])
        elif metric == "euclidean":
            return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)
        elif metric == "diagonal":
            # Diagonal distance (Chebyshev)
            return max(abs(a[0] - b[0]), abs(a[1] - b[1]))
        return 0.0

    @staticmethod
    def find_path(
        start: Tuple[int, int],
        goal: Tuple[int, int],
        walkable_grid: np.ndarray,
        allow_diagonal: bool = True,
        max_iterations: int = 10000
    ) -> Optional[List[Tuple[int, int]]]:
        """
        Find shortest path from start to goal using A*.

        Args:
            start: Starting position (x, y)
            goal: Goal position (x, y)
            walkable_grid: Boolean grid where True = walkable
            allow_diagonal: Allow diagonal movement
            max_iterations: Maximum search iterations

        Returns:
            List of positions from start to goal, or None if no path
        """
        if not AStar._is_valid_position(start, walkable_grid):
            return None
        if not AStar._is_valid_position(goal, walkable_grid):
            return None

        # Initialize open and closed sets
        open_set = []
        closed_set: Set[Tuple[int, int]] = set()

        # Create start node
        start_node = PathNode(
            position=start,
            g_cost=0,
            h_cost=AStar.heuristic(start, goal, "euclidean")
        )

        heapq.heappush(open_set, start_node)
        open_dict = {start: start_node}

        iterations = 0

        while open_set and iterations < max_iterations:
            iterations += 1

            # Get node with lowest f_cost
            current = heapq.heappop(open_set)
            del open_dict[current.position]

            # Check if goal reached
            if current.position == goal:
                return AStar._reconstruct_path(current)

            closed_set.add(current.position)

            # Check neighbors
            neighbors = AStar._get_neighbors(current.position, walkable_grid, allow_diagonal)

            for neighbor_pos in neighbors:
                if neighbor_pos in closed_set:
                    continue

                # Calculate costs
                move_cost = AStar._get_move_cost(current.position, neighbor_pos)
                g_cost = current.g_cost + move_cost
                h_cost = AStar.heuristic(neighbor_pos, goal, "euclidean")

                # Check if neighbor is in open set
                if neighbor_pos in open_dict:
                    neighbor_node = open_dict[neighbor_pos]
                    if g_cost < neighbor_node.g_cost:
                        # Found better path to this neighbor
                        neighbor_node.g_cost = g_cost
                        neighbor_node.parent = current
                        heapq.heapify(open_set)  # Re-sort heap
                else:
                    # Add new neighbor to open set
                    neighbor_node = PathNode(
                        position=neighbor_pos,
                        g_cost=g_cost,
                        h_cost=h_cost,
                        parent=current
                    )
                    heapq.heappush(open_set, neighbor_node)
                    open_dict[neighbor_pos] = neighbor_node

        # No path found
        return None

    @staticmethod
    def _is_valid_position(pos: Tuple[int, int], grid: np.ndarray) -> bool:
        """Check if position is valid and walkable"""
        x, y = pos
        return (0 <= x < grid.shape[1] and
                0 <= y < grid.shape[0] and
                grid[y, x])

    @staticmethod
    def _get_neighbors(
        pos: Tuple[int, int],
        grid: np.ndarray,
        allow_diagonal: bool
    ) -> List[Tuple[int, int]]:
        """Get valid neighboring positions"""
        x, y = pos
        neighbors = []

        # Cardinal directions
        directions = [
            (0, 1),   # Right
            (1, 0),   # Down
            (0, -1),  # Left
            (-1, 0),  # Up
        ]

        if allow_diagonal:
            # Diagonal directions
            directions.extend([
                (1, 1),   # Down-right
                (1, -1),  # Up-right
                (-1, 1),  # Down-left
                (-1, -1), # Up-left
            ])

        for dx, dy in directions:
            new_pos = (x + dx, y + dy)
            if AStar._is_valid_position(new_pos, grid):
                # For diagonal movement, check that both cardinal neighbors are walkable
                if allow_diagonal and abs(dx) + abs(dy) == 2:
                    if (AStar._is_valid_position((x + dx, y), grid) and
                        AStar._is_valid_position((x, y + dy), grid)):
                        neighbors.append(new_pos)
                else:
                    neighbors.append(new_pos)

        return neighbors

    @staticmethod
    def _get_move_cost(from_pos: Tuple[int, int], to_pos: Tuple[int, int]) -> float:
        """Calculate movement cost between adjacent positions"""
        dx = abs(to_pos[0] - from_pos[0])
        dy = abs(to_pos[1] - from_pos[1])

        # Diagonal movement costs more
        if dx + dy == 2:
            return 1.414  # sqrt(2)
        return 1.0

    @staticmethod
    def _reconstruct_path(node: PathNode) -> List[Tuple[int, int]]:
        """Reconstruct path from goal node to start"""
        path = []
        current = node

        while current is not None:
            path.append(current.position)
            current = current.parent

        return list(reversed(path))


class PathSmoother:
    """
    Path smoothing utilities for more natural movement.
    Reduces zigzag patterns in paths.
    """

    @staticmethod
    def smooth_path(
        path: List[Tuple[int, int]],
        walkable_grid: np.ndarray,
        iterations: int = 2
    ) -> List[Tuple[int, int]]:
        """
        Smooth path by removing unnecessary waypoints.
        Uses line-of-sight checks to skip intermediate points.
        """
        if not path or len(path) < 3:
            return path

        smoothed = path.copy()

        for _ in range(iterations):
            i = 0
            while i < len(smoothed) - 2:
                start = smoothed[i]
                end = smoothed[i + 2]

                # Check if we can move directly from start to end
                if PathSmoother._has_line_of_sight(start, end, walkable_grid):
                    # Remove intermediate point
                    smoothed.pop(i + 1)
                else:
                    i += 1

        return smoothed

    @staticmethod
    def _has_line_of_sight(
        start: Tuple[int, int],
        end: Tuple[int, int],
        walkable_grid: np.ndarray
    ) -> bool:
        """
        Check if there's a clear line of sight between two points.
        Uses Bresenham's line algorithm.
        """
        x0, y0 = start
        x1, y1 = end

        dx = abs(x1 - x0)
        dy = abs(y1 - y0)

        sx = 1 if x0 < x1 else -1
        sy = 1 if y0 < y1 else -1

        err = dx - dy

        while True:
            # Check if current position is walkable
            if not (0 <= x0 < walkable_grid.shape[1] and
                    0 <= y0 < walkable_grid.shape[0]):
                return False

            if not walkable_grid[y0, x0]:
                return False

            if x0 == x1 and y0 == y1:
                break

            e2 = 2 * err

            if e2 > -dy:
                err -= dy
                x0 += sx

            if e2 < dx:
                err += dx
                y0 += sy

        return True


class FlowField:
    """
    Flow field pathfinding for multiple agents heading to same goal.
    More efficient than individual A* for crowds.
    """

    def __init__(self, grid_size: Tuple[int, int]):
        self.width, self.height = grid_size
        self.flow_field = np.zeros((self.height, self.width, 2), dtype=np.float32)

    def generate(
        self,
        goal: Tuple[int, int],
        walkable_grid: np.ndarray
    ):
        """
        Generate flow field pointing toward goal.
        Uses Dijkstra's algorithm to compute distances from goal.
        """
        # Initialize distance map
        distance_map = np.full((self.height, self.width), float('inf'))
        distance_map[goal[1], goal[0]] = 0

        # BFS from goal to compute distances
        queue = deque([goal])
        visited = {goal}

        while queue:
            x, y = queue.popleft()

            # Check neighbors
            for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.width and 0 <= ny < self.height and
                    (nx, ny) not in visited and walkable_grid[ny, nx]):

                    distance_map[ny, nx] = distance_map[y, x] + 1
                    visited.add((nx, ny))
                    queue.append((nx, ny))

        # Generate flow vectors pointing toward lower distance
        for y in range(self.height):
            for x in range(self.width):
                if not walkable_grid[y, x]:
                    continue

                # Find neighbor with lowest distance
                best_dir = (0, 0)
                min_dist = distance_map[y, x]

                for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0),
                               (1, 1), (1, -1), (-1, 1), (-1, -1)]:
                    nx, ny = x + dx, y + dy

                    if (0 <= nx < self.width and 0 <= ny < self.height and
                        distance_map[ny, nx] < min_dist):
                        min_dist = distance_map[ny, nx]
                        best_dir = (dx, dy)

                # Normalize direction
                if best_dir != (0, 0):
                    length = np.sqrt(best_dir[0]**2 + best_dir[1]**2)
                    self.flow_field[y, x] = (best_dir[0] / length, best_dir[1] / length)

    def get_direction(self, pos: Tuple[int, int]) -> Tuple[float, float]:
        """Get flow direction at position"""
        x, y = pos
        if 0 <= x < self.width and 0 <= y < self.height:
            return tuple(self.flow_field[y, x])
        return (0, 0)


if __name__ == "__main__":
    # Test pathfinding
    grid_size = 50
    walkable = np.ones((grid_size, grid_size), dtype=bool)

    # Add some obstacles
    walkable[20:30, 20:30] = False
    walkable[10, :] = False

    # Find path
    start = (5, 5)
    goal = (45, 45)

    print("Finding path...")
    path = AStar.find_path(start, goal, walkable)

    if path:
        print(f"Path found! Length: {len(path)}")

        # Smooth path
        smoothed = PathSmoother.smooth_path(path, walkable)
        print(f"Smoothed path length: {len(smoothed)}")
    else:
        print("No path found!")
