import numpy as np


def load(n, rng):
    pt = 30.0 * rng.standard_exponential(n, dtype=np.float32)
    eta = 5.0 * rng.random(n, dtype=np.float32) - 2.5
    return pt, eta


def smear(pt, rng):
    return pt * rng.normal(1.0, 0.02, len(pt))


def momentum(pt, eta):
    return pt * np.cosh(eta)


def select(p, eta):
    return p[np.abs(eta) < 2.4]


def main():
    rng = np.random.default_rng(5)
    pt, eta = load(30_000_000, rng)
    smeared = smear(pt, rng)
    p = momentum(smeared, eta)
    selected = select(p, eta)
    print(len(selected), round(float(selected.mean()), 1))


if __name__ == "__main__":
    main()
