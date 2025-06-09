from collections import deque

from snake.main.game import Game


class DFS(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = []  # Will be used as a stack
        self.closed = set()

        # Calculate initial path
        self.generate_path()

    def generate_path(self):
        """Implements Depth First Search algorithm for snake traversal"""
        self.path = []
        self.closed = set()
        self.open = []  # Initialize as empty list

        if self.head:
            self.head.origin = None  # Ensure origin is None for the head
            self.open.append(self.head)  # Add head to start DFS

        while self.open:
            # Pop last entry from the open stack
            current = self.open.pop()

            if (
                current in self.closed
            ):  # Avoid processing already visited nodes in cycles
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
                if (
                    neighbor in self.closed  # Already visited
                    or neighbor in self.obstacles  # Obstacle
                    or neighbor in current_simulated_snake  # Snake body collision
                    or neighbor
                    in self.open  # Already in stack to be visited
                ):
                    continue

                neighbor.origin = current
                self.open.append(neighbor)

        # If the loop finishes, no path was found, self.path remains [] as initialized.

    def main(self):
        return self.multi_step_traversal()
