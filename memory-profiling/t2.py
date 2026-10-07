import time

import numpy as np


def main():
    a = np.ones(10_000_000)
    time.sleep(0.5)
    b = np.zeros(30_000_000)
    time.sleep(0.5)
    scratch = np.ones(60_000_000)
    total = scratch.sum()
    time.sleep(0.5)
    del scratch
    time.sleep(0.5)
    print(a.sum() + total, len(b))


if __name__ == "__main__":
    main()
