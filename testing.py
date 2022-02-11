# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:04:03 2022

@author: chorgan
"""

import streamlit as st
import datetime

st.write("Remove all songs listened to since this time")
col1, col2 = st.columns(2)

today = datetime.date.today()
one_week_ago = today - datetime.timedelta(days=7)
right_now = datetime.datetime.now().time()

since_date = col1.date_input("Date (max one week ago)",
                             value=today,
                             min_value=one_week_ago)
since_time = col2.time_input("Time",
                             value=right_now)
st.write(datetime.datetime.combine(since_date, since_time))




# %% leave for testing
response = "http://localhost:8501/?code=AQA9Z5vUqnbu1-DhsCiaJXqga4mNBUhmJqUvy3FlWBodfe71L50gUT4WV0KdHtv2NpyFEQDLNuucQZC0-J36cXEZnmy8xV7c2yKi2E-apRTMWO6ufuv4U1Fs_IKnF2_3PXIFXuB4f8rj0PzcBzsn9wIAJf_3fdsTKx1Ua_mOsTho2iFUkh91AepXyNcUwJQnaAOrqJ6b-MsC2-as7leddDTZzQtTH7UZ7uo0YEuHYGzigO_Z6dh1SEO1_ezW6bbI9vjm9MXDu3dIKNSnPk0XOvuJBZ796Elrf-wR4JaBNDbhbU_QPYFUXTPhSOSIAQyx"
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)

