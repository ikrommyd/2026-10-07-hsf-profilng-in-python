import awkward as ak
import numpy as np
import uproot
import vector

MUON_BRANCHES = ["Muon_pt", "Muon_eta", "Muon_phi", "Muon_mass"]


def dimuon_masses(events):
    muons = vector.zip(
        {
            "pt": events.Muon_pt,
            "eta": events.Muon_eta,
            "phi": events.Muon_phi,
            "mass": events.Muon_mass,
        }
    )
    first, second = ak.unzip(ak.combinations(muons, 2))
    return ak.flatten((first + second).mass)


def main():
    counts = np.zeros(100, dtype=np.int64)
    n_pairs = 0
    for events in uproot.iterate(
        "../data/SMHiggsToZZTo4L.root:Events", MUON_BRANCHES, step_size=50_000
    ):
        masses = dimuon_masses(events)
        n_pairs += len(masses)
        counts += np.histogram(ak.to_numpy(masses), bins=100, range=(0, 200))[0]
    print(n_pairs, counts.sum())


if __name__ == "__main__":
    main()
