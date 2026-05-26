import streamlit as st
from openai import OpenAI

st.set_page_config(page_title="CosmoAi", page_icon="🚀")
st.title("CosmoAi Chat")

client = OpenAI(api_key=st.secrets["OPENAI_API_KEY"])

if "history" not in st.session_state:
    st.session_state.history = []

prompt = st.chat_input("Ask about space:")
if prompt:
    st.session_state.history.append({"role":"user","content":prompt})
    resp = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role":"system","content":"You are CosmoAi, a friendly space expert."}] + st.session_state.history
    )
    answer = resp.choices[0].message.content
    st.session_state.history.append({"role":"assistant","content":answer})

for msg in st.session_state.history:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])
