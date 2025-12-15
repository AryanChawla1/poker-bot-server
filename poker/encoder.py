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
    2,
    3,
    5,
    7,
    11,
    13,
    17,
    19,
    23,
    29,
    31,
    37,
    41
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

if __name__ == "__main__":
    cards = [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.TEN, Suit.HEARTS)
    ]
    encoded = [Encoder.encode(c) for c in cards]

    # detect flush
    flush_mask = encoded[0]
    for c in encoded[1:]:
        flush_mask &= c
    
    assert flush_mask & 0xF000 != 0

    # detect straight
    rank_mask = 0
    for c in encoded:
        rank_mask |=c
    
    rank_mask = (rank_mask >> 16) & 0x1FFF

    assert rank_mask == 0x1F00
