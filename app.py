import streamlit as st
from eda_script import eda

st.set_option('deprecation.showPyplotGlobalUse', False)
st.set_page_config(layout="wide")

eda()
