import threading

import numpy as np


def python_loop():
    total = 0
    for i in range(50_000_000):
        total += i * i
    return total


def numpy_sort():
    rng = np.random.default_rng(3)
    return np.sort(rng.random(50_000_000))


def run_in_two_threads(function):
    first = threading.Thread(target=function, name=f"{function.__name__}-1")
    second = threading.Thread(target=function, name=f"{function.__name__}-2")
    first.start()
    second.start()
    first.join()
    second.join()


def main():
    run_in_two_threads(python_loop)
    run_in_two_threads(numpy_sort)


if __name__ == "__main__":
    main()
