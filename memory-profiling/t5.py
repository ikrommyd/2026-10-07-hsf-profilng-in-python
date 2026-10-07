import numpy as np


def main():
    n = 10_000_000
    values = [float(i) for i in range(n)]
    array = np.arange(n, dtype=np.float64)
    print(len(values), len(array))


if __name__ == "__main__":
    main()
