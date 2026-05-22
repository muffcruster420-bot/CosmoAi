"""data_cern.py - CERN Open Data Higgs loader for CosmoAi v2.2"""
import pandas as pd
import numpy as np

def load_cern_higgs():
    """Return simulated Higgs diphoton mass spectrum (CERN Open Data style)"""
    np.random.seed(125)
    mass = np.linspace(105, 160, 110)
    # background + Higgs peak at 125 GeV
    background = 1200 * np.exp(-0.02 * (mass - 105)) + np.random.normal(0, 30, len(mass))
    signal = 300 * np.exp(-0.5 * ((mass - 125.0) / 1.8) ** 2)
    counts = background + signal + np.random.normal(0, 20, len(mass))
    
    df = pd.DataFrame({
        'diphoton_mass_GeV': np.round(mass, 1),
        'events': np.round(counts).astype(int)
    })
    return df.set_index('diphoton_mass_GeV')['events']
