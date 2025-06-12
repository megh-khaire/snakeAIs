import random

from snake.configs.directions import Direction
from snake.main.game import Game


class Random(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)

    def generate_path(self):
        """Randomly selects a direction for the snake to move"""
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        while directions:
            direction = random.choice(directions)
            random_point = self.get_next_head(direction)
            if self.detect_random_point_collision(random_point):
                directions.remove(direction)
            else:
                return direction
        return None

    def main(self):
        """Executes single-step traversal based on the randomly selected path."""
        return self.single_step_traversal()
