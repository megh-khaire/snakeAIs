from snake.main.game import Game


class AStar(Game):
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
        '''Implements A* Search algorithm for snake traversal'''
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            # Select start node as the node with lowest f value
            current = min(self.open, key=lambda x: x.f)
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
                if neighbor not in self.obstacles and neighbor not in self.snake:
                    g_temp = current.g + 1
                    # If neighbor is not in self.open increase the cost of path and append neighbor to open
                    if neighbor not in self.open and neighbor not in self.closed:
                        neighbor.h = self.calculate_h(neighbor)
                        neighbor.g = g_temp
                        neighbor.f = neighbor.g + neighbor.h
                        neighbor.origin = current
                        self.open.append(neighbor)
                    # If neighbor is in self.open or self.closed
                    else:
                        # If neighbor is in self.open check if current neighbor has a better g value
                        if neighbor in self.open:
                            old_neighbor = [x for x in self.open if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                # update heuristic and g value
                                old_neighbor.h = self.calculate_h(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                # update parent
                                old_neighbor.origin = current

                        # If neighbor is in self.open check if current neighbor has a better g value
                        elif neighbor in self.closed:
                            old_neighbor = [x for x in self.closed if x == neighbor][0]
                            if old_neighbor.g > g_temp:
                                # update heuristic and g value
                                old_neighbor.h = self.calculate_h(neighbor)
                                old_neighbor.g = g_temp
                                old_neighbor.f = neighbor.g + neighbor.h
                                # update parent
                                old_neighbor.origin = current
                                # Remove neighbor from closed and move it to open
                                self.closed = [self.closed[i] for i in range(len(self.closed)) if not self.closed[i] == old_neighbor]
                                self.open.append(old_neighbor)
        self.path = []
