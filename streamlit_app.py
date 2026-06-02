import streamlit as st
from openai import OpenAI
import datetime

st.set_page_config(page_title="CosmoAi", layout="wide")
st.title("CosmoAi")

import pathlib
readme = pathlib.Path("README.md").read_text()
st.markdown(readme)
st.caption("v2.9.9 - Groq free")

client = OpenAI(
    api_key=st.secrets["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

MODEL = "llama-3.1-8b-instant"

tab1, tab2, tab3, tab4 = st.tabs(["AI Chat","Orbit Sim","What-If","Phone Tools"])

with tab1:
    if "h" not in st.session_state:
        st.session_state.h = []

    for m in st.session_state.h:
        with st.chat_message(m["role"]):
            st.write(m["content"])

    p = st.chat_input("Ask about space")
    if p:
        st.session_state.h.append({"role":"user","content":p})
        with st.chat_message("user"):
            st.write(p)

        try:
            r = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":"You are CosmoAi, a helpful space expert. Keep answers short and friendly."}] + st.session_state.h[-8:]
            )
            a = r.choices[0].message.content
        except Exception as e:
            a = f"Groq error: {e}"

        st.session_state.h.append({"role":"assistant","content":a})
        with st.chat_message("assistant"):
            st.write(a)

with tab2:
    st.subheader("Orbit Sim")
    st.write("ISS: 435 km altitude, 27,547 km/h")
    st.write("Updated:", datetime.datetime.now(datetime.UTC).strftime("%H:%M UTC"))

with tab3:
    st.subheader("What-If")
    q = st.text_input("What if...", key="whatif_input")
    if q:
        try:
            r = client.chat.completions.create(
                model=MODEL,
                messages=[{"role":"system","content":"Answer briefly."},{"role":"user","content":q}]
            )
            st.write(r.choices[0].message.content)
        except Exception as e:
            st.error(f"Groq error: {e}")

with tab4:
    st.subheader("Phone Tools")
    st.write("Flashlight / Compass / Calculator - coming soon")
