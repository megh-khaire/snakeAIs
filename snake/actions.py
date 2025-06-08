# snake/actions.py

# --- Main Menu Actions ---
ACTION_PLAY_MANUAL = "ACTION_PLAY_MANUAL"
ACTION_SELECT_ALGORITHM = "ACTION_SELECT_ALGORITHM"
ACTION_QUIT_GAME = "ACTION_QUIT_GAME"  # Also used by PauseMenu

# --- Mode Selection Screen Actions & Game Mode Identifiers ---
# These strings are used both as actions returned by ModeSelectionScreen
# and as keys in AppController.get_game_class().
# They also become the value of AppController.selected_game_mode.
MODE_MANUAL = "MODE_MANUAL" # Needed for AppController when "Play Game" is chosen from MainMenu
MODE_ASTAR = "MODE_ASTAR"
MODE_BEST_FS = "MODE_BEST_FS"
MODE_BFS = "MODE_BFS"
MODE_DFS = "MODE_DFS"
MODE_SIMPLE_HILL_CLIMBING = "MODE_SIMPLE_HILL_CLIMBING"
MODE_STEEPEST_ASCENT_HILL_CLIMBING = "MODE_STEEPEST_ASCENT_HILL_CLIMBING"
MODE_STOCHASTIC_HILL_CLIMBING = "MODE_STOCHASTIC_HILL_CLIMBING"
MODE_RANDOM = "MODE_RANDOM" # Note: In mode_selection.py, this was MODE_RANDOM_SEARCH. Will need to align.

ACTION_BACK_TO_MENU = "ACTION_BACK_TO_MENU"  # From ModeSelection to MainMenu

# --- Game Over Screen Actions ---
ACTION_PLAY_AGAIN = "ACTION_PLAY_AGAIN"
ACTION_MAIN_MENU = "ACTION_MAIN_MENU"    # From GameOver/PauseMenu to MainMenu

# --- Pause Menu Actions ---
ACTION_RESUME_GAME = "ACTION_RESUME_GAME"
ACTION_RESTART_GAME = "ACTION_RESTART_GAME"
# ACTION_MAIN_MENU is reused (defined above)
# ACTION_QUIT_GAME is reused (defined above)
