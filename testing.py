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

# testing for recent func
combined = datetime.datetime.combine(one_week_ago, right_now)
after = int(time.mktime(combined.timetuple())) * 1000
after = time.mktime(combined.timetuple())

since_date = col1.date_input("Date (max one week ago)",
                             value=today,
                             min_value=one_week_ago)
since_time = col2.time_input("Time",
                             value=right_now)
st.write(datetime.datetime.combine(since_date, since_time))




# %% leave for testing
response = "http://localhost:8501/?code=AQAdDdJJokjchKiPih10c8SqcTpflPxnXa-KWSnVf9D_BMA22Bzl3G_mpIb9PZoIHGZmwzpQMX6_KVGfVHN3kz5h9PyMBb_lSbOXFdGZTBX5MeXslAU8YT1_j2QC4_uneTMGxLEhP7LigbfUZeuxyXVrny_ZkUCoPowpucV933xCSJGwl_i1eac1QN0nttpKw75LnJwacqzjGhjaHin-34OZdEToFgVjDt3iDQ2azAgzJ6M8pL7TNNI50mNCWM8giGqqat_JfNyPa2Nju1v5WENO3VbjYS0bVIs3jRBVg20OZQPoM19nrTATu9DAGZv6"
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)
