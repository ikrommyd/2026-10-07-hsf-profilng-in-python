import numpy as np
import pandas as pd


def make_table(n, n_runs):
    rng = np.random.default_rng(6)
    return pd.DataFrame(
        {
            "run": rng.integers(0, n_runs, n),
            "pt": rng.exponential(30.0, n),
            "weight": rng.normal(1.0, 0.1, n),
        }
    )


def main():
    table = make_table(2_000_000, 100_000)
    table["weighted_pt"] = table["pt"] * table["weight"]
    sums = table.groupby("run")[["weighted_pt", "weight"]].sum()
    result = sums["weighted_pt"] / sums["weight"]
    print(round(float(result.mean()), 4))


if __name__ == "__main__":
    main()
