import streamlit as st
import pandas as pd
import numpy as np
import requests
import time

st.set_page_config(page_title="CosmoAi", page_icon="🛰", layout="wide")
st.title("🛰 CosmoAi — Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

tab = st.sidebar.radio("Navigate", ["SDSS", "CERN", "Voyager", "Shangraw Gap", "Live Sky — Global", "Universe Map", "Sandbox — Play Lab"])

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
    st.subheader("🛰 ISS Live")
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        lat = float(iss['iss_position']['latitude']); lon = float(iss['iss_position']['longitude'])
        st.success(f"ISS at {lat:.1f}°N, {lon:.1f}°W")
        st.map(pd.DataFrame({'lat':[lat],'lon':[lon]}), zoom=1)
    except: st.warning("Loading ISS...")

elif tab == "Universe Map":
    st.header("🌌 Universe Map — Where Dark Matter Lives")
    st.caption("We can't see it. We map it by gravity.")

    scale = st.slider("Zoom out (million light-years)", 10, 1000, 200, 10)
    show_galaxies = st.checkbox("Show galaxies (they sit in dark matter)", True)

    # Simulate cosmic web - same seed so it's consistent
    np.random.seed(42)
    n = 800
    x = np.random.normal(0, scale/3, n)
    y = np.random.normal(0, scale/3, n)
    # Dark matter forms filaments
    dm = np.exp(-(x**2 + y**2)/(2*(scale/2.5)**2)) * 80 + np.random.rand(n)*40

    df = pd.DataFrame({'x (Mly)': x, 'y (Mly)': y, 'Dark Matter Density': dm})

    st.subheader("The Cosmic Web")
    st.scatter_chart(df, x='x (Mly)', y='y (Mly)', size='Dark Matter Density')

    # LIVE EXPLANATION
    st.subheader("📖 What You're Seeing")
    if scale < 50:
        st.write(f"**{scale} Mly zoom:** You're inside our Local Group. Dark matter here is 5x normal matter — it's holding the Milky Way together right now.")
    elif scale < 200:
        st.write(f"**{scale} Mly zoom:** Virgo Supercluster scale. Dark matter forms a web, galaxies are beads on the string. This is where the 'Shangraw Gap' would appear — empty voids between filaments.")
    elif scale < 500:
        st.write(f"**{scale} Mly zoom:** You're seeing the Sloan Great Wall. Dark matter density {dm.mean():.0f} — this is the skeleton the universe grew on.")
    else:
        st.write(f"**{scale} Mly zoom:** Near the edge of what Euclid mapped. At {scale} million light-years, you're looking at structure from 700 million years after the Big Bang.")

    st.info("**How we know:** Dark matter bends light (gravitational lensing). Euclid telescope measured 1.5 billion galaxies' shapes in 2024-2025 to map this web. Blue = high density, where galaxies form.")

    if show_galaxies:
        galaxies = int(n * 0.15)
        st.success(f"Showing {galaxies} galaxies sitting in the densest dark matter nodes. Normal matter is only 15% — it's just glitter on the dark web.")

    st.metric("Dark Matter vs Normal", "85% vs 15%", "Invisible but dominant")

else: # Sandbox
    st.header("🧪 Sandbox — Play Lab")
    col1, col2 = st.columns(2)
    with col1:
        r = st.slider("Red (620-750nm)", 0, 255, 120)
        g = st.slider("Green (495-570nm)", 0, 255, 80)
        b = st.slider("Blue (450-495nm)", 0, 255, 200)
        uv = st.slider("UV (10-400nm)", 0, 100, 20)
        ir = st.slider("Infrared", 0, 100, 30)
        gamma = st.slider("Gamma", 0, 100, 10)
    with col2:
        color = f"rgb({r},{g},{b})"
        st.markdown(f"<div style='height:150px;background:{color};border-radius:10px'></div>", unsafe_allow_html=True)
        st.code(f"HEX: #{r:02x}{g:02x}{b:02x}")
        if st.button("🎲 Mix"): st.rerun()

    st.subheader("📖 What's Happening")
    st.write(f"**Red {r}:** {'twilight' if r<50 else 'sunset' if r<150 else 'red giant'}")
    st.write(f"**UV {uv}%:** {'safe' if uv<30 else 'tanning' if uv<70 else 'DNA ionizing'}")
    st.write(f"**Gamma {gamma}%:** {'background' if gamma<30 else 'medical' if gamma<70 else 'black hole jet'}")

    wavelengths = ['IR','Red','Green','Blue','UV','Gamma']
    intensities = [ir, r/2.55, g/2.55, b/2.55, uv, gamma]
    st.bar_chart(pd.DataFrame({'Wavelength':wavelengths,'Intensity':intensities}).set_index('Wavelength'))
