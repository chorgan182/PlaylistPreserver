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
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
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

# %% base func definitions

def get_token(oauth, user, pw):
    
    # retrieve auth url
    auth_url = oauth.get_authorize_url()
    
    # pass a service object to avoid deprecation warning
    s = Service("/home/appuser/.wdm/drivers/geckodriver/linux64/v0.30.0/geckodriver")
    
    # open the auth link in a new headless window
    fireFoxOptions = Options()
    fireFoxOptions.headless = True
    driver = webdriver.Firefox(service=s,
                               options=fireFoxOptions)
    driver.get(auth_url)
    
    # pass the provided user and pw
    driver.find_element(by=By.ID, value="login-username").send_keys(user)
    driver.find_element(by=By.ID, value="login-password").send_keys(pw)
    # click login
    driver.find_element(by=By.ID, value="login-button").click()
    
    # wait until the user inputs creds and the url changes
    WebDriverWait(driver, 120).until(EC.url_contains("code="),
                                    "Sign in timed out")
    # get the new url
    response_url = driver.current_url
    # close window
    driver.quit()
    
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

def update_creds():
    st.session_state["input_user"] = st.session_state["user_new"]
    st.session_state["input_pw"] = st.session_state["pw_new"]
    
def app_delete_creds():
    if "input_user" in st.session_state:
        st.session_state["input_user"] = ""
    if "input_pw" in st.session_state:
        st.session_state["input_pw"] = ""
    if "user_new" in st.session_state:
        del st.session_state["user_new"]
    if "pw_new" in st.session_state:
        del st.session_state["pw_new"]
    

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
        app_delete_creds()
        st.session_state["cached_token"] = token
        ### troubleshooting
        st.write(st.session_state)

def app_sign_in():
    try:
        sp = sign_in(st.session_state["cached_token"])
    except Exception as e:
        st.error("An error occurred during sign-in!")
        st.write("The error is as follows:")
        st.write(e)
    else:
        app_delete_creds()
        st.success("Sign in success!")
        st.session_state["signed_in"] = True
        ### troubleshooting
        st.write(st.session_state)
    return sp

# %% app auth

st.title("Spotify Playlist Preserver")

# initialize session variables
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = ""
if "input_user" not in st.session_state:
    st.session_state["input_user"] = ""
if "input_pw" not in st.session_state:
    st.session_state["input_pw"] = ""
    
### troubleshooting
st.write(st.session_state)

# attempt sign in with cached token
if st.session_state["cached_token"] != "":
    sp = app_sign_in()
# get token if it does not exist and creds do
elif (
        st.session_state["input_user"] != "" and
        st.session_state["input_pw"] != ""
     ):
    app_get_token()
    sp = app_sign_in()
else:
    st.write("No tokens found for this session. Please log in below.")

# display the login button
sign_in_clicked = st.button("Sign in to Spotify",
                            disabled=st.session_state["signed_in"])

# %% app auth form

# log in once the button is clicked
# save the token in this session to prevent multiple sign-ins
if sign_in_clicked and "sp" not in locals():
    
    with st.form("login", clear_on_submit=True):
        user = st.text_input("User",
                             placeholder="Email associated with Spotify account",
                             key="user_new")
        pw = st.text_input("Password",
                           placeholder="Spotify password",
                           type="password",
                           key="pw_new")
        submitted = st.form_submit_button("Log in", on_click=update_creds)

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
