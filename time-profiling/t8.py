import awkward as ak
import numpy as np
import uproot
import vector


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
        with uproot.open("../data/SMHiggsToZZTo4L.root") as file:
            events = file["Events"].arrays()
        masses = dimuon_masses(events, scale)
        counts, edges = np.histogram(ak.to_numpy(masses), bins=100, range=(0, 200))
        histograms[scale] = counts
    print(len(histograms), sum(counts.sum() for counts in histograms.values()))


if __name__ == "__main__":
    main()
