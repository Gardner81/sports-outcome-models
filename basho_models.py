"""
Round-robin tournament from Elo ratings.

Sixteen competitors, each plays the other fifteen once. Bout probability
uses the standard Elo formula

    P(A beats B) = 1 / (1 + 10 ** ((R_B - R_A) / 400))

Ratings stay fixed for the whole tournament (a pre-tournament forecast).
The title (yusho) goes to the most wins. Ties can be reported as a shared
first place or broken with extra bouts from the same Elo probabilities.
"""

import random


def expected(elo_a, elo_b):
    return 1.0 / (1.0 + 10 ** ((elo_b - elo_a) / 400.0))


def play_bout(elo_a, elo_b):
    return random.random() <= expected(elo_a, elo_b)


def one_basho(elo):
    """Return win counts for a complete round robin."""
    n = len(elo)
    wins = [0] * n
    for i in range(n):
        for j in range(i + 1, n):
            if play_bout(elo[i], elo[j]):
                wins[i] += 1
            else:
                wins[j] += 1
    return wins


def leaders(wins):
    best = max(wins)
    return [i for i, w in enumerate(wins) if w == best]


def playoff(champs, elo):
    """Eliminate tied leaders with extra Elo bouts until one remains."""
    remaining = list(champs)
    while len(remaining) > 1:
        a, b = remaining[0], remaining[1]
        winner = a if play_bout(elo[a], elo[b]) else b
        remaining = [winner] + remaining[2:]
    return remaining[0]


def simulate(elo, n_basho, use_playoff=True):
    """
    Repeat the tournament n_basho times from the same ratings.

    Returns (title_share, first_place_share).
    title_share uses a playoff so it sums to 1.
    first_place_share credits every co-leader (may sum above 1).
    """
    n = len(elo)
    titles = [0] * n
    firsts = [0] * n
    for _ in range(n_basho):
        wins = one_basho(elo)
        champs = leaders(wins)
        for i in champs:
            firsts[i] += 1
        winner = playoff(champs, elo) if use_playoff else champs[0]
        titles[winner] += 1
    return (
        [t / n_basho for t in titles],
        [f / n_basho for f in firsts],
    )
