import copy
import random

from poker_monte_carlo.combinations import compare_combinations, find_best_combination
from poker_monte_carlo.model import Card


def get_percentage_for_hands(hands: list[tuple[Card, ...]],
                             stack: list[Card], board: tuple[Card, ...], n: int = 100000) -> list[float]:
    if len(hands) < 2 or len(hands) > 10:
        raise Exception(f'Too many or too little hands (count: {len(hands)})')

    wins = [0 for _ in range(len(hands))]

    for sim_id in range(n):
        sim_board = copy.copy(board)
        sim_stack = copy.copy(stack)

        while len(sim_board) < 5:
            next_card_index = random.randint(0, len(sim_stack) - 1)
            sim_board = (*sim_board, sim_stack.pop(next_card_index))

        winning_hands = [hands[0]]
        for hand in hands[1:]:
            result = compare_combinations(find_best_combination(winning_hands[0], sim_board),
                                          find_best_combination(hand, sim_board))

            if result == -1:
                winning_hands = [hand]
            elif result == 0:
                winning_hands.append(hand)

        for hand in winning_hands:
            wins[hands.index(hand)] += 1

    return [100 * w / n for w in wins]
