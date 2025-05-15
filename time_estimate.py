"""
Time estimation of a musical bingo
"""
import math
from typing import Generator
import itertools
import functools

def probability_bingo_won(songs_played: int, card_size: int, playlist_size: int) -> float:
    """
    Probability given the number of songs played, the card size 
    and the playlist size that this bingo card has won.
    """
    return (math.comb(songs_played, card_size) / math.comb(playlist_size, card_size))


def probability_of_winning(bingo_cards: int, card_size: int, playlist_size: int) -> Generator[float, None, None]:
    """
    List of probabilitiet of given players (bingo cards),
    a card size, and a playlist that they win on index.

    Index 0 means the probability of winning on *song 2*

    """
    #  NOTE: this compuetes the probabiltity of winning
    # at songs_played and below.
    # Thus, we substract the previous value to get it.
    it1 = ((1 - (1 
        - probability_bingo_won(songs_played, card_size, playlist_size) 
        + probability_bingo_won(songs_played - 1, card_size, playlist_size)) ** bingo_cards)
        for songs_played in range(1, playlist_size + 1))
    return (b-a for a, b in itertools.pairwise(it1))


def expected_value(bingo_cards: int, card_size: int, playlist_size: int) -> float:
    """
    Expected value that given players (bingo cards), the card
    size and the song list, *it expects* to last
    """

    it1 = ((1 - (1 
        - probability_bingo_won(ti, card_size, playlist_size) 
        + probability_bingo_won(ti - 1, card_size, playlist_size)) ** bingo_cards)
        for ti in range(card_size-1, playlist_size + 1))
    it2 = (b-a for a, b in itertools.pairwise(it1))

    return sum(ti * res for ti,res in enumerate(it2, start=card_size))


def bisection_algorithm(f, start, end, target=0) -> int:
    "magic"
    assert f(start) < target
    assert f(end) > target
    for _ in range(32):
        midp = (start + end) // 2
        if f(midp) < target:
            start = midp
        else:
            end = midp
    return start


