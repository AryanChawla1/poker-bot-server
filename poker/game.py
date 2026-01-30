from typing import List, Tuple
from enum import Enum
from random import randint
from dataclasses import dataclass

from poker.player import Player
from poker.deck import Deck
from poker.card import Card
from poker.evaluator import evaluate_7

# TODO Skip if everyone all-in

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

class ActionType(Enum):
    FOLD = "fold"
    CALL = "call"
    RAISE = "raise"
    CHECK = "check"

@dataclass
class Action:
    type: ActionType
    amount: int = 0


class GameState:
    def __init__(self, num_players, big_blind):
        self.pot = [0] * num_players
        self.state = [State.NEED_ACTION] * num_players
        self.call_amount = big_blind
        self.community: List[Card] = []
        self.current_player: int = 0
        self.street: str = "preflop"


    def reset_for_new_street(self):
        self.state = [State.NEED_ACTION] * len(self.state)

class PokerEngine:
    def __init__(self, players: List[Player], button: int, small_blind: int, big_blind: int):
        self.players = players
        self.button = button
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.deck = Deck()
        self.state = GameState(len(players), big_blind)
        self.start_hand()


    def start_hand(self):
        print("\n=== NEW HAND ===\n")
        self.deck.shuffle()
        self.deal_hole_cards()
        self.post_blinds()
        self.state.current_player = (self.button + 3) % len(self.players)
        self.state.street = "preflop"


    def deal_hole_cards(self):
        for i in range(len(self.players)):
            self.players[i].hole_cards = [self.deck.draw(), self.deck.draw()]


    def post_blinds(self):
        sb_index = (self.button + 1) % len(self.players)
        bb_index = (self.button + 2) % len(self.players)

        sb_player = self.players[sb_index]
        bb_player = self.players[bb_index]

        sb_value = sb_player.bet(self.small_blind)
        bb_value = bb_player.bet(self.big_blind)

        self.state.pot[sb_index] += sb_value # if small blind is all in, it is irrelevant to big blind
        self.state.pot[bb_index] += bb_value

        if sb_value < self.small_blind:
            self.state.state[sb_index] = State.ALL_IN
        if bb_value < self.big_blind:
            self.state.state[bb_index] = State.ALL_IN

        self.state.call_amount = self.big_blind


    def get_legal_actions(self, player_index: int) -> List[ActionType]:
        state = self.state.state[player_index]
        if state.value < 2: # FOLD or ALL IN
            return []
        
        call_required = self.state.call_amount - self.state.pot[player_index]
        player = self.players[player_index]

        actions = [ActionType.FOLD]

        if call_required <= 0:
            actions.append(ActionType.CHECK)
        elif player.bankroll > 0:
            actions.append(ActionType.CALL)
        
        if player.bankroll > call_required:
            actions.append(ActionType.RAISE)
        
        return actions


    def apply_action(self, player_index: int, action: Action):
        player = self.players[player_index]
        state = self.state

        match action.type:
            case ActionType.FOLD:
                state.state[player_index] = State.FOLD
            case ActionType.CHECK:
                state.state[player_index] = State.CALLED
            case ActionType.CALL:
                call_required = state.call_amount - state.pot[player_index]
                amount = min(call_required, player.bankroll)
                value = player.bet(amount)
                state.pot[player_index] += value
                state.state[player_index] = State.ALL_IN if value < call_required else State.CALLED
            case ActionType.RAISE:
                total = action.amount
                to_put_in = total - state.pot[player_index]
                value = player.bet(to_put_in)
                state.pot[player_index] += value
                state.call_amount = total
                state.state[player_index] = State.ALL_IN if player.bankroll == 0 else State.RAISED

                for i in range(len(state.state)):
                    if i != player_index and state.state[i].value > 1: # FOLD or ALL IN
                        state.state[i] = State.NEED_ACTION
        self.advance_turn_or_street()


    def advance_turn_or_street(self):
        if self.is_betting_round_over():
            self.advance_street()
        else:
            self.advance_to_next_player()


    def advance_to_next_player(self):
        n = len(self.players)
        i = self.state.current_player

        for _ in range(n):
            i = (i + 1) % n
            if self.state.state[i] == State.NEED_ACTION:
                self.state.current_player = i
                return


    def is_betting_round_over(self):
        for s in self.state.state:
            if s == State.NEED_ACTION:
                return False
            if s == State.RAISED:
                return False
        return True


    def advance_street(self):
        state = self.state
        if state.street == "preflop":
            self.deck.draw()
            state.community = [self.deck.draw(), self.deck.draw(), self.deck.draw()]
            state.street = "flop"
            print("\n=== FLOP ===\n")
            print(state.community)
        
        elif state.street == "flop":
            self.deck.draw()
            state.community.append(self.deck.draw())
            state.street = "turn"
            print("\n=== TURN ===\n")
            print(state.community)
        
        elif state.street == "turn":
            self.deck.draw()
            state.community.append(self.deck.draw())
            state.street = "river"
            print("\n=== RIVER ===\n")
            print(state.community)
        
        elif state.street == "river":
            state.street = "showdown"
        
        if state.street != "showdown":
            state.reset_for_new_street()
            self.state.current_player = (self.button + 1) % len(self.players)


    def is_hand_over(self):
        active_players = [i for i,s in enumerate(self.state.state) if s != State.FOLD]
        return len(active_players) <= 1 or self.state.street == "showdown"


    def resolve_hand(self):
        state = self.state
        pot = state.pot
        payouts = []
        active = [i for i,s in enumerate(state.state) if s != State.FOLD]
        active.sort(key=lambda i: evaluate_7(state.community + self.players[i].hole_cards))

        # TODO fix this to share pot
        while pot.count(0) != len(pot) and active:
            winner = active.pop(0)
            winner_pot = pot[winner]
            payout = 0
            for i in range(len(pot)):
                stake = min(pot[i], winner_pot)
                pot[i] -= stake
                payout += stake
            payouts.append((winner, payout))
        return payouts


