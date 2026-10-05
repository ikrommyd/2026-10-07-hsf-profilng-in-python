import numpy as np

QUANTILES = np.linspace(0.01, 0.99, 99)


def distance(sample, reference):
    sample_quantiles = np.quantile(sample, QUANTILES)
    reference_quantiles = np.quantile(reference, QUANTILES)
    return np.abs(sample_quantiles - reference_quantiles).max()


def main():
    rng = np.random.default_rng(5)
    reference = rng.normal(91.0, 2.5, 5_000_000)
    distances = []
    for _ in range(40):
        sample = rng.normal(91.0, 2.5, 10_000)
        distances.append(distance(sample, reference))
    print(round(float(np.mean(distances)), 4))


if __name__ == "__main__":
    main()
