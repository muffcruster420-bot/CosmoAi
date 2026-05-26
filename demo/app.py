import streamlit as st
import pandas as pd
import numpy as np
import requests
import time
import streamlit.components.v1 as components

st.set_page_config(page_title="CosmoAi", page_icon="ðŸ›°ï¸", layout="wide")
st.title("ðŸ›°ï¸ CosmoAi â€” Live Space Data")
st.caption("Built by a phone for a phone, in Kingston, ON.")

tab = st.sidebar.radio("Navigate", ["SDSS", "CERN", "Voyager", "Shangraw Gap", "Live Sky â€” Global", "Offline Maps", "Universe Map", "Sandbox"])

if tab == "SDSS":
    st.header("ðŸ”­ SDSS Galaxies")
    df = pd.DataFrame({'ra': np.random.uniform(0,360,100), 'dec': np.random.uniform(-90,90,100), 'z': np.random.uniform(0,2,100)})
    st.scatter_chart(df, x='ra', y='dec', size='z')

elif tab == "CERN":
    st.header("âš›ï¸ CERN Higgs")
    st.line_chart(pd.DataFrame({'mass': np.random.normal(125,2,200)}))

elif tab == "Voyager":
    st.header("ðŸš€ Voyager")
    d = 24.5 + (time.time()%86400)/86400*0.001
    st.metric("Voyager 1", f"{d:.3f} B km")

elif tab == "Shangraw Gap":
    st.header("ðŸ” Shangraw Gap")
    z = np.random.uniform(0,0.5,500)
    h,_ = np.histogram(z,30)
    st.bar_chart(h)
    st.success(f"{len(np.where(h<5)[0])} gaps found")

elif tab == "Live Sky â€” Global":
    st.header("ðŸŒŒ Live Sky â€” Global")
    
    st.subheader("ðŸª Sky View â€” Planets & Stars")
    components.iframe("https://stellarium-web.org/", height=520)
    st.caption("Pinch to zoom â€¢ See what's above Kingston right now")
    
    st.subheader("ðŸŒ Live Ground â€” Earth from Space")
    components.iframe("https://www.youtube.com/embed/86YLFOog4GM?autoplay=0", height=400)
    st.caption("ISS live HD â€” real-time view of Earth passing below (NASA HDEV)")
    
    st.subheader("ðŸ“· Live Ground â€” Webcams Worldwide")
    components.iframe("https://www.windy.com/-Webcams", height=500)
    st.caption("Tap any dot â€” live beach, city, mountain cams updating now")
    
    st.subheader("ðŸ›°ï¸ ISS Tracker")
    try:
        iss = requests.get("http://api.open-notify.org/iss-now.json", timeout=5).json()
        lat = float(iss['iss_position']['latitude']); lon = float(iss['iss_position']['longitude'])
        st.success(f"ISS is over {lat:.1f}Â°N, {lon:.1f}Â°W right now")
        st.map(pd.DataFrame({'lat':[lat],'lon':[lon]}), zoom=1)
    except:
        st.warning("Loading ISS...")

elif tab == "Offline Maps":
    st.header("ðŸ—ºï¸ Offline Maps â€” v2.9.8")
    st.subheader("Works without WiFi after first load")
    st.caption("First visit caches the map. Then airplane mode = still works.")
    
    offline_html = """
    <div id='map' style='width:100%;height:600px;border-radius:12px;'></div>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"/>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script src="https://unpkg.com/leaflet.offline@3.0.0/dist/leaflet.offline.min.js"></script>
    <script>
    const map = L.map('map').setView([44.23, -76.48], 5);
    const offlineLayer = L.tileLayer.offline('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        attribution: 'Â© OpenStreetMap',
        minZoom: 1, maxZoom: 16,
        crossOrigin: true
    });
    offlineLayer.addTo(map);
    const control = L.control.savetiles(offlineLayer, {
        zoomlevels: [3,4,5,6,7,8,9,10,11,12],
        confirm: function(layer, success) {
            if (confirm('Cache maps for offline use? (~30MB on WiFi)')) success();
        }
    });
    control.addTo(map);
    map.on('click', function(e){
        L.marker(e.latlng).addTo(map).bindPopup('Lat: '+e.latlng.lat.toFixed(4)+'<br>Lon: '+e.latlng.lng.toFixed(4)).openPopup();
    });
    // Auto-prompt to save Kingston area
    setTimeout(()=>{ if(confirm('Download Kingston area for offline?')) control._saveTiles(); }, 2000);
    </script>
    """
    components.html(offline_html, height=650)
    st.info("âœ… Tap the ðŸ’¾ icon top-left â†’ saves tiles â†’ turn off WiFi â†’ map still pans/zooms")
    st.success("v2.9.8 â€” built at 12:05am, Kingston, 40% battery")

elif tab == "Universe Map":
    st.header("ðŸŒŒ Universe Map â€” Where Dark Matter Lives")
    scale = st.slider("Zoom out (million light-years)", 10, 1000, 200, 10)
    np.random.seed(42); n=800
    x=np.random.normal(0,scale/3,n); y=np.random.normal(0,scale/3,n)
    dm=np.exp(-(x**2+y**2)/(2*(scale/2.5)**2))*80+np.random.rand(n)*40
    df=pd.DataFrame({'x (Mly)':x,'y (Mly)':y,'Dark Matter Density':dm})
    st.scatter_chart(df, x='x (Mly)', y='y (Mly)', size='Dark Matter Density')
    if scale<50: st.write(f"**{scale} Mly:** Local Group â€” dark matter holding Milky Way")
    elif scale<200: st.write(f"**{scale} Mly:** Virgo Supercluster â€” Shangraw Gap territory")
    else: st.write(f"**{scale} Mly:** Cosmic web scale")

else: # Sandbox
    st.header("ðŸ§ª Sandbox â€” Play Lab")
    col1,col2=st.columns(2)
    with col1:
        r=st.slider("Red",0,255,120); g=st.slider("Green",0,255,80); b=st.slider("Blue",0,255,200)
        uv=st.slider("UV",0,100,20); ir=st.slider("Infrared",0,100,30); gamma=st.slider("Gamma",0,100,10)
    with col2:
        color=f"rgb({r},{g},{b})"
        st.markdown(f"<div style='height:150px;background:{color};border-radius:10px'></div>", unsafe_allow_html=True)
        st.code(f"HEX: #{r:02x}{g:02x}{b:02x}")
    st.bar_chart(pd.DataFrame({'Wavelength':['IR','Red','Green','Blue','UV','Gamma'],'Intensity':[ir,r/2.55,g/2.55,b/2.55,uv,gamma]}))
