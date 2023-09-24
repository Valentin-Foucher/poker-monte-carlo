import argparse
import os
from typing import Optional

from poker_monte_carlo import stack
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


def play_street(s: list[str], hands: list[tuple[Card, ...]], b: Optional[str] = None) -> list[float]:

    parsed_board = parse_board(b) if b else []

    win_percentages = get_percentage_for_hands(
        hands,
        parse_stack(s),
        parsed_board
    )

    clear_screen()
    scoreboard = ''
    for i, (hand, percentage) in enumerate(zip(hands, win_percentages)):
        scoreboard += f'Player {i + 1}: {hand} - {percentage}%\n'

    scoreboard += f'\n{f"Board: {parsed_board}" if parsed_board else ""}\n'
    print(scoreboard)

    return win_percentages


def main(player_count: int):
    while True:
        s = stack.generate_stack()

        hands = [parse_hand(stack.draw_hand(s)) for _ in range(player_count)]
        play_street(s, hands)

        board = stack.draw_flop(s)
        play_street(s, hands, board)

        board = stack.draw_turn(s, board)
        play_street(s, hands, board)

        board = stack.draw_river(s, board)
        win_percentages = play_street(s, hands, board)

        winners = []
        for i, percentage in enumerate(win_percentages):
            if percentage == 100:
                winners.append(str(i + 1))

        print(f'Player{"s" if len(winners) > 1 else ""} {", ".join(winners)} win{"s" if len(winners) == 1 else ""}!')

        user_response = input('\nDo you want to play another hand? (y/n)')
        if user_response not in ('y', 'Y'):
            break


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Script allowing to play random poker hands and hinting the win odds '
                                                 'for each player')
    parser.add_argument(
        '-n', '--players-count',
        default=2,
        type=int,
        choices=range(2, 11)
    )

    main(parser.parse_args().players_count)
