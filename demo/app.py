import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

st.set_page_config(page_title="CosmoAi", page_icon="🛰", layout="wide")
st.title("🛰 CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

tab = st.sidebar.radio("Navigate", ["SDSS", "CERN", "Voyager", "Shangraw Gap", "Live Sky — Global", "Sandbox — Play Lab"])

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

elif tab == "Live Sky — Global":
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

else: # SANDBOX
    st.header("🧪 Sandbox — Play Lab")
    st.caption("Mix light, gamma, waves. See what you get.")

    col1, col2 = st.columns(2)

    with col1:
        st.subheader("🌈 Light Mixer")
        r = st.slider("Red", 0, 255, 120)
        g = st.slider("Green", 0, 255, 80)
        b = st.slider("Blue", 0, 255, 200)
        uv = st.slider("UV", 0, 100, 20)
        ir = st.slider("Infrared", 0, 100, 30)
        gamma = st.slider("Gamma", 0, 100, 10)

    with col2:
        st.subheader("Your Creation")
        # Color preview
        color = f"rgb({r},{g},{b})"
        st.markdown(f"<div style='width:100%;height:150px;background:{color};border-radius:10px;'></div>", unsafe_allow_html=True)
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        st.code(f"HEX: {hex_code}")

        if st.button("🎲 Mix & Match Random"):
            st.rerun()

    st.subheader("📊 Spectrum Meter")
    wavelengths = ['IR', 'Red', 'Green', 'Blue', 'UV', 'Gamma']
    intensities = [ir, r/2.55, g/2.55, b/2.55, uv, gamma]
    spec_df = pd.DataFrame({'Wavelength': wavelengths, 'Intensity': intensities})
    st.bar_chart(spec_df.set_index('Wavelength'))

    st.subheader("🧠 Theta Waves (4-8 Hz)")
    theta = st.slider("Theta Frequency", 4.0, 8.0, 6.0, 0.1)
    t = np.linspace(0, 2, 500)
    wave = np.sin(2 * np.pi * theta * t) * (gamma/50)
    wave_df = pd.DataFrame({'time': t, 'amplitude': wave})
    st.line_chart(wave_df.set_index('time'))
    st.caption(f"Brainwave at {theta} Hz • Gamma boost: {gamma}%")

    st.subheader("✨ Full Spectrum")
    total_energy = sum(intensities)
    st.metric("Total Energy", f"{total_energy:.1f} units")
    if total_energy > 400:
        st.success("🔥 HIGH ENERGY CREATION!")
    elif total_energy > 200:
        st.info("⚡ Medium energy mix")
    else:
        st.write("🌙 Low energy — calm waves")
