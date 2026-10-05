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


def weighted_mean(group):
    return (group["pt"] * group["weight"]).sum() / group["weight"].sum()


def main():
    table = make_table(2_000_000, 100_000)
    result = table.groupby("run").apply(weighted_mean)
    print(round(float(result.mean()), 4))


if __name__ == "__main__":
    main()
