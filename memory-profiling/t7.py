import numpy as np


def read_file(index):
    rng = np.random.default_rng(index)
    return rng.normal(size=(1_500_000, 4))


def preview(tracks, n=1_000):
    return tracks[:n]


def main():
    previews = []
    for index in range(15):
        tracks = read_file(index)
        previews.append(preview(tracks))
    combined = np.concatenate(previews)
    print(combined.shape, round(float(combined.mean()), 4))


if __name__ == "__main__":
    main()
