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
import datetime as dt
import time

time.tzset()

# %% spotify connection set up

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

# %% base func definitions

def get_token(code):

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
        st.session_state["signed_in"] = True
        app_display_welcome()
        st.success("Sign in success!")
        
    return sp



def app_display_welcome():

    st.title("Spotify Playlist Preserver")

    welcome_msg = """
    Welcome! :wave: This app uses the Spotify API interact with music info and 
    eventually, your playlists! In order to view and modify information associated
    with your account, you must log in. You only need to do this once. Even if no 
    tokens are found, if you are signed in on this browser, you'll just be
    redirected to the app after clicking the link.
    """
    note_temp = """
    _Note: Unfortunately, the current version of Streamlit will not allow for
    staying on the same page, so the authorization and redirection will open in a 
    new tab. This has already been addressed in a development release, so it should
    be implemented in Streamlit Cloud soon!_
    """

    st.markdown(welcome_msg)

    if not st.session_state["signed_in"]:
        st.markdown(note_temp)
        
        

def app_remove_recent(username, nm_playlist, since, nm_playlist_new):
    st.experimental_show()
    
    # get playlist id of selected playlist
    playlists = sp.user_playlists(username)
    playlist_names = [x["name"] for x in playlists["items"]]
    playlist_ids = [x["id"] for x in playlists["items"]]
    pl_index = playlist_names.index(nm_playlist)
    pl_selected_id = playlist_ids[pl_index]
    
    # get playlist tracks of selected playlist
    ### don't forget about pagination
    pl_tracks = sp.playlist_tracks(pl_selected_id)
    pl_ids = [x["track"]["id"] for x in pl_tracks["items"]]
    
    # get listening history
    since_unix = int(time.mktime(since.timetuple()))
    ### don't forget about pagination
    recent_tracks = sp.current_user_recently_played(after=since_unix)
    recent_ids = [x["track"]["id"] for x in recent_tracks["items"]]
    
    # create new playlist, info of playlist returned
    new_pl = sp.user_playlist_create(user=username, name=nm_playlist_new)
    # need to get id of new playlist
    new_pl_id = new_pl["id"]
    
    # remove recently played from selected playlist
    new_tracks = [x for x in pl_ids if x not in recent_ids]
    
    # add tracks to new playlist!
    sp.user_playlist_add_tracks(user=username,
                                playlist_id=new_pl_id, 
                                tracks=new_tracks)    
   
# %% app session variable initialization

if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""
if "code" not in st.session_state:
    st.session_state["code"] = ""
    
    st.session_state()

# %% authenticate with response stored in url

# get current url (stored as dict)
url_params = st.experimental_get_query_params()

# attempt sign in with cached token
if st.session_state["cached_token"] != "":
    sp = app_sign_in()
# if no token, but code in url, get code, parse token, and sign in
elif "code" in url_params:
    # all params stored as lists, see doc for explanation
    st.session_state["code"] = url_params["code"][0]
    app_get_token()
    sp = app_sign_in()
# otherwise, prompt for redirect
else:
    app_display_welcome()
    # this SHOULD open the link in the same tab when Streamlit Cloud is updated
    # via the "_self" target
    st.write(" ".join(["No tokens found for this session. Please log in by",
                      "clicking the link below."]))
    link_html = " <a target=\"_self\" href=\"{url}\" >{msg}</a> ".format(
        url=auth_url,
        msg="Click me to authenticate!"
    )
    st.markdown(link_html, unsafe_allow_html=True)
    
# %% after auth, get user info

# only display the following after login
### is there another way to do this? clunky to have everything in an if:
if st.session_state["signed_in"]:
    user = sp.current_user()
    name = user["display_name"]
    username = user["id"]

    st.markdown("Hi {n}! Let's modify a playlist or two :smiley:".format(n=name))

    playlists = sp.user_playlists(username)
    ### don't forget about pagination
    playlist_names = [x["name"] for x in playlists["items"]]
    playlist_ids = [x["id"] for x in playlists["items"]]
    
    with st.form("playlist_modify"):
        # pick playlist
        st.write("Please pick a playlist to modify")
        pl_selected = st.selectbox("Playlist: ", playlist_names)
        
        # time cutoff
        st.write("Remove all songs listened to since this time")
        col1, col2 = st.columns(2)
        
        today = dt.date.today()
        one_week_ago = today - dt.timedelta(days=7)
        right_now = dt.datetime.now().time()
        
        since_date = col1.date_input("Date (max one week ago)",
                                     value=today,
                                     min_value=one_week_ago)
        since_time = col2.time_input("Time",
                                     value=right_now)
        since_combined = dt.datetime.combine(since_date, since_time)        
        
        # new playlist name
        new_name = st.text_input("New playlist name", key="new_name")
        
        modify_confirm = st.form_submit_button("Modify!",
                                               on_click=app_remove_recent,
                                               args=(
                                                   username,
                                                   pl_selected,
                                                   since_combined,
                                                   st.session_state["new_name"]
                                                   )
                                               )
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
