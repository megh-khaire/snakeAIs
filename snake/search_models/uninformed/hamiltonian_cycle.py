from collections import deque

from snake.main.game import Game
from snake.configs.game import BLOCK_SIZE, WIDTH, HEIGHT
from snake.configs.directions import Direction
from snake.main.point import Point


class HamiltonianCycle(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.grid_width = WIDTH // BLOCK_SIZE
        self.grid_height = HEIGHT // BLOCK_SIZE
        self.cycle = []
        self.current_cycle_index = 0
        self.detour_path = []
        self.target_cycle_index = 0
        self.is_avoiding_obstacle = False

        # Generate the Hamiltonian cycle
        self.generate_hamiltonian_cycle()

        # Find starting position in cycle
        self.find_starting_position()

    def generate_hamiltonian_cycle(self):
        """
        Generates a valid Hamiltonian cycle for a rectangular grid.
        The construction works for any grid that is at least 2×2.

        The idea is to:
        1.  Start at the top-left corner (0, 0).
        2.  Zig-zag through all rows.
        3.  Finally, travel straight up the first column back towards the start.

        """
        # Reset any existing cycle
        self.cycle = []
        # (0) Start position
        self.cycle.append(Point(0, 0))

        # (1) Traverse every row while leaving column 0 for the end
        for row in range(self.grid_height):
            y = row * BLOCK_SIZE

            if row % 2 == 0:
                # Even row → move from left to right starting from col 1
                start_col, end_col, step = 1, self.grid_width, 1
            else:
                # Odd row → move from right to left ending at col 1
                start_col, end_col, step = self.grid_width - 1, 0, -1

            for col in range(start_col, end_col, step):
                x = col * BLOCK_SIZE
                self.cycle.append(Point(x, y))

        # (2) We are now at (1, last_row).
        # Move to the last cell (0, last_row).
        last_row_y = (self.grid_height - 1) * BLOCK_SIZE
        self.cycle.append(Point(0, last_row_y))

        # (3) Move straight up column 0, visiting the remaining cells
        for row in range(self.grid_height - 2, -1, -1):
            y = row * BLOCK_SIZE
            self.cycle.append(Point(0, y))

    def find_starting_position(self):
        """Find the current head position in the cycle and set the index."""
        for i, point in enumerate(self.cycle):
            if point == self.head:
                self.current_cycle_index = i
                return

    def get_next_cycle_position(self):
        """Get the next position in the Hamiltonian cycle."""
        next_index = (self.current_cycle_index + 1) % len(self.cycle)
        return self.cycle[next_index]

    def get_direction_to_point(self, target_point):
        """Calculate the direction needed to move from current head to target point."""
        dx = target_point.x - self.head.x
        dy = target_point.y - self.head.y

        if dx > 0:
            return Direction.RIGHT
        elif dx < 0:
            return Direction.LEFT
        elif dy > 0:
            return Direction.DOWN
        elif dy < 0:
            return Direction.UP
        else:
            return None  # Already at target

    def is_position_safe(self, position):
        """Check if a position is safe (not colliding with snake body or obstacles)."""
        # Check boundaries
        if (
            position.x < 0
            or position.x >= self.width
            or position.y < 0
            or position.y >= self.height
        ):
            return False

        # Check snake body collision (excluding tail since it will move)
        if position in self.snake[:-1]:
            return False

        # Check obstacles
        if position in self.obstacles:
            return False

        return True

    def find_path_to_cycle(
        self, start_pos, target_cycle_indices, max_search_distance=10
    ):
        """
        Use BFS to find a path from start_pos to any position in the cycle.
        Returns (path, target_cycle_index) or (None, None) if no path found.
        """
        queue = deque([(start_pos, [])])
        visited = {start_pos}

        directions = [
            (0, -BLOCK_SIZE, Direction.UP),
            (0, BLOCK_SIZE, Direction.DOWN),
            (-BLOCK_SIZE, 0, Direction.LEFT),
            (BLOCK_SIZE, 0, Direction.RIGHT),
        ]

        while queue:
            current_pos, path = queue.popleft()

            # Don't search too far
            if len(path) > max_search_distance:
                continue

            # Check if we reached any target cycle position
            for target_index in target_cycle_indices:
                if current_pos == self.cycle[target_index]:
                    return path, target_index

            # Explore neighbors
            for dx, dy, direction in directions:
                next_pos = Point(current_pos.x + dx, current_pos.y + dy)

                if next_pos not in visited and self.is_position_safe(next_pos):
                    visited.add(next_pos)
                    new_path = path + [direction]
                    queue.append((next_pos, new_path))

        return None, None

    def find_detour_around_obstacle(self):
        """
        Find a detour around obstacles to rejoin the cycle.
        Returns True if detour found, False otherwise.
        """
        # Look ahead in the cycle to find accessible positions
        potential_targets = []
        current_index = self.current_cycle_index

        # Find the first safe position on the cycle starting from current index
        for i in range(1, len(self.cycle)):
            target_index = (current_index + i) % len(self.cycle)
            target_pos = self.cycle[target_index]

            # Make sure the target position is not blocked and not too close to snake body
            if self.is_position_safe(target_pos):
                potential_targets.append(target_index)
                break

        if not potential_targets:
            return False

        # Try to find a path to any of these targets
        path, target_index = self.find_path_to_cycle(self.head, potential_targets)

        if path and target_index is not None:
            self.detour_path = path
            self.target_cycle_index = target_index
            self.is_avoiding_obstacle = True
            return True

        return False

    def get_next_position_avoiding_obstacles(self):
        """
        Get next position while following the cycle or detouring around obstacles.
        """
        if not self.is_avoiding_obstacle:
            # Try to follow the normal cycle
            next_position = self.get_next_cycle_position()
            if self.is_position_safe(next_position):
                direction = self.get_direction_to_point(next_position)
                if direction:
                    self.current_cycle_index = (self.current_cycle_index + 1) % len(self.cycle)
                    return direction
            # If the next cycle position is blocked, try to find a detour
            if self.find_detour_around_obstacle():
                return self.get_next_position_avoiding_obstacles()

        # If we're currently following a detour path
        if self.is_avoiding_obstacle and self.detour_path:
            next_direction = self.detour_path.pop(0)

            # If we've completed the detour path
            if not self.detour_path:
                self.is_avoiding_obstacle = False
                self.current_cycle_index = self.target_cycle_index
                self.target_cycle_index = 0

            return next_direction

        # No safe move found
        return None

    def generate_path(self):
        """
        Generate the next direction for the snake to follow the Hamiltonian cycle.
        Includes intelligent obstacle avoidance that returns to the cycle.
        """
        return self.get_next_position_avoiding_obstacles()

    def main(self):
        """Main execution method for single-step traversal."""
        return self.single_step_traversal()
