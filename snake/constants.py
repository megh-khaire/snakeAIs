from enum import Enum

# Grid values
WIDTH = 640
HEIGHT = 640
BLOCK_SIZE = 20
OBSTACLE_THRESHOLD = 15

# Speedup values
INITIAL_SPEED = 10
SPEED_THRESHOLD = 25
SPEEDUP = 5

# RGB colors
WHITE = (255, 255, 255)
RED = (200,0,0)
BLUE = (0, 0, 200)
GREEN = (0, 200, 0)
BLACK = (0,0,0)

class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4
