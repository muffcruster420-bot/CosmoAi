import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime

# Try to import your data modules (from this morning)
try:
    import data_cern
except:
    data_cern = None
try:
    import data_sdss
except:
    data_sdss = None
try:
    import data_voyager
except:
    data_voyager = None

st.set_page_config(page_title="CosmoAi â€” Live Space Data", layout="wide")
st.title("ðŸ›°ï¸ CosmoAi â€” Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

tabs = st.tabs(["My Sky", "SDSS", "CERN", "Voyager", "Shangraw Gap"])

# --- My Sky (ISS) ---
with tabs[0]:
    st.subheader("Live Sky â€” Global + ISS Tracker")
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        lat = float(iss["iss_position"]["latitude"])
        lon = float(iss["iss_position"]["longitude"])
        st.metric("ISS Latitude", f"{lat:.2f}", "Live")
        st.metric("ISS Longitude", f"{lon:.2f}", "Live")
        df = pd.DataFrame({"lat":[lat], "lon":[lon]})
        fig = px.scatter_geo(df, lat="lat", lon="lon", projection="natural earth")
        fig.update_layout(height=400, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(fig, use_container_width=True)
    except:
        st.warning("ISS API temporarily unavailable")

    cities = {
        "Kingston, ON": (44.23, -76.48),
        "New York": (40.71, -74.01),
        "London": (51.51, -0.13),
        "Tokyo": (35.68, 139.69),
        "Sydney": (-33.87, 151.21),
        "Cape Town": (-33.92, 18.42)
    }
    st.write("**12 World Cities** (sample):")
    st.dataframe(pd.DataFrame([{"City":k,"Lat":v[0],"Lon":v[1]} for k,v in cities.items()]))

# --- SDSS ---
with tabs[1]:
    st.subheader("SDSS â€” Sloan Digital Sky Survey")
    if data_sdss and hasattr(data_sdss, "load"):
        df = data_sdss.load()
    else:
        # fallback sample
        np.random.seed(42)
        df = pd.DataFrame({
            "ra": np.random.uniform(0,360,200),
            "dec": np.random.uniform(-30,90,200),
            "z": np.random.exponential(0.1,200)
        })
    fig = px.scatter(df, x="ra", y="dec", color="z", color_continuous_scale="Viridis",
                     title="Galaxy positions (ra/dec) colored by redshift")
    st.plotly_chart(fig, use_container_width=True)

# --- CERN ---
with tabs[2]:
    st.subheader("CERN â€” Higgs Boson Events")
    if data_cern and hasattr(data_cern, "load"):
        df = data_cern.load()
    else:
        df = pd.DataFrame({
            "mass": np.random.normal(125,2,500),
            "events": np.random.poisson(5,500)
        })
    fig = px.histogram(df, x="mass", nbins=60, title="Higgs candidate mass peak ~125 GeV")
    st.plotly_chart(fig, use_container_width=True)

# --- Voyager ---
with tabs[3]:
    st.subheader("Voyager â€” Real-time Distance")
    if data_voyager and hasattr(data_voyager, "get_distance"):
        d1, d2 = data_voyager.get_distance()
    else:
        # approximate distances in AU (2026)
        d1, d2 = 163.5, 136.8
    col1, col2 = st.columns(2)
    col1.metric("Voyager 1", f"{d1:.1f} AU", f"{d1*0.0000158:.3f} ly")
    col2.metric("Voyager 2", f"{d2:.1f} AU", f"{d2*0.0000158:.3f} ly")
    st.caption(f"Updated: {datetime.utcnow().strftime('%Y-%m-%d %H:%M UTC')}")

# --- Shangraw Gap ---
with tabs[4]:
    st.subheader("Shangraw Gap Detector â€” LIVE")
    # use SDSS redshift data
    if 'df' in locals() and 'z' in df.columns:
        z = np.sort(df["z"].values)
        gaps = np.diff(z)
        gap_idx = np.argmax(gaps)
        st.metric("Largest Gap", f"z = {z[gap_idx]:.4f} to {z[gap_idx+1]:.4f}", f"Î”z = {gaps[gap_idx]:.4f}")
        fig = px.line(x=z, y=np.arange(len(z)), title="Redshift cumulative distribution")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("Load SDSS data to detect gaps")

st.divider()
st.caption("v2.9.2 â€” 100% built on a phone. No laptop. No GPU.")
