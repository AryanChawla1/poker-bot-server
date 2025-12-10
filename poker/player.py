from typing import List

from card import Card

class Player:
    def __init__(self, name: str, buy_in: int):
        self.__name = name
        self.__bankroll = buy_in
        self.__hole_cards: List[Card] = []

    @property
    def name(self) -> str:
        return self.__name
    
    @property
    def bankroll(self) -> int:
        return self.__bankroll

    @property
    def hole_cards(self) -> List[Card]:
        return self.__hole_cards

    @hole_cards.setter
    def hole_cards(self, hole_cards: List[Card]):
        self.__hole_cards = hole_cards
    
    def bet(self, bet: int) -> int:
        bet = min(bet, self.__bankroll)
        self.__bankroll -= bet
        return bet
    
    def win_the_pot(self, pot: int):
        self.__bankroll += pot
    
    def __repr__(self) -> str:
        return f"Name: {self.__name} Bankroll: {self.__bankroll} Hole Cards: {self.hole_cards}"

    def __str__(self) -> str:
        return f"Name: {self.__name} Bankroll: {self.__bankroll} Hole Cards: {self.hole_cards}"
