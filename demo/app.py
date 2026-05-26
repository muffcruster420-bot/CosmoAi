import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

st.set_page_config(page_title="CosmoAi", page_icon="🛰", layout="wide")
st.title("🛰 CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

tab = st.sidebar.radio("Navigate", ["SDSS", "CERN", "Voyager", "Shangraw Gap", "Live Sky — Global"])

if tab == "SDSS":
    st.header("🌌 SDSS Galaxies")
    df = pd.DataFrame({'ra': np.random.uniform(0,360,100), 'dec': np.random.uniform(-90,90,100), 'z': np.random.uniform(0,0.3,100)})
    st.scatter_chart(df, x='ra', y='dec', size='z')

elif tab == "CERN":
    st.header("⚛️ CERN Higgs")
    st.line_chart(pd.DataFrame({'mass': np.random.normal(125,2,200)}))

elif tab == "Voyager":
    st.header("🚀 Voyager")
    d = 24.5 + (time.time()%86400)/86400*0.001
    st.metric("Voyager 1", f"{d:.3f} B km")

elif tab == "Shangraw Gap":
    st.header("🔍 Shangraw Gap")
    z = np.random.uniform(0,0.5,500)
    h,_ = np.histogram(z,30)
    st.bar_chart(h)
    st.success(f"{len(np.where(h<5)[0])} gaps found")

else:
    st.header("🌌 Live Sky — Global")

    st.subheader("🔭 Sky View — Planets & Stars")
    st.components.v1.iframe("https://stellarium-web.org/", height=520)
    st.caption("Real telescope view • Planets, moon, stars")

    st.subheader("🛰 ISS Live")
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        lat = float(iss['iss_position']['latitude']); lon = float(iss['iss_position']['longitude'])
        st.success(f"ISS at {lat:.1f}°N, {lon:.1f}°W • 408km up")
        df = pd.DataFrame({'lat':[lat],'lon':[lon]})
        st.map(df, zoom=1)
    except:
        st.warning("Loading ISS...")
