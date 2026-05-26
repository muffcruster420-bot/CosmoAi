import streamlit as st
import numpy as np
import plotly.graph_objects as go
import math

st.set_page_config(page_title="CosmoAi - Live Space Data", layout="wide")
st.title("CosmoAi - Live Space Data")
st.caption("v2.9.9 ASCII - no emojis, mobile-safe")

page = st.sidebar.selectbox("Navigation", [
    "Live Tracker",
    "Live Sky - Global",
    "Offline Maps",
    "Universe Map",
    "Sandbox"
])

if page == "Live Tracker":
    st.header("Live Tracker")
    st.write("SDSS galaxies and Voyager data placeholder")
    st.metric("ISS Altitude", "435 km")
    st.metric("ISS Speed", "27,547 km/h")
    st.metric("Orbits Completed", "143,923")

elif page == "Live Sky - Global":
    st.header("Live Sky - Global")
    st.subheader("Sky View - Planetarium")
    st.components.v1.iframe("https://stellarium-web.org/", height=500)
    st.caption("Pinch to zoom - See what is overhead right now")
    
    st.subheader("Live Ground - Earth from ISS")
    st.components.v1.iframe("https://www.youtube.com/embed/8LX7DnMpIIE?autoplay=1&mute=1", height=500)
    st.caption("ISS live HD - real-time Earth view")

elif page == "Offline Maps":
    st.header("Offline Maps - v2.9.9")
    st.write("Kingston, ON centered. Tap the save icon to cache tiles for offline use.")
    
    offline_html = """
<div id="map" style="height:600px;"></div>
<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
<script src="https://unpkg.com/leaflet.offline@3.0.0/dist/leaflet.offline.min.js"></script>
<script>
var map = L.map('map').setView([44.2312, -76.4860], 13);
var offlineLayer = L.tileLayer.offline('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    attribution: 'OSM',
    minZoom: 12,
    maxZoom: 16
});
offlineLayer.addTo(map);
var control = L.control.savetiles(offlineLayer, {confirm: function(layer, success) {
    if(window.confirm('Download Kingston area for offline? ~30MB')) success();
}});
control.addTo(map);
map.on('click', function(e){
    L.marker(e.latlng).addTo(map).bindPopup('Lat: '+e.latlng.lat.toFixed(4)+' Lon: '+e.latlng.lng.toFixed(4)).openPopup();
});
</script>
"""
    st.components.v1.html(offline_html, height=620)
    st.info("Tip: Download on WiFi, then airplane mode works.")

elif page == "Universe Map":
    st.header("Universe Map")
    st.write("3D visualization placeholder")
    x, y, z = np.random.normal(0,1,100), np.random.normal(0,1,100), np.random.normal(0,1,100)
    fig = go.Figure(data=go.Scatter3d(x=x, y=y, z=z, mode="markers"))
    st.plotly_chart(fig, use_container_width=True)

elif page == "Sandbox":
    st.header("Sandbox")
    tab1, tab2, tab3, tab4 = st.tabs(["AI Chat", "Orbit Sim", "What-If", "Phone Tools"])
    
    with tab1:
        st.subheader("CosmoAi Chat")
        prompt = st.text_input("Ask about space:", key="sb_chat")
        if prompt:
            st.write(f"**You:** {prompt}")
            st.write(f"**CosmoAi:** That's a great question about '{prompt}'. In v2.9.9, the ISS is at 435km, moving 27,547 km/h.")
    
    with tab2:
        st.subheader("Orbit Simulator")
        planet = st.selectbox("Planet", ["Earth", "Mars", "Jupiter", "Custom"])
        altitude = st.slider("Altitude (km)", 200, 40000, 435)
        mu_earth = 398600.4418
        v = math.sqrt(mu_earth/(6371+altitude))
        st.metric("Orbital velocity", f"{v:.2f} km/s")
        st.write(f"At {altitude}km around {planet}, you'd orbit every {2*math.pi*(6371+altitude)/v/60:.1f} minutes")
    
    with tab3:
        st.subheader("What-If Calculator")
        mass = st.number_input("Spacecraft mass (kg)", 1000, 100000, 5000)
        thrust = st.number_input("Thrust (N)", 100, 1000000, 50000)
        accel = thrust/mass
        st.write(f"Acceleration: {accel:.2f} m/s² ({accel/9.81:.2f} g)")
    
    with tab4:
        st.subheader("Phone Tools")
        st.write("These open your native apps - works with cellular:")
        phone = st.text_input("Number", "613-555-0100")
        st.markdown(f"[Call {phone}](tel:{phone})")
        st.markdown(f"[Text {phone}](sms:{phone}?body=From CosmoAi: )")
        st.caption("Note: Streamlit page needs internet to load, but call/text uses cell towers.")
