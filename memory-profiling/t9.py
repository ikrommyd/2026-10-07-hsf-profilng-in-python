import awkward as ak
import numpy as np
import uproot
import vector


def load(path):
    with uproot.open(path) as file:
        return file["Events"].arrays()


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
    events = load("data/SMHiggsToZZTo4L.root")
    selected = events[events.nMuon >= 2]
    masses = dimuon_masses(selected)
    counts, edges = np.histogram(ak.to_numpy(masses), bins=100, range=(0, 200))
    print(len(masses), counts.sum())


if __name__ == "__main__":
    main()
