"""Print a side-by-side comparison for one match."""

from soccer_models import (
    both_teams_score,
    matrix_for,
    outcome_1x2,
    outcome_handicap,
    formatted_row,
)

# Example match: modest home edge, mild positive covariance.
MU_H = 1.6
MU_A = 1.1
COV = 0.15
RHO = -0.08
ADJ = 0.0

MODELS = ("independent", "dixon-coles", "bivariate")


def main():
    print(f"mu_home = {MU_H}, mu_away = {MU_A}, cov = {COV}, rho = {RHO}\n")
    print("1X2")
    print(f"{'model':14s}  {'home':>8s}  {'draw':>8s}  {'away':>8s}")
    for model in MODELS:
        m = matrix_for(MU_H, MU_A, model, cov=COV, rho=RHO)
        print(formatted_row(model, outcome_1x2(m)))

    print("\nboth teams to score")
    for model in MODELS:
        m = matrix_for(MU_H, MU_A, model, cov=COV, rho=RHO)
        yes = both_teams_score(m)
        print(f"{model:14s}  yes {yes:.4f}   no {1.0 - yes:.4f}")

    print(f"\nhandicap (home goals + {ADJ:g})")
    print(f"{'model':14s}  {'home':>8s}  {'push':>8s}  {'away':>8s}")
    for model in MODELS:
        m = matrix_for(MU_H, MU_A, model, cov=COV, rho=RHO)
        print(formatted_row(model, outcome_handicap(m, ADJ)))


if __name__ == "__main__":
    main()
