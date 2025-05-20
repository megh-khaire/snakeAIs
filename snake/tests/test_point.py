import unittest
from snake.main.point import Point
from snake.configs.game import BLOCK_SIZE, WIDTH, HEIGHT
from snake.configs.directions import Direction

class TestPoint(unittest.TestCase):

    def test_initialization(self):
        point = Point(10, 20)
        self.assertEqual(point.x, 10)
        self.assertEqual(point.y, 20)
        self.assertIsNone(point.f)
        self.assertIsNone(point.g)
        self.assertIsNone(point.h)
        self.assertEqual(point.neighbors, [])
        self.assertIsNone(point.origin)

    def test_equality_and_hashability(self):
        point1 = Point(10, 20)
        point2 = Point(10, 20)
        point3 = Point(30, 40)
        
        self.assertEqual(point1, point2)
        self.assertNotEqual(point1, point3)
        
        # Test hashability by adding to a set
        point_set = {point1, point2, point3}
        self.assertEqual(len(point_set), 2) # point1 and point2 are considered the same
        self.assertIn(point1, point_set)
        self.assertIn(point3, point_set)

    def test_generate_neighbors(self):
        # Using default WIDTH, HEIGHT, BLOCK_SIZE for this test.
        # Adjust if these constants are too large for practical neighbor generation testing.
        # For this test, assume point is not near border to get all 4 neighbors.
        point = Point(WIDTH // 2, HEIGHT // 2) 
        point.generate_neighbors()
        
        self.assertEqual(len(point.neighbors), 4)
        for neighbor in point.neighbors:
            self.assertIsInstance(neighbor, Point)
        
        expected_neighbors = [
            Point(point.x - BLOCK_SIZE, point.y), # Left
            Point(point.x + BLOCK_SIZE, point.y), # Right
            Point(point.x, point.y - BLOCK_SIZE), # Up
            Point(point.x, point.y + BLOCK_SIZE)  # Down
        ]
        
        # Check if all expected neighbors are generated, order doesn't matter for this check
        self.assertCountEqual(point.neighbors, expected_neighbors)

    def test_generate_neighbors_at_boundary(self):
        # Top-left corner
        point_tl = Point(0, 0)
        point_tl.generate_neighbors()
        # Expected: Right and Down neighbors
        expected_tl_neighbors = [
            Point(BLOCK_SIZE, 0),
            Point(0, BLOCK_SIZE)
        ]
        self.assertEqual(len(point_tl.neighbors), 2)
        self.assertCountEqual(point_tl.neighbors, expected_tl_neighbors)

        # Bottom-right corner
        # Requires careful calculation of max valid x, y based on WIDTH, HEIGHT, BLOCK_SIZE
        # Assuming WIDTH and HEIGHT are multiples of BLOCK_SIZE
        max_x = WIDTH - BLOCK_SIZE
        max_y = HEIGHT - BLOCK_SIZE
        point_br = Point(max_x, max_y)
        point_br.generate_neighbors()
        # Expected: Left and Up neighbors
        expected_br_neighbors = [
            Point(max_x - BLOCK_SIZE, max_y),
            Point(max_x, max_y - BLOCK_SIZE)
        ]
        self.assertEqual(len(point_br.neighbors), 2)
        self.assertCountEqual(point_br.neighbors, expected_br_neighbors)


    def test_get_direction(self):
        point = Point(50, 50)
        
        # No origin
        self.assertIsNone(point.get_direction())
        
        # Origin below (moves UP)
        point.origin = Point(50, 50 + BLOCK_SIZE)
        self.assertEqual(point.get_direction(), Direction.UP)
        
        # Origin above (moves DOWN)
        point.origin = Point(50, 50 - BLOCK_SIZE)
        self.assertEqual(point.get_direction(), Direction.DOWN)
        
        # Origin to the right (moves LEFT)
        point.origin = Point(50 + BLOCK_SIZE, 50)
        self.assertEqual(point.get_direction(), Direction.LEFT)
        
        # Origin to the left (moves RIGHT)
        point.origin = Point(50 - BLOCK_SIZE, 50)
        self.assertEqual(point.get_direction(), Direction.RIGHT)

        # Origin is the same (should ideally not happen or return None)
        point.origin = Point(50, 50)
        self.assertIsNone(point.get_direction()) # No change in x or y

if __name__ == '__main__':
    unittest.main()