class Game:
    def __init__(self, buy_in: int, num_players: int, small_blind: int, big_blind: int):
        self.players: List[Player] = [Player(f"bot{i+1}", buy_in) for i in range(num_players)]
        self.button: int = 0
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.engine: PokerEngine | None = None
    

    @property
    def num_players(self) -> int:
        return len(self.players)


    def start_hand(self):
        self.engine = PokerEngine(self.players, self.button, self.small_blind, self.big_blind)

    def handle_action(self, player_index: int, action: Action):
        self.engine.apply_action(player_index, action)

        if self.engine.is_hand_over():
            self.finish_hand()


    def finish_hand(self):
        payouts: List[tuple[int, int]] = self.engine.resolve_hand()
        for index, amount in payouts:
            print(f"{self.players[index]} won ${amount}")
            self.players[index].win_the_pot(amount)
        
        self.button = (self.button + 1) % len(self.players)
        self.players = [p for p in self.players if p.bankroll > 0]


def prompt_action(engine: PokerEngine, player_index: int) -> Action:
    legal = engine.get_legal_actions(player_index)
    print(engine.players[player_index])
    print("Pot:", engine.state.pot)
    print("Call Amount:", engine.state.call_amount)
    print("Legal Actions:", [a.value for a in legal])

    while True:
        choice = input("Enter action: ").strip().lower()
        match choice:
            case "f" | "fold":
                return Action(ActionType.FOLD)
            case "c" | "call":
                return Action(ActionType.CALL)
            case "k" | "check":
                return Action(ActionType.CHECK)
            case "r" | "raise":
                amount = int(input("Enter total bet amount "))
                # todo raise validation
                return Action(ActionType.RAISE, amount)
            case _:
                print("Invalid action, try again.")


if __name__ == "__main__":
    game = Game(BANKROLL, NUM_PLAYERS, SMALL_BLIND, BIG_BLIND)

    while game.num_players > 1:
        game.start_hand()

        while not game.engine.is_hand_over():
            engine = game.engine
            player_index = engine.state.current_player
            action = prompt_action(engine, player_index)
            game.handle_action(player_index, action)
        
        print("Game over!")
