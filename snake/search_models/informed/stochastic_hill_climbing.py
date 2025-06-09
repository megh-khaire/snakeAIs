import random

from snake.configs.directions import Direction
from snake.main.game import Game


class StochasticHillClimbing(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)

    def calculate_h(self, point):
        """Calculates heuristic i.e. the Manhattan distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Selects a direction for the snake to move using Stochastic Hill Climbing (random selection of a better neighbor) algorithm"""
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        current_h = self.calculate_h(self.head)

        while directions:
            # Generate valid neighbor
            direction = random.choice(directions)
            neighbor = self.get_next_head(direction)
            if self.detect_random_point_collision(neighbor):
                directions.remove(direction)
            else:
                # Climb the hill if the generated neighbor is better than the current state
                neighbor_h = self.calculate_h(neighbor)
                if neighbor_h < current_h:
                    return direction
                else:
                    directions.remove(direction)
        return None

    def main(self):
        """Executes single-step traversal based on the Stochastic Hill Climbing algorithm."""
        self.single_step_traversal()
