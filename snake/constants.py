from enum import Enum

BLOCK_SIZE = 20
INITIAL_SPEED = 15
SPEEDUP = 20
OBSTACLE_THRESHOLD = 1000000

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
