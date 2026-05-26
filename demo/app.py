import streamlit as st
import pandas as pd
import numpy as np
import requests
from data_sdss import load_sdss_sample
from data_cern import load_cern_higgs
from data_voyager import get_voyager_status

st.set_page_config(page_title="CosmoAi v2.9.2", layout="wide")

st.caption("🛰 446 clones and counting. Built on a phone in Kingston.")

st.markdown("""
<style>
.stApp { background-color: #000000; }
.main { background-color: #000000; }
  footer {visibility: hidden;}
  header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

st.title("🛰 CosmoAi - Live Space Data")
st.caption("v2.9.2 • Global Sky Tracker • Kingston, ON")

tab1, tab2, tab3, tab4, tab5 = st.tabs(["🛰 SDSS", "⚛️ CERN", "🚀 Voyager", "🔍 Shangraw Gap", "🌍 Live Sky"])

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

    df = load_sdss_sample(500)
    zs = np.sort(df["z"].values)
    diffs = np.diff(zs)
    threshold = np.median(diffs) * 5.0
    gaps = np.where(diffs > threshold)[0]

    plot_df = pd.DataFrame({"redshift": zs, "galaxies": np.random.rand(len(zs))*0.1})
    st.scatter_chart(plot_df, x="redshift", y="galaxies", height=300)

    st.metric("Gaps detected", len(gaps), f"threshold {threshold:.4f}")
    if len(gaps):
        st.write("Top gaps (z ranges):")
        for i in gaps[:8]:
            st.code(f"{zs[i]:.4f} → {zs[i+1]:.4f} (Δ={diffs[i]:.4f})")

with tab5:
    st.subheader("🌍 Live Sky — Anywhere on Earth")

    cities = {
        "Kingston, ON": (44.23, -76.48),
        "Toronto, ON": (43.65, -79.38),
        "New York, NY": (40.71, -74.01),
        "London, UK": (51.51, -0.13),
        "Tokyo, JP": (35.68, 139.69),
        "Sydney, AU": (-33.87, 151.21),
        "São Paulo, BR": (-23.55, -46.63),
        "Cairo, EG": (30.04, 31.24),
        "Reykjavik, IS": (64.14, -21.90),
        "Cape Town, ZA": (-33.92, 18.42),
        "Mumbai, IN": (19.07, 72.88),
        "Los Angeles, CA": (34.05, -118.24)
    }

    location = st.selectbox("Choose your city", list(cities.keys()), index=0)
    lat, lon = cities[location]
    st.caption(f"Lat {lat}°, Lon {lon}° • Built on a phone")

    # Live ISS position
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        iss_lat = float(iss["iss_position"]["latitude"])
        iss_lon = float(iss["iss_position"]["longitude"])

        st.metric("ISS is currently over", f"{iss_lat:.2f}°, {iss_lon:.2f}°")

        # World map
        map_df = pd.DataFrame({
            "lat": [lat, iss_lat],
            "lon": [lon, iss_lon],
            "location": [location, "ISS"]
        })
        st.map(map_df, zoom=1)

    except:
        st.warning("ISS tracker offline — showing your sky only")
        st.map(pd.DataFrame({"lat": [lat], "lon": [lon]}), zoom=3)

    df_sky = load_sdss_sample(100)
    st.dataframe(df_sky.head(30), use_container_width=True)
    st.write(f"SDSS sample for {location} sky region")
