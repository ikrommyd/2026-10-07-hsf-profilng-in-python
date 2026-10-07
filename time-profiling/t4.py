import numpy as np


def median_with_sort(x):
    return np.sort(x)[len(x) // 2]


def median_with_partition(x):
    middle = len(x) // 2
    return np.partition(x, middle)[middle]


def count_with_indexing(x):
    return len(x[x > 0.5])


def count_with_count_nonzero(x):
    return np.count_nonzero(x > 0.5)


def main():
    rng = np.random.default_rng(4)
    x = rng.random(20_000_000)
    for _ in range(6):
        median_with_sort(x)
        median_with_partition(x)
        count_with_indexing(x)
        count_with_count_nonzero(x)


if __name__ == "__main__":
    main()
