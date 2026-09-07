"""Compare Monte Carlo place frequencies with Harville and Henery."""

import numpy as np

from horse_models import (
    HENERY_GAMMA,
    gamma_params,
    harville_place,
    henery_place,
    simulate_races,
)

MUS = [100.0, 105.0, 110.0, 115.0, 120.0, 112.7, 125.1, 98.5, 114.2, 106.9]
VARS = [105.0, 109.7, 99.4, 150.2, 120.5, 90.4, 110.3, 125.2, 115.8, 117.4]
N_SIMS = 1_000_000


def main():
    alphas, thetas = gamma_params(MUS, VARS)
    sim_win, sim_place, _sim_show = simulate_races(alphas, thetas, N_SIMS)
    hv_place = harville_place(sim_win)
    hn_place = henery_place(sim_win, HENERY_GAMMA)

    print(f"{len(MUS)} horses, {N_SIMS:,} races, Henery gamma = {HENERY_GAMMA}")
    print(
        f"{'horse':>6}  {'sim win':>8}  {'sim place':>10}  "
        f"{'Harville':>8}  {'Henery':>8}"
    )
    for i in range(len(MUS)):
        print(
            f"{i + 1:6d}  {100 * sim_win[i]:7.2f}%  {100 * sim_place[i]:9.2f}%  "
            f"{100 * hv_place[i]:7.2f}%  {100 * hn_place[i]:7.2f}%"
        )
    print(f"\nwin column sums to {100 * sim_win.sum():.2f}%")


if __name__ == "__main__":
    main()
