import random
from snake.main.game import Game
from snake.resources.directions import Direction


class StochasticHillClimbing(Game):
    def __init__(self, game_has_obstacles):
        Game.__init__(self, game_has_obstacles)

    def calculate_h(self, point):
        '''Calculates heuristic i.e the Manhatten distance between selected node and goal state'''
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        '''Selects a direction for the snake to move using Stochastic Hill Climbing (random selection of a better neighbor) algorithm'''
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        while directions:
            # Generate valid neighbor
            direction = random.choice(directions)
            neighbor = self.get_next_head(direction)
            if self.detect_random_point_collision(neighbor, 0):
                directions.remove(direction)
            else:
                # Climb the hill if the generated neighbor is better than current state
                current_h = self.calculate_h(self.head)
                neighbor_h = self.calculate_h(neighbor)
                if neighbor_h < current_h:
                    return direction
                else:
                    directions.remove(direction)
        return None

    def main(self):
        self.single_step_traversal()
