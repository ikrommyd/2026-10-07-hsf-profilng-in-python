import time

import numpy as np


def python_loop(n):
    total = 0
    for i in range(n):
        total += i * i
    return total


def main():
    rng = np.random.default_rng(1)
    for _ in range(3):
        time.sleep(1.0)
        python_loop(20_000_000)
        np.sort(rng.random(20_000_000))


if __name__ == "__main__":
    main()
