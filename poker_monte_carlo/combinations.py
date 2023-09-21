import copy
import enum

from poker_monte_carlo.model import Card, Color
from poker_monte_carlo.types import Hand, Board


class CombinationValue(enum.Enum):
    pass


def _find_highest_cards(combo: list[Card], cards_left: list[Card]) -> list[Card]:
    return combo + cards_left[-(5 - len(combo)):]


def _find_pair(cards: [Card]) -> tuple[list[Card], list[Card]]:
    cards_copy = copy.copy(cards)
    cards_count = len(cards)
    cpt = cards_count - 1
    pair_value = []

    while cpt >= 1:
        if cards[cpt].values[0] == cards[cpt - 1].values[0]:
            first = cards_copy.pop(cpt)
            second = cards_copy.pop(cpt - 1)
            pair_value = [first, second]
            break

        cpt -= 1

    return pair_value, cards_copy


def _find_two_pairs(cards: [Card]) -> tuple[list[Card], list[Card]]:
    first_pair, cards_left = _find_pair(cards)
    if not first_pair:
        return [], cards
    second_pair, cards_left = _find_pair(cards_left)
    if not second_pair:
        return [], cards

    return [*first_pair, *second_pair], cards_left


def _find_set(cards: [Card]) -> tuple[list[Card], list[Card]]:
    cards_copy = copy.copy(cards)
    cards_count = len(cards)
    cpt = cards_count - 1
    set_value = []

    while cpt >= 2:
        if cards[cpt].values[0] == cards[cpt - 1].values[0] == cards[cpt - 2].values[0]:
            first = cards_copy.pop(cpt)
            second = cards_copy.pop(cpt - 1)
            third = cards_copy.pop(cpt - 2)
            set_value = [first, second, third]
            break

        cpt -= 1

    return set_value, cards_copy


def _find_straight(cards: [Card]) -> tuple[list[Card], list[Card]]:
    cards_copy = copy.copy(cards)
    cpt = 0
    straight_cpt = []
    straight_value = []

    while cpt < len(cards):
        if straight_cpt:
            last = straight_cpt[-1]
            next_ = cards_copy[cpt]
            # getting the value 1 for aces for last and the value 14 for next_
            if last.values[-1] == next_.values[0]:
                cpt += 1
                continue
            if last.values[-1] + 1 != next_.values[0]:
                straight_cpt.clear()
                continue

        straight_cpt.append(cards_copy[cpt])
        if len(straight_cpt) == 5:
            straight_value = straight_cpt
            break

        cpt += 1

    for c in straight_cpt:
        cards_copy.remove(c)

    return straight_value, cards_copy


def _find_flush(cards: [Card]) -> tuple[list[Card], list[Card]]:
    cards_copy = copy.copy(cards)
    cards_count = len(cards)
    cpt = cards_count - 1
    flush_cpt = {Color.CLUB: [], Color.SPADE: [], Color.DIAMOND: [], Color.HEART: []}
    flush_value = []

    while cpt >= 0:
        current_flush = flush_cpt[cards_copy[cpt].color]
        current_flush.append(cards_copy[cpt])
        if len(current_flush) == 5:
            flush_value = current_flush
            break

        cpt -= 1

    return flush_value, cards_copy


def _find_full_house(cards: [Card]) -> tuple[list[Card], list[Card]]:
    set_, cards_left = _find_set(cards)
    if not set_:
        return [], cards
    second_pair, cards_left = _find_pair(cards_left)
    if not second_pair:
        return [], cards

    return [*set_, *second_pair], cards_left


def _find_quads(cards: [Card]) -> tuple[list[Card], list[Card]]:
    cards_copy = copy.copy(cards)
    cards_count = len(cards)
    cpt = cards_count - 1
    quads_value = []

    while cpt >= 2:
        if cards[cpt].values[0] == cards[cpt - 1].values[0] == cards[cpt - 2].values[0] == cards[cpt - 3].values[0]:
            first = cards_copy.pop(cpt)
            second = cards_copy.pop(cpt - 1)
            third = cards_copy.pop(cpt - 2)
            fourth = cards_copy.pop(cpt - 3)
            quads_value = [first, second, third, fourth]
            break

        cpt -= 1

    return quads_value, cards_copy


def _find_straight_flush(cards: [Card]) -> tuple[list[Card], list[Card]]:
    flush, cards_left = _find_flush(cards)
    if not flush:
        return [], cards
    straight_flush, cards_left = _find_straight(flush)
    if not straight_flush:
        return [], cards

    return straight_flush, cards_left


def find_best_combination(hand: Hand, board: Board) -> list[Card]:
    cards = sorted(hand + board, key=lambda c: c.values[0])
    best_combo = []

    for rule in (_find_straight_flush,
                 _find_quads,
                 _find_full_house,
                 _find_flush,
                 _find_straight,
                 _find_set,
                 _find_two_pairs,
                 _find_pair):

        combination, cards_left = rule(cards)
        if combination:
            best_combo = combination
            cards = cards_left
            break

    return _find_highest_cards(best_combo, cards)
