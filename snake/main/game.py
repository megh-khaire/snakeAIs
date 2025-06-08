import random
import sys
from abc import ABC, abstractmethod

import pygame

from snake.configs.colors import BLACK, BLUE, GREEN, RED, WHITE
from snake.configs.directions import Direction
from snake.configs import game as game_configs # Import game_configs
from snake.configs.game import (
    BLOCK_SIZE,
    FIXED_AUTO_SPEED,
    # HEIGHT and WIDTH will be used from game_configs for game_area
    OBSTACLE_THRESHOLD,
)
from snake.main.point import Point


class Game(ABC):
    def __init__(self, game_has_obstacles=False): # width and height params removed
        self.game_area_width = game_configs.WIDTH
        self.game_area_height = game_configs.HEIGHT

        self.direction = Direction.UP
        # Head initialized relative to game_area
        self.head = Point(self.game_area_width // 2, self.game_area_height // 2)
        self.snake = [self.head]
        self.score = 0
        self.game_has_obstacles = game_has_obstacles
        self.obstacles = []
        self.food = None
        self.path = []

        self.display = None # Will be set by AppController via on_resize
        self.font = pygame.font.SysFont("arial", 25) # For score
        self.clock = pygame.time.Clock() # Game instance manages its own clock/speed

        # Initialize obstacles and food (uses game_area_width/height now)
        self.generate_obstacles()
        self.generate_food()

    def on_resize(self, new_display_surface):
        """Called by AppController when the window is resized."""
        self.display = new_display_surface

    def reset(self):
        """Completely resets the game back to the initial starting point."""
        self.direction = Direction.UP
        self.head = Point(self.game_area_width // 2, self.game_area_height // 2) # Use game_area
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
            # Generate within game_area
            x = random.randint(0, (self.game_area_width - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
            y = random.randint(0, (self.game_area_height - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
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
                    # Generate within game_area
                    x = (
                        random.randint(0, (self.game_area_width - BLOCK_SIZE) // BLOCK_SIZE)
                        * BLOCK_SIZE
                    )
                    y = (
                        random.randint(0, (self.game_area_height - BLOCK_SIZE) // BLOCK_SIZE)
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
        - Boundary of the game (based on game_area)
        - The snake itself
        - Any obstacles in the game
        """
        if (
            self.head.x >= self.game_area_width
            or self.head.x < 0
            or self.head.y >= self.game_area_height
            or self.head.y < 0
        ):
            return True
        if self.head in self.snake[1:] or self.head in self.obstacles:
            return True
        return False

    def detect_random_point_collision(self, next_head):
        """
        Checks if the given point collides with any of the following entities:
        - Boundary of the game (based on game_area)
        - The snake itself
        - Any obstacles in the game

        Note: Here we assume that the random point is the next head.
        """
        if (
            next_head.x >= self.game_area_width
            or next_head.x < 0
            or next_head.y >= self.game_area_height
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
        if self.display is None:
            return # Cannot draw if display surface isn't set

        window_width = self.display.get_width()
        window_height = self.display.get_height()

        offset_x = (window_width - self.game_area_width) // 2
        offset_y = (window_height - self.game_area_height) // 2

        self.display.fill(BLACK) # Fill entire window

        # Optional: Draw a border for the game area
        game_area_rect = pygame.Rect(offset_x, offset_y, self.game_area_width, self.game_area_height)
        pygame.draw.rect(self.display, WHITE, game_area_rect, 1) # Thin white border

        for point in self.snake:
            point.plot(self.display, GREEN, offset_x, offset_y)
        self.head.plot(self.display, WHITE, offset_x, offset_y)
        for point in self.obstacles:
            point.plot(self.display, RED, offset_x, offset_y)
        self.food.plot(self.display, BLUE, offset_x, offset_y)

        text = self.font.render(f"Score: {self.score}", True, WHITE)
        # Position score text relative to game area or window corner
        # For now, relative to game area corner + offset
        self.display.blit(text, [offset_x, offset_y])
        # pygame.display.flip() # Removed, AppController will handle flipping

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
        # Defensive return, should be unreachable if loop logic is complete
        return self.score

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
