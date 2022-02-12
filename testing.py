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
response = "http://localhost:8501/?code=AQBlt_aKJCXDJFQ42pr7JAFXGWb4MfXSUlmeEwcpBAbyEWKmtH86Z5WCHuSnMJdBa5uJ7jSbeMcaGComm7-LjgPRAsjlqFXyoDpKMo0rHU0QzRHPnfs864GiJmaf2qUhRrxIi2ZCHA-36-_nqqqkMgzrXxbZ3pNeEDiPX7r96BgogntGFfEnMI1UO2wiFsP6HIoHZMs7LUAIU3lt4IHThXSYab-j4NOSj-YpXiIBBTgMRn4NqRf_ZRJBDvanLM0KOVh9nIUTVHli2UxqNBE_yAH1ukTkmY-I4Ec86g4jEd43b1OYFXeouIIwT3_sDZ4V"
code = oauth.parse_response_code(response)
token = oauth.get_access_token(code, as_dict=False)
sp = spotipy.Spotify(auth=token)

