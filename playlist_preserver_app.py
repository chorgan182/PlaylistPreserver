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
import os

# set ids and secrets
os.environ["SPOTIPY_CLIENT_ID"] = "490a0db12cc04207bdc1719f40132717"
os.environ["SPOTIPY_CLIENT_SECRET"] = "21466d35e131432dbe3214377696d04e"
os.environ["SPOTIPY_REDIRECT_URI"] = "http://127.0.0.1:9090"


# %% spotify connection

# set scope and establish connection
#scope = "user-read-currently-playing"
#scope = "user-read-playback-state"
scope_user = "user-read-private"
scope_plist_read = "playlist-read-private"
scope_plist_write = "playlist-modify-private"
sp_pl_read = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope_plist_read))
sp_pl_write = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope_plist_write))
sp_user = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope_user))

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
