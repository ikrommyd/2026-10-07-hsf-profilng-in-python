import numpy as np


def with_temporaries(data, n):
    return [np.sum((data - i) ** 2) for i in range(n)]


def with_buffer(data, n):
    buffer = np.empty_like(data)
    results = []
    for i in range(n):
        np.subtract(data, i, out=buffer)
        np.square(buffer, out=buffer)
        results.append(buffer.sum())
    return results


def main():
    data = np.ones(5_000_000)
    print(with_temporaries(data, 100) == with_buffer(data, 100))


if __name__ == "__main__":
    main()
