import numpy as np


def load(n, rng):
    pt = 30.0 * rng.standard_exponential(n, dtype=np.float32)
    eta = 5.0 * rng.random(n, dtype=np.float32) - 2.5
    return pt, eta


def main():
    rng = np.random.default_rng(5)
    n = 30_000_000
    pt, eta = load(n, rng)
    smeared = pt * rng.normal(1.0, 0.02, n)
    p = smeared * np.cosh(eta)
    selected = p[np.abs(eta) < 2.4]
    print(len(selected), round(float(selected.mean()), 1))


if __name__ == "__main__":
    main()
