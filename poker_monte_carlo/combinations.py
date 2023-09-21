import copy
import dataclasses
import enum

from poker_monte_carlo.model import Card, Colors


class Combinations(enum.Enum):
    HIGH_CARD = 'High card', 1
    PAIR = 'Pair', 2
    TWO_PAIRS = 'Two Pairs', 3
    SET = 'Set', 4
    STRAIGHT = 'Straight', 5
    FLUSH = 'Flush', 6
    FULL_HOUSE = 'Full House', 7
    QUADS = 'Quads', 8
    STRAIGHT_FLUSH = 'Straight Flush', 9

    def __str__(self):
        return self.value[0]


@dataclasses.dataclass
class BestCards:
    cards: list[Card]
    combination: Combinations


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
    flush_cpt = {Colors.CLUB: [], Colors.SPADE: [], Colors.DIAMOND: [], Colors.HEART: []}
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


def find_best_combination(hand: tuple[Card, ...], board: tuple[Card, ...]) -> BestCards:
    cards = sorted(hand + board, key=lambda c: c.values[0])
    best_combo = []
    best_combination = Combinations.HIGH_CARD

    for rule, combination in ((_find_straight_flush, Combinations.STRAIGHT_FLUSH),
                              (_find_quads, Combinations.QUADS),
                              (_find_full_house, Combinations.FULL_HOUSE),
                              (_find_flush, Combinations.STRAIGHT_FLUSH),
                              (_find_straight, Combinations.STRAIGHT),
                              (_find_set, Combinations.SET),
                              (_find_two_pairs, Combinations.TWO_PAIRS),
                              (_find_pair, Combinations.PAIR)):

        used_cards, cards_left = rule(cards)
        if used_cards:
            best_combo = used_cards
            best_combination = combination
            cards = cards_left
            break

    return BestCards(cards=_find_highest_cards(best_combo, cards), combination=best_combination)


def compare_combinations(first_player_hand: BestCards, second_player_hand: BestCards) -> int:
    first_player_hand_value = first_player_hand.combination.value[1]
    second_player_hand_value = second_player_hand.combination.value[1]
    if first_player_hand_value > second_player_hand_value:
        return 1
    elif first_player_hand_value < second_player_hand_value:
        return -1
    else:
        for first_player_card, second_player_card in zip(first_player_hand.cards, second_player_hand.cards):
            if first_player_card.values[0] > second_player_card.values[0]:
                return 1
            elif first_player_card.values[0] < second_player_card.values[0]:
                return -1

        return 0
