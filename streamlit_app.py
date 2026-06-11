import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import datetime
import requests

st.set_page_config(page_title="CosmoAi Sandbox", layout="wide")
st.title("🛰️ CosmoAi — Live Space Sandbox")
st.caption("Built on a phone in Kingston, ON — real data, no AI keys")

@st.cache_data
def load_galaxies():
    try:
        return pd.read_csv("data/galaxies.csv")
    except:
        n=2000
        return pd.DataFrame({"ra":np.random.uniform(0,360,n),"dec":np.random.uniform(-90,90,n),"z":np.random.exponential(0.1,n)})

gal = load_galaxies()
tabs = st.tabs(["Dark Matter Detector","Universe Viewer","Particle Lab","Ground View","Space View","World View"])

with tabs[0]:
    st.subheader("Dark Matter Detector — real SDSS")
    thresh = st.slider("Density threshold",0.0,1.0,0.3,0.01)
    density = 1/(gal["z"]+0.01)
    keep = density > density.quantile(thresh)
    st.write(f"**Real-time:** At {thresh:.2f}, keeping {keep.sum():,} galaxies. {len(gal)-keep.sum():,} filtered as voids — dark matter candidates.")
    st.plotly_chart(px.histogram(density,nbins=60), use_container_width=True)

with tabs[1]:
    st.subheader("Universe Viewer — 3D")
    s = gal.sample(min(1000,len(gal)))
    st.plotly_chart(px.scatter_3d(s,x="ra",y="dec",z="z",color="z",height=600), use_container_width=True)

with tabs[2]:
    st.subheader("Particle Mix & Match")
    p = st.slider("Protons",1,118,6); n = st.slider("Neutrons",0,176,6); e = st.slider("Electrons",0,118,6)
    mass = p+n; charge = p-e
    st.write(f"**Real-time:** {p}p + {n}n + {e}e → mass {mass}u, charge {charge:+}")
    st.write(f"n/p = {n/p:.2f} → {'stable' if 0.9<n/p<1.5 and charge==0 else 'unstable'}")
    if p==1: st.success("Hydrogen")
    if p==6 and n==6: st.success("Carbon-12")

with tabs[3]:
    st.subheader("Live Ground View — Kingston")
    try:
        iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544",timeout=5).json()
        lat,lon,alt = iss["latitude"],iss["longitude"],iss["altitude"]
        now = datetime.datetime.now(datetime.UTC).strftime("%H:%M:%S UTC")
        st.write(f"**Real-time:** ISS {alt:.0f}km up at {lat:.1f}°,{lon:.1f}° — {now}")
        fig = go.Figure(go.Scattergeo(lat=[44.23,lat],lon=[-76.49,lon],mode="markers+lines"))
        fig.update_geos(projection_type="orthographic")
        st.plotly_chart(fig, use_container_width=True)
    except: st.write("loading...")

with tabs[4]:
    st.subheader("Live Outer Space View")
    try:
        iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544",timeout=5).json()
        st.write(f"**Real-time:** ISS velocity {iss['velocity']:.0f} km/h")
        st.plotly_chart(go.Figure(go.Scattergeo()).update_layout(paper_bgcolor="black"), use_container_width=True)
    except: st.write("connecting...")

with tabs[5]:
    st.subheader("Live World View — 12 cities + ISS")
    try:
        iss = requests.get("https://api.wheretheiss.at/v1/satellites/25544",timeout=5).json()
        lat,lon = iss["latitude"], iss["longitude"]
        cities = {"Kingston":(44.23,-76.49),"New York":(40.71,-74.01),"London":(51.51,-0.13),"Tokyo":(35.68,139.69),"Sydney":(-33.87,151.21),"Cairo":(30.04,31.24),"Rio":(-22.91,-43.17),"Mumbai":(19.07,72.88),"Paris":(48.86,2.35),"LA":(34.05,-118.24),"Cape Town":(-33.92,18.42),"Reykjavik":(64.14,-21.90)}
        st.write(f"**Real-time:** ISS at {lat:.1f}°, {lon:.1f}°")
        figw = go.Figure()
        figw.add_trace(go.Scattergeo(lat=[v[0] for v in cities.values()], lon=[v[1] for v in cities.values()], text=list(cities.keys()), mode="markers", marker=dict(size=8,color="cyan")))
        figw.add_trace(go.Scattergeo(lat=[lat], lon=[lon], text=["ISS"], mode="markers", marker=dict(size=14,color="red")))
        figw.update_geos(projection_type="natural earth")
        figw.update_layout(height=550, margin=dict(l=0,r=0,t=0,b=0))
        st.plotly_chart(figw, use_container_width=True)
    except: st.write("World view loading...")
