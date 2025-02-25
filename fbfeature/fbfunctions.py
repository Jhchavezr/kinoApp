# fbfeature/fbfunctions.py
import streamlit as st
import facebook as fb
from data_manager import get_data

def prepare_facebook_post(film):
    """Prepare the message and image URL for a Facebook post."""
    title = film.get('title', 'No Title')
    body = next((content['body'] for content in film.get('contents', []) if content['language_id'] == 1), "No body available")
    image_url = next((asset['url'] for asset in film.get('assets', []) if asset['type'] == 'poster'), None)
    booked_from = film.get('booked_from', 'Unknown date')

    message = f"{title}\n\n{body}\n booked from {booked_from}\nBestill billetten din på: https://tynsetkulturhus.no/kinoprogram/"
    return message, image_url

def publish_to_facebook(message, image_url):
    """Publish a message and optional image URL to Facebook."""
   # Retrieve the username from session state
    username = st.session_state.get('username')
    
    if not username:
        return "No user logged in."

    # Retrieve user information from the database
    users = get_data("users", "user_accounts")
    current_user = next((user for user in users if user.get('user') == username), None)
    
    if not current_user:
        return "User not found."

    # Get the GPT token from the user's information
    page_access_token = current_user.get('fbToken')

    page_id = current_user.get('fbPage')

    if not page_access_token:
        st.error("Page Access Token is not set. Please configure it in User Information Page")
        return

    try:
        graph_api = fb.GraphAPI(page_access_token)
        if image_url:
            response = graph_api.put_object(
                parent_object='me',
                connection_name='photos',
                message=message,
                url=image_url,
                published=True 
            )
        else:
            response = graph_api.put_object('me', 'feed', message=message)

        if 'id' in response:
            st.success(f"Post published successfully! Post ID: {response['id']}")
        else:
            st.error("Failed to publish the post.")
    except fb.GraphAPIError as e:
        st.error(f"An error occurred while posting to Facebook: {e}")
