from typing import List, Tuple
from enum import Enum

from player import Player
from deck import Deck
from card import Card

BANKROLL = 100
NUM_PLAYERS = 5
SMALL_BLIND = 1
BIG_BLIND = 2

class State(Enum):
    FOLD = 0 # no action
    ALL_IN = 1 # no action, but eligible to win pot
    CALLED = 2 # no action, but can receive action if raised
    RAISED = 3 # no action, but can receive action if re-raised
    NEED_ACTION = 4 # fold, call, raise

#TODO: Poker hand Evaluator, Testing
# NOTE: These nested functions will have a changed design when not local, should fix

class Game:
    def __init__(self, buy_in: int, num_players: int, small_blind: int, big_blind: int):
        self.__num_players: int = num_players
        self.__players: List[Player] = [Player(f"bot{i+1}", buy_in) for i in range(self.__num_players)]
        self.__button: int = 0
        self.__small_blind: int = small_blind
        self.__big_blind: int = big_blind
        self.__deck = Deck()

    @property
    def num_players(self) -> int:
        return self.__num_players

    def play_hand(self):
        self.__deck.shuffle()
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
            player.hole_cards = [self.__deck.draw(), self.__deck.draw()]
        
        # get user input
        def get_action(call: int, index: int) -> int:
            required_bet = min(call - pot[index], self.__players[index].bankroll) # this calculates the call
            input_string = f"Enter action: [f] fold [c] check [r] raise" if required_bet == 0 else f"Enter action: [f] fold [c] call {required_bet} [r] raise"
            action = input(input_string)
            match action:
                case 'c':
                    if required_bet == 0:
                        state[index] = State.CALLED
                        return
                    value = player.bet(required_bet)
                    pot[index] += value
                    if value < call:
                        state[index] = State.ALL_IN
                    else:
                        state[index] = State.CALLED
                case 'r':
                    value = input(f"How much are you raising it by? Minimum is {required_bet}")
                    call += int(value)
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
            return call

        # simulate betting
        def betting(call: int, offset: int) -> Tuple[int]:
            while any(s.value > 2 for s in state):
                for i in range(self.__num_players):
                    index = (i + self.__button + offset) % self.__num_players
                    player = self.__players[index]
                    if sum(s.value == 0 for s in state) == self.__num_players - 1:
                        return (call, index)
                    if state[index].value < 3:
                        continue
                    if state[index] == State.RAISED:
                        state[index] = State.CALLED # previous raise is now called
                        continue

                    print(player)
                    print("Current Pot is: ", pot)
                    call = get_action(call, index)
            return (call, -1)

        def score(cards):
            pass

        def end(unanimous: bool):
            def get_winner_money(winner=winner):
                # use winner index to distribute wealth
                winner_pot = pot[winner]
                winner_payout = 0
                for i, p in enumerate(pot):
                    stake = min(p, winner_pot)
                    pot[i] -= stake
                    winner_payout += stake
                self.__players[winner].win_the_pot(winner_payout)
            if not unanimous:
                # score every players cards and then sort their indices in descending order
                winners: List[int] = [i for i in range(len(self.__players)) if state[i].value != 0]
                winners.sort(reverse=True, key= lambda x: score(community + self.__players[x].hole_cards))
                index = 0
                # for every winner, subtract their pot and continue until no money left
                while index < len(winners) and pot.count(0) != self.__num_players:
                    get_winner_money(winners[index])
                    index += 1
            else:
                get_winner_money()
            self.__button = (self.__button + 1) % self.__num_players
            self.__players = [p for p in self.__players if p.bankroll > 0]
            self.__num_players = len(self.__players)

        # pre_flop
        winner: int
        call, winner = betting(call, 3)
        if winner != -1:
            end(True)
        self.__deck.draw()
        community = [self.__deck.draw(), self.__deck.draw(), self.__deck.draw()]

        ## flop
        call, winner = betting(call, 1)
        if winner != -1:
            end(True)
        self.__deck.draw()
        community.append(self.__deck.draw())

        ## turn
        call, winner = betting(call, 1)
        if winner != -1:
            end(True)
        self.__deck.draw()
        community.append(self.__deck.draw())

        ## river
        call, winner = betting(call, 1)
        end(winner == -1)

if __name__ == "__main__":
    game = Game(BANKROLL, NUM_PLAYERS, SMALL_BLIND, BIG_BLIND)
    while game.num_players > 1:
        game.play_hand()
