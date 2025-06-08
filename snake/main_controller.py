import pygame
import sys # For sys.exit()

from snake.configs.game import WIDTH, HEIGHT, FPS
from snake.configs import colors # Assuming colors.py exists with BLACK etc.
from snake.configs.game import WIDTH, HEIGHT, FPS # Ensure FPS is imported
from snake.game_state import GameState
from snake.ui.menu import MainMenu, ACTION_SELECT_MODE, ACTION_QUIT_GAME
from snake.ui.mode_selection import (
    ModeSelectionScreen, ACTION_BACK_TO_MENU,
    MODE_MANUAL, MODE_ASTAR, MODE_BEST_FS, MODE_BFS, MODE_DFS,
    MODE_SIMPLE_HILL_CLIMBING, MODE_STEEPEST_ASCENT_HILL_CLIMBING,
    MODE_STOCHASTIC_HILL_CLIMBING, MODE_RANDOM_SEARCH
)
from snake.ui.game_over import GameOverScreen, ACTION_PLAY_AGAIN, ACTION_MAIN_MENU as GAMEOVER_ACTION_MAIN_MENU

# Import all game mode classes
from snake.main.manual import Manual
from snake.informed_search_models.a_star_search import AStar
from snake.informed_search_models.best_first_search import BestFS
from snake.uninformed_search_models.breadth_first_search import BFS
from snake.uninformed_search_models.depth_first_search import DFS
from snake.informed_search_models.simple_hill_climbing import HillClimbing
from snake.informed_search_models.steepest_ascent_hill_climbing import SteepestAscentHillClimbing
from snake.informed_search_models.stochastic_hill_climbing import StochasticHillClimbing
from snake.uninformed_search_models.random_search import Random

class AppController:
    def __init__(self):
        pygame.init()
        pygame.font.init() # Explicitly initialize font module

        self.display = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Snake AI Game")

        # Attempt to load a common system font; fall back if not found.
        try:
            self.font = pygame.font.SysFont("arial", 25)
        except pygame.error:
            print("Arial font not found, using default pygame font.")
            self.font = pygame.font.Font(None, 30) # Default font, size 30

        self.current_state = GameState.MAIN_MENU
        self.main_menu = MainMenu(self.display, self.font)
        self.mode_selection_screen = ModeSelectionScreen(self.display, self.font)

        self.game_instance = None # Will hold the current game model instance
        self.game_over_screen = None # Will be instantiated when game ends

        self.selected_game_mode = None # Stores string like "MODE_ASTAR"
        self.last_score = 0
        self.game_obstacles_enabled = True # Default, can be made configurable

        self.clock = pygame.time.Clock()

    def get_game_class(self, mode_string):
        game_mode_map = {
            MODE_MANUAL: Manual,
            MODE_ASTAR: AStar,
            MODE_BEST_FS: BestFS,
            MODE_BFS: BFS,
            MODE_DFS: DFS,
            MODE_SIMPLE_HILL_CLIMBING: HillClimbing,
            MODE_STEEPEST_ASCENT_HILL_CLIMBING: SteepestAscentHillClimbing,
            MODE_STOCHASTIC_HILL_CLIMBING: StochasticHillClimbing,
            MODE_RANDOM_SEARCH: Random,
        }
        return game_mode_map.get(mode_string)

    def run(self):
        running = True
        while running:
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    self.current_state = GameState.QUIT

            if self.current_state == GameState.MAIN_MENU:
                self.main_menu.draw() # UI screen handles its own display.flip()
                for event in events:
                    action = self.main_menu.handle_event(event)
                    if action == ACTION_SELECT_MODE:
                        self.current_state = GameState.MODE_SELECTION
                    elif action == ACTION_QUIT_GAME:
                        self.current_state = GameState.QUIT

            elif self.current_state == GameState.MODE_SELECTION:
                self.mode_selection_screen.draw() # UI screen handles its own display.flip()
                for event in events:
                    action = self.mode_selection_screen.handle_event(event)
                    if action == ACTION_BACK_TO_MENU:
                        self.current_state = GameState.MAIN_MENU
                    elif action and action.startswith("MODE_"):
                        self.selected_game_mode = action
                        self.current_state = GameState.GAME_PLAYING
                        # Reset game_over_screen instance so it's fresh for next game over
                        self.game_over_screen = None

            elif self.current_state == GameState.GAME_PLAYING:
                if self.selected_game_mode:
                    GameAlgorithmClass = self.get_game_class(self.selected_game_mode)
                    if GameAlgorithmClass:
                        # TODO: Consider making game_has_obstacles configurable via UI
                        print(f"Starting game mode: {self.selected_game_mode} with obstacles: {self.game_obstacles_enabled}")
                        self.game_instance = GameAlgorithmClass(game_has_obstacles=self.game_obstacles_enabled)

                        # This assumes game_instance.main() is blocking and will return score
                        # This part will be refactored in the next subtask.
                        # For now, if game_instance.main() calls sys.exit(), app will close.
                        self.last_score = self.game_instance.main()
                        print(f"Game ended. Score: {self.last_score}")

                        self.current_state = GameState.GAME_OVER
                        self.selected_game_mode = None # Clear selection for next round
                    else:
                        print(f"Error: Unknown game mode {self.selected_game_mode}")
                        self.current_state = GameState.MAIN_MENU
                else:
                    # This case should ideally not be reached if state transitions are correct
                    print("Error: GAME_PLAYING state reached without a selected game mode.")
                    self.current_state = GameState.MAIN_MENU

            elif self.current_state == GameState.GAME_OVER:
                # Ensure game_over_screen is instantiated only once or if score changes
                if not self.game_over_screen or self.game_over_screen.final_score != self.last_score:
                    self.game_over_screen = GameOverScreen(self.display, self.font, self.last_score)

                self.game_over_screen.draw() # UI screen handles its own display.flip()
                for event in events:
                    action = self.game_over_screen.handle_event(event)
                    if action == ACTION_PLAY_AGAIN:
                        self.current_state = GameState.MODE_SELECTION
                    elif action == GAMEOVER_ACTION_MAIN_MENU: # Use aliased import if names clash
                        self.current_state = GameState.MAIN_MENU

            elif self.current_state == GameState.QUIT:
                running = False

            # pygame.display.flip() # Not needed here if UI screens call it in their draw methods
            self.clock.tick(FPS) # Use FPS from game_configs

        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    # This allows direct execution of the controller for testing UI flow
    controller = AppController()
    controller.run()
