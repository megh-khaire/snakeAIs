import pygame
from snake.main.game import Game
from snake.resources.constants import INITIAL_SPEED, SPEED_THRESHOLD, SPEEDUP, FIXED_AUTO_SPEED
from snake.resources.directions import Direction


class Manual(Game):
    def __init__(self, game_type):
        Game.__init__(self, game_type)

    def main(self):
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
                        self.direction = Direction.LEFT
                    elif event.key == pygame.K_RIGHT:
                        self.direction = Direction.RIGHT
                    elif event.key == pygame.K_UP:
                        self.direction = Direction.UP
                    elif event.key == pygame.K_DOWN:
                        self.direction = Direction.DOWN

            # If the user is moving in the
            temp_head = self.get_next_head(self.direction)

            # Move snake
            self.head = temp_head
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
