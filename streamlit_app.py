# streamlit_app.py
import os
import json
import requests
import streamlit as st
from pathlib import Path
from dotenv import load_dotenv

# Load .env if present
env_path = Path('.') / '.env'
if env_path.exists():
    load_dotenv(env_path)

# Configuration (can be overridden by environment)
BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")
API_KEY = os.getenv("DEMO_API_KEY", "demo-secret-key")

HEADERS = {"X-API-KEY": API_KEY}

st.set_page_config(page_title="PLUM Backend Assignment", layout="centered")

st.title("Plum Backend — Text & Image OCR UI")
st.markdown("A tiny Streamlit UI to demo the backend endpoints: text processing and image OCR + chain.")

st.sidebar.header("Configuration")
st.sidebar.write("Change these if you're using ngrok or a remote instance.")
base_url = st.sidebar.text_input("API base URL", value=BASE_URL)
api_key = st.sidebar.text_input("API key (X-API-KEY)", value=API_KEY, type="password")

# Update HEADERS based on sidebar
HEADERS = {"X-API-KEY": api_key}

st.header("Text input → /v1/process/text")
text_input = st.text_area("Enter text to process", height=160, value="Hello, this is a demo input.")
input_id_text = st.text_input("input_id (optional)", value="demo-1")

if st.button("Send text"):
    with st.spinner("Calling API..."):
        try:
            url = f"{base_url.rstrip('/')}/v1/process/text"
            payload = {"input_id": input_id_text or "demo-1", "text": text_input}
            resp = requests.post(url, json=payload, headers=HEADERS, timeout=30)
            st.markdown(f"**HTTP {resp.status_code}**")
            try:
                st.json(resp.json())
            except Exception:
                st.text(resp.text)
        except Exception as e:
            st.error(f"Request failed: {e}")

st.markdown("---")
st.header("Image upload → /v1/process/image")
st.markdown("Upload an image (PNG/JPEG). The app will call `/v1/process/image` and display the OCR result.")

uploaded_file = st.file_uploader("Choose an image file", type=["png", "jpg", "jpeg"])
input_id_img = st.text_input("input_id for image", value="img-1")

if st.button("Upload image"):
    if not uploaded_file:
        st.warning("Please choose an image file first.")
    else:
        with st.spinner("Uploading and calling API..."):
            try:
                url = f"{base_url.rstrip('/')}/v1/process/image"
                files = {
                    "image": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)
                }
                data = {"input_id": input_id_img or "img-1"}
                resp = requests.post(url, headers=HEADERS, files=files, data=data, timeout=60)
                st.markdown(f"**HTTP {resp.status_code}**")
                try:
                    st.json(resp.json())
                except Exception:
                    st.text(resp.text)
            except Exception as e:
                st.error(f"Request failed: {e}")

st.markdown("---")
st.header("Raw endpoints")
st.markdown(f"- Text endpoint: `{base_url.rstrip('/')}/v1/process/text`")
st.markdown(f"- Image endpoint: `{base_url.rstrip('/')}/v1/process/image`")
st.markdown("Use the sidebar to change `BASE_URL` to a public ngrok URL if you want to demo remotely.")
