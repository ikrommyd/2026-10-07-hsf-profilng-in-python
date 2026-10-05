import numpy as np

QUANTILES = np.linspace(0.01, 0.99, 99)


def distance(sample, reference):
    sample_quantiles = np.quantile(sample, QUANTILES)
    reference_quantiles = np.quantile(reference, QUANTILES)
    return np.abs(sample_quantiles - reference_quantiles).max()


def pseudo_experiment(reference, rng):
    sample = rng.normal(91.0, 2.5, 10_000)
    return distance(sample, reference)


def main():
    rng = np.random.default_rng(5)
    reference = rng.normal(91.0, 2.5, 5_000_000)
    distances = [pseudo_experiment(reference, rng) for _ in range(40)]
    print(round(float(np.mean(distances)), 4))


if __name__ == "__main__":
    main()
