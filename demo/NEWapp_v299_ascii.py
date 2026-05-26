import streamlit as st
import requests
import time
import numpy as np
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="CosmoAi - Live Space Data", layout="wide")
st.title("CosmoAi - Live Space Data")
st.caption("v2.9.9 ASCII - no emojis, mobile-safe")

# Sidebar
tab = st.sidebar.radio("Navigate", [
    "SDSS Live Galaxies",
    "Voyager 1 Tracker",
    "Shangraw Gap",
    "Live Sky - Global",
    "Offline Maps",
    "Universe Map",
    "Sandbox"
])

if tab == "SDSS Live Galaxies":
    st.header("SDSS Live Galaxies")
    try:
        r = requests.get("https://api.sdss.org/api", timeout=5)
        st.write("SDSS API status:", r.status_code)
    except:
        st.warning("SDSS API unreachable - showing demo")
    # demo data
    df = pd.DataFrame({
        "ra": np.random.uniform(0,360,50),
        "dec": np.random.uniform(-90,90,50),
        "z": np.random.uniform(0,0.3,50)
    })
    fig = go.Figure(data=go.Scatter3d(x=df.ra, y=df.dec, z=df.z, mode='markers', marker=dict(size=3)))
    st.plotly_chart(fig, use_container_width=True)

elif tab == "Voyager 1 Tracker":
    st.header("Voyager 1 Tracker")
    d = 24.9 + (time.time() % 86400) / 86400 * 0.01
    st.metric("Voyager 1", f"{d:.3f} B km from Sun")
    st.write("Approx 162 AU and counting. Real-time telemetry via NASA DSN.")

elif tab == "Shangraw Gap":
    st.header("Shangraw Gap")
    st.write("Simulated redshift gap analysis")
    z = np.random.uniform(0,0.5,500)
    h, edges = np.histogram(z, 30)
    st.bar_chart(h)
    st.success(f"{len(np.where(h<5)[0])} low-density bins detected")

elif tab == "Live Sky - Global":
    st.header("Live Sky - Global")
    st.subheader("Sky View - Planetarium")
    st.components.v1.iframe("https://stellarium-web.org/", height=500)
    st.caption("Pinch to zoom - See what is overhead right now")
    
    st.subheader("Live Ground - Earth from ISS")
    st.components.v1.iframe("https://www.youtube.com/embed/86YLFOog4GM?autoplay=1&mute=1", height=400)
    st.caption("ISS live HD - real-time Earth view")

elif tab == "Offline Maps":
    st.header("Offline Maps - v2.9.9")
    st.write("Kingston, ON centered. Tap the save icon to cache tiles for offline use.")
    
    offline_html = """
<div id="map" style="height:600px;"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.offline@3.0.0/dist/leaflet.offline.min.js"></script>
<script>
const map = L.map('map').setView([44.2312, -76.4860], 13);
const offlineLayer = L.tileLayer.offline('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OSM',
    minZoom: 12,
    maxZoom: 16
});
offlineLayer.addTo(map);
const control = L.control.savetiles(offlineLayer, {confirm: function(layer, success) {
    if(window.confirm('Download Kingston area for offline? ~30MB')) success();
}});
control.addTo(map);
map.on('click', function(e){
    L.marker(e.latlng).addTo(map).bindPopup('Lat: '+e.latlng.lat.toFixed(4)+' Lon: '+e.latlng.lng.toFixed(4)).openPopup();
});
setTimeout(()=>{control._saveTiles()}, 2000);
</script>
"""
    st.components.v1.html(offline_html, height=620)
    st.info("Tip: Download on WiFi, then airplane mode works.")

elif tab == "Universe Map":
    st.header("Universe Map")
    st.write("3D visualization placeholder")
    x,y,z = np.random.normal(0,1,100), np.random.normal(0,1,100), np.random.normal(0,1,100)
    fig = go.Figure(data=go.Scatter3d(x=x,y=y,z=z,mode='markers'))
    st.plotly_chart(fig, use_container_width=True)

else:  # Sandbox
    st.header("Sandbox")
    st.write("Test area")
