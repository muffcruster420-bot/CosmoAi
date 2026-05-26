"""
src/data_voyager.py — NASA Voyager 1 & 2 Interstellar Plasma Data
Jesse Shangraw — Kingston, Ontario
Hunts coherence in plasma waves at 24.9 billion km
"""

import pandas as pd
import numpy as np
from pathlib import Path
from datetime import datetime, timedelta

def load_voyager_sample(n=5000, data_path="data/voyager_plasma_sample.csv"):
    """
    Load Voyager 1 plasma wave data. If real CSV exists, use it.
    Otherwise generate synthetic interstellar medium data matching NASA PWS.
    """
    path = Path(data_path)
    if path.exists():
        df = pd.read_csv(path)
        print(f"[VOYAGER] Loaded {len(df)} real plasma measurements from {path}")
    else:
        # Synthetic fallback — matches Voyager PWS plasma oscillations
        np.random.seed(42)
        
        # Voyager 1 crossed heliopause Aug 2012, now ~24.9B km
        # Plasma frequency ~2-3 kHz in interstellar medium
        base_date = datetime(2012, 8, 25)
        dates = [base_date + timedelta(days=i*30) for i in range(n)]
        
        # 95% background noise, 5% coherent plasma waves
        n_noise = int(n * 0.95)
        n_waves = n - n_noise
        
        noise = pd.DataFrame({
            'timestamp': dates[:n_noise],
            'distance_au': np.linspace(122, 165, n_noise),  # AU from Sun
            'plasma_freq_khz': np.random.normal(2.5, 0.8, n_noise),
            'electron_density': np.random.normal(0.055, 0.02, n_noise),  # cm^-3
            'magnetic_field_nt': np.random.normal(0.45, 0.15, n_noise),
            'is_coherent': 0
        })
        
        waves = pd.DataFrame({
            'timestamp': dates[n_noise:],
            'distance_au': np.linspace(122, 165, n_waves),
            'plasma_freq_khz': np.random.normal(2.85, 0.15, n_waves),  # tight coherence
            'electron_density': np.random.normal(0.08, 0.01, n_waves),
            'magnetic_field_nt': np.random.normal(0.52, 0.05, n_waves),
            'is_coherent': 1
        })
        
        df = pd.concat([noise, waves]).sample(frac=1).reset_index(drop=True)
        df = df.sort_values('timestamp').reset_index(drop=True)
        print(f"[VOYAGER] Generated synthetic {len(df)} plasma measurements (5% coherent waves)")
    
    # Coherence score — Shangraw Gap for plasma
    # Stable frequency + density correlation = interstellar coherence
    freq_stability = 1 - np.abs(df['plasma_freq_khz'] - 2.85) / 2.0
    freq_stability = np.clip(freq_stability, 0, 1)
    
    density_norm = np.clip(df['electron_density'] / 0.1, 0, 1)
    field_stability = 1 - np.abs(df['magnetic_field_nt'] - 0.5) / 0.5
    field_stability = np.clip(field_stability, 0, 1)
    
    df['coherence'] = 0.5*freq_stability + 0.3*density_norm + 0.2*field_stability
    
    return df

def detect_plasma_waves(df, gamma=2.5, alpha=0.25):
    """
    Apply FocalLossV2 to find rare coherent plasma waves
    """
    p = df['coherence'].values
    weight = (1 - p) ** gamma
    
    threshold = np.quantile(weight, 1 - alpha)
    rare_mask = weight >= threshold
    
    rare_waves = df[rare_mask].copy()
    rare_waves['focal_weight'] = weight[rare_mask]
    
    return rare_waves.sort_values('focal_weight', ascending=False)

def get_live_voyager_status():
    """Return current Voyager status (hardcoded, updates via NASA)"""
    # As of May 2026
    return {
        'voyager1_distance_km': 24_900_000_000,
        'voyager1_distance_au': 166.4,
        'voyager2_distance_km': 20_800_000_000,
        'voyager2_distance_au': 139.0,
        'signal_travel_time_hours': 23.0,
        'status': 'Both spacecraft in interstellar space, transmitting'
    }

if __name__ == "__main__":
    df = load_voyager_sample(5000)
    rare = detect_plasma_waves(df, gamma=2.5)
    status = get_live_voyager_status()
    print(f"Voyager 1: {status['voyager1_distance_au']:.1f} AU")
    print(f"Found {len(rare)} coherent plasma waves out of {len(df)}")
    print(f"Coherence purity in rare set: {rare['is_coherent'].mean():.1%}")
    print(f"vs overall: {df['is_coherent'].mean():.1%}")
