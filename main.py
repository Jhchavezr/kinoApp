import streamlit as st
from authenticator import authenticate_user, logout
from data_manager import get_data
from features import display_key_features

# Fetch data from the database
items = get_data()

# Authenticate the user
if authenticate_user():
    # If authenticated, display the features
    display_key_features(items)
    logout()  # Show the logout button
else:
    # If not authenticated, only show the authentication forms
    st.write("### Please log in to access the features.")
