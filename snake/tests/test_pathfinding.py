import unittest
from unittest.mock import patch, MagicMock

from snake.main.point import Point
from snake.configs.game import WIDTH, HEIGHT, BLOCK_SIZE # Using actual game dimensions for now

# Import algorithm classes
from snake.uninformed_search_models.breadth_first_search import BFS
from snake.uninformed_search_models.depth_first_search import DFS
from snake.informed_search_models.a_star_search import AStar
from snake.informed_search_models.best_first_search import BestFS

# Test dimensions can be actual game dimensions or smaller specific ones
# Using smaller dimensions for pathfinding tests can speed them up and simplify debugging.
TEST_WIDTH = 10 * BLOCK_SIZE 
TEST_HEIGHT = 10 * BLOCK_SIZE

def configure_mock_pygame(mock_pygame_obj):
    """Helper to configure the mocked pygame object."""
    # Reset call counts etc. before reconfiguring for a specific test context
    mock_pygame_obj.reset_mock() 
    
    # Configure return values for pygame calls made in Game.__init__
    mock_pygame_obj.display.set_mode.return_value = MagicMock()
    mock_pygame_obj.font.SysFont.return_value = MagicMock()
    mock_pygame_obj.display.set_caption.return_value = MagicMock() # Though not strictly necessary for pathfinding logic
    mock_pygame_obj.time.Clock.return_value = MagicMock()      # Though not strictly necessary for pathfinding logic


