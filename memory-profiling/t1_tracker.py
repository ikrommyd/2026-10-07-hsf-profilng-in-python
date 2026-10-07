import time

import memray
import numpy as np


def main():
    a = np.ones(20_000_000)
    time.sleep(0.5)
    with memray.Tracker("t1_tracker.bin"):
        b = np.zeros(20_000_000)
        time.sleep(0.5)
        c = a + b
        time.sleep(0.5)
    print(c.sum())


if __name__ == "__main__":
    main()
