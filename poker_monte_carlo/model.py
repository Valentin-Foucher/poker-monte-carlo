import enum
from dataclasses import dataclass


class Color(enum.Enum):
    DIAMOND = 1
    HEART = 2
    SPADE = 3
    CLUB = 4

    @classmethod
    def values_as_text(cls) -> [str]:
        return ['c', 'd', 'h', 's']


@dataclass
class Card:
    color: Color
    values: [int]
