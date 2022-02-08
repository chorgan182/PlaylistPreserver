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

def get_token(code):
    
    # parse the token from the response url
    #code = oauth.parse_response_code(response_url)
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
        token = get_token(st.session_state["code"])
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

st.markdown("""
Welcome! :wave: This app uses the Spotify API interact with music info and 
eventually, your playlists! In order to view and modify information associated
with your account, you must log in. You only need to do this once. Even if no 
tokens are found, if you are signed in on this browser, you'll just be
redirected to the app after clicking the link.

_Note: Unfortunately, the current version of Streamlit will not allow for
staying on the same page, so the authorization and redirection will open in a 
new tab. This has already been addressed in a development release, so it should
be implemented in Streamlit Cloud soon!_
""")

# initialize session variables
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""
if "code" not in st.session_state:
    st.session_state["code"] = ""

# get current url params
url_params = st.experimental_get_query_params()

# attempt sign in with cached token
if st.session_state["cached_token"] != "":
    sp = app_sign_in()
# if no token, but code in url, get code, token, and sign in
elif "code" in url_params:
    st.session_state["code"] = url_params["code"]
    st.session_state["cached_token"] = app_get_token()
    sp = app_sign_in()
# otherwise, prompt for redirect
else:
    st.write(" ".join(["No tokens found for this session. Please log in by",
                      "clicking the link below."]))
    link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )
    st.markdown(link_html, unsafe_allow_html=True)
    
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
