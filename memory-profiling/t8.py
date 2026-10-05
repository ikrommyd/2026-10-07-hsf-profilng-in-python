import numpy as np
import pandas as pd

CHANNELS = ["ee", "mumu", "emu"]
TRIGGERS = ["single_muon", "single_electron", "double_muon", "double_electron"]


def make_table(n):
    rng = np.random.default_rng(7)
    return pd.DataFrame(
        {
            "channel": rng.choice(CHANNELS, n),
            "trigger": rng.choice(TRIGGERS, n),
            "mass": rng.normal(91.0, 5.0, n),
        }
    )


def main():
    table = make_table(3_000_000)
    categorized = table.copy()
    categorized["category"] = categorized["channel"] + "_" + categorized["trigger"]
    print(categorized.groupby("category")["mass"].mean())


if __name__ == "__main__":
    main()
