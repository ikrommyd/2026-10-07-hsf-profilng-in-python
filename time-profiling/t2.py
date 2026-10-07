import os
import time

import numpy as np


def python_loop(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def main():
    print("pid:", os.getpid())
    rng = np.random.default_rng(2)
    for _ in range(200):
        python_loop(2_000_000)
        np.sort(rng.random(2_000_000))
        time.sleep(0.1)


if __name__ == "__main__":
    main()
