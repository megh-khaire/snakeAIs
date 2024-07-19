from snake.main.game import Game


class AStar(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = [self.head]
        self.closed = []

        # Calculate initial path
        self.generate_path()

    def calculate_h(self, point):
        """Calculates heuristic i.e. the Manhattan distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Implements A* Search algorithm for snake traversal"""
        self.path = []
        self.closed = []
        self.open = [self.head]
        temp_snake = self.snake.copy()

        while self.open:
            # Select node with the lowest f value
            current = min(self.open, key=lambda x: x.f)
            self.open.remove(current)
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
                if neighbor not in self.obstacles and neighbor not in temp_snake:
                    g_temp = current.g + 1
                    if neighbor not in self.open and neighbor not in self.closed:
                        neighbor.h = self.calculate_h(neighbor)
                        neighbor.g = g_temp
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.origin = current
                        self.open.append(neighbor)
                    else:
                        # Check if this path to neighbor is better
                        if neighbor in self.open:
                            old_neighbor = next(x for x in self.open if x == neighbor)
                        elif neighbor in self.closed:
                            old_neighbor = next(x for x in self.closed if x == neighbor)
                            if old_neighbor.g > g_temp:
                                self.closed.remove(old_neighbor)
                                self.open.append(old_neighbor)
                        if old_neighbor.g > g_temp:
                            old_neighbor.g = g_temp
                            old_neighbor.f = old_neighbor.g + old_neighbor.h
                            old_neighbor.origin = current
        self.path = []

    def main(self):
        """Executes multi-step traversal based on the A* generated path."""
        self.multi_step_traversal()
