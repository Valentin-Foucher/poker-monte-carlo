import enum
from dataclasses import dataclass


class Colors(enum.Enum):
    DIAMOND = '♦️'
    HEART = '♥️️'
    SPADE = '♣️'
    CLUB = '♠️'

    @classmethod
    def values_as_text(cls) -> [str]:
        return ['c', 'd', 'h', 's']

    def __str__(self):
        return self.value


@dataclass
class Card:
    color: Colors
    values: [int]

    def __repr__(self):
        return f'{self.values[0]} {self.color}'
