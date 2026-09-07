"""
Gamma running-time model for a horse race.

Each horse has a finishing time T ~ Gamma(alpha, theta), independent,
parameterized from a mean and variance:

    theta = var / mu
    alpha = mu / theta = mu^2 / var

The race is won by the smallest time. Place is finish first or second.
Show is first, second, or third.

Harville place/show probabilities are computed from the win vector only,
assuming residual independence after the winner is removed. Henery uses
the same recursion after replacing leftover win probabilities with
p ** gamma (gamma = 0.8 by default).

The Monte Carlo frequencies need not match Harville or Henery. That
gap is the point of the comparison.
"""

import numpy as np

HENERY_GAMMA = 0.8


def gamma_params(mus, variances):
    """Return (alphas, thetas) for numpy's Gamma(shape=alpha, scale=theta)."""
    mus = np.asarray(mus, dtype=float)
    variances = np.asarray(variances, dtype=float)
    thetas = variances / mus
    alphas = mus / thetas
    return alphas, thetas


def simulate_races(alphas, thetas, n_sims):
    """
    Draw finishing times and return win / place / show frequencies.

    times shape is (n_horses, n_sims). Winner of a race is argmin over horses.
    """
    n = len(alphas)
    times = np.random.gamma(
        shape=alphas[:, np.newaxis],
        scale=thetas[:, np.newaxis],
        size=(n, n_sims),
    )
    ranks = np.argsort(times, axis=0)
    first = ranks[0]
    second = ranks[1]
    third = ranks[2]
    win = np.bincount(first, minlength=n) / n_sims
    place = win + np.bincount(second, minlength=n) / n_sims
    show = place + np.bincount(third, minlength=n) / n_sims
    return win, place, show


def harville_place(win):
    """P(i finishes 1st or 2nd) from Harville's formula."""
    win = np.asarray(win, dtype=float)
    n = len(win)
    out = np.empty(n)
    for i in range(n):
        x = win[i]
        for j in range(n):
            if i != j:
                x += win[j] * (win[i] / (1.0 - win[j]))
        out[i] = x
    return out


def harville_show(win):
    """P(i finishes in the first three) from Harville's formula."""
    win = np.asarray(win, dtype=float)
    n = len(win)
    out = np.empty(n)
    for i in range(n):
        x = win[i]
        for j in range(n):
            if i == j:
                continue
            x += win[j] * (win[i] / (1.0 - win[j]))
            for k in range(n):
                if k == i or k == j:
                    continue
                x += (
                    win[j]
                    * (win[k] / (1.0 - win[j]))
                    * (win[i] / (1.0 - win[j] - win[k]))
                )
        out[i] = x
    return out


def henery_place(win, gam=HENERY_GAMMA):
    """Harville place recursion after raising win probabilities to gam."""
    win = np.asarray(win, dtype=float)
    n = len(win)
    powered = win ** gam
    out = np.empty(n)
    for i in range(n):
        x = win[i]
        for j in range(n):
            if i == j:
                continue
            remaining = powered.sum() - powered[j]
            x += win[j] * (powered[i] / remaining)
        out[i] = x
    return out
