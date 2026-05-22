import streamlit as st
import numpy as np
import pandas as pd
import sys
from pathlib import Path

# add repo root and src to path
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
sys.path.insert(0, str(ROOT / "src"))

from data_sdss import load_sdss_sample
from data_cern import load_cern_higgs
from data_voyager import get_voyager_status

st.set_page_config(page_title="CosmoAi v2.2", layout="wide")
st.title("🌌 CosmoAi — Live Space Data")
st.caption("v2.2 • CERN Open Data + NASA Voyager • Kingston, ON")

tab1, tab2, tab3 = st.tabs(["🛰️ SDSS Galaxies", "⚛️ CERN Higgs", "🚀 Voyager 1 & 2"])

with tab1:
    df = load_sdss_sample()
    st.dataframe(df.head(50), use_container_width=True)

with tab2:
    higgs = load_cern_higgs()
    st.line_chart(higgs, use_container_width=True)

with tab3:
    v1, v2 = get_voyager_status()
    c1, c2 = st.columns(2)
    c1.metric("Voyager 1", f"{v1['distance_au']:.2f} AU", f"{v1['velocity_kms']:.1f} km/s")
    c2.metric("Voyager 2", f"{v2['distance_au']:.2f} AU", f"{v2['velocity_kms']:.1f} km/s")
    st.json({"voyager_1": v1, "voyager_2": v2})
