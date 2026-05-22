import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import time

from data_sdss import load_sdss_sample
from data_cern import load_cern_higgs
from data_voyager import get_voyager_status

st.set_page_config(page_title="CosmoAi v2.5", layout="wide")
st.title("🛰️ CosmoAi – Live Space Data")
st.caption("v2.5 • Shangraw Gap Detector • Kingston, ON")

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
    live = st.toggle("Live mode", value=True, help="Updates every 3 seconds without flashing")

    # This is the fix: use a placeholder that updates, not full page reload
    placeholder = st.empty()

    # run once, then loop only if live
    for _ in range(1 if not live else 1000):
        with placeholder.container():
            np.random.seed(int(time.time() // 3))
            df = load_sdss_sample(2000)
            zs = np.sort(df["z"].values)
            diffs = np.diff(zs)
            threshold = np.median(diffs) * 2.5
            gap_idx = np.where(diffs > threshold)[0]

            fig = px.scatter(x=zs, y=np.zeros_like(zs),
                             title=f"Live Redshift — {time.strftime('%H:%M:%S')}",
                             labels={"x": "Redshift (z)", "y": ""})
            fig.update_traces(marker=dict(size=5, color="cyan"))
            fig.update_layout(height=380, yaxis=dict(visible=False), margin=dict(t=40,b=20))
            for i in gap_idx:
                fig.add_vrect(x0=zs[i], x1=zs[i+1], fillcolor="red", opacity=0.35, line_width=0)

            st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
            st.metric("Gaps detected right now", len(gap_idx), f"Δz > {threshold:.4f}")

        if not live:
            break
        time.sleep(3)
        st.rerun() # soft rerun, not full browser refresh
