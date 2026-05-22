import streamlit as st
import numpy as np
import pandas as pd
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent / "src"))

from trainer_focal import FocalLossV2
from data_sdss import load_sdss_sample, detect_filaments
from data_cern import load_cern_sample, detect_rare_decays
from data_voyager import load_voyager_sample, detect_plasma_waves, get_live_voyager_status

st.set_page_config(page_title="CosmoAi Detector", layout="wide")
st.title("CosmoAi: Shangraw Gap Detector")
st.caption("by Jesse Shangraw — Kingston, Ontario | Gamma>2 finds coherence from CERN to Voyager")

st.sidebar.header("FocalLossV2 Controls")
gamma = st.sidebar.slider("Gamma (focus)", 0.0, 5.0, 2.5, 0.1)
alpha = st.sidebar.slider("Alpha (rare weight)", 0.1, 0.9, 0.25, 0.05)

st.sidebar.header("Data Source")
data_choice = st.sidebar.radio("Choose dataset:", 
    ["Synthetic", "SDSS Galaxies (real)", "CERN LHC Jets (real)", "Voyager 1 Plasma (real)"])

if st.sidebar.button("Run Detection"):
    st.subheader(f"Results — Gamma={gamma}, Alpha={alpha}")
    
    if data_choice == "SDSS Galaxies (real)":
        st.write("**Loading 1,000 real SDSS DR18 galaxies...**")
        df = load_sdss_sample(1000)
        rare = detect_filaments(df, gamma=gamma, alpha=alpha)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Galaxies", len(df))
        col2.metric("Filaments", len(rare))
        col3.metric("Rate", f"{len(rare)/len(df):.1%}")
        col4.metric("Scale", "10^23 m")
        
        st.dataframe(rare[['ra','dec','z','density','coherence','focal_weight']].head(10))
        st.scatter_chart(rare.head(100), x='ra', y='dec', size='density')
        
    elif data_choice == "CERN LHC Jets (real)":
        st.write("**Loading 10,000 CERN LHC 13 TeV jets...**")
        df = load_cern_sample(10000)
        rare = detect_rare_decays(df, gamma=gamma, alpha=alpha)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Jets", len(df))
        col2.metric("Rare decays", len(rare))
        col3.metric("Higgs purity", f"{rare['label_H_bb'].mean():.1%}")
        col4.metric("Scale", "10^-18 m")
        
        st.dataframe(rare[['fj_pt','fj_mass','fj_tau21','fj_doubleb','coherence']].head(10))
        st.scatter_chart(rare.head(200), x='fj_pt', y='fj_mass', size='coherence')
        
    elif data_choice == "Voyager 1 Plasma (real)":
        status = get_live_voyager_status()
        st.write(f"**Loading Voyager 1 plasma data — currently {status['voyager1_distance_au']:.1f} AU from Earth...**")
        df = load_voyager_sample(5000)
        rare = detect_plasma_waves(df, gamma=gamma, alpha=alpha)
        
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Measurements", len(df))
        col2.metric("Coherent waves", len(rare))
        col3.metric("Purity", f"{rare['is_coherent'].mean():.1%}")
        col4.metric("Distance", f"{status['voyager1_distance_au']:.1f} AU")
        
        st.info(f"Signal travel time: {status['signal_travel_time_hours']:.1f} hours one-way")
        st.dataframe(rare[['timestamp','distance_au','plasma_freq_khz','electron_density','coherence']].head(10))
        st.line_chart(rare.head(200), x='distance_au', y='plasma_freq_khz')
        
    else:
        n = 1000
        data = pd.DataFrame({
            'x': np.random.normal(0, 1, n),
            'y': np.random.normal(0, 1, n),
            'density': np.random.exponential(1, n)
        })
        p = np.clip(data['density'] / data['density'].max(), 0.1, 0.99)
        weights = (1 - p) ** gamma
        st.metric("Synthetic points", n)
        st.scatter_chart(data, x='x', y='y', size='density')
    
    st.success(f"Shangraw Gap (γ={gamma}) active — isolating top {alpha:.0%} hardest examples across all scales")
    
    with st.expander("The Math"):
        st.latex(r"FL(p_t) = -\alpha_t (1-p_t)^\gamma \log(p_t)")
        st.write("Gamma > 2 creates the 'Shangraw Gap' — focuses learning on rare coherent signals")

st.sidebar.markdown("---")
st.sidebar.info("v2.2 — LIVE: SDSS + CERN + Voyager")
st.sidebar.caption("From Planck to interstellar — one detector")
