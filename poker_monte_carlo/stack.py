import random

from poker_monte_carlo.model import Colors


def generate_stack(n: int = 52) -> list[str]:
    if n > 52:
        raise Exception(f'Cannot generate a stack larger than 52 cards (got {n})')

    s = []
    for val in ('A', 'K', 'Q', 'J', *range(2, 12)):
        for col in Colors.values_as_text():
            s.append(f'{val}{col}')

    random.shuffle(s)
    return s[:n]


def draw_hand(stack: list[str]) -> str:
    return f'{stack.pop()} {stack.pop()}'


def draw_flop(stack: list[str]) -> str:
    return f'{stack.pop()} {stack.pop()} {stack.pop()}'


def draw_turn(stack: list[str], board: str) -> str:
    return f'{board} {stack.pop()}'


def draw_river(stack: list[str], board: str) -> str:
    return f'{board} {stack.pop()}'
