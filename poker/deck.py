from random import shuffle
from typing import List

from card import Card
from rank import Rank
from suit import Suit

class Deck:
    def __init__(self):
        self.__cards: List[Card] = [Card(r, s) for r in Rank for s in Suit]
        shuffle(self.__cards)
        self.__index = 0
    
    def draw(self) -> Card:
        card: Card = self.__cards[self.__index]
        self.__index += 1
        return card

    def shuffle(self):
        shuffle(self.__cards)
        self.__index = 0
