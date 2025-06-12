from enum import Enum, auto

class GameState(Enum):
    MAIN_MENU = auto()
    MODE_SELECTION = auto()
    GAME_PLAYING = auto()
    GAME_OVER = auto()
    PAUSE_MENU = auto()
    QUIT = auto()
