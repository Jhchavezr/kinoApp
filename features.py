#features.py
import streamlit as st
from data_manager import get_data

def display_key_features(items):
    """Display the key features of the app."""
    st.write("### Key Features")
    application = st.selectbox('Choose an action:', ('Do something', 'Do something again'))
    st.write(f"You selected: {application}")
    st.write("### Items from the Database:")
    st.table(items)
