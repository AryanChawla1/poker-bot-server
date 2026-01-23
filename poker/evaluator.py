from encoder import Encoder
from generator import generate_lookup
from card import Card
from rank import Rank
from suit import Suit

STRAIGHT_FLUSH_LOOKUP, FLUSH_LOOKUP, STRAIGHT_LOOKUP, PRODUCT_LOOKUP = generate_lookup()

def evaluate_5(cards):
    encoded = [Encoder.encode(c) for c in cards]

    # Flush check
    flush_mask = encoded[0]
    for c in encoded[1:]:
        flush_mask &= c
    is_flush = (flush_mask & 0xF000) != 0

    # Straight check
    straight_mask = 0
    for c in encoded:
        straight_mask |= c
    straight_mask = (straight_mask >> 16) & 0x1FFF
    is_straight = straight_mask in STRAIGHT_LOOKUP

    # Straight Flush
    if is_flush and is_straight:
        return STRAIGHT_FLUSH_LOOKUP[straight_mask]

    # Prime product
    prime_product = 1
    for c in encoded:
        prime_product *= (c & 0xFF)

    # Flush
    if is_flush:
        return FLUSH_LOOKUP[prime_product]

    # Straight
    if is_straight:
        return STRAIGHT_LOOKUP[straight_mask]

    # All others
    return PRODUCT_LOOKUP[prime_product]


if __name__ == "__main__":
    # Royal flush (best possible hand)
    rf = [
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.SPADES),
    ]
    assert evaluate_5(rf) == 1

    # Four of a kind (Aces)
    quads = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.ACE, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.KING, Suit.CLUBS),
    ]
    quad_rank = evaluate_5(quads)
    assert 1 < quad_rank < 167  # must be in quad range

    # Full house (Kings over Tens)
    full_house = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
    ]
    fh_rank = evaluate_5(full_house)
    assert 166 < fh_rank < 323  # must be in full house range

    # Flush (non-straight)
    flush = [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.TWO, Suit.HEARTS),
    ]
    flush_rank = evaluate_5(flush)
    assert 322 < flush_rank < 1600  # flush range

    # Straight (wheel)
    wheel = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.TWO, Suit.DIAMONDS),
        Card(Rank.THREE, Suit.HEARTS),
        Card(Rank.FOUR, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
    ]
    straight_rank = evaluate_5(wheel)
    assert 1599 < straight_rank < 1610  # straight range

    # High card
    high_card = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    hc_rank = evaluate_5(high_card)
    assert hc_rank > 6185  # high card range

    # ---------- PAIRS ----------
    pair_kings = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.NINE, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    pair_queens = [
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.NINE, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    assert evaluate_5(pair_kings) < evaluate_5(pair_queens)

    # ---------- TWO PAIR ----------
    two_pair_kings = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS),
    ]
    two_pair_queens = [
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.TEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.ACE, Suit.CLUBS),
    ]
    assert evaluate_5(two_pair_kings) < evaluate_5(two_pair_queens)

    # ---------- TRIPS ----------
    trips_kings = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    trips_queens = [
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.ACE, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    assert evaluate_5(trips_kings) < evaluate_5(trips_queens)

    # ---------- FULL HOUSE ----------
    fh_kings_over_tens = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
    ]
    fh_queens_over_tens = [
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.TEN, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
    ]
    assert evaluate_5(fh_kings_over_tens) < evaluate_5(fh_queens_over_tens)

    # ---------- QUADS ----------
    quads_kings = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.KING, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    quads_queens = [
        Card(Rank.QUEEN, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.QUEEN, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    assert evaluate_5(quads_kings) < evaluate_5(quads_queens)

    # ---------- STRAIGHTS ----------
    straight_broadway = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.QUEEN, Suit.HEARTS),
        Card(Rank.JACK, Suit.SPADES),
        Card(Rank.TEN, Suit.CLUBS),
    ]
    straight_nine_high = [
        Card(Rank.NINE, Suit.CLUBS),
        Card(Rank.EIGHT, Suit.DIAMONDS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.SIX, Suit.SPADES),
        Card(Rank.FIVE, Suit.CLUBS),
    ]
    assert evaluate_5(straight_broadway) < evaluate_5(straight_nine_high)

    # ---------- FLUSHES ----------
    flush_ace_high = [
        Card(Rank.ACE, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.TWO, Suit.HEARTS),
    ]
    flush_king_high = [
        Card(Rank.KING, Suit.HEARTS),
        Card(Rank.JACK, Suit.HEARTS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.HEARTS),
        Card(Rank.TWO, Suit.HEARTS),
    ]
    assert evaluate_5(flush_ace_high) < evaluate_5(flush_king_high)

    # ---------- HIGH CARD ----------
    hc_ace_high = [
        Card(Rank.ACE, Suit.CLUBS),
        Card(Rank.KING, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    hc_king_high = [
        Card(Rank.KING, Suit.CLUBS),
        Card(Rank.QUEEN, Suit.DIAMONDS),
        Card(Rank.NINE, Suit.HEARTS),
        Card(Rank.SEVEN, Suit.SPADES),
        Card(Rank.TWO, Suit.CLUBS),
    ]
    assert evaluate_5(hc_ace_high) < evaluate_5(hc_king_high)
