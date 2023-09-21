from poker_monte_carlo.model import Card, Color
from poker_monte_carlo.types import Board, Hand


def _color_from_string(c: str) -> Color:
    match c:
        case 'd':
            return Color.DIAMOND
        case 'h':
            return Color.HEART
        case 's':
            return Color.SPADE
        case 'c':
            return Color.CLUB

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
    if count := len(cl) != 5:
        raise Exception(f'Invalid count of cards for a board ({count})')
    # noinspection PyTypeChecker
    return cl


def parse_hand(card_list_str: str) -> Hand:
    cl = _parse_card_list(card_list_str)
    if count := len(cl) != 2:
        raise Exception(f'Invalid count of cards for a hand ({count})')
    # noinspection PyTypeChecker
    return cl
