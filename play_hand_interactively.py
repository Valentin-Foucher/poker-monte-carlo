import os
from typing import Optional

from poker_monte_carlo import stack
from poker_monte_carlo.combinations import find_best_combination, compare_combinations
from poker_monte_carlo.model import Card
from poker_monte_carlo.parser import parse_board, parse_hand, parse_stack
from poker_monte_carlo.simulation import get_percentage_for_hands


def clear_screen():
    from sys import platform
    match platform:
        case 'linux' | 'linux2' | 'darwin':
            os.system('clear')
        case 'win32':
            os.system('cls')
        case other:
            raise Exception(f'OS not recognized ({other}')


def play_street(s: list[str], first_player_hand: tuple[Card, ...], second_player_hand: tuple[Card, ...],
                b: Optional[str] = None):

    parsed_board = parse_board(b) if b else []

    first_player_chances, second_player_chances = get_percentage_for_hands(
        first_player_hand,
        second_player_hand,
        parse_stack(s),
        parsed_board
    )

    clear_screen()
    print(f'first player hand: {first_player_hand} - {first_player_chances}%\n\n'
          f'{f"Board: {parsed_board}" if parsed_board else ""}\n\n'
          f'Second player hand: {second_player_hand} - {second_player_chances}%\n')

    return parsed_board


def select_player_hand(s: list[str], player_number: str = 'first') -> tuple[Card, ...]:
    player_input = input(f'Select {player_number} player hand or press enter to choose randomly (eg: 10s Ad): ')
    player_hand = None
    try:
        if player_input:
            player_hand = parse_hand(player_input)
            for card in player_input.strip().split(' '):
                s.remove(card)

    except:
        print(f'Could not parse {player_input}, player hand was chosen randomly')

    player_hand = player_hand or parse_hand(stack.draw_hand(s))
    return player_hand


def select_flop(s: list[str]) -> str:
    flop_input = input(f'Select flop cards or press enter to choose randomly (eg: Kc 3h 7d): ')
    board = None
    try:
        if flop_input:
            parse_board(flop_input)
            for card in flop_input.strip().split(' '):
                s.remove(card)

    except:
        print(f'Could not parse {flop_input}, flop was chosen randomly')

    board = board or stack.draw_flop(s)
    return board


def _select_single_card(s: list[str], board: str, action_name: str) -> str:
    card_input = input(f'Select a {action_name} card or press enter to choose randomly (eg: Qd): ')
    new_board = None
    try:
        if card_input:
            parse_board(f'{board} {card_input}')
            new_board = f'{board} {card_input}'
            s.remove(card_input.strip())
    except:
        print(f'Could not parse {card_input}, {action_name} was chosen randomly')

    return new_board or stack.draw_turn(s, board)


def select_turn(s: list[str], board: str) -> str:
    return _select_single_card(s, board, 'turn')


def select_river(s: list[str], board: str) -> str:
    return _select_single_card(s, board, 'river')


def main():
    while True:
        s = stack.generate_stack()

        first_player_hand = select_player_hand(s)
        second_player_hand = select_player_hand(s, player_number='second')

        play_street(s, first_player_hand, second_player_hand)

        board = select_flop(s)
        play_street(s, first_player_hand, second_player_hand, board)

        board = select_turn(s, board)
        play_street(s, first_player_hand, second_player_hand, board)

        board = select_river(s, board)
        final_board = play_street(s, first_player_hand, second_player_hand, board)

        result = compare_combinations(find_best_combination(first_player_hand, final_board),
                                      find_best_combination(second_player_hand, final_board))

        if result == 1:
            print('Player 1 wins!')
        elif result == -1:
            print('Player 2 wins!')
        else:
            print('Draw!')

        user_response = input('\nDo you want to play another hand? (y/n)')
        if user_response not in ('y', 'Y'):
            break


if __name__ == '__main__':
    main()

