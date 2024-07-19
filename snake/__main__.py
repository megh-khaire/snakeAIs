import sys
from argparse import ArgumentParser, ArgumentTypeError

import pygame

from snake.informed_search_models.a_star_search import AStar
from snake.informed_search_models.best_first_search import BestFS
from snake.informed_search_models.simple_hill_climbing import HillClimbing
from snake.informed_search_models.steepest_ascent_hill_climbing import (
    SteepestAscentHillClimbing,
)
from snake.informed_search_models.stochastic_hill_climbing import StochasticHillClimbing
from snake.main.manual import Manual
from snake.uninformed_search_models.breadth_first_search import BFS
from snake.uninformed_search_models.depth_first_search import DFS
from snake.uninformed_search_models.random_search import Random


def str2bool(value):
    if isinstance(value, bool):
        return value
    if value.lower() in {"false", "f", "0", "no", "n"}:
        return False
    elif value.lower() in {"true", "t", "1", "yes", "y"}:
        return True
    else:
        raise ArgumentTypeError("Boolean value expected.")


def get_game_class(game_type):
    game_classes = {
        "manual": Manual,
        "random": Random,
        "simple_hc": HillClimbing,
        "stochastic_hc": StochasticHillClimbing,
        "steepest_ascent_hc": SteepestAscentHillClimbing,
        "bfs": BFS,
        "dfs": DFS,
        "bestfs": BestFS,
        "a_star": AStar,
    }
    return game_classes.get(game_type, Manual)


parser = ArgumentParser(description="Start snakeAIs!")
parser.add_argument(
    "-gt",
    "--game_type",
    default="manual",
    type=str,
    help="Type of game you want to play. Options: manual, random, simple_hc, stochastic_hc, steepest_ascent_hc, bfs, dfs, bestfs, a_star",
)
parser.add_argument(
    "-o",
    "--obstacles",
    default=False,
    type=str2bool,
    help="Specify if you would like to include obstacles in the game (true/false).",
)
args = parser.parse_args()
game_type = args.game_type
game_has_obstacles = args.obstacles

pygame.init()

try:
    game_class = get_game_class(game_type)
    game = game_class(game_has_obstacles)
    score = game.main()
    print("Final Score: ", score)
except Exception as e:
    print(f"An error occurred: {e}")
finally:
    pygame.quit()
    sys.exit()
