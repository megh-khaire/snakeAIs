import heapq
from collections import deque
from snake.main.game import Game


class AStar(Game):
    def __init__(self, game_has_obstacles):
        super().__init__(game_has_obstacles)
        self.open = []  # Will be a min-priority queue (heap)
        self.closed = set()

        # Calculate initial path
        self.generate_path()

    def calculate_h(self, point):
        """Calculates heuristic i.e. the Manhattan distance between selected node and goal state"""
        return abs(self.food.x - point.x) + abs(self.food.y - point.y)

    def generate_path(self):
        """Implements A* Search algorithm for snake traversal"""
        self.path = []
        self.closed = set()
        self.open = []

        # Initialize the start node
        self.head.g = 0
        self.head.h = self.calculate_h(self.head)
        self.head.f = self.head.g + self.head.h
        self.head.origin = None # Ensure origin is None for the head
        heapq.heappush(self.open, (self.head.f, self.head))

        temp_snake = self.snake.copy()
        # food_eaten flag is not strictly needed here as we return upon finding food.
        # It was used to control temp_snake.pop(), which should happen if food not yet reached by current.

        while self.open:
            # Select node with the lowest f value
            _, current = heapq.heappop(self.open)

            if current in self.closed: # Already processed this node via a shorter or equal path
                continue
            self.closed.add(current)

            is_current_node_food = (current == self.food)

            # Simulate moving the snake to current position for collision checks
            current_simulated_snake = deque(self.snake) # Start with actual game snake state
            current_simulated_snake.appendleft(current) # Assume head moves to current
            if not is_current_node_food:
                if len(current_simulated_snake) > 1: # Snake grows if food is eaten
                    current_simulated_snake.pop() # Tail moves forward only if not eating

            # Check if snake has reached the goal state (food)
            if is_current_node_food:
                # Reconstruct path
                while current.origin: # Backtrack from food to head
                    self.path.append(current)
                    current = current.origin
                # self.path.append(self.head) # if head is not part of loop
                self.path.reverse()
                return

            # Explore neighbors of the selected node
            current.generate_neighbors()
            for neighbor in current.neighbors:
                # Basic collision checks
                if neighbor in self.obstacles or neighbor in current_simulated_snake:
                    continue

                if neighbor in self.closed: # Already found the optimal path to this neighbor
                    continue

                g_temp = current.g + 1
                h_temp = self.calculate_h(neighbor)
                f_temp = g_temp + h_temp

                # The neighbor Point object from generate_neighbors() is a new instance.
                # We set its g, h, f, and origin for this specific path.
                # If a Point with the same coordinates is already in the open list
                # with a higher f_temp, this new one will be prioritized by the heap.
                # If one with lower f_temp is already there, that one will be explored first.
                # If one with same f_temp but different g_temp is there, heapq behavior might vary
                # based on Point comparison if f_values are equal (not ideal).
                # Point class does not have __lt__ by default for tie-breaking, heapq uses insertion order.
                # This is generally fine. We are pushing (priority, point_object).
                
                # Create a new Point instance or update the existing one?
                # The Point objects from generate_neighbors are temporary.
                # To maintain consistency of g, h, f on the points themselves,
                # it's better to use the point instances that are put on the heap.
                # The 'neighbor' here is a template. Let's make a new point for the heap.
                # No, Point class from generate_neighbors() can be used, as its state (g,h,f,origin)
                # is set here before pushing. Equality (for 'in self.closed') is by x,y.
                
                neighbor.g = g_temp
                neighbor.h = h_temp
                neighbor.f = f_temp
                neighbor.origin = current
                heapq.heappush(self.open, (neighbor.f, neighbor))
                
        # If the loop finishes, no path was found, self.path remains [] as initialized.

    def main(self):
        """Executes multi-step traversal based on the A* generated path."""
        self.multi_step_traversal()
