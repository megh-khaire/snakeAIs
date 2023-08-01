import sys
import pygame
from argparse import ArgumentParser
from snake.main.manual import Manual
from snake.uninformed_search_models.random_search import Random
from snake.informed_search_models.simple_hill_climbing import HillClimbing
from snake.informed_search_models.stochastic_hill_climbing import StochasticHillClimbing
from snake.informed_search_models.steepest_ascent_hill_climbing import (
    SteepestAscentHillClimbing,
)
from snake.uninformed_search_models.breadth_first_search import BFS
from snake.uninformed_search_models.depth_first_search import DFS
from snake.informed_search_models.best_first_search import BestFS
from snake.informed_search_models.a_star_search import AStar


def get_game_class(game_type):
    return {
        "manual": Manual,
        "random": Random,
        "simple_hc": HillClimbing,
        "stochastic_hc": StochasticHillClimbing,
        "steepest_ascent_hc": SteepestAscentHillClimbing,
        "bfs": BFS,
        "dfs": DFS,
        "bestfs": BestFS,
        "a_star": AStar,
    }.get(game_type, Manual)


parser = ArgumentParser(description="Start snakeAIs!")
parser.add_argument(
    "-gt",
    "--game_type",
    default="manual",
    type=str,
    help="type of game you want to play",
)
parser.add_argument(
    "-o",
    "--obstacles",
    default=False,
    type=bool,
    help="specify if you would like to include obstacles in the game",
)
args = vars(parser.parse_args())
game_type = args["game_type"]
game_has_obstaces = args["obstacles"]

pygame.init()
game_class = get_game_class(game_type)
game = game_class(game_has_obstaces)
score = game.main()
print("Final Score: ", score)
pygame.quit()
sys.exit()
