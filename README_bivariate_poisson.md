# Bivariate Poisson soccer model

Prices **1X2**, **team-to-score / BTTS**, and **totals** from a single joint distribution of home and away goals.

The independent Poisson model treats the two scores as unrelated. Real matches are not quite like that: low-scoring games and 0-0 / 1-1 cells are correlated. This script uses the classical **bivariate Poisson** construction so that dependence is a parameter you can set, not an accident of the simulation.

## Model

Let

\[
X \sim \mathrm{Poisson}(\lambda_H),\quad
Y \sim \mathrm{Poisson}(\lambda_A),\quad
Z \sim \mathrm{Poisson}(\lambda_C)
\]

be independent, and define the observed scores by

\[
H = X + Z,\qquad A = Y + Z.
\]

Then \((H,A)\) is bivariate Poisson with

\[
\mathbb{E}[H] = \mu_H = \lambda_H + \lambda_C,\qquad
\mathbb{E}[A] = \mu_A = \lambda_A + \lambda_C,\qquad
\mathrm{Cov}(H,A) = \lambda_C.
\]

The shared component \(Z\) is the dependence. If \(\lambda_C = 0\) the model collapses to two independent Poissons, which is the engine in `soccer01.py`.

The joint mass function is

\[
P(H=i,A=j)
= e^{-(\lambda_H+\lambda_A+\lambda_C)}
\sum_{k=0}^{\min(i,j)}
\frac{\lambda_H^{i-k}}{(i-k)!}\,
\frac{\lambda_A^{j-k}}{(j-k)!}\,
\frac{\lambda_C^{k}}{k!}.
\]

The code builds this by enumerating \(k\) and accumulating into a score matrix `m[i,j]`, then renormalising so the truncated grid sums to 1.

## Inputs

| Input | Meaning | Constraint |
|---|---|---|
| `muH` | Expected home goals | \(\ge 0\) |
| `muA` | Expected away goals | \(\ge 0\) |
| `cov` | Covariance of the two scores (\(\lambda_C\)) | \(0 \le \mathrm{cov} \le \min(\mu_H,\mu_A)\) |
| `line` | Totals line (e.g. 2.5) | \(\ge 0\) |

The covariance bound is required by the construction: \(\lambda_H = \mu_H - \mathrm{cov}\) and \(\lambda_A = \mu_A - \mathrm{cov}\) must stay non-negative.

`mg=31` is the truncation (scores \(0,\ldots,30\)). For ordinary football means that tail is negligible; the matrix is then divided by its own sum so the output probabilities remain coherent.

## Outputs

Three length-3 lists:

1. **1X2** — \(P(H>A)\), \(P(H=A)\), \(P(H<A)\)
2. **Scoring** — \(P(H\ge 1)\), \(P(A\ge 1)\), \(P(H\ge 1 \land A\ge 1)\) (BTTS)
3. **Totals** — \(P(H+A > L)\), \(P(H+A = L)\), \(P(H+A < L)\)

If `line` is not an integer (2.5, 3.5, …) the middle “equal” mass is zero, which is intended.

These are **fair** probabilities. To turn them into book prices, pass them through the margin routine in the odds engine (`apply_margin` / vig).

## How to run

```text
python soccer_biv.py
```

You will be prompted for home mean, away mean, covariance, and the totals line.

Example, roughly a 1.60–1.10 home favourite with mild positive dependence:

```text
home mean:     1.60
away mean:     1.10
covariance:    0.15
line:          2.5
```

Compare `cov = 0` against `cov > 0` on the same means. Positive covariance typically **lifts the draw and BTTS** relative to the independent model and slightly reshapes the totals.

## Why this is useful on a desk

From one joint matrix you can price:

- match result (1X2)
- both teams to score
- over / under / exact total
- derived markets that are functions of \((H,A)\): exact score, Asian totals (by splitting the integer mass), team totals, clean sheets

That is the point of a generative score model. You do not price those markets as unrelated numbers. You price them as different slices of the same distribution, then apply one commercial margin.

## What this model does not do

- It only allows **non-negative** correlation. Football sometimes needs a little negative dependence in the 0-0 / 1-0 / 0-1 / 1-1 cells (Dixon–Coles \(\rho\)). Bivariate Poisson cannot produce \(\mathrm{Cov}(H,A) < 0\).
- Means are inputs. Attack / defence ratings and home advantage are upstream:  
  \(\mu_H = \mathrm{att}_H \cdot \mathrm{def}_A \cdot \mathrm{home}\),  
  \(\mu_A = \mathrm{att}_A \cdot \mathrm{def}_H\).
- No in-play intensity, red cards, or scoreline-dependent rates.
- Truncation at 30–30 is a numerical convenience, not a claim about football.

If you need down-weighting of low-score independence without forcing \(\mathrm{Cov} \ge 0\), Dixon–Coles on top of independent Poisson is the usual next patch. If you need a richer dependence structure, a copula or a bivariate negative binomial is the next model, not a larger `mg`.

## Numerics

The Poisson pmf is built recursively,

\[
P(K=i) = P(K=i-1)\cdot \frac{\lambda}{i},\qquad P(K=0)=e^{-\lambda},
\]

so there is no call to `scipy.stats.poisson` inside the inner loop. The triple loop over \(k,i,j\) is \(O(\mathtt{mg}^3)\) with \(\mathtt{mg}=31\), which is instant for a single match and fine for a portfolio demo. Vectorising the outer sum over \(k\) is the obvious speed-up if this is later run on a full coupon.

## Relation to the rest of the toolkit

| Script | Role |
|---|---|
| Odds / vig engine | American ↔ decimal, de-vig, apply margin |
| Independent Poisson 1X2 | Special case of this model with `cov = 0` |
| This script | Joint scores with \(\mathrm{Cov}(H,A)\ge 0\), several markets from one matrix |
| Horse gamma + Harville / Henery | Ordering probabilities in a different sport |

Same pricing loop in every case: model → fair probabilities → margin → book odds.
