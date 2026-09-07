"""
Football score models on a truncated goal grid.

Three specifications for the joint distribution of (home goals, away goals):

* Independent Poisson: H ~ Pois(mu_H), A ~ Pois(mu_A), independent.
* Dixon-Coles: same Poisson margins, with a low-score dependence
  correction on the (0,0), (0,1), (1,0), (1,1) cells.
* Bivariate Poisson (common-shock): H = X1 + X3, A = X2 + X3 with
  independent Poisson Xi. Then Cov(H, A) = lambda_3, so the covariance
  must satisfy 0 <= cov <= min(mu_H, mu_A).

The matrix m[i, j] is P(home = i, away = j).
"""

import numpy as np
from scipy.stats import poisson

MAX_GOALS = 20
RHO = -0.08


def _poisson_pmf_vector(mu, mg):
    """P(K = 0), ..., P(K = mg-1) for K ~ Poisson(mu), via recurrence."""
    p = np.empty(mg)
    p[0] = 1.0
    for i in range(1, mg):
        p[i] = p[i - 1] * mu / i
    p *= np.exp(-mu)
    return p


def soccer_indep(mu_h, mu_a, mg=MAX_GOALS):
    """Independent Poisson joint pmf on {0, ..., mg-1}^2."""
    return np.outer(_poisson_pmf_vector(mu_h, mg), _poisson_pmf_vector(mu_a, mg))


def soccer_dixon(mu_h, mu_a, rho=RHO, mg=MAX_GOALS):
    """
    Dixon-Coles adjustment of the independent Poisson matrix.

    Only the four lowest scorelines are rescaled. rho < 0 increases
    the probability of low-scoring draws relative to independence.
    """
    m = soccer_indep(mu_h, mu_a, mg).copy()
    m[0, 0] *= 1.0 - rho * mu_h * mu_a
    m[0, 1] *= 1.0 + rho * mu_h
    m[1, 0] *= 1.0 + rho * mu_a
    m[1, 1] *= 1.0 - rho
    return m


def soccer_biv(mu_h, mu_a, cov, mg=MAX_GOALS):
    """
    Common-shock bivariate Poisson.

    H = X1 + X3, A = X2 + X3, Xi independent Poisson.
    lambda_3 = cov, lambda_1 = mu_h - cov, lambda_2 = mu_a - cov.
    Returns a zero matrix if cov is outside [0, min(mu_h, mu_a)].
    """
    m = np.zeros((mg, mg))
    if cov < 0.0 or cov > min(mu_h, mu_a):
        return m
    p1 = poisson.pmf(np.arange(mg), mu_h - cov)
    p2 = poisson.pmf(np.arange(mg), mu_a - cov)
    p3 = poisson.pmf(np.arange(mg), cov)
    for k in range(mg):
        for i in range(mg - k):
            for j in range(mg - k):
                m[i + k, j + k] += p1[i] * p2[j] * p3[k]
    return m


def matrix_for(mu_h, mu_a, model, cov=0.0, rho=RHO, mg=MAX_GOALS):
    if model == "independent":
        return soccer_indep(mu_h, mu_a, mg)
    if model == "dixon-coles":
        return soccer_dixon(mu_h, mu_a, rho, mg)
    if model == "bivariate":
        return soccer_biv(mu_h, mu_a, cov, mg)
    raise ValueError("model must be independent, dixon-coles, or bivariate")


def outcome_1x2(m):
    """Home win, draw, away win from a joint score matrix."""
    home = float(np.tril(m, -1).sum())
    draw = float(np.trace(m))
    away = float(np.triu(m, 1).sum())
    return home, draw, away


def outcome_handicap(m, adj):
    """
    Home / push / away after adding adj to the home goal count.

    adj = 0 is ordinary 1X2. adj = -0.5 is a half-goal home handicap
    (no push).
    """
    home = push = away = 0.0
    mg = m.shape[0]
    for i in range(mg):
        for j in range(mg):
            margin = i + adj - j
            if margin > 0:
                home += m[i, j]
            elif margin == 0:
                push += m[i, j]
            else:
                away += m[i, j]
    return home, push, away


def both_teams_score(m):
    """P(H >= 1 and A >= 1)."""
    return float(1.0 - m[0, :].sum() - m[:, 0].sum() + m[0, 0])


def formatted_row(name, triple):
    a, b, c = triple
    return f"{name:14s}  {a:8.4f}  {b:8.4f}  {c:8.4f}"
