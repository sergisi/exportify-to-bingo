"""
Time estimation of a musical bingo
"""
import math
import itertools

def p(songs_played: int, card_size: int, playlist_size: int) -> float:
    """
    Probability given the number of songs played, the card size 
    and the playlist size that this bingo card has won.
    """
    return (math.comb(songs_played, card_size) / math.comb(playlist_size, card_size))


def expected_value(bingo_cards: int, card_size: int, playlist_size: int) -> float:
    it1 = ((1 - (1 
        - p(ti, card_size, playlist_size) 
        + p(ti - 1, card_size, playlist_size)) ** bingo_cards)
        for ti in range(card_size-1, playlist_size + 1))
    it2 = (b-a for a, b in itertools.pairwise(it1))

    return sum(ti * res for ti,res in enumerate(it2, start=card_size))

card_size = 9
playlist_size = 100
bingo_cards = 300

print()
