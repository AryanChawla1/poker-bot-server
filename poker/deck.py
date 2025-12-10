from random import shuffle
from typing import List

from card import Card
from rank import Rank
from suit import Suit

class Deck:
    def __init__(self):
        self.__cards: List[Card] = [Card(r, s) for r in Rank for s in Suit]
        shuffle(self.__cards)
    
    def draw(self) -> Card:
        return self.__cards.pop()
