from snake.main.game import Game


class BestFS(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)
        self.open = [self.head]
        self.closed = []

        # Calculate initial path
        self.generate_path()

    def calculate_h(self, point):
        '''Calculates heuristic i.e the Manhatten distance between selected node and goal state'''
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        '''Implements Best First Search algorithm for snake traversal'''
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            # Select start node as the node with lowest h value
            current = min(self.open, key=lambda x: x.h)
            # Remove selected node from self.open
            self.open = [self.open[i] for i in range(len(self.open)) if not self.open[i] == current]
            # Append selected node to closed_points
            self.closed.append(current)
            # Check if snake has reached the goal state
            if current == self.food:
                # Based on its origin determine the direction in which the snake will move
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                return
            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if neighbor not in self.closed and neighbor not in self.obstacles and neighbor not in self.snake:
                    # If neighbor is not in self.open increase the cost of path and append neighbor to self.open
                    if neighbor not in self.open:
                        neighbor.h = self.calculate_h(neighbor)
                        neighbor.origin = current
                        self.open.append(neighbor)
        self.path = []
