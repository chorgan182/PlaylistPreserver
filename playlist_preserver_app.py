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
from selenium.webdriver.firefox import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from urllib.parse import quote

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

# sign in function
def get_token(oauth, user, pw):
    
    # retrieve auth url
    auth_url = oauth.get_authorize_url()
    
    ### not sure if this should be kept
    s = Service("/home/appuser/.wdm/drivers/geckodriver/linux64/v0.30.0/geckodriver")
    
    # open the auth link in a new headless window
    fireFoxOptions = Options()
    fireFoxOptions.headless = True
    driver = webdriver.Firefox(service=s,
                               options=fireFoxOptions)
    driver.get(auth_url)
    
    # pass the provided user and pw
    driver.find_element_by_id("login-email").send_keys(user)
    driver.find_element_by_id("login-password").send_keys(pw)
    # click login
    driver.find_element_by_id("login-button").click()
    
    # wait until the user inputs creds and the url changes
    encoded_uri = quote(uri, safe="")
    WebDriverWait(driver, 120).until(EC.url_contains(encoded_uri),
                                    "Sign in timed out")
    # get the new url
    response_url = driver.current_url
    # close window
    driver.quit()
    
    # parse the token from the response url
    code = oauth.parse_response_code(response_url)
    token = oauth.get_access_token(code, as_dict=False)
    
    # return the token
    return token

def sign_in(token):
    sp = spotipy.Spotify(auth=token)
    return sp

# %% app UI auth

st.title("Spotify Playlist Preserver")

# initialize session variables
if "signed_in" not in st.session_state:
    st.session_state["signed_in"] = False
if "cached_token" not in st.session_state:
    st.session_state["cached_token"] = None
    
### troubleshooting
st.write(st.session_state)

# attempt sign in with cached token
if st.session_state["cached_token"] is not None:
    sp = sign_in(st.session_state["cached_token"])
    st.write("sign in success!")
else:
    st.write("No tokens found for this session. Please log in below.")

# display the login button
sign_in_clicked = st.button("Sign in to Spotify",
                            disabled=st.session_state["signed_in"])

# log in once the button is clicked
# save the token in this session to prevent multiple sign-ins
if sign_in_clicked and "sp" not in locals():
    
    # with st.form("login", clear_on_submit=True):
    #     input_user = st.text_input("User",
    #                                placeholder="Email associated with Spotify account")
    #     input_pw = st.text_input("Password",
    #                              placeholder="Spotify password",
    #                              type="password")
    #     submitted = st.form_submit_button("Log in")
    
    form = st.form("login")
    input_user = form.text_input("User",
                                 placeholder="Email associated with Spotify account")
    input_pw = form.text_input("Password",
                               placeholder="Spotify password",
                               type="password")
    submitted = form.form_submit_button("Log in")

    if submitted:
        try:
            token = get_token(oauth, user=input_user, pw=input_pw)
            sp = sign_in(token)
            st.session_state["cached_token"] = token
            st.write("sign in success!")
        except Exception as e:
            st.write("An error occurred during authentication!")
            st.write("The error is as follows:")
            st.write(e)
        else:
            st.session_state["signed_in"] = True
    
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
