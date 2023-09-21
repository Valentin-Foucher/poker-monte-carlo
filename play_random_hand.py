from typing import Optional

from poker_monte_carlo import stack
from poker_monte_carlo.combinations import find_best_combination, compare_combinations
from poker_monte_carlo.model import Card
from poker_monte_carlo.parser import parse_board, parse_hand, parse_stack
from poker_monte_carlo.simulation import get_percentage_for_hands


def play_street(s: list[str], first_player_hand: tuple[Card, ...], second_player_hand: tuple[Card, ...],
                b: Optional[str] = None):
    if b:
        parsed_board = parse_board(b)
        print(f'Board: {parsed_board}')
    else:
        parsed_board = []

    first_player_chances, second_player_chances = get_percentage_for_hands(
        first_player_hand,
        second_player_hand,
        parse_stack(s),
        parsed_board
    )

    print(f'first player hand: {find_best_combination(first_player_hand, parsed_board).combination} - '
          f'{find_best_combination(first_player_hand, parsed_board).cards} - '
          f'{first_player_chances}%')
    print(f'Second player hand: {find_best_combination(second_player_hand, parsed_board).combination} - '
          f'{find_best_combination(second_player_hand, parsed_board).cards} - '
          f'{second_player_chances}%\n')

    return parsed_board


def main():
    while True:
        s = stack.generate_stack()

        first_player_hand = parse_hand(stack.draw_hand(s))
        second_player_hand = parse_hand(stack.draw_hand(s))

        preflop_first_player_chances, preflop_second_player_chances = get_percentage_for_hands(
            first_player_hand,
            second_player_hand,
            parse_stack(s),
            tuple()
        )

        print(f'first player hand: {first_player_hand} - {preflop_first_player_chances}%')
        print(f'Second player hand: {second_player_hand} - {preflop_second_player_chances}%\n')

        board = stack.draw_flop(s)
        play_street(s, first_player_hand, second_player_hand, board)

        board = stack.draw_turn(s, board)
        play_street(s, first_player_hand, second_player_hand, board)

        board = stack.draw_river(s, board)
        final_board = play_street(s, first_player_hand, second_player_hand, board)

        result = compare_combinations(find_best_combination(first_player_hand, final_board),
                                      find_best_combination(second_player_hand, final_board))

        if result == 1:
            print('Player 1 wins')
        elif result == -1:
            print('Player 2 wins')
        else:
            print('Draw')

        user_response = input('Do you want to play another hand? (y/n)')
        if user_response not in ('y', 'Y'):
            break

        print('\033c', end='')


if __name__ == '__main__':
    main()
