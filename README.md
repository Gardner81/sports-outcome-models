# sports-outcome-models
# Sports outcome models

Probability models for sports results, written in Python.

This folder starts with football scores. Sumo tournament simulation and a
gamma running-time model for horse racing will be added later.

## Football scores

Three models for the joint distribution of home and away goals:

1. **Independent Poisson** — baseline. Each side’s goals are Poisson and independent.
2. **Dixon–Coles** — same margins, with a correction on the four lowest scorelines so that low-scoring draws are not understated.
3. **Bivariate Poisson** — common-shock construction \(H = X_1 + X_3\), \(A = X_2 + X_3\). The shared count is the covariance, which must lie in \([0, \min(\mu_H, \mu_A)]\).

From the joint matrix the code reports 1X2, both-teams-to-score, and a goal-difference (handicap) split.

### Example

\(\mu_H = 1.6\), \(\mu_A = 1.1\), Dixon–Coles \(\rho = -0.08\), bivariate covariance \(0.15\), grid truncated at 20 goals.

```
1X2
model              home      draw      away
independent      0.4896    0.2489    0.2615
dixon-coles      0.4801    0.2678    0.2521
bivariate        0.4870    0.2659    0.2471

both teams to score
independent      yes 0.5324   no 0.4676
dixon-coles      yes 0.5419   no 0.4581
bivariate        yes 0.5433   no 0.4567
```

Dixon–Coles and the bivariate both put more mass on draws than independence, which is the usual reason to leave the baseline.

### Run

```bash
pip install -r requirements.txt
python demo.py
```

`soccer_models.py` is the library. `demo.py` prints the table above. There is no betting interface.

### Notes

- The goal grid is truncated at 20. Residual mass above that is negligible for ordinary football means.
- Dixon–Coles only rescales (0,0), (0,1), (1,0), (1,1).
- A covariance of 0 in the bivariate model turns the common shock off.
