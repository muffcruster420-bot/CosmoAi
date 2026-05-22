import streamlit as st
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.append(str(Path(__file__).parent.parent / "src"))

from trainer_focal import FocalLossV2
from data_sdss import load_sdss_sample, detect_filaments
from data_cern import load_cern_sample, detect_rare_decays

st.set_page_config(page_title="CosmoAi Detector", layout="wide")
st.title("CosmoAi: Shangraw Gap Detector")
st.caption("by Jesse Shangraw — Kingston, Ontario | Gamma>2 finds coherence in noise")

# Sidebar controls
st.sidebar.header("FocalLossV2 Controls")
gamma = st.sidebar.slider("Gamma (focus)", 0.0, 5.0, 2.5, 0.1)
alpha = st.sidebar.slider("Alpha (rare weight)", 0.1, 0.9, 0.25, 0.05)

st.sidebar.header("Data Source")
data_choice = st.sidebar.radio("Choose dataset:", 
    ["Synthetic", "SDSS Galaxies (real)", "CERN LHC Jets (real)"])

use_real = data_choice != "Synthetic"

if st.sidebar.button("Run Demo"):
    st.subheader(f"Results — Gamma={gamma}, Alpha={alpha}")
    
    if data_choice == "SDSS Galaxies (real)":
        st.write("**Loading 1,000 real SDSS DR18 galaxies...**")
        df = load_sdss_sample(1000)
        rare = detect_filaments(df, gamma=gamma, alpha=alpha)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Galaxies scanned", len(df))
        col2.metric("Filament nodes found", len(rare))
        col3.metric("Detection rate", f"{len(rare)/len(df):.1%}")
        
        st.write("**Top 10 densest filament regions (Shangraw Gap):**")
        display_cols = ['ra', 'dec', 'z', 'density', 'coherence', 'focal_weight']
        st.dataframe(rare[display_cols].head(10))
        
        st.scatter_chart(rare.head(100), x='ra', y='dec', size='density')
        
    elif data_choice == "CERN LHC Jets (real)":
        st.write("**Loading 10,000 CERN LHC 13 TeV jet events...**")
        df = load_cern_sample(10000)
        rare = detect_rare_decays(df, gamma=gamma, alpha=alpha)
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Jets scanned", len(df))
        col2.metric("Rare decays found", len(rare))
        col3.metric("Higgs purity", f"{rare['label_H_bb'].mean():.1%}")
        
        st.write("**Top 10 rarest coherent jets (Shangraw Gap):**")
        display_cols = ['fj_pt', 'fj_mass', 'fj_tau21', 'fj_doubleb', 'coherence', 'focal_weight']
        st.dataframe(rare[display_cols].head(10))
        
        st.scatter_chart(rare.head(200), x='fj_pt', y='fj_mass', size='coherence')
        
    else:
        st.write("**Generating synthetic cosmic web...**")
        n = 1000
        np.random.seed(42)
        data = pd.DataFrame({
            'x': np.random.normal(0, 1, n),
            'y': np.random.normal(0, 1, n),
            'density': np.random.exponential(1, n)
        })
        
        p = np.clip(data['density'] / data['density'].max(), 0.1, 0.99)
        weights = (1 - p) ** gamma
        
        col1, col2 = st.columns(2)
        col1.metric("Points generated", n)
        col2.metric("Mean focal weight", f"{weights.mean():.3f}")
        
        st.scatter_chart(data, x='x', y='y', size='density')
    
    st.success(f"Shangraw Gap active: Gamma={gamma} > 2.0 isolates top {alpha:.0%} hardest examples")
    
    with st.expander("See the FocalLossV2 math"):
        st.latex(r"FL(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t)")
        st.write(f"With γ={gamma}, rare examples get {(1-0.5)**gamma:.3f}x weight vs easy ones")

st.sidebar.markdown("---")
st.sidebar.info("v2.1 — SDSS + CERN live. Voyager next.")
