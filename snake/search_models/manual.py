import pygame

from snake.configs.directions import Direction
from snake.configs.game import FIXED_AUTO_SPEED, INITIAL_SPEED, SPEED_THRESHOLD, SPEEDUP
from snake.main.game import Game


class Manual(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)

    def generate_path(self):
        """Handles user input to change the direction of the snake"""
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                return "USER_REQUESTED_QUIT"  # Signal to main loop
            # Keyboard event
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and self.direction != Direction.RIGHT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT and self.direction != Direction.LEFT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP and self.direction != Direction.DOWN:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN and self.direction != Direction.UP:
                    self.direction = Direction.DOWN

    def main(self):
        while True:
            user_action = self.generate_path()  # Update direction based on user input
            if user_action == "USER_REQUESTED_QUIT":
                return self.score  # Exit game loop, return score

            temp_head = self.get_next_head(self.direction)

            # Disallow movement of snake in the direction opposite to its current direction
            if len(self.snake) > 1 and temp_head == self.snake[1]:
                self.head = self.get_next_head(self.direction)
            else:
                self.head = temp_head

            # Move snake
            self.snake.insert(0, self.head)
            # Check if snake has hit something
            if self.detect_collision():
                return self.score

            # Check if snake has reached the food
            if self.head == self.food:
                self.score += 1
                self.generate_food()
            else:
                # Remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # Update UI and Clock
            speed = INITIAL_SPEED + (self.score // SPEED_THRESHOLD) * SPEEDUP
            speed = min(speed, FIXED_AUTO_SPEED)
            self.update_ui()
            self.clock.tick(speed)
