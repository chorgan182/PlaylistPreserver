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
scope = "user-read-currently-playing"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))


# %% app prep

# get user playlists
user_id = sp.current_user()["id"]

# bc results are paginated, need to define a func to get all results
def get_all_playlists(user_id):
    results = sp.user_playlists(user=user_id)
    playls = results["items"]
    while results["next"]:
        results = sp.next(results)
        playls.extend(results["items"])
    return playls
    
playlists = get_all_playlists(user_id)
#playlist_names = [x["name"] for x in playlists["items"]]

test = sp.user_playlists(user_id)
test2 = sp.current_user_playing_track()
# %% app UI

st.title("Spotify Playlist Preserver")

st.text("Please pick a playlist (note the limit is 50)")

st.selectbox("Playlist: ", playlists)
