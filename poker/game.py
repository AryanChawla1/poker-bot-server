from typing import List
from enum import Enum

from player import Player
from deck import Deck
from card import Card

class State(Enum):
    FOLD = 0 # no action
    ALL_IN = 1 # no action, but eligible to win pot
    CALLED = 2 # no action, but can receive action if raised
    RAISED = 3 # no action, but can receive action if re-raised
    NEED_ACTION = 4 # fold, call, raise
    LAST = 5 # fold, check, raise (pre-flop this is big blind, otherwise button)

#TODO: Poker hand Evaluator, Hand End Logic, Minimum Raise Logic, Flop -> River

class Game:
    def __init__(self, buy_in: int, num_players: int, small_blind: int, big_blind: int):
        self.__num_players: int = num_players
        self.__players: List[Player] = [Player(f"bot{i+1}", buy_in) for i in range(self.__num_players)]
        self.__button: int = 0
        self.__small_blind: int = small_blind
        self.__big_blind: int = big_blind

    @property
    def num_players(self) -> int:
        return self.__num_players

    def play_hand(self):
        deck = Deck()
        pot = [0] * self.__num_players
        state = [State.NEED_ACTION] * self.__num_players
        call = self.__big_blind
        community: List[Card] = []

        # deal cards
        for i in range(self.__num_players):
            index = (i + self.__button + 1) % self.__num_players
            player = self.__players[(i + self.__button + 1) % self.__num_players]
            # small blind
            if i == 0:
                pot[index] += player.bet(self.__small_blind)
            # big blind
            if i == 1:
                value = player.bet(self.__big_blind)
                pot[index] += value
                if value < self.__big_blind:
                    state[index] = State.ALL_IN
                else:
                    state[index] = State.LAST
            player.hole_cards = [deck.draw(), deck.draw()]
        
        def get_action(big_blind: bool):
            nonlocal call
            input_string = f"Enter action: [f] fold [c] check [r] raise" if big_blind else f"Enter action: [f] fold [c] call {call} [r] raise"
            action = input(input_string)
            match action:
                case 'c':
                    if big_blind:
                        state[index] = State.CALLED
                        return
                    value = player.bet(call)
                    pot[index] += value
                    if value < call:
                        state[index] = State.ALL_IN
                    else:
                        state[index] = State.CALLED
                case 'r':
                    value = input(f"What is raise? Minimum is {call}")
                    value = int(value)
                    call = value
                    for i in range(len(state)):
                        if state[i].value > 1:
                            state[i] = State.NEED_ACTION
                    pot[index] += value
                    if value < call:
                        state[index] = State.ALL_IN
                    else:
                        state[index] = State.RAISED
                case _:
                    state[index] = State.FOLD

        # pre_flop
        while all(s.value < 3 for s in state):
            for i in range(self.__num_players):
                index = (i + self.__button + 3) % self.__num_players
                player = self.__players[index]
                if state[index].value < 3:
                    continue
                if state[index] == State.RAISED:
                    state[index] = State.CALLED # previous raise is now called
                    continue

                print(player)
                print("Current Pot is: ", pot)
                get_action(state[index] == State.LAST)
        deck.draw()
        community = [deck.draw(), deck.draw(), deck.draw()]

        ## flop

        ## turn

        ## river

        # end (give money)
        self.__button = (self.__button + 1) % self.__num_players
        for player in self.__players:
            player.folded = False
            player.all_in = False
            if player.bankroll == 0:
                self.__players.remove(player)
                self.__num_players -= 1


if __name__ == "__main__":
    game = Game(100, 5, 1, 2)
    while game.num_players > 1:
        game.play_hand()
