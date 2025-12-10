from __future__ import annotations
from functools import total_ordering

from suit import Suit
from rank import Rank

@total_ordering
class Card:
    def __init__(self, rank: Rank, suit: Suit):
        self.__rank: Rank = rank
        self.__suit: Suit = suit
    
    @property
    def rank(self) -> Rank:
        return self.__rank
    
    @property
    def suit(self) -> Suit:
        return self.__suit

    def __lt__(self, other: Card) -> bool:
        return self.rank < other.rank
    
    def __eq__(self, other: Card) -> bool:
        return self.rank == other.rank

    def __repr__(self) -> str:
        return f"{self.__rank.name} of {self.__suit.name}"

    def __str__(self) -> str:
        return f"{self.__rank.name} of {self.__suit.name}"
