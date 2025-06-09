import heapq
from collections import deque

from snake.main.game import Game


class BestFS(Game):
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
        """Implements Best First Search algorithm for snake traversal"""
        self.path = []
        self.open = []
        self.closed = set()
        self.counter = 0  # Reset counter for each path generation call

        # Initialize the start node
        # For BestFS, only h matters for priority. g and f are not strictly needed for the algorithm itself.
        self.head.h = self.calculate_h(self.head)
        self.head.origin = None  # Ensure origin is None for the head
        heapq.heappush(self.open, (self.head.h, self.counter, self.head))
        self.counter += 1

        # food_eaten flag not needed due to early return

        while self.open:
            # Select node with the lowest h value
            _h_value, _count, current = heapq.heappop(self.open)

            if current in self.closed:  # Already processed this node
                continue
            self.closed.add(current)

            is_current_node_food = current == self.food

            # Simulate moving the snake to current position for collision checks
            current_simulated_snake = deque(
                self.snake
            )  # Start with actual game snake state
            current_simulated_snake.appendleft(current)  # Assume head moves to current
            if not is_current_node_food:
                if len(current_simulated_snake) > 1:  # Snake grows if food is eaten
                    current_simulated_snake.pop()  # Tail moves forward only if not eating

            # Check if snake has reached the goal state (food)
            if is_current_node_food:
                # Reconstruct path
                while current.origin:  # Backtrack from food to head
                    self.path.append(current)
                    current = current.origin
                self.path.reverse()
                return

            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if neighbor in self.obstacles or neighbor in current_simulated_snake:
                    continue

                if (
                    neighbor in self.closed
                ):  # Already found the optimal path (by h) to this neighbor
                    continue

                # The neighbor Point object from generate_neighbors() is a new instance.
                # Set its h and origin for this specific path consideration.
                neighbor.h = self.calculate_h(neighbor)
                neighbor.origin = current
                heapq.heappush(self.open, (neighbor.h, self.counter, neighbor))
                self.counter += 1

        # If the loop finishes, no path was found, self.path remains [] as initialized.

    def main(self):
        self.multi_step_traversal()
