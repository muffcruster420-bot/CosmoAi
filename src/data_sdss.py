"""
CosmoAi - Real Data Loader (SDSS DR18 sample)
by Jesse Shangraw
Step 3: loads real galaxy coordinates
"""
import pandas as pd
import numpy as np
import os

def load_sdss_sample(path="data/galaxies_sample.csv", n_max=10000):
    """
    Loads SDSS galaxy sample.
    If file exists locally, uses it.
    Returns X, y where y=1 for clustered (filament-like) regions
    """
    if not os.path.exists(path):
        raise FileNotFoundError(f"Place galaxies_sample.csv at {path}")
    
    df = pd.read_csv(path).head(n_max)
    
    # features: ra, dec, z
    X_base = df[['ra', 'dec', 'z']].values.astype(np.float32)
    
    # normalize
    X_norm = (X_base - X_base.mean(axis=0)) / (X_base.std(axis=0) + 1e-6)
    
    # Shangraw Gap coherence: detect local overdensity
    # simple proxy: galaxies with neighbors within 1 degree
    from sklearn.neighbors import NearestNeighbors
    nbrs = NearestNeighbors(n_neighbors=6, algorithm='ball_tree').fit(X_norm[:, :2])
    distances, _ = nbrs.kneighbors(X_norm[:, :2])
    coherence = 1.0 / (distances.mean(axis=1) + 1e-3)
    coherence = coherence / coherence.max()
    
    # label top 5% most coherent as rare (y=1)
    threshold = np.percentile(coherence, 95)
    y = (coherence >= threshold).astype(int)
    
    # add coherence as feature (your 45Hz analog)
    X = np.hstack([X_norm, coherence.reshape(-1,1)])
    
    return X, y

def get_real_data():
    """Wrapper for demo"""
    return load_sdss_sample()
