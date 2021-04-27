import random
import pygame
from constants import Direction, BLOCK_SIZE, INITIAL_SPEED, BLACK, BLUE, GREEN, RED, WHITE, SPEEDUP, OBSTACLE_THRESHOLD, SPEED_THRESHOLD, WIDTH, HEIGHT

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __eq__(self, point) : 
        if self.__class__ != point.__class__:
            return False
        return self.__dict__ == point.__dict__
    
    # Function to plot draw point
    def plot(self, display, color):
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()
        self.direction = Direction.UP
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.generate_obstacles()
        self.place_food()
        
    # Function to randomly place food in the game
    def place_food(self):
        x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
        y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
        self.food = Point(x, y)
        if self.food in self.snake or self.food in self.obstacles:
            self.place_food()

    # Function to randomly generate obstacles in the game
    def generate_obstacles(self):
        for i in range(0, OBSTACLE_THRESHOLD):
            x = random.randint(0, (self.width-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE 
            y = random.randint(0, (self.height-BLOCK_SIZE )//BLOCK_SIZE )*BLOCK_SIZE
            obstacle = Point(x, y)
            if obstacle not in self.snake:
                self.obstacles.append(obstacle)
            
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
        return Point(x, y)

    def is_collision(self, point, start=1):
        # Checking boundary condition
        if point.x > self.width - BLOCK_SIZE or point.x < 0 or point.y > self.height - BLOCK_SIZE or point.y < 0:
            return True
        # Checking if the snake hit itself
        if point in self.snake[start:]:
            return True
        # Checking if the snake hit an obstacle
        if point in self.obstacles:
            return True

    # Function to update game ui
    def update_ui(self):
        self.display.fill(BLACK)
        # Drawing snake's body
        for point in self.snake:
            point.plot(self.display, GREEN)
        # Drawing snake's head
        self.head.plot(self.display, WHITE)
        # Drawing obstacles
        for point in self.obstacles:
            point.plot(self.display, RED)
        # Drawing food
        self.food.plot(self.display, BLUE)
        # Display score
        text = font.render("Score: " + str(self.score), True, WHITE)
        self.display.blit(text, [0, 0])
        pygame.display.flip()

    def calculate_h(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    # Function to select random direction for the snake to move
    def hill_climbing(self, directions):
        while True:
            if len(directions) == 0:
                return False
            # Generating valid neighbor
            index = random.randint(0, len(directions)-1)
            neighbor = self.move_snake(directions[index])
            if self.is_collision(neighbor, 0):
                _ = directions.pop(index)
            else:
                # Checking if the generated neighbor is better than current state
                current_h = self.calculate_h(self.head)
                neighbor_h = self.calculate_h(neighbor)
                # Climbing the hill if generated neighbor is better
                if neighbor_h <= current_h:
                    self.direction = directions[index]
                    return True
                else:
                    _ = directions.pop(index)
        
    def process(self):
        directions = [Direction.LEFT, Direction.RIGHT, Direction.UP, Direction.DOWN]
        # Checking user input
        for event in pygame.event.get():
            # Quit event
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        path_found = self.hill_climbing(directions)
        if not path_found:
            return True, self.score
        # Moving snake
        self.head = self.move_snake(self.direction)
        self.snake.insert(0, self.head)

        # Check if snake has reached the food
        # if self.head.position_check(self.food):
        if self.head == self.food:
            self.score += 1
            self.place_food()
        else:
            #Remove the last element from the snake's body as we have added a new head
            self.snake.pop()

        # Updating UI and Clock
        speed = INITIAL_SPEED + (self.score//SPEED_THRESHOLD)*SPEEDUP
        self.update_ui()
        self.clock.tick(speed)

        return False, self.score

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
