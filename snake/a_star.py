import random
import pygame
from constants import Direction, BLOCK_SIZE, INITIAL_SPEED, BLACK, BLUE, GREEN, RED, WHITE, SPEEDUP, OBSTACLE_THRESHOLD, SPEED_THRESHOLD, WIDTH, HEIGHT

class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.origin = None

    def __eq__(self, point) : 
        if self.__class__ != point.__class__: 
            return False
        return self.x == point.x and self.y == point.y

    # Function to plot draw point
    def plot(self, display, color):
        pygame.draw.rect(display, color, pygame.Rect(self.x, self.y, BLOCK_SIZE, BLOCK_SIZE))

    # Function to  generate neighbor for point object
    def generate_neighbors(self):
        if self.x > 0:
            self.neighbors.append(Point(self.x - BLOCK_SIZE,self.y))
        if self.y > 0:
            self.neighbors.append(Point(self.x, self.y - BLOCK_SIZE))
        if self.x < WIDTH - BLOCK_SIZE:
            self.neighbors.append(Point(self.x + BLOCK_SIZE, self.y))
        if self.y < HEIGHT - BLOCK_SIZE:
            self.neighbors.append(Point(self.x, self.y + BLOCK_SIZE))

class Game:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = width
        self.height = height
        self.direction = Direction.UP
        self.head = Point(self.width/2, self.height/2)
        self.snake = [self.head]
        self.score = 0
        self.obstacles = []
        self.food = None
        self.open = [self.head]
        self.closed = []
        self.path = []

        # Pygame initializations
        self.display = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption('Snake Game')
        self.clock = pygame.time.Clock()

        # Initializing obstacles
        self.generate_obstacles()
        # Initializing food point
        self.place_food()
        # Calculating initial path
        self.a_star()
        
    # Function to determine direction in which the snake moves
    def set_direction(self, point):
        if point.x == point.origin.x and point.y < point.origin.y:
            self.direction = Direction.UP
        elif point.x == point.origin.x and point.y > point.origin.y:
            self.direction = Direction.DOWN
        elif point.x < point.origin.x and point.y == point.origin.y:
            self.direction = Direction.LEFT
        elif point.x > point.origin.x and point.y == point.origin.y:
            self.direction = Direction.RIGHT

    # Function to calculate heuristic - Manhatten distance between selected node and goal state
    def calculate_h(self, point):
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    # Function to implement A* algorithm
    def a_star(self):
        self.path = [self.head]
        self.closed = []
        self.open = [self.head]
        while self.open:
            # Select start node as the node with lowest f value
            current = min(self.open, key=lambda x: x.f)
            # Remove selected node from self.open
            self.open = [self.open[i] for i in range(len(self.open)) if not self.open[i] == current]
            # Append selected node to closed_points
            self.closed.append(current)
            
            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                if neighbor not in self.closed and neighbor not in self.obstacles and neighbor not in self.snake:
                    # If neighbor is not in self.open increase the cost of path and append neighbor to self.open
                    if neighbor not in self.open:
                        neighbor.g = current.g+1
                        self.open.append(neighbor)
                    neighbor.h = self.calculate_h(neighbor)
                    neighbor.f = neighbor.g + neighbor.h
                    neighbor.origin = current

            if current == self.food:
                # Based on its origin determine the direction in which the snake will move
                while current.origin:
                    self.path.append(current)
                    current = current.origin
                return
        self.path = []

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
        
    # Function to move the snake in given direction
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

    # Function to check if the game is over
    def is_collision(self):
        # Checking boundary condition
        if self.head.x > self.width - BLOCK_SIZE or self.head.x < 0 or self.head.y > self.height - BLOCK_SIZE or self.head.y < 0:
            return True
        # Checking if the snake hit itself
        if self.head in self.snake[1:]:
            return True
        # Checking if the snake hit an obstacle
        if self.head in self.obstacles:
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

    def process(self):
        while self.path:
            # Checking user input
            for event in pygame.event.get():
                # Quit event
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            self.set_direction(self.path.pop(-1))
            # Moving snake
            self.move_snake(self.direction)
            self.snake.insert(0, self.head)

            # Check if snake has hit something
            if self.is_collision():
                return self.score

            # Check if snake has reached the food
            if self.head == self.food:
                self.score += 1
                self.place_food()
                self.a_star()
            else:
                #Remove the last element from the snake's body as we have added a new head
                self.snake.pop()

            # Updating UI and Clock
            speed = INITIAL_SPEED + (self.score//SPEED_THRESHOLD)*SPEEDUP
            self.update_ui()
            self.clock.tick(speed)

        return self.score

if __name__ == '__main__':
    pygame.init()
    font = pygame.font.SysFont('arial', 25)
    game = Game()
    score = game.process()
    print('Final Score: ', score)
    pygame.quit()
    