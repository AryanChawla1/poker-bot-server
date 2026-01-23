from card import Card
from suit import Suit
from rank import Rank

SUIT_MAPPING = {
    Suit.CLUBS: 0b0001,
    Suit.DIAMONDS: 0b0010,
    Suit.HEARTS: 0b0100,
    Suit.SPADES: 0b1000
}

PRIMES = [
    41, 37, 31, 29, 23, 19, 17, 13, 11, 7, 5, 3, 2
]

# bits      | 31 ...... 16 | 15 ... 12 | 11 ..... 8 | 7 ... 0 |
# fields:   | rank bitmask | suit bits | rank index | prime   |


class Encoder:
    @staticmethod
    def encode(card: Card) -> int:
        rank = card.rank
        suit = SUIT_MAPPING[card.suit]
        prime = PRIMES[rank]

        return (
            (1 << rank) << 16 |
            suit << 12 |
            rank << 8 |
            prime
        )
