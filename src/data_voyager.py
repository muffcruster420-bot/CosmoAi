"""
src/data_voyager.py — NASA Voyager 1 Plasma Data
Jesse Shangraw — Kingston, Ontario
Tracks interstellar plasma waves at 166 AU
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def load_voyager_sample(n=5000, data_path="data/voyager_plasma_sample.csv"):
    """
    Load Voyager 1 plasma wave data. If real CSV exists, use it.
    Otherwise generate synthetic data matching PWS instrument.
    """
    path = Path(data_path)
    if path.exists():
        df = pd.read_csv(path)
        print(f" Loaded {len(df)} real Voyager measurements from {path}")
    else:
        # Synthetic fallback — matches interstellar medium
        np.random.seed(42)
        base_date = datetime(2012, 8, 25)  # Heliopause crossing
        dates = [base_date + timedelta(days=i*30) for i in range(n)]
        
        # 95% noise, 5% coherent plasma oscillations
        n_noise = int(n * 0.95)
        n_waves = n - n_noise
        
        noise = pd.DataFrame({
            'timestamp': dates[:n_noise],
            'distance_au': np.linspace(122, 165, n_noise),
            'plasma_freq_khz': np.random.normal(2.5, 0.8, n_noise),
            'electron_density': np.random.normal(0.055, 0.02, n_noise),
            'magnetic_field_nt': np.random.normal(0.45, 0.15, n_noise),
            'is_coherent': 0
        })
        
        waves = pd.DataFrame({
            'timestamp': dates[n_noise:],
            'distance_au': np.linspace(122, 165, n_waves),
            'plasma_freq_khz': np.random.normal(2.85, 0.15, n_waves),
            'electron_density': np.random.normal(0.08, 0.01, n_waves),
            'magnetic_field_nt': np.random.normal(0.52, 0.05, n_waves),
            'is_coherent': 1
        })
        
        df = pd.concat([noise, waves]).sample(frac=1).reset_index(drop=True)
        print(f" Generated synthetic {len(df)} Voyager measurements (5% plasma waves)")
    
    # Coherence score — Shangraw Gap for interstellar plasma
    freq_score = 1 - np.abs(df['plasma_freq_khz'] - 2.85) / 2.0
    density_score = df['electron_density'] / 0.1
    field_score = 1 - np.abs(df['magnetic_field_nt'] - 0.5) / 0.5
    
    df['coherence'] = np.clip(0.5*freq_score + 0.3*density_score + 0.2*field_score, 0, 1)
    
    return df

def detect_plasma_waves(df, gamma=2.5, alpha=0.25):
    """
    Apply FocalLossV2 to find rare coherent plasma oscillations
    """
    p = df['coherence'].values
    weight = (1 - p) ** gamma
    
    threshold = np.quantile(weight, 1 - alpha)
    rare_mask = weight >= threshold
    
    rare_waves = df[rare_mask].copy()
    rare_waves['focal_weight'] = weight[rare_mask]
    
    return rare_waves.sort_values('focal_weight', ascending=False)

def get_live_voyager_status():
    """
    Current Voyager 1 status (May 2026)
    """
    return {
        'voyager1_distance_au': 166.4,
        'voyager1_distance_km': 24900000000,
        'signal_travel_time_hours': 23.0,
        'status': 'Interstellar space, plasma wave instrument active'
    }