@patch('snake.main.game.pygame') # Mocks pygame for all test methods in this class
class TestPathfindingAlgorithms(unittest.TestCase):

    # --- Helper (runner) methods for different test scenarios ---
    # These are called by the actual test methods (test_bfs_xxx, test_dfs_xxx, etc.)
    # They receive the algorithm class, its name for logging, and the mock_pygame instance.

    def run_test_simple_path(self, algorithm_class, algorithm_name, current_mock_pygame):
        configure_mock_pygame(current_mock_pygame) # Configure mock before algorithm instantiation
        algo = algorithm_class(game_has_obstacles=False)
        algo.width = TEST_WIDTH # Use test dimensions
        algo.height = TEST_HEIGHT
        
        algo.head = Point(0, 0)
        algo.food = Point(BLOCK_SIZE * 2, 0) # Two steps to the right
        algo.snake = [algo.head]
        algo.obstacles = []

        algo.generate_path()
        
        self.assertTrue(len(algo.path) > 0, f"{algorithm_name}: Path should not be empty for a simple case. Path: {algo.path}")
        self.assertEqual(len(algo.path), 2, f"{algorithm_name}: Path length should be 2 for this simple case. Path: {algo.path}")
        if algo.path and len(algo.path) == 2:
            first_step_expected = Point(BLOCK_SIZE, 0)
            self.assertEqual(algo.path[0], first_step_expected, f"{algorithm_name}: First step is incorrect.")
            self.assertEqual(algo.path[1], algo.food, f"{algorithm_name}: Last step should be food.")
        for p_idx, p_obj in enumerate(algo.path): # Check all items are Point objects
            self.assertIsInstance(p_obj, Point, f"{algorithm_name}: Item at index {p_idx} in path is not a Point object.")

    def run_test_no_path_blocked(self, algorithm_class, algorithm_name, current_mock_pygame):
        configure_mock_pygame(current_mock_pygame)
        algo = algorithm_class(game_has_obstacles=True) # game_has_obstacles can be True
        algo.width = TEST_WIDTH
        algo.height = TEST_HEIGHT

        algo.head = Point(0, 0)
        algo.food = Point(BLOCK_SIZE * 2, 0)
        algo.snake = [algo.head]
        # To ensure no path to (2*BS, 0), block the only intermediate step (BS,0)
        # and also spaces around the food to be certain.
        algo.obstacles = [
            Point(BLOCK_SIZE, 0),                   # Blocks direct path
            Point(BLOCK_SIZE * 2, BLOCK_SIZE),    # Below food
            Point(BLOCK_SIZE * 3, 0),             # Right of food (if in bounds)
            Point(BLOCK_SIZE, -BLOCK_SIZE),       # Above food (if valid, but usually not)
            # More robustly for food at (2,0) relative to (0,0) head:
            # Block (1,0), (2,1), (1,1), (0,1) if trying to go around (1,0)
            Point(BLOCK_SIZE, BLOCK_SIZE),        # Block potential detour path
            Point(0, BLOCK_SIZE),                 # Block potential detour path
        ]
        # Critical obstacle to block path from (0,0) to (2*BS,0)
        algo.obstacles = [Point(BLOCK_SIZE,0)]


        algo.generate_path()
        self.assertEqual(len(algo.path), 0, f"{algorithm_name}: Path should be empty when food is blocked. Path found: {algo.path}")

    def run_test_path_with_obstacles(self, algorithm_class, algorithm_name, current_mock_pygame):
        configure_mock_pygame(current_mock_pygame)
        algo = algorithm_class(game_has_obstacles=True)
        algo.width = TEST_WIDTH 
        algo.height = TEST_HEIGHT

        algo.head = Point(0, 0)
        algo.food = Point(BLOCK_SIZE * 2, 0) 
        algo.snake = [algo.head]
        algo.obstacles = [Point(BLOCK_SIZE, 0)] # Obstacle at (1,0), forcing a detour

        algo.generate_path()
        
        self.assertTrue(len(algo.path) > 0, f"{algorithm_name}: Path should be found around obstacle. Path: {algo.path}")
        if algo.path:
            self.assertEqual(algo.path[-1], algo.food, f"{algorithm_name}: Path should lead to food.")
            for p_obstacle in algo.obstacles:
                self.assertNotIn(p_obstacle, algo.path, f"{algorithm_name}: Path should not go through obstacles.")
        
        # Verify path points are valid steps (adjacent)
        last_point = algo.head
        for p_idx, p_step in enumerate(algo.path):
            self.assertIsInstance(p_step, Point, f"{algorithm_name}: Path item at index {p_idx} is not a Point.")
            dx = abs(p_step.x - last_point.x)
            dy = abs(p_step.y - last_point.y)
            is_valid_step = (dx == BLOCK_SIZE and dy == 0) or (dx == 0 and dy == BLOCK_SIZE)
            self.assertTrue(is_valid_step,
                            f"{algorithm_name}: Path step from {last_point} to {p_step} is not valid (not adjacent or diagonal).")
            last_point = p_step


    def run_test_food_adjacent(self, algorithm_class, algorithm_name, current_mock_pygame):
        configure_mock_pygame(current_mock_pygame)
        algo = algorithm_class(game_has_obstacles=False)
        algo.width = TEST_WIDTH
        algo.height = TEST_HEIGHT

        algo.head = Point(0, 0)
        algo.food = Point(BLOCK_SIZE, 0) 
        algo.snake = [algo.head]
        algo.obstacles = []

        algo.generate_path()
        self.assertEqual(len(algo.path), 1, f"{algorithm_name}: Path should be 1 step long. Path: {algo.path}")
        if algo.path: # Check if path is not empty before accessing its elements
            self.assertEqual(algo.path[0], algo.food, f"{algorithm_name}: Path should directly go to adjacent food.")

    def run_test_food_on_head(self, algorithm_class, algorithm_name, current_mock_pygame):
        configure_mock_pygame(current_mock_pygame)
        algo = algorithm_class(game_has_obstacles=False)
        algo.width = TEST_WIDTH
        algo.height = TEST_HEIGHT

        algo.head = Point(0, 0)
        algo.food = Point(0, 0) 
        algo.snake = [algo.head]
        algo.obstacles = []

        algo.generate_path()
        self.assertEqual(len(algo.path), 0, f"{algorithm_name}: Path should be empty if food is on head. Path: {algo.path}")

    # --- Test methods for each algorithm, passing the mock from the decorator ---

    def test_bfs_simple_path(self, mock_pygame_injected):
        self.run_test_simple_path(BFS, "BFS", mock_pygame_injected)
    def test_bfs_no_path_blocked(self, mock_pygame_injected):
        self.run_test_no_path_blocked(BFS, "BFS", mock_pygame_injected)
    def test_bfs_path_with_obstacles(self, mock_pygame_injected):
        self.run_test_path_with_obstacles(BFS, "BFS", mock_pygame_injected)
    def test_bfs_food_adjacent(self, mock_pygame_injected):
        self.run_test_food_adjacent(BFS, "BFS", mock_pygame_injected)
    def test_bfs_food_on_head(self, mock_pygame_injected):
        self.run_test_food_on_head(BFS, "BFS", mock_pygame_injected)

    def test_dfs_simple_path(self, mock_pygame_injected):
        self.run_test_simple_path(DFS, "DFS", mock_pygame_injected)
    def test_dfs_no_path_blocked(self, mock_pygame_injected):
        self.run_test_no_path_blocked(DFS, "DFS", mock_pygame_injected)
    def test_dfs_path_with_obstacles(self, mock_pygame_injected):
        self.run_test_path_with_obstacles(DFS, "DFS", mock_pygame_injected)
    def test_dfs_food_adjacent(self, mock_pygame_injected):
        self.run_test_food_adjacent(DFS, "DFS", mock_pygame_injected)
    def test_dfs_food_on_head(self, mock_pygame_injected):
        self.run_test_food_on_head(DFS, "DFS", mock_pygame_injected)

    def test_astar_simple_path(self, mock_pygame_injected):
        self.run_test_simple_path(AStar, "AStar", mock_pygame_injected)
    def test_astar_no_path_blocked(self, mock_pygame_injected):
        self.run_test_no_path_blocked(AStar, "AStar", mock_pygame_injected)
    def test_astar_path_with_obstacles(self, mock_pygame_injected):
        self.run_test_path_with_obstacles(AStar, "AStar", mock_pygame_injected)
    def test_astar_food_adjacent(self, mock_pygame_injected):
        self.run_test_food_adjacent(AStar, "AStar", mock_pygame_injected)
    def test_astar_food_on_head(self, mock_pygame_injected):
        self.run_test_food_on_head(AStar, "AStar", mock_pygame_injected)

    def test_bestfs_simple_path(self, mock_pygame_injected):
        self.run_test_simple_path(BestFS, "BestFS", mock_pygame_injected)
    def test_bestfs_no_path_blocked(self, mock_pygame_injected):
        self.run_test_no_path_blocked(BestFS, "BestFS", mock_pygame_injected)
    def test_bestfs_path_with_obstacles(self, mock_pygame_injected):
        self.run_test_path_with_obstacles(BestFS, "BestFS", mock_pygame_injected)
    def test_bestfs_food_adjacent(self, mock_pygame_injected):
        self.run_test_food_adjacent(BestFS, "BestFS", mock_pygame_injected)
    def test_bestfs_food_on_head(self, mock_pygame_injected):
        self.run_test_food_on_head(BestFS, "BestFS", mock_pygame_injected)

if __name__ == '__main__':
    unittest.main()
