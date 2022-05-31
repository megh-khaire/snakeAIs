import pygame
from snake.main.game import Game
from snake.resources.constants import INITIAL_SPEED, SPEED_THRESHOLD, SPEEDUP, FIXED_AUTO_SPEED
from snake.resources.directions import Direction


class Manual(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)

    def main(self):
        input_direction = self.direction
        while True:
            # Check user input
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()
                # Keyboard event
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_LEFT:
                        input_direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        input_direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        input_direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        input_direction = Direction.DOWN

            temp_head = self.get_next_head(input_direction)

            # Disallow movement of snake in the direction opposite to its current direction
            if len(self.snake) > 1 and temp_head == self.snake[1]:
                self.head = self.get_next_head(self.direction)
            else:
                self.direction = input_direction
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
            speed = FIXED_AUTO_SPEED if speed > FIXED_AUTO_SPEED else speed
            self.update_ui()
            self.clock.tick(speed)
