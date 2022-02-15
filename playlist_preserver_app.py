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



def get_correct_limit(stop, start):
    '''
    All credit to https://github.com/irenechang1510 for this function idea.
    '''    
    
    # start at 50 and move backwards until correct timestamp is found
    # re run the API call until 'before' is greater than the stop timestamp
    limit = 50
    while limit > 0:
        obj = sp.current_user_recently_played(before=start, limit=limit)
        mark = int(obj['cursors']['before'])
        
        # get the track played right after the stop timestamp
        if mark > stop:
            break
        # otherwise, decrease the limit by 1 and try again
        limit -= 1
    
    return limit


### in the end, this endpoint is simply broken
### cannot do anything until Spotify fixes it
def get_recents_all(since):
    
    # for some reason, you have to move backwards instead of forward
    # the after header seems pointless because it still starts at current time
    # but the next() method returns a results object with no 'next' dict element?
    
    now = int(time.mktime(dt.datetime.now().timetuple())) * 1000
    start = now
    
    tracks = []
    while (start > since):
        results = sp.current_user_recently_played(before=start, limit=50)
        try:
            next_stop = int(results["cursors"]["before"])
        except:
            next_stop = since
        # eventually, the next stop will move past the desired since timestamp
        if next_stop < since:
            last_limit = get_correct_limit(since, start)
            if last_limit != 0:
                results = sp.current_user_recently_played(before=start,
                                                          limit=last_limit)
            else:
                break
        tracks.extend(results["items"])
        start = next_stop
    return tracks



def get_playlists_all(username):
    results = sp.user_playlists(username)
    playlists = results["items"]
    while results["next"]:
        results = sp.next(results)
        playlists.extend(results["items"])
    return playlists



def get_tracks_all(username, playlist_id):
    results = sp.user_playlist_tracks(username, playlist_id)
    tracks = results["items"]
    while results["next"]:
        results = sp.next(results)
        tracks.extend(results["items"])
    return tracks

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
        
        

def app_remove_recent(username):
    nm_playlist = st.session_state["pl_selected"]
    since_date = st.session_state["since_date"]
    since_time = st.session_state["since_time"]
    nm_playlist_new = st.session_state["new_name"]
    
    # get playlist id of selected playlist
    playlists = get_playlists_all(username)
    playlist_names = [x["name"] for x in playlists]
    playlist_ids = [x["id"] for x in playlists]
    pl_index = playlist_names.index(nm_playlist)
    pl_selected_id = playlist_ids[pl_index]
    
    # get playlist tracks of selected playlist
    pl_tracks = get_tracks_all(username, pl_selected_id)
    pl_ids = [x["track"]["id"] for x in pl_tracks]
    
    # get listening history
    # combine date inputs to datetime object
    since_combined = dt.datetime.combine(since_date, since_time)
    # needs to be in milliseconds
    since_unix = int(time.mktime(since_combined.timetuple()))*1000
    recent_tracks = get_recents_all(since_unix)
    recent_ids = [x["track"]["id"] for x in recent_tracks]
    
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
    
    # gotta do a celly
    st.success("New playlist created! Check your Spotify App")
    st.balloons()
   
# %% app session variable initialization

if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""
if "code" not in st.session_state:
    st.session_state["code"] = ""

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

    playlists = get_playlists_all(username)
    playlist_names = [x["name"] for x in playlists]
    playlist_ids = [x["id"] for x in playlists]
    
    with st.form("playlist_modify", clear_on_submit=False):
        # get input for playlist to modify
        st.write("Please pick a playlist to modify")
        pl_selected = st.selectbox("Playlist: ", playlist_names,
                                   key="pl_selected")
        
        # get input for new playlist name
        new_name = st.text_input("New playlist name", key="new_name")

        # get input for time cutoff
        st.write("Remove all songs listened to since this time")
        col1, col2 = st.columns(2)
        # store current times
        today = dt.date.today()
        one_week_ago = today - dt.timedelta(days=7)
        right_now = dt.datetime.now().time()
        # get date inputs
        since_date = col1.date_input("Date (max one week ago)",
                                     value=today,
                                     min_value=one_week_ago,
                                     key="since_date")
        since_time = col2.time_input("Time",
                                     value=right_now,
                                     key="since_time")
                
        
        # submit button
        modify_confirm = st.form_submit_button("Modify!",
                                               on_click=app_remove_recent,
                                               args=(username,))
                                               