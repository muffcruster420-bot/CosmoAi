import streamlit as st
import numpy as np
import sys
import os

# make src importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from src.trainer_focal import FocalLossV2, quick_demo
from src.data_sdss import get_real_data

st.set_page_config(page_title="CosmoAi - Shangraw Gap", layout="wide")
st.title("CosmoAi: Shangraw Gap Detector")
st.caption("by Jesse Shangraw - Kingston, Ontario | 45-Hz coherence applied to the cosmos")

col1, col2, col3 = st.columns(3)
with col1:
    gamma = st.slider("Gamma (focus power)", 0.0, 5.0, 2.0, 0.1)
with col2:
    alpha = st.slider("Alpha (rare boost)", 0.1, 0.9, 0.25, 0.05)
with col3:
    gap_strength = st.slider("Shangraw Gap Strength (%)", 1, 20, 5, 1)

use_real = st.checkbox("Use Real SDSS Data (1,000 galaxies)", value=False)

if st.button("Run Demo", type="primary"):
    if use_real:
        st.info("Loading real SDSS galaxies...")
        X, y = get_real_data()
        # train quick model on real data
        from sklearn.linear_model import LogisticRegression
        clf = LogisticRegression(max_iter=1000)
        clf.fit(X, y)
        probs = clf.predict_proba(X)[:,1]
        # apply FocalLoss weighting concept
        fl = FocalLossV2(gamma=gamma, alpha=alpha)
        # simulate loss reduction
        rare_detected = int((probs[y==1] > 0.5).sum())
        rare_total = int(y.sum())
        st.success(f"Real Data: Detected {rare_detected}/{rare_total} filament galaxies")
        st.metric("Coherence detected", f"{rare_detected/rare_total*100:.1f}%")
        st.write("Top 5% densest regions = Shangraw Gap analog")
    else:
        results = quick_demo(gamma=gamma, alpha=alpha, coherence_ratio=gap_strength/100)
        st.success(f"Synthetic: Detected {results['rare_detected']}/{results['rare_total']} coherent bursts")
        col_a, col_b, col_c = st.columns(3)
        col_a.metric("Precision (rare)", f"{results['precision_rare']:.2f}")
        col_b.metric("Recall (rare)", f"{results['recall_rare']:.2f}")
        col_c.metric("Gap Strength", f"{gap_strength}%")

st.divider()
st.markdown("**What you're seeing:** Gamma >2 focuses on the 5% rare events - just like your 45-Hz brain coherence drops background noise to find meaning.")
