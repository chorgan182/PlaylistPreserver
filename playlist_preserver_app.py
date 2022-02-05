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
scopes = " ".join(["user-read-private",
                   "playlist-read-private",
                   "playlist-modify-private"])

# create oauth object
oauth = SpotifyOAuth(scope=scopes,
                     redirect_uri=uri,
                     client_id=cid,
                     client_secret=csecret)
sp = spotipy.Spotify(oauth_manager=oauth)

# # retrieve auth url
# auth_url = oauth.get_authorize_url()

# # sign in function
# def sign_in(auth_url):
#     # open the auth link in a modal window
    
    
#     # get a response from the redirect uri
#     response = "idk get it from the redirect uri"
    
#     # parse the token from the link
#     code = oauth.parse_response_code(response)
#     token_info = oauth.get_access_token(code)
#     token = token_info["access_token"]
    
#     # return a spotify object    
#     return spotipy.Spotify(auth=token,)

# test = spotipy.Spotify(oauth_manager=oauth)
# test.current_user()
# %% app UI auth

st.title("Spotify Playlist Preserver")

#sp = st.button("Sign in to Spotify", on_click=sign_in(auth_url))

# %% test auth

username = sp.current_user()["id"]
st.write("this should work")
st.write("Your username is %s" % username)

st.write("Please pick a playlist to modify")

playlists = sp.user_playlists(username)
playlist_names = [x["name"] for x in playlists["items"]]
st.selectbox("Playlist: ", playlist_names)

# %% testing other features
status = st.radio("Is this the coolest thing you've ever seen?",
                  ('Yes', 'Yes but with more words'))

if (status == 'Yes'):
    st.success("Thank you")
else:
    st.success("Thank you much")
