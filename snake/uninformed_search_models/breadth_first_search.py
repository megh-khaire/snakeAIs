from snake.main.game import Game


class BFS(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = [self.head]
        self.closed = []

        # Calculate initial path
        self.generate_path()

    def generate_path(self):
        """Implements Breadth First Search algorithm for snake traversal"""
        self.path = []
        self.closed = []
        self.open = [self.head]
        temp_snake = self.snake.copy()
        food_eaten = False

        while self.open:
            # Pop first entry from the open queue
            current = self.open.pop(0)
            self.closed.append(current)

            # Check if snake has reached the goal state (food)
            if current == self.food:
                food_eaten = True
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                self.path.reverse()  # Ensure the path is in the correct order from head to food
                return

            # Simulate moving the snake
            temp_snake.insert(0, current)
            if not food_eaten:
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
