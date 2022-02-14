# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:04:03 2022

@author: chorgan
"""

import streamlit as st
import datetime as dt

st.write("Remove all songs listened to since this time")
col1, col2 = st.columns(2)

today = dt.date.today()
one_week_ago = today - dt.timedelta(days=7)
yesterday = today - dt.timedelta(days=1)
right_now = dt.datetime.now().time()

# testing for recent func
combined = dt.datetime.combine(one_week_ago, right_now)
after = int(time.mktime(combined.timetuple())) * 1000
after = time.mktime(combined.timetuple())

since_date = col1.date_input("Date (max one week ago)",
                             value=today,
                             min_value=one_week_ago)
since_time = col2.time_input("Time",
                             value=right_now)
st.write(datetime.datetime.combine(since_date, since_time))




# %% leave for testing
response = ""
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)
