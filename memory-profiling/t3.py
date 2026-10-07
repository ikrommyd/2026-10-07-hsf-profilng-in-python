import os
import time

import numpy as np

kept = []


def main():
    print("pid:", os.getpid())
    for i in range(120):
        array = np.ones(1_000_000)
        if i % 2 == 0:
            kept.append(array)
        time.sleep(0.5)


if __name__ == "__main__":
    main()
