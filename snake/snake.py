import random
import pygame
from constants import Direction, BLOCK_SIZE, INITIAL_SPEED, BLACK, BLUE, GREEN, RED, WHITE, SPEEDUP

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def position_check(self, point):
        if self.x == point.x and self.y == point.y:
            return True
        else:
            return False

class Game:
    def __init__(self, width=640, height=640):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.direction = Direction.UP
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head]
        self.score = 0
        # self.obstacles = []
        self.food = None
        self.place_food()
        # self.generate_obstacles()

    # Function to randomly place food in the game
    def place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake:
            self.place_food()

    def move_snake(self, direction):
        x = self.head.x
        y = self.head.y
        if direction == Direction.RIGHT:
            x += BLOCK_SIZE
        elif direction == Direction.LEFT:
            x -= BLOCK_SIZE
        elif direction == Direction.DOWN:
            y += BLOCK_SIZE
        elif direction == Direction.UP:
            y -= BLOCK_SIZE
        self.head = Point(x, y)

    def is_collision(self):
        # Checking boundary condition
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        # Checking if the snake hit itself
        if self.head in self.snake[1:]:
            return True

    def update_ui(self):
        self.display.fill(BLACK)
        # Drawing snake's body
        for point in self.snake:
            pygame.draw.rect(self.display, GREEN, pygame.Rect(point.x, point.y, BLOCK_SIZE, BLOCK_SIZE))
        # Drawing snake's head
        pygame.draw.rect(self.display, WHITE, pygame.Rect(self.head.x, self.head.y, BLOCK_SIZE, BLOCK_SIZE))
        # Drawing food
        pygame.draw.rect(self.display, RED, pygame.Rect(self.food.x, self.food.y, BLOCK_SIZE, BLOCK_SIZE))
        # Display score
        text = font.render("Score: " + str(self.score), True, BLUE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def process(self):
        # Checking user input
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    self.direction = Direction.LEFT
                elif event.key == pygame.K_RIGHT:
                    self.direction = Direction.RIGHT
                elif event.key == pygame.K_UP:
                    self.direction = Direction.UP
                elif event.key == pygame.K_DOWN:
                    self.direction = Direction.DOWN

        # Moving snake
        self.move_snake(self.direction)
        self.snake.insert(0, self.head)
        # Check if snake has hit something
        is_over = False
        if self.is_collision():
            is_over = True
            return is_over, self.score

        # Check if snake has reached the food
        if self.head.position_check(self.food):
            self.score += 1
            self.place_food()
        else:
            #Remove the last element from the snake's body as we have added a new head
            self.snake.pop()

        # Updating UI and Clock
        speed = INITIAL_SPEED + (self.score%SPEEDUP)
        self.update_ui()
        self.clock.tick(speed)

        return is_over, self.score

if __name__ == '__main__':
    pygame.init()
    font = pygame.font.SysFont('arial', 25)
    game = Game()
    while True:
        game_over, score = game.process()
        if game_over:
            break
    print('Final Score: ', score)
    pygame.quit()
