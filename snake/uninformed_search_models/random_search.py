import random
from snake.main.game import Game
from snake.resources.directions import Direction


class Random(Game):
    def __init__(self):
        Game.__init__(self)

    def generate_path(self):
        '''Randomly selects a direction for the snake to move'''
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        while directions:
            direction = random.choice(directions)
            random_point = self.get_next_head(direction)
            if self.detect_random_point_collision(random_point, 0):
                directions.remove(direction)
            else:
                return direction
        return None

    def main(self):
        self.single_step_traversal()
