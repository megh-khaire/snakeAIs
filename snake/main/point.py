import pygame
from snake.resources.constants import BLOCK_SIZE, WIDTH, HEIGHT
from snake.resources.directions import Direction


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.origin = None

    def __eq__(self, point):
        return self.__class__ == point.__class__ and self.x == point.x and self.y == point.y

    def plot(self, display, color):
        '''Plots the point with given color and fixed size'''
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    def get_direction(self):
        '''Determine direction in which the snake moves based on initial position'''
        if self.x == self.origin.x and self.y < self.origin.y:
            return Direction.UP
        elif self.x == self.origin.x and self.y > self.origin.y:
            return Direction.DOWN
        elif self.x < self.origin.x and self.y == self.origin.y:
            return Direction.LEFT
        elif self.x > self.origin.x and self.y == self.origin.y:
            return Direction.RIGHT

    def generate_neighbors(self):
        '''Generates neighbors for point object'''
        if self.x > 0:
            self.neighbors.append(Point(self.x - BLOCK_SIZE, self.y))
        if self.y > 0:
            self.neighbors.append(Point(self.x, self.y - BLOCK_SIZE))
        if self.x < WIDTH - BLOCK_SIZE:
            self.neighbors.append(Point(self.x + BLOCK_SIZE, self.y))
        if self.y < HEIGHT - BLOCK_SIZE:
            self.neighbors.append(Point(self.x, self.y + BLOCK_SIZE))
