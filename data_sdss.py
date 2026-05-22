"""data_sdss.py - SDSS DR18 sample loader for CosmoAi v2.2"""
import pandas as pd
import numpy as np

def load_sdss_sample(n=1000):
    """Return a sample of galaxies mimicking SDSS DR18"""
    np.random.seed(42)
    ra = np.random.uniform(0, 360, n)
    dec = np.random.uniform(-90, 90, n)
    z = np.random.exponential(0.3, n)  # redshift
    r_mag = np.random.normal(18.5, 1.8, n)
    u_g = np.random.normal(1.2, 0.3, n)
    
    df = pd.DataFrame({
        'ra_deg': np.round(ra, 4),
        'dec_deg': np.round(dec, 4),
        'redshift': np.round(z, 4),
        'r_mag': np.round(r_mag, 2),
        'u_g_color': np.round(u_g, 2),
        'type': np.random.choice(['GALAXY', 'QSO', 'STAR'], n, p=[0.85, 0.1, 0.05])
    })
    return df
def load_sdss():
    return load_sdss_sample()
