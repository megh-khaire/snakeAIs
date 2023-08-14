from snake.main.game import Game
from snake.resources.directions import Direction


class HillClimbing(Game):
    def __init__(self, game_has_obstacles):
        Game.__init__(self, game_has_obstacles)

    def calculate_h(self, point):
        """Calculates heuristic i.e the Manhatten distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Selects a direction for the snake to move using Hill Climbing (selection of the first better neighbor) algorithm"""
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        # Generate valid neighbors
        for direction in directions:
            neighbor = self.get_next_head(direction)
            if not self.detect_random_point_collision(neighbor):
                # Climb the hill if generated neighbor is better than current state
                current_h = self.calculate_h(self.head)
                neighbor.h = self.calculate_h(neighbor)
                if neighbor.h < current_h:
                    return direction
        return None

    def main(self):
        self.single_step_traversal()
