# -*- coding: utf-8 -*-
"""
Created on Mon Feb  7 14:04:03 2022

@author: chorgan
"""

import streamlit as st

the_url = "https://www.google.com/"


html = """ <a target=\"_self\" href=\"{}\" >Google</a> """.format(the_url)

st.markdown(html, unsafe_allow_html=True)