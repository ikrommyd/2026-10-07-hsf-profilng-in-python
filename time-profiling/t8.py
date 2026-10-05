import awkward as ak
import numpy as np
import uproot
import vector


def load(path):
    with uproot.open(path) as file:
        return file["Events"].arrays()


def dimuon_masses(events, scale):
    muons = vector.zip(
        {
            "pt": events.Muon_pt * scale,
            "eta": events.Muon_eta,
            "phi": events.Muon_phi,
            "mass": events.Muon_mass,
        }
    )
    first, second = ak.unzip(ak.combinations(muons, 2))
    return ak.flatten((first + second).mass)


def main():
    histograms = {}
    for scale in np.linspace(0.98, 1.02, 21):
        events = load("../data/SMHiggsToZZTo4L.root")
        masses = dimuon_masses(events, scale)
        histograms[scale] = np.histogram(ak.to_numpy(masses), bins=100, range=(0, 200))[
            0
        ]
    print(len(histograms), sum(counts.sum() for counts in histograms.values()))


if __name__ == "__main__":
    main()
