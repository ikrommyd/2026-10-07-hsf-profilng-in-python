import time

import memray
import numpy as np


def main():
    x1 = np.random.normal(size=100_000)
    x2 = np.random.normal(size=100_000)
    x3 = np.random.normal(size=100_000)
    x4 = np.random.normal(size=100_000)
    x5 = np.random.normal(size=100_000)
    x6 = np.random.normal(size=100_000)
    with memray.Tracker("bonus.bin", native_traces=True):
        out = x1 * x2 / x3 + x4 - x5 * x6
    print(out)
    time.sleep(0.5)


if __name__ == "__main__":
    main()
