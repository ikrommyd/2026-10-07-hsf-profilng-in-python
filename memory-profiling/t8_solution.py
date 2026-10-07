import numpy as np
import pandas as pd

CHANNELS = ["ee", "mumu", "emu"]
TRIGGERS = ["single_muon", "single_electron", "double_muon", "double_electron"]


def make_table(n):
    rng = np.random.default_rng(7)
    return pd.DataFrame(
        {
            "channel": pd.Categorical(rng.choice(CHANNELS, n)),
            "trigger": pd.Categorical(rng.choice(TRIGGERS, n)),
            "mass": rng.normal(91.0, 5.0, n),
        }
    )


def main():
    table = make_table(3_000_000)
    groups = table.groupby(["channel", "trigger"], observed=True)
    print(groups["mass"].mean())


if __name__ == "__main__":
    main()
