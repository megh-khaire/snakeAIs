import random
from abc import ABC, abstractmethod

import pygame

from snake.configs.colors import BLACK, BLUE, GREEN, RED, WHITE
from snake.configs.directions import Direction
from snake.configs.game import (
    BLOCK_SIZE,
    FIXED_AUTO_SPEED,
    HEIGHT,
    OBSTACLE_THRESHOLD,
    WIDTH,
)
from snake.main.point import Point


class Game(ABC):
    def __init__(self, game_has_obstacles=False, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.direction = Direction.UP
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head]
        self.score = 0
        self.game_has_obstacles = game_has_obstacles
        self.obstacles = []
        self.food = None
        self.path = []

        # Pygame initializations
        self.display = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.SysFont("arial", 25)
        self.clock = pygame.time.Clock()
        pygame.display.set_caption("Snake Game")

        # Initialize obstacles and food
        self.generate_obstacles()
        self.generate_food()

    def reset(self):
        """Completely resets the game back to the initial starting point."""
        self.direction = Direction.UP
        self.head = Point(self.width // 2, self.height // 2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles.clear()
        self.food = None
        self.generate_obstacles()
        self.generate_food()

    def generate_food(self):
        """
        Randomly generates a food Point in the game.
        Ensures that obstacles and the snake are avoided in the process.
        """
        while True:
            x = random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            self.food = Point(x, y)
            if self.food not in self.snake and self.food not in self.obstacles:
                break

    def generate_obstacles(self):
        """
        Randomly generates obstacles in the game.
        Ensures that the snake is avoided in the process.
        """
        if self.game_has_obstacles:
            for _ in range(OBSTACLE_THRESHOLD):
                while True:
                    x = (
                        random.randint(0, (self.width - BLOCK_SIZE) // BLOCK_SIZE)
                        * BLOCK_SIZE
                    )
                    y = (
                        random.randint(0, (self.height - BLOCK_SIZE) // BLOCK_SIZE)
                        * BLOCK_SIZE
                    )
                    obstacle = Point(x, y)
                    if obstacle not in self.snake and obstacle not in self.obstacles:
                        self.obstacles.append(obstacle)
                        break

    def get_next_head(self, direction):
        """Returns a point at which the snake's head should move next based on the given direction."""
        direction_offsets = {
            Direction.RIGHT: (BLOCK_SIZE, 0),
            Direction.LEFT: (-BLOCK_SIZE, 0),
            Direction.DOWN: (0, BLOCK_SIZE),
            Direction.UP: (0, -BLOCK_SIZE),
        }
        offset = direction_offsets.get(direction, (0, 0))
        return Point(self.head.x + offset[0], self.head.y + offset[1])

    def detect_collision(self):
        """
        Checks if the snake has collided with any of the following entities:
        - Boundary of the game
        - The snake itself
        - Any obstacles in the game
        """
        if (
            self.head.x >= self.width
            or self.head.x < 0
            or self.head.y >= self.height
            or self.head.y < 0
        ):
            return True
        if self.head in self.snake[1:] or self.head in self.obstacles:
            return True
        return False

    def detect_random_point_collision(self, next_head):
        """
        Checks if the given point collides with any of the following entities:
        - Boundary of the game
        - The snake itself
        - Any obstacles in the game

        Note: Here we assume that the random point is the next head.
        """
        if (
            next_head.x >= self.width
            or next_head.x < 0
            or next_head.y >= self.height
            or next_head.y < 0
        ):
            return True
        if next_head in self.snake[:-1] or next_head in self.obstacles:
            return True
        return False

    def update_ui(self):
        """
        Updates the game's UI by plotting the following entities on the display window:
        - The snake's body
        - The snake's head
        - Obstacles
        - Food source
        - Current score
        """
        self.display.fill(BLACK)
        for point in self.snake:
            point.plot(self.display, GREEN)
        self.head.plot(self.display, WHITE)
        for point in self.obstacles:
            point.plot(self.display, RED)
        self.food.plot(self.display, BLUE)
        text = self.font.render(f"Score: {self.score}", True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    @abstractmethod
    def generate_path(self):
        """
        Core function that is redefined for each algorithm to generate
        the path on which the snake will traverse.
        """
        pass

    def single_step_traversal(self):
        """
        Executes traversal of the snake for algorithms where the snake's
        moves are evaluated step by step, one at a time.
        """
        while True:
            # Check user input
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    # Signal AppController to handle quit by returning current score
                    return self.score

            # Set movement of snake
            self.direction = self.generate_path()
            if not self.direction:
                return self.score

            # Move snake
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            # Check if the snake has collided with something
            if self.detect_collision():
                return self.score
            # Check if snake has reached the food point
            elif self.head == self.food:
                self.score += 1
                self.generate_food()
            else:
                # Remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # Update UI and Clock
            self.update_ui()
            self.clock.tick(FIXED_AUTO_SPEED)

    def multi_step_traversal(self):
        """
        Executes traversal of the snake for algorithms where the complete path
        of the snake's movement is evaluated all at once.
        """
        while self.path:
            # Check user input
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    # Signal AppController to handle quit by returning current score
                    return self.score

            # Move snake
            self.direction = self.path.pop(0).get_direction()
            self.head = self.get_next_head(self.direction)
            self.snake.insert(0, self.head)

            # Check if the snake has collided with something
            if self.detect_collision():
                return self.score
            # Check if snake has reached the food point and generate path to this new point
            elif self.head == self.food:
                self.score += 1
                self.generate_food()
                self.generate_path()
            else:
                # Remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # Update UI and Clock
            self.update_ui()
            self.clock.tick(FIXED_AUTO_SPEED)
        return self.score

    @abstractmethod
    def main(self):
        """
        Wrapper function that is redefined for each algorithm to execute - single or
        multi-step traversal based on the type of path generated by the algorithm.
        """
        pass
