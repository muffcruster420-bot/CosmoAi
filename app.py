import streamlit as st
import sys, os

# make src/ importable
sys.path.append(os.path.join(os.path.dirname(__file__), '..', 'src'))
from trainer_focal import FocalLossV2, quick_demo

st.set_page_config(page_title="CosmoAi Detector", layout="centered")
st.title("CosmoAi: FocalLossV2 Detector")
st.caption("by Jesse Shangraw · Kingston, Ontario")

st.write("Test the focal-loss substitute you committed. Adjust gamma/alpha to trade precision for recall.")

gamma = st.slider("Gamma (focus on hard examples)", 0.5, 3.0, 1.5, 0.1)
alpha = st.slider("Alpha (positive weight)", 0.25, 0.95, 0.75, 0.05)
thresh = st.slider("Decision threshold", 0.2, 0.8, 0.45, 0.05)

if st.button("Run quick demo"):
    with st.spinner("Training synthetic dark-matter set..."):
        result = quick_demo(gamma=gamma, alpha=alpha, thresh=thresh)
    
    st.success(f"Precision: {result['precision']:.3f}  |  Recall: {result['recall']:.3f}  |  F1: {result['f1']:.3f}")
    st.json(result)

st.markdown("---")
st.markdown("Uses `src/trainer_focal.py` — the file you just shipped. No API keys, runs locally with `streamlit run demo/app.py`")
