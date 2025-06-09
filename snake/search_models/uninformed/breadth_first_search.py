from collections import deque

from snake.main.game import Game


class BFS(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = deque()
        self.closed = set()

        # Calculate initial path
        self.generate_path()

    def generate_path(self):
        """Implements Breadth First Search algorithm for snake traversal"""
        self.path = []
        self.closed = set()
        self.open = deque()

        if self.head:
            self.head.origin = None  # Ensure origin is None for the head
            self.open.append(self.head)

        while self.open:
            # Pop first entry from the open queue
            current = self.open.popleft()

            if (
                current in self.closed
            ):  # Should not happen if we check before adding to open
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
                    or neighbor in self.open  # Already in queue to be visited
                ):
                    continue

                neighbor.origin = current
                self.open.append(neighbor)

        # If the loop finishes, no path was found, self.path remains [] as initialized.

    def main(self):
        self.multi_step_traversal()
