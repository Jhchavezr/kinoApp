#authenticator.py
import streamlit as st
import pymongo
from data_manager import get_data, connect_db


# def connect_db():
#     client = pymongo.MongoClient(
#           **st.secrets["mongo"])
#     db = client.get_database('users')
#     return db.user_accounts

# def get_data():
#     db = user_db
#     items = db.find()
#     items = list(items)  # make hashable for st.cache_data
#     return items

user_db = connect_db()
items = get_data()

# Initialize Session States.
if 'username' not in st.session_state:
       st.session_state.username = ''
if 'form' not in st.session_state:
       st.session_state.form = ''
def select_signup():
    st.session_state.form = 'signup_form'

def user_update(name):
    st.session_state.username = name

if st.session_state.username != '':
    st.sidebar.write(f"You are logged in as {st.session_state.username.upper()}")

# Initialize Sing In or Sign Up forms
if st.session_state.form == 'signup_form' and st.session_state.username == '':
  
    signup_form = st.sidebar.form(key='signup_form', clear_on_submit=True)
    new_username = signup_form.text_input(label='Enter Username*')
    new_user_email = signup_form.text_input(label='Enter Email Address*')
    new_user_pas = signup_form.text_input(label='Enter Password*', type='password')
    user_pas_conf = signup_form.text_input(label='Confirm Password*', type='password')
    note = signup_form.markdown('**required fields*')
    signup = signup_form.form_submit_button(label='Sign Up')
    
    if signup:
        if '' in [new_username, new_user_email, new_user_pas]:
            st.sidebar.error('Some fields are missing')
        else:
            if user_db.find_one({'user' : new_username}):
                st.sidebar.error('Username already exists')
            if user_db.find_one({'email' : new_user_email}):
                st.sidebar.error('Email is already registered')
            else:
                if new_user_pas != user_pas_conf:
                    st.sidebar.error('Passwords do not match')
                else:
                    user_update(new_username)
                    user_db.insert_one({'user' : new_username, 'email' : new_user_email, 'pwd' : new_user_pas})
                    st.sidebar.success('You have successfully registered!')
                    st.sidebar.success(f"You are logged in as {new_username.upper()}")
                    del new_user_pas, user_pas_conf
                    
elif st.session_state.username == '':
    login_form = st.sidebar.form(key='signin_form', clear_on_submit=True)
    username = login_form.text_input(label='Enter Username')
    user_pas = login_form.text_input(label='Enter Password', type='password')
    
    if user_db.find_one({'user' : username, 'pwd' : user_pas}):
        login = login_form.form_submit_button(label='Sign In', on_click=user_update(username))
        if login:
            st.sidebar.success(f"You are logged in as {username.upper()}")
            del user_pas
    else:
        login = login_form.form_submit_button(label='Sign In')
        if login:
            st.sidebar.error("Username or Password is incorrect. Please try again or create an account.")
else:
    logout = st.sidebar.button(label='Log Out')
    if logout:
        user_update('')
        st.session_state.form = ''

# 'Create Account' button
if st.session_state.username == "" and st.session_state.form != 'signup_form':
    signup_request = st.sidebar.button('Create Account', on_click=select_signup)

# Show Key Features Only for Authenticated Users
if st.session_state.username != '':
    display_key_features()  # Call the external function to load key features
else:
    st.write("### Please log in to access the features.")