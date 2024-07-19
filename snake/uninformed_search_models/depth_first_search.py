from snake.main.game import Game


class DFS(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = [self.head]
        self.closed = []

        # Calculate initial path
        self.generate_path()

    def generate_path(self):
        """Implements Depth First Search algorithm for snake traversal"""
        self.path = []
        self.closed = []
        self.open = [self.head]
        temp_snake = self.snake.copy()

        while self.open:
            # Pop last entry from the open stack
            current = self.open.pop()
            self.closed.append(current)

            # Check if snake has reached the goal state
            if current == self.food:
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                self.path.reverse()  # Ensure the path is in the correct order from head to food
                return

            # Simulate moving the snake
            temp_snake.insert(0, current)
            if temp_snake[-1] != self.food:
                temp_snake.pop()

            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if (
                    neighbor not in self.closed
                    and neighbor not in self.obstacles
                    and neighbor not in temp_snake
                ):
                    if neighbor not in self.open:
                        neighbor.origin = current
                        self.open.append(neighbor)
        self.path = []

    def main(self):
        self.multi_step_traversal()
