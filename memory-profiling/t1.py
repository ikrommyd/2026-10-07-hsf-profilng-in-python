import time

import numpy as np


def main():
    a = np.ones(20_000_000)
    time.sleep(0.5)
    b = np.zeros(20_000_000)
    time.sleep(0.5)
    c = a + b
    time.sleep(0.5)
    print(c.sum())


if __name__ == "__main__":
    main()
