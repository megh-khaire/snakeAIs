from enum import Enum


class Direction(Enum):
    RIGHT = 1
    LEFT = 2
    UP = 3
    DOWN = 4


STRAIGHT = [1, 0, 0]
TURN_LEFT = [0, 0, 1]
TURN_RIGHT = [0, 1, 0]
