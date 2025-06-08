import pygame # Pygame might be initialized in AppController, but good practice if used directly here too
from snake.main_controller import AppController

def main():
    """Initializes and runs the main application controller."""
    controller = AppController()
    controller.run()

if __name__ == "__main__":
    main()
