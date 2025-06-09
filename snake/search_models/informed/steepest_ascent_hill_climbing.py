from snake.configs.directions import Direction
from snake.main.game import Game


class SteepestAscentHillClimbing(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)

    def calculate_h(self, point):
        """Calculates heuristic i.e. the Manhattan distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Selects a direction for the snake to move using Steepest Ascent Hill Climbing (selection of best neighbor) algorithm"""
        neighbors = []
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]

        # Generate valid neighbors
        for direction in directions:
            neighbor = self.get_next_head(direction)
            if not self.detect_random_point_collision(neighbor):
                neighbor.h = self.calculate_h(neighbor)
                neighbors.append((neighbor, direction))

        if neighbors:
            # Climb the hill if best neighbor is better than current state
            current_h = self.calculate_h(self.head)
            best_neighbor, best_direction = min(neighbors, key=lambda x: x[0].h)
            if best_neighbor.h < current_h:
                return best_direction
        return None

    def main(self):
        """Executes single-step traversal based on the Steepest Ascent Hill Climbing algorithm."""
        self.single_step_traversal()
