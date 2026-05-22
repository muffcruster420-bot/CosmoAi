"""
src/data_cern.py — CERN LHC Open Data loader
Jesse Shangraw — Kingston, Ontario
Hunts Higgs → bb coherence at 13 TeV
"""

import pandas as pd
import numpy as np
from pathlib import Path

def load_cern_sample(n=10000, data_path="data/cern_jets_sample.csv"):
    """
    Load CERN LHC jet data. If real CSV exists, use it.
    Otherwise generate synthetic Higgs-like data matching CMS Open Data.
    """
    path = Path(data_path)
    if path.exists():
        df = pd.read_csv(path)
        print(f" Loaded {len(df)} real jet events from {path}")
    else:
        # Synthetic fallback — matches H→bb topology
        np.random.seed(42)
        n_qcd = int(n * 0.95)
        n_higgs = n - n_qcd
        
        qcd_jets = pd.DataFrame({
            'fj_pt': np.random.exponential(200, n_qcd),
            'fj_mass': np.random.normal(80, 30, n_qcd),
            'fj_tau21': np.random.beta(2, 5, n_qcd),
            'fj_doubleb': np.random.beta(1, 9, n_qcd),
            'label_QCD': 1,
            'label_H_bb': 0
        })
        
        higgs_jets = pd.DataFrame({
            'fj_pt': np.random.normal(450, 100, n_higgs),
            'fj_mass': np.random.normal(125, 10, n_higgs),
            'fj_tau21': np.random.beta(5, 2, n_higgs),
            'fj_doubleb': np.random.beta(8, 2, n_higgs),
            'label_QCD': 0,
            'label_H_bb': 1
        })
        
        df = pd.concat([qcd_jets, higgs_jets]).sample(frac=1).reset_index(drop=True)
        print(f" Generated synthetic {len(df)} jet events (5% Higgs)")
    
    # Coherence score — Shangraw Gap for particle physics
    df['coherence'] = 1 - np.abs(df['fj_mass'] - 125) / 125
    df['coherence'] = np.clip(df['coherence'] * df['fj_doubleb'], 0, 1)
    
    return df

def detect_rare_decays(df, gamma=2.5, alpha=0.25):
    """
    Apply FocalLossV2 to find rare Higgs decays
    """
    p = df['coherence'].values
    weight = (1 - p) ** gamma
    
    threshold = np.quantile(weight, 1 - alpha)
    rare_mask = weight >= threshold
    
    rare_decays = df[rare_mask].copy()
    rare_decays['focal_weight'] = weight[rare_mask]
    
    return rare_decays.sort_values('focal_weight', ascending=False)
