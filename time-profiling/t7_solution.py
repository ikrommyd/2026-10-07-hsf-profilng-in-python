import awkward as ak
import numpy as np
import uproot
import vector

FIELDS = ["pt", "eta", "phi", "mass", "charge"]
Z_MASS = 91.19


def load(path):
    branches = [f"{name}_{field}" for name in ("Muon", "Electron") for field in FIELDS]
    with uproot.open(path) as file:
        events = file["Events"].arrays(branches)
    muons = vector.zip({field: events[f"Muon_{field}"] for field in FIELDS})
    electrons = vector.zip({field: events[f"Electron_{field}"] for field in FIELDS})
    return ak.concatenate([muons, electrons], axis=1)


def distance_to_z(q):
    pairings = [
        ((q.a + q.b).mass, (q.c + q.d).mass),
        ((q.a + q.c).mass, (q.b + q.d).mass),
        ((q.a + q.d).mass, (q.b + q.c).mass),
    ]
    distances = [np.minimum(abs(m1 - Z_MASS), abs(m2 - Z_MASS)) for m1, m2 in pairings]
    return np.minimum(np.minimum(distances[0], distances[1]), distances[2])


def four_lepton_masses(leptons, min_pt):
    leptons = leptons[leptons.pt > min_pt]
    q = ak.combinations(leptons, 4, fields=["a", "b", "c", "d"])
    q = q[q.a.charge + q.b.charge + q.c.charge + q.d.charge == 0]
    q = q[distance_to_z(q) < 10.0]
    return ak.flatten((q.a + q.b + q.c + q.d).mass)


def main():
    leptons = load("../data/SMHiggsToZZTo4L.root")
    for min_pt in np.linspace(10.0, 30.0, 15):
        masses = four_lepton_masses(leptons, min_pt)
        print(f"{min_pt:5.1f} {len(masses):6d} {float(ak.mean(masses)):8.3f}")


if __name__ == "__main__":
    main()
