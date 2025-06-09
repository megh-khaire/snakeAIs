import heapq
from collections import deque

from snake.main.game import Game


class AStar(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = []  # Will be a min-priority queue (heap)
        self.closed = set()
        self.counter = 0  # Initialize counter

        # Calculate initial path
        self.generate_path()

    def calculate_h(self, point):
        """Calculates heuristic i.e. the Manhattan distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Implements A* Search algorithm for snake traversal"""
        self.path = []
        self.open = []
        self.closed = set()
        self.counter = 0  # Reset counter for each path generation call

        # Initialize the start node
        self.head.g = 0
        self.head.h = self.calculate_h(self.head)
        self.head.f = self.head.g + self.head.h
        self.head.origin = None  # Ensure origin is None for the head
        heapq.heappush(self.open, (self.head.f, self.counter, self.head))
        self.counter += 1

        while self.open:
            # Select node with the lowest f value
            _f_value, _count, current = heapq.heappop(self.open)

            if (current in self.closed):
                # Already processed this node via a shorter or equal path
                continue
            self.closed.add(current)

            is_current_node_food = current == self.food

            # Simulate moving the snake to current position for collision checks
            current_simulated_snake = deque(self.snake)
            # Start with actual game snake state
            current_simulated_snake.appendleft(current)  # Assume head moves to current
            if not is_current_node_food:
                if len(current_simulated_snake) > 1:  # Snake grows if food is eaten
                    current_simulated_snake.pop()  # Tail moves forward only if not eating

            # Check if snake has reached the goal state (food)
            if is_current_node_food:
                # Reconstruct path - backtrack from food to head
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                self.path.reverse()
                return

            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                # Basic collision checks
                if neighbor in self.obstacles or neighbor in current_simulated_snake:
                    continue

                if (neighbor in self.closed):
                    # Already found the optimal path to this neighbor
                    continue

                neighbor.g = current.g + 1
                neighbor.h = self.calculate_h(neighbor)
                neighbor.f = neighbor.g + neighbor.h
                neighbor.origin = current
                heapq.heappush(self.open, (neighbor.f, self.counter, neighbor))
                self.counter += 1

        # If the loop finishes, no path was found, self.path remains [] as initialized.

    def main(self):
        """Executes multi-step traversal based on the A* generated path."""
        self.multi_step_traversal()
