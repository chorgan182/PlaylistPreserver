# -*- coding: utf-8 -*-
"""
Created on Tue Feb  1 19:35:20 2022

@author: chorg
"""

# %% setup

# libraries
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from spotipy.oauth2 import SpotifyClientCredentials
import streamlit as st

# %% spotify connection

# import secrets from streamlit deployment
pl_prsvr_client_id = st.secrets["SPOTIPY_CLIENT_ID"]
pl_prsvr_client_secret = st.secrets["SPOTIPY_CLIENT_SECRET"]
pl_prsvr_redirect_uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# set the client creds for connections to spotify api
client_creds = SpotifyClientCredentials(client_id=pl_prsvr_client_id,
                                        client_secret=pl_prsvr_client_secret)

# set scope and establish connection
scope_user = "user-read-private"
scope_plist_read = "playlist-read-private"
scope_plist_write = "playlist-modify-private"
sp_pl_read = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope_plist_read,
                              redirect_uri=pl_prsvr_redirect_uri),
    client_credentials_manager=client_creds)
sp_pl_write = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope_plist_write,
                              redirect_uri=pl_prsvr_redirect_uri),
    client_credentials_manager=client_creds)
sp_user = spotipy.Spotify(
    auth_manager=SpotifyOAuth(scope=scope_user,
                              redirect_uri=pl_prsvr_redirect_uri),
    client_credentials_manager=client_creds)

# %% app prep

# get user playlists
user_id = sp_user.current_user()["id"]

playlists = sp_pl_read.user_playlists(user_id)
playlist_names = [x["name"] for x in playlists["items"]]

# bc results are paginated, need to define a func to get all results
### should implement eventually but I only have 30
# def get_all_playlists(user_id):
#     results = sp.user_playlists(user=user_id)
#     playls = results["items"]
#     while results["next"]:
#         results = sp.next(results)
#         playls.extend(results["items"])
#     return playls
    
#playlists = get_all_playlists(user_id)

# %% app UI

st.title("Spotify Playlist Preserver")

st.text("Please pick a playlist to modify")

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
