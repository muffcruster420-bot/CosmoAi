import streamlit as st
import requests
import plotly.graph_objects as go
import io
from datetime import datetime

st.set_page_config(page_title="CosmoAi - Live Space Data", layout="wide")
st.title("🛰️ CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

st.subheader("Live ISS Tracker")
try:
    r = requests.get("http://api.open-notify.org/iss-now.json", timeout=10)
    data = r.json()
    lat = float(data["iss_position"]["latitude"])
    lon = float(data["iss_position"]["longitude"])
    timestamp = datetime.utcfromtimestamp(data["timestamp"]).strftime("%H:%M:%S UTC")

    fig = go.Figure(go.Scattergeo(lon=[lon], lat=[lat], mode="markers+text",
        marker=dict(size=12, color="red"), text=["ISS"], textposition="top center"))
    fig.update_geos(projection_type="natural earth", showland=True)
    fig.update_layout(height=500, margin=dict(l=0,r=0,t=0,b=0), paper_bgcolor="black")

    st.plotly_chart(fig, use_container_width=True)
    buf = io.BytesIO()
    fig.write_image(buf, format="png", scale=2)
    st.download_button("💾 Download this map as PNG", buf.getvalue(),
                       f"cosmoai_iss_{timestamp}.png", "image/png")
    st.success(f"ISS: {lat:.2f}°, {lon:.2f}° at {timestamp}")
except Exception as e:
    st.error(f"Could not load ISS: {e}")
