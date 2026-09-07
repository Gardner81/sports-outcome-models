"""Print yusho probabilities from one random Elo field."""

import random

from basho_models import simulate

N = 16
N_BASHO = 20_000
SEED = 7


def main():
    random.seed(SEED)
    elo = [random.gauss(1500.0, 100.0) for _ in range(N)]
    titles, firsts = simulate(elo, N_BASHO, use_playoff=True)

    print(f"{N} competitors, {N_BASHO:,} tournaments, seed {SEED}")
    print(f"{'rikishi':>8}  {'Elo':>8}  {'yusho %':>8}  {'share of first %':>16}")
    order = sorted(range(N), key=lambda i: -elo[i])
    for i in order:
        print(
            f"{i + 1:8d}  {elo[i]:8.1f}  {100 * titles[i]:7.2f}%  "
            f"{100 * firsts[i]:15.2f}%"
        )
    print(
        f"\nyusho column sums to {100 * sum(titles):.2f}%  "
        f"(playoff, one champion per basho)"
    )
    print(
        f"share-of-first sums to {100 * sum(firsts):.2f}%  "
        f"(ties credited to every co-leader)"
    )


if __name__ == "__main__":
    main()
