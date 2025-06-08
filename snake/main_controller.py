import pygame
import sys # For sys.exit()

from snake.configs.game import WIDTH, HEIGHT, FPS
import pygame # Added for K_ESCAPE
import sys # For sys.exit()

from snake.configs import colors
from snake.configs.game import WIDTH, HEIGHT, FPS
from snake.game_state import GameState
from snake.ui.menu import MainMenu, ACTION_PLAY_MANUAL, ACTION_SELECT_ALGORITHM, ACTION_QUIT_GAME
from snake.ui.mode_selection import (
    ModeSelectionScreen, ACTION_BACK_TO_MENU,
    MODE_MANUAL, MODE_ASTAR, MODE_BEST_FS, MODE_BFS, MODE_DFS,
    MODE_SIMPLE_HILL_CLIMBING, MODE_STEEPEST_ASCENT_HILL_CLIMBING,
    MODE_STOCHASTIC_HILL_CLIMBING, MODE_RANDOM_SEARCH
)
from snake.ui.game_over import GameOverScreen, ACTION_PLAY_AGAIN, ACTION_MAIN_MENU as GAMEOVER_ACTION_MAIN_MENU
from snake.ui.pause_menu import PauseMenuScreen # Added
from snake.ui.pause_menu import ACTION_RESUME_GAME, ACTION_RESTART_GAME # Added
# ACTION_MAIN_MENU and ACTION_QUIT_GAME are already imported or will use existing ones

# Import all game mode classes
from snake.main.manual import Manual # Already here
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
        self.pause_menu_screen = PauseMenuScreen(self.display, self.font) # Added

        self.current_game_instance = None # Renamed from game_instance for clarity with pause
        self.game_over_screen = None

        self.selected_game_mode = None
        self.last_score = 0
        self.game_obstacles_enabled = True

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
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        if self.current_state == GameState.GAME_PLAYING:
                            self.current_state = GameState.PAUSE_MENU
                        elif self.current_state == GameState.PAUSE_MENU:
                            # Optional: ESC from pause resumes
                            self.current_state = GameState.GAME_PLAYING

            if self.current_state == GameState.MAIN_MENU:
                self.main_menu.draw()
                for event in events:
                    action = self.main_menu.handle_event(event)
                    if action == ACTION_PLAY_MANUAL:
                        self.selected_game_mode = MODE_MANUAL # Assuming MODE_MANUAL is the string "MODE_MANUAL"
                        self.current_game_instance = None # Ensure fresh game start
                        self.current_state = GameState.GAME_PLAYING
                    elif action == ACTION_SELECT_ALGORITHM:
                        self.current_state = GameState.MODE_SELECTION
                    elif action == ACTION_QUIT_GAME:
                        self.current_state = GameState.QUIT

            elif self.current_state == GameState.MODE_SELECTION:
                self.mode_selection_screen.draw()
                for event in events:
                    action = self.mode_selection_screen.handle_event(event)
                    if action == ACTION_BACK_TO_MENU:
                        self.current_state = GameState.MAIN_MENU
                    elif action and action.startswith("MODE_"):
                        self.selected_game_mode = action
                        self.current_game_instance = None # Ensure fresh game start
                        self.current_state = GameState.GAME_PLAYING
                        self.game_over_screen = None

            elif self.current_state == GameState.GAME_PLAYING:
                if not self.current_game_instance: # If no active game instance (e.g., new game or after restart)
                    GameAlgorithmClass = self.get_game_class(self.selected_game_mode)
                    if GameAlgorithmClass:
                        print(f"Starting/Restarting game mode: {self.selected_game_mode} with obstacles: {self.game_obstacles_enabled}")
                        self.current_game_instance = GameAlgorithmClass(game_has_obstacles=self.game_obstacles_enabled)
                    else:
                        print(f"Error: Unknown game mode {self.selected_game_mode} or no mode selected.")
                        self.current_state = GameState.MAIN_MENU
                        continue # Skip to next iteration of main loop

                if self.current_game_instance:
                    # This call will block until that game's loop ends (due to game over or quit event)
                    self.last_score = self.current_game_instance.main()

                    # If the state changed during game_instance.main() (e.g., due to ESC to PAUSE_MENU),
                    # don't automatically go to GAME_OVER.
                    if self.current_state == GameState.GAME_PLAYING:
                        print(f"Game ended. Score: {self.last_score}")
                        self.current_state = GameState.GAME_OVER
                        # self.current_game_instance = None # Clear instance only when truly over, not paused
                else: # Fallback if instance couldn't be created
                    self.current_state = GameState.MAIN_MENU


            elif self.current_state == GameState.PAUSE_MENU:
                self.pause_menu_screen.draw()
                for event in events:
                    action = self.pause_menu_screen.handle_event(event)
                    if action == ACTION_RESUME_GAME:
                        self.current_state = GameState.GAME_PLAYING
                    elif action == ACTION_RESTART_GAME:
                        self.current_game_instance = None # Force re-creation in GAME_PLAYING
                        self.current_state = GameState.GAME_PLAYING
                    elif action == ACTION_MAIN_MENU: # PauseMenu's "Main Menu" action
                        self.current_game_instance = None # Game is abandoned
                        self.current_state = GameState.MAIN_MENU
                    elif action == ACTION_QUIT_GAME: # PauseMenu's "Quit Game" action
                        self.current_state = GameState.QUIT

            elif self.current_state == GameState.GAME_OVER:
                if not self.game_over_screen or self.game_over_screen.final_score != self.last_score:
                    self.game_over_screen = GameOverScreen(self.display, self.font, self.last_score)

                self.current_game_instance = None # Game is over, clear instance

                self.game_over_screen.draw()
                for event in events:
                    action = self.game_over_screen.handle_event(event)
                    if action == ACTION_PLAY_AGAIN:
                        self.current_state = GameState.MODE_SELECTION
                    elif action == GAMEOVER_ACTION_MAIN_MENU:
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
