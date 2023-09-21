import copy
import random

from poker_monte_carlo.combinations import compare_combinations, find_best_combination
from poker_monte_carlo.model import Card


def get_percentage_for_hands(first_player_hand: tuple[Card, ...], second_player_hand: tuple[Card, ...],
                             stack: list[Card], board: tuple[Card, ...], n: int = 100000):
    player_1_wins = 0
    player_2_wins = 0

    for sim_id in range(n):
        sim_board = copy.copy(board)
        sim_stack = copy.copy(stack)

        while len(sim_board) < 5:
            next_card_index = random.randint(0, len(sim_stack) - 1)
            sim_board = (*sim_board, sim_stack.pop(next_card_index))

        result = compare_combinations(find_best_combination(first_player_hand, sim_board),
                                      find_best_combination(second_player_hand, sim_board))

        if result == 1:
            player_1_wins += 1
        elif result == -1:
            player_2_wins += 1

    return player_1_wins * 100 / n, player_2_wins * 100 / n
