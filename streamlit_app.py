import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import requests
from datetime import datetime, timezone
import pathlib

st.set_page_config(page_title="CosmoAi", layout="wide")
st.title("🛰 CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

# Show README at top
readme = pathlib.Path("README.md").read_text() if pathlib.Path("README.md").exists() else ""
with st.expander("About v2.9.2", expanded=False):
    st.markdown(readme)

tabs = st.tabs(["SDSS", "CERN", "Voyager", "Shangraw Gap", "Live Sky — Global"])

# --- SDSS ---
with tabs[0]:
    st.subheader("Sloan Digital Sky Survey — sample galaxies")
    # mock SDSS data (replace with data_sdss.py if you have it)
    np.random.seed(42)
    df = pd.DataFrame({
        "ra": np.random.uniform(0,360,200),
        "dec": np.random.uniform(-30,90,200),
        "z": np.random.normal(0.1,0.05,200).clip(0,0.3),
        "mag": np.random.normal(18,1.5,200)
    })
    fig = px.scatter(df, x="ra", y="dec", color="z", size="mag",
                     color_continuous_scale="Turbo", title="200 galaxies (redshift = color)")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(df.head(10))

# --- CERN ---
with tabs[1]:
    st.subheader("CERN — Higgs boson events")
    # simulate Higgs peak at 125 GeV
    data = np.concatenate([np.random.normal(125,2,800), np.random.normal(90,15,400)])
    fig = px.histogram(data, nbins=60, title="Di-photon invariant mass (GeV)")
    fig.add_vline(x=125, line_dash="dash", annotation_text="Higgs ~125 GeV")
    st.plotly_chart(fig, use_container_width=True)

# --- Voyager ---
with tabs[2]:
    st.subheader("Voyager telemetry — real-time distance")
    launch = datetime(1977,9,5, tzinfo=timezone.utc)
    now = datetime.now(timezone.utc)
    days = (now - launch).days
    v1_km = 24_900_000_000 + days*1_500_000 # rough
    v2_km = 20_800_000_000 + days*1_300_000
    col1,col2 = st.columns(2)
    col1.metric("Voyager 1", f"{v1_km/1e9:.2f} billion km", f"{v1_km*0.621371/1e9:.2f} B mi")
    col2.metric("Voyager 2", f"{v2_km/1e9:.2f} billion km", f"{v2_km*0.621371/1e9:.2f} B mi")
    st.caption(f"Updated {now.strftime('%Y-%m-%d %H:%M UTC')}")

# --- Shangraw Gap Detector ---
with tabs[3]:
    st.subheader("Shangraw Gap Detector — LIVE")
    z_sorted = np.sort(df["z"].values)
    gaps = np.diff(z_sorted)
    gap_idx = np.argmax(gaps)
    st.write(f"Largest redshift gap: **{gaps[gap_idx]:.4f}** between z={z_sorted[gap_idx]:.3f} and z={z_sorted[gap_idx+1]:.3f}")
    fig = px.line(x=z_sorted, y=gaps, markers=True, title="Redshift gaps")
    st.plotly_chart(fig, use_container_width=True)

# --- Live Sky ---
with tabs[4]:
    st.subheader("Live Sky — Global + ISS tracker")
    cities = {
        "Kingston, ON": (44.23,-76.48), "New York": (40.71,-74.01), "London": (51.5,-0.12),
        "Tokyo": (35.68,139.76), "Sydney": (-33.87,151.21), "Cairo": (30.04,31.24),
        "São Paulo": (-23.55,-46.64), "Cape Town": (-33.92,18.42), "Mumbai": (19.07,72.88),
        "Paris": (48.86,2.35), "Dubai": (25.27,55.29), "Reykjavik": (64.14,-21.9)
    }
    city_df = pd.DataFrame([{"city":k,"lat":v[0],"lon":v[1]} for k,v in cities.items()])
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        iss_lat = float(iss["iss_position"]["latitude"])
        iss_lon = float(iss["iss_position"]["longitude"])
        iss_df = pd.DataFrame([{"city":"ISS","lat":iss_lat,"lon":iss_lon}])
        st.success(f"ISS now: {iss_lat:.2f}°, {iss_lon:.2f}°")
    except:
        iss_df = pd.DataFrame()
        st.warning("ISS API offline")
    all_pts = pd.concat([city_df, iss_df])
    fig = px.scatter_geo(all_pts, lat="lat", lon="lon", text="city",
                         projection="natural earth", title="12 cities + live ISS")
    st.plotly_chart(fig, use_container_width=True)
    st.dataframe(city_df)
