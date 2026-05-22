import pandas as pd
import numpy as np

def load_sdss_sample(n=1000):
    np.random.seed(42)
    ra = np.random.uniform(0, 360, n)
    dec = np.random.uniform(-30, 90, n)
    z = np.random.exponential(0.3, n)
    df = pd.DataFrame({
        "ra": ra,
        "dec": dec,
        "z": z,
        "galaxy_type": np.random.choice(["spiral", "elliptical", "irregular"], n)
    })
    return df

def load_sdss():
    return load_sdss_sample()
