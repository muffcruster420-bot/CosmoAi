import pandas as pd
import numpy as np

def load_cern_higgs():
    # synthetic Higgs-like peak at 125 GeV for demo
    np.random.seed(7)
    mass = np.concatenate([
        np.random.normal(125, 1.8, 300),
        np.random.normal(90, 12, 700)
    ])
    events = np.random.poisson(25, 1000)
    df = pd.DataFrame({"mass_GeV": mass, "events": events})
    return df.sort_values("mass_GeV").reset_index(drop=True)

def load_cern():
    return load_cern_higgs()
