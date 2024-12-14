#data_manager.py
import pymongo
import streamlit as st

@st.cache_resource
def connect_db():
    client = pymongo.MongoClient(**st.secrets["mongo"])
    db = client.get_database('users')
    return db.user_accounts

def get_data():
    db = connect_db()
    items = db.find()
    return list(items)