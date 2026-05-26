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

else:
    st.header("🧪 Sandbox — Play Lab")
    st.caption("Move a slider. Read what you're doing to the universe.")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🌈 Light Mixer")
        r = st.slider("Red (620-750nm)", 0, 255, 120)
        g = st.slider("Green (495-570nm)", 0, 255, 80)
        b = st.slider("Blue (450-495nm)", 0, 255, 200)
        uv = st.slider("UV (10-400nm)", 0, 100, 20)
        ir = st.slider("Infrared (700nm-1mm)", 0, 100, 30)
        gamma = st.slider("Gamma (<0.01nm)", 0, 100, 10)

    with col2:
        st.subheader("Your Creation")
        color = f"rgb({r},{g},{b})"
        st.markdown(f"<div style='width:100%;height:150px;background:{color};border-radius:10px;'></div>", unsafe_allow_html=True)
        hex_code = f"#{r:02x}{g:02x}{b:02x}"
        st.code(f"HEX: {hex_code}")
        if st.button("🎲 Mix & Match"): st.rerun()

    # --- LIVE EXPLANATIONS ---
    st.subheader("📖 What's Happening Right Now")

    # Red explanation
    if r < 50: red_txt = "Very low red — your mix is cool, like twilight."
    elif r < 150: red_txt = "Medium red — warm, like sunset."
    else: red_txt = "High red — intense heat energy, like a red giant star."
    st.write(f"**Red {r}/255:** {red_txt}")

    # Green explanation
    if g < 50: green_txt = "Low green — nature is muted."
    elif g < 150: green_txt = "Balanced green — human eyes see this best."
    else: green_txt = "High green — peak photosynthesis energy."
    st.write(f"**Green {g}/255:** {green_txt}")

    # Blue explanation
    if b < 50: blue_txt = "Low blue — calm, evening sky."
    elif b < 150: blue_txt = "Medium blue — daylight balance."
    else: blue_txt = "High blue — high energy, scatters in atmosphere (why sky is blue)."
    st.write(f"**Blue {b}/255:** {blue_txt}")

    # UV
    if uv > 70: st.warning(f"**UV {uv}%:** DANGER ZONE — this is sunburn/sterilization level. Real UV ionizes DNA.")
    elif uv > 30: st.info(f"**UV {uv}%:** Tanning level — triggers vitamin D.")
    else: st.write(f"**UV {uv}%:** Safe background level.")

    # IR
    if ir > 70: st.write(f"**Infrared {ir}%:** Heat vision mode — you’re making thermal radiation like a campfire.")
    else: st.write(f"**Infrared {ir}%:** Low heat — like warm skin.")

    # Gamma
    if gamma > 70: st.error(f"**Gamma {gamma}%:** EXTREME — this is CERN/black hole jet energy. Breaks atoms.")
    elif gamma > 30: st.warning(f"**Gamma {gamma}%:** Medical scan level — penetrates body.")
    else: st.write(f"**Gamma {gamma}%:** Background cosmic rays.")

    st.subheader("📊 Spectrum Meter")
    wavelengths = ['IR', 'Red', 'Green', 'Blue', 'UV', 'Gamma']
    intensities = [ir, r/2.55, g/2.55, b/2.55, uv, gamma]
    spec_df = pd.DataFrame({'Wavelength': wavelengths, 'Intensity': intensities})
    st.bar_chart(spec_df.set_index('Wavelength'))
    st.caption("Left = low energy/long waves (heat). Right = high energy/short waves (danger).")

    st.subheader("🧠 Theta Waves")
    theta = st.slider("Theta Frequency (4-8 Hz)", 4.0, 8.0, 6.0, 0.1)
    t = np.linspace(0, 2, 500)
    wave = np.sin(2 * np.pi * theta * t) * (1 + gamma/100)
    st.line_chart(pd.DataFrame({'time': t, 'wave': wave}).set_index('time'))

    if theta < 5: theta_txt = "4-5 Hz: Deep meditation, sleep, memory consolidation."
    elif theta < 6.5: theta_txt = "5-6.5 Hz: Creativity, daydreaming, 'flow state'."
    else: theta_txt = "6.5-8 Hz: Light meditation, learning, intuition."
    st.write(f"**Theta {theta} Hz:** {theta_txt}")
    st.write(f"Gamma boost is amplifying your wave by {gamma}% — in real brains, gamma + theta = insight moments.")

    total = sum(intensities)
    st.metric("Total Energy Output", f"{total:.0f} / 600")
    if total > 450: st.success("You're making quasar-level energy. Everything is ionized.")
    elif total > 300: st.info("Star-level mix. Balanced and powerful.")
    else: st.write("Calm energy — like Earth at night.")
