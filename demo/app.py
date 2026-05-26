import streamlit as st
import requests
import plotly.graph_objects as go
from datetime import datetime

st.set_page_config(page_title="CosmoAi - Live Space Data", layout="wide")
st.title("🛰️ CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

st.subheader("Live ISS Tracker")

# try two APIs, use https
apis = [
    "https://api.open-notify.org/iss-now.json",
    "https://api.wheretheiss.at/v1/satellites/25544"
]

lat = lon = None
source = ""

for url in apis:
    try:
        r = requests.get(url, timeout=8)
        data = r.json()
        if "iss_position" in data: # open-notify format
            lat = float(data["iss_position"]["latitude"])
            lon = float(data["iss_position"]["longitude"])
            source = "open-notify"
        else: # wheretheiss format
            lat = float(data["latitude"])
            lon = float(data["longitude"])
            source = "wheretheiss"
        break
    except:
        continue

if lat and lon:
    fig = go.Figure(go.Scattergeo(lon=[lon], lat=[lat], mode="markers+text",
        marker=dict(size=12, color="red"), text=["ISS"], textposition="top center"))
    fig.update_geos(projection_type="natural earth", showland=True, landcolor="#E0C987")
    fig.update_layout(height=520, margin=dict(l=0,r=0,t=20,b=0), paper_bgcolor="#0E1117", font_color="white")

    st.plotly_chart(fig, use_container_width=True)
    st.success(f"ISS: {lat:.2f}°, {lon:.2f}° — source: {source} at {datetime.utcnow().strftime('%H:%M:%S UTC')}")
    st.caption("Tip: use the camera icon top-right of the map to save PNG — no extra install needed.")
else:
    st.error("Both ISS APIs are down right now. Refresh in 30 seconds — your app is fine, the data feed is just busy.")
