import streamlit as st
import pandas as pd
import numpy as np

from data_sdss import load_sdss_sample
from data_cern import load_cern_higgs
from data_voyager import get_voyager_status

st.set_page_config(page_title="CosmoAi v2.2", layout="wide")
st.title("🛰️ CosmoAi – Live Space Data")
st.caption("v2.2 • CERN Open Data + NASA Voyager • Kingston, ON")

tab1, tab2, tab3 = st.tabs(["🌌 SDSS Galaxies", "⚛️ CERN Higgs", "🚀 Voyager 1 & 2"])

with tab1:
    df = load_sdss_sample()
    st.dataframe(df.head(50), use_container_width=True)

with tab2:
    higgs = load_cern_higgs()
    st.line_chart(higgs, x="mass_GeV", y="events", use_container_width=True)

with tab3:
    v = get_voyager_status()
    v1, v2 = v["voyager1"], v["voyager2"]
    c1, c2 = st.columns(2)
    c1.metric("Voyager 1", f"{v1['distance_au']:.2f} AU")
    c2.metric("Voyager 2", f"{v2['distance_au']:.2f} AU")
    st.json(v)
