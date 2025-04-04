from pathlib import Path
import streamlit as st

st.set_page_config(page_title="README", page_icon="📝", layout="wide")

README_PATH = Path(__file__).parent / "README.md"

if README_PATH.exists():
    st.markdown(README_PATH.read_text(), unsafe_allow_html=True)
else:
    st.error("README.md file not found in the current directory. Please ensure the file exists.", icon="🔥")
