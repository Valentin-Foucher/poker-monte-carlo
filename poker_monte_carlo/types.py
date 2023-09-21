from typing import NewType

from poker_monte_carlo.model import Card

Hand = NewType('Hand', tuple[Card, Card])
Board = NewType('Board', tuple[Card, Card, Card, ...])

Stack = NewType('Stack', list[str])
