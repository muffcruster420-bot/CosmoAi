import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="CosmoAi", layout="wide")
st.title("CosmoAi")
st.caption("v2.9.9 - Groq free")

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

tab1, tab2, tab3, tab4 = st.tabs(["AI Chat","Orbit Sim","What-If","Phone Tools"])

with tab1:
    if "h" not in st.session_state: st.session_state.h = []
    p = st.chat_input("Ask about space")
    if p:
        st.session_state.h.append({"role":"user","content":p})
        r = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"system","content":"You are CosmoAi, a helpful space expert. Keep answers short."}] + st.session_state.h[-6:]
        )
        a = r.choices[0].message.content
        st.session_state.h.append({"role":"assistant","content":a})
    for m in st.session_state.h:
        with st.chat_message(m["role"]): st.write(m["content"])

with tab2:
    st.subheader("Orbit Sim")
    st.write("ISS: 435 km altitude, 27,547 km/h")
    st.write("Updated:", datetime.datetime.utcnow().strftime("%H:%M UTC"))

with tab3:
    st.subheader("What-If")
    q = st.text_input("What if...")
    if q:
        r = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role":"system","content":"Answer briefly."},{"role":"user","content":q}]
        )
        st.write(r.choices[0].message.content)

with tab4:
    st.subheader("Phone Tools")
    st.write("Flashlight / Compass / Calculator - coming soon")
