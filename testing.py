# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:04:03 2022

@author: chorgan
"""

# %%
import spotipy
import streamlit as st
import datetime as dt
from spotipy.oauth2 import SpotifyOAuth
import time

# import secrets from streamlit deployment
cid = st.secrets["SPOTIPY_CLIENT_ID"]
csecret = st.secrets["SPOTIPY_CLIENT_SECRET"]
uri = st.secrets["SPOTIPY_REDIRECT_URI"]

# set scope and establish connection
scopes = " ".join(["user-read-private",
                   "playlist-read-private",
                   "playlist-modify-private",
                   "playlist-modify-public",
                   "user-read-recently-played"])

# create oauth object
oauth = SpotifyOAuth(scope=scopes,
                     redirect_uri=uri,
                     client_id=cid,
                     client_secret=csecret)

# retrieve auth url
auth_url = oauth.get_authorize_url()

# %% leave for testing
response = ""
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)





#%%
today = dt.date.today()
one_week_ago = today - dt.timedelta(days=7)
yesterday = today - dt.timedelta(days=1)
right_now = dt.datetime.now().time()

# testing for recent func
combined = dt.datetime.combine(one_week_ago, right_now)
since = int(time.mktime(combined.timetuple())) * 1000

# %%
# a playlist with more than 100 tracks
playlist_id = "3m8vvNPoEN83tbwgz5xY1Q"

# %%
st.write("Remove all songs listened to since this time")
col1, col2 = st.columns(2)

since_date = col1.date_input("Date (max one week ago)",
                             value=today,
                             min_value=one_week_ago)
since_time = col2.time_input("Time",
                             value=right_now)
st.write(dt.datetime.combine(since_date, since_time))
