import random

from poker_monte_carlo.model import Color
from poker_monte_carlo.types import Stack


def generate_stack(n: int = 52) -> Stack:
    if n > 52:
        raise Exception(f'Cannot generate a stack larger than 52 cards (got {n})')

    s = []
    for val in ('A', 'K', 'Q', 'J', *range(10)):
        for col in Color.values_as_text():
            s.append(f'{val}{col}')

    random.shuffle(s)
    return s[:n]
