import streamlit as st
import pandas as pd
import numpy as np
from data_sdss import load_sdss_sample
from data_cern import load_cern_higgs
from data_voyager import get_voyager_status

st.set_page_config(page_title="CosmoAi v2.7", layout="wide")
st.title("🛰️ CosmoAi – Live Space Data")
st.caption("v2.7 • Shangraw Gap Detector • Kingston, ON")

tab1, tab2, tab3, tab4 = st.tabs(["🌌 SDSS", "⚛️ CERN", "🚀 Voyager", "🔍 Shangraw Gap"])

with tab1:
    st.dataframe(load_sdss_sample().head(50), use_container_width=True)

with tab2:
    higgs = load_cern_higgs()
    st.line_chart(higgs, x="mass_GeV", y="events", use_container_width=True)

with tab3:
    v = get_voyager_status()
    c1, c2 = st.columns(2)
    c1.metric("Voyager 1", f"{v['voyager1']['distance_au']:.2f} AU")
    c2.metric("Voyager 2", f"{v['voyager2']['distance_au']:.2f} AU")

with tab4:
    st.subheader("Shangraw Gap Detector — LIVE")
    if st.button("🔄 Refresh sky"):
        st.rerun()

    df = load_sdss_sample(2000)
    zs = np.sort(df["z"].values)
    diffs = np.diff(zs)
    threshold = np.median(diffs) * 2.5
    gaps = np.where(diffs > threshold)[0]

    plot_df = pd.DataFrame({"redshift": zs, "galaxies": np.random.rand(len(zs))*0.1})
    st.scatter_chart(plot_df, x="redshift", y="galaxies", height=300)

    st.metric("Gaps detected", len(gaps), f"threshold {threshold:.4f}")
    if len(gaps):
        st.write("Top gaps (z ranges):")
        for i in gaps[:8]:
            st.code(f"{zs[i]:.4f} → {zs[i+1]:.4f} (Δ={diffs[i]:.4f})")
