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

# %% spotify connection set up

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

# retrieve auth url
auth_url = oauth.get_authorize_url()

# %% base func definitions

def get_token(response_url):
    
    # parse the token from the response url
    code = oauth.parse_response_code(response_url)
    token = oauth.get_access_token(code, as_dict=False, check_cache=False)
    # remove cached token saved in directory
    os.remove(".cache")
    
    # return the token
    return token

def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp

# %% app func definitions

def app_get_token():
    try:
        token = get_token(oauth,
                          user=st.session_state["input_user"],
                          pw=st.session_state["input_pw"])
    except Exception as e:
        st.error("An error occurred during token retrieval!")
        st.write("The error is as follows:")
        st.write(e)
    else:
        st.session_state["cached_token"] = token

def app_sign_in():
    try:
        sp = sign_in(st.session_state["cached_token"])
    except Exception as e:
        st.error("An error occurred during sign-in!")
        st.write("The error is as follows:")
        st.write(e)
    else:
        st.success("Sign in success!")
        st.session_state["signed_in"] = True
    return sp

# %% app auth

st.title("Spotify Playlist Preserver")

# initialize session variables
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""

# attempt sign in with cached token
if st.session_state["cached_token"] != "":
    sp = app_sign_in()
else:
    st.write(" ".join("No tokens found for this session. Please log in by",
                      "clicking the link below."))
    st.markdown("[Click me to authenticate!](%s)" % auth_url)
             

# %% app after auth

# only display the following after login
if "sp" in locals():
    user = sp.current_user()
    name = user["display_name"]
    username = user["id"]

    st.markdown("Hi {n}! Let's modify a playlist or two :smiley:".format(n=name))
    st.write("Your username is {u}".format(u=username))

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
