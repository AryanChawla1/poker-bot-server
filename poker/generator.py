from itertools import combinations

from poker.encoder import PRIMES

STRAIGHT_MASKS = [
    0x1F00, 0x0F80, 0x07C0, 0x03E0, 0x01F0,
    0x00F8, 0x007C, 0x003E, 0x001F, 0x100F
]

RANKS = [12, 11, 10, 9, 8, 7, 6, 5, 4, 3, 2, 1, 0]

def prime_product(ranks):
    product = 1
    for r in ranks:
        product *= PRIMES[r]
    return product

def generate_lookup():
    straight_flush_lookup = {}
    flush_lookup = {}
    straight_lookup = {}
    product_lookup = {}

    rank = 1

    # Straight Flush
    for mask in STRAIGHT_MASKS:
        straight_flush_lookup[mask] = rank
        rank += 1

    # Four of a Kind
    for quad in RANKS:
        for kicker in RANKS:
            if kicker != quad:
                prod = PRIMES[quad]**4 * PRIMES[kicker]
                product_lookup[prod] = rank
                rank += 1

    # Full House
    for trip in RANKS:
        for pair in RANKS:
            if pair != trip:
                prod = PRIMES[trip]**3 * PRIMES[pair]**2
                product_lookup[prod] = rank
                rank += 1

    # Flush (non-straight)
    for ranks in combinations(RANKS, 5):
        rank_mask = sum(1 << r for r in ranks)
        if rank_mask in STRAIGHT_MASKS:
            continue
        prod = prime_product(ranks)
        flush_lookup[prod] = rank
        rank += 1

    # Straight
    for mask in STRAIGHT_MASKS:
        straight_lookup[mask] = rank
        rank += 1

    # Three of a Kind
    for trip in RANKS:
        kickers = [r for r in RANKS if r != trip]
        for k1, k2 in combinations(kickers, 2):
            prod = PRIMES[trip]**3 * PRIMES[k1] * PRIMES[k2]  # FIXED
            product_lookup[prod] = rank
            rank += 1

    # Two Pair
    for p1, p2 in combinations(RANKS, 2):
        for kicker in RANKS:
            if kicker not in (p1, p2):
                prod = PRIMES[p1]**2 * PRIMES[p2]**2 * PRIMES[kicker]
                product_lookup[prod] = rank
                rank += 1

    # Pair
    for pair in RANKS:
        kickers = [r for r in RANKS if r != pair]
        for k1, k2, k3 in combinations(kickers, 3):
            prod = PRIMES[pair]**2 * PRIMES[k1] * PRIMES[k2] * PRIMES[k3]
            product_lookup[prod] = rank
            rank += 1

    # High Card
    for ranks in combinations(RANKS, 5):
        rank_mask = sum(1 << r for r in ranks)
        if rank_mask in STRAIGHT_MASKS:
            continue
        prod = prime_product(ranks)
        product_lookup[prod] = rank
        rank += 1

    return straight_flush_lookup, flush_lookup, straight_lookup, product_lookup
