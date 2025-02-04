# pages/userInformation.property
# User information page where we'll show and update the current users information.
# It'll have the fields name, user, password, facebook token, and dx token which will be possible to see and modify.
import streamlit as st
from data_manager import get_users,  update_user
st.title("User Information Management")

# Fetch users
users = get_users()

# Display users
st.subheader("Current Users:")
for user in users:
    st.write(user)

# Add New User
st.subheader("Add a New User")
new_user = {
    "name": st.text_input("Name"),
    "user": st.text_input("Username"),
    "password": st.text_input("Password", type="password"),
    "facebook_token": st.text_area("Facebook Token"),
    "dx_token": st.text_area("DX Token"),
}

# Update User
st.subheader("Update User Information")
update_username = st.selectbox("Select User to Update", [u["user"] for u in users])
updated_data = {
    "name": st.text_input("New Name"),
    "password": st.text_input("New Password", type="password"),
    "facebook_token": st.text_area("New Facebook Token"),
    "dx_token": st.text_area("New DX Token"),
}

if st.button("Update User"):
    update_user(update_username, updated_data)
    st.success(f"User {update_username} updated successfully!")

