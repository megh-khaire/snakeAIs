import pygame

from snake.configs.directions import Direction
from snake.configs.game import BLOCK_SIZE, HEIGHT, WIDTH


class Point:
    # Class-level constants for neighbor offsets
    NEIGHBOR_OFFSETS = [
        (-BLOCK_SIZE, 0),
        (BLOCK_SIZE, 0),
        (0, -BLOCK_SIZE),
        (0, BLOCK_SIZE),
    ]

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = None
        self.g = None
        self.h = None
        self.neighbors = []
        self.origin = None

    def __eq__(self, other):
        return isinstance(other, Point) and self.x == other.x and self.y == other.y

    def __hash__(self):
        return hash((self.x, self.y))

    def __repr__(self):
        return f"Point(x={self.x}, y={self.y})"

    def plot(self, display, color):
        """Plots the point with given color and fixed size."""
        pygame.draw.rect(
            display, color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE)
        )

    def get_direction(self):
        """Determine direction in which the snake moves based on initial position."""
        if self.origin is None:
            return None
        if self.x == self.origin.x:
            if self.y < self.origin.y:
                return Direction.UP
            elif self.y > self.origin.y:
                return Direction.DOWN
        elif self.y == self.origin.y:
            if self.x < self.origin.x:
                return Direction.LEFT
            elif self.x > self.origin.x:
                return Direction.RIGHT
        return None

    def generate_neighbors(self):
        """Generates neighbors for the point object."""
        self.neighbors.clear()
        for dx, dy in Point.NEIGHBOR_OFFSETS:
            new_x, new_y = self.x + dx, self.y + dy
            if 0 <= new_x < WIDTH and 0 <= new_y < HEIGHT:
                self.neighbors.append(Point(new_x, new_y))
