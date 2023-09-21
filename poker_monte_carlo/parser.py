from poker_monte_carlo.model import Card, Colors
from poker_monte_carlo.types import Board, Hand


def _color_from_string(c: str) -> Colors:
    match c:
        case 'd':
            return Colors.DIAMOND
        case 'h':
            return Colors.HEART
        case 's':
            return Colors.SPADE
        case 'c':
            return Colors.CLUB

    raise Exception(f'Invalid color {c}')


def _values_from_string(v: str) -> [int]:
    match v:
        case 'A':
            return [14, 1]
        case 'K':
            return [13]
        case 'Q':
            return [12]
        case 'J':
            return [11]
        case other:
            try:
                return [int(other)]
            except ValueError:
                raise Exception(f'Invalid value {v}')


def _parse_card(card_str: str) -> Card:
    val, col = card_str[:-1], card_str[-1]

    return Card(values=_values_from_string(val),
                color=_color_from_string(col))


def _parse_card_list(card_list_str: str) -> tuple[Card, ...]:
    return tuple(map(lambda x: _parse_card(x), card_list_str.split(' ')))


def parse_board(card_list_str: str) -> Board:
    cl = _parse_card_list(card_list_str)
    if (count := len(cl)) > 5 or count < 3:
        raise Exception(f'Invalid count of cards for a board ({count})')
    # noinspection PyTypeChecker
    return cl


def parse_hand(card_list_str: str) -> Hand:
    cl = _parse_card_list(card_list_str)
    if count := len(cl) != 2:
        raise Exception(f'Invalid count of cards for a hand ({count})')
    # noinspection PyTypeChecker
    return cl
