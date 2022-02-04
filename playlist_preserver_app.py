# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 19:35:20 2022

@author: chorg
"""

# %% setup

# libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import streamlit as st

# %% spotify connection

# import secrets from streamlit deployment
cid = st.secrets["SPOTIPY_CLIENT_ID"]
csecret = st.secrets["SPOTIPY_CLIENT_SECRET"]
uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# set scope and establish connection
scopes = "user-read-private playlist-read-private playlist-modify-private"

# create oauth object
oauth = SpotifyOAuth(scope=scopes,
                     redirect_uri=uri,
                     client_id=cid,
                     client_secret=csecret)

# retrieve auth url
auth_url = oauth.get_authorize_url()

# %% app UI

st.title("Spotify Playlist Preserver")

st.header("Connect to Spotify")
st.markdown("[Click me to authenticate!](%s)" % auth_url)

response = st.text_input("Click the link above, copy the URL from the new tab, paste it here, and press enter: ")
code = oauth.parse_response_code(response)
token_info = oauth.get_access_token(code)
token = token_info["access_token"]
sp = spotipy.Spotify(auth=token)

username = sp.current_user()["id"]
st.write("Your username is %s" % username)

st.write("Please pick a playlist to modify")

playlists = sp.user_playlists(username)
playlist_names = [x["name"] for x in playlists["items"]]
st.selectbox("Playlist: ", playlist_names)

# radio button
# first argument is the title of the radio button
# second argument is the options for the ratio button
status = st.radio("Is this the coolest thing you've ever seen?",
                  ('Yes', 'Yes but with more words'))
 
# conditional statement to print
# Male if male is selected else print female
# show the result using the success function
if (status == 'Yes'):
    st.success("Thank you")
else:
    st.success("Thank you much")
