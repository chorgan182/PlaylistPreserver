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
response = "http://localhost:8501/?code=AQAKgHMsSuWgXLjlVYNIPCnKuNK-7wtoj8XJgxYqh0KqWgbktnje28V8oU_C7EyCMvr1oEkfTaiRf0Cpq0KqKwnZxT9ETRiT26nlQD4xCrtWugqHAR0nui7lD4TqQ3PG9UZmVm8XyGAKuWgOQh0h2DSJD_3sG2Cppxt3-xRjOPshwej8mHOPx9yi6VUYmvN-N-CE9KtU2WWFvEtA-UriP1SGItdkiiPUDamlNIkbbVlbxTuwivYljCZsfD40ZJvfPlQopNzMLLxzJ33i0Jd8qPJ-8OkYPlYaGwZYg-QSXow0Z7cOMLiuYC4FMTP--O3x"
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)

