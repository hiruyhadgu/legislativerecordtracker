import os
import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
import plotly.graph_objects as go
import numpy as np
import requests
import streamlit.components.v1 as components
import glob
import importlib.machinery
import importlib.util
from pathlib import Path
from server_thread import ServerThread
import subprocess
# from fastapi import app as app

import sys
current_dir = os.path.dirname(__file__)
module_dir = os.path.join(current_dir,'..','..','fastapi')
sys.path.insert(1, "../fastapi")

# absolute_path = os.path.dirname(__file__)
# relateive_path = "/fastapi"
# print(absolute_path)
# print(relateive_path)
# full_path = os.path.join(absolute_path, relateive_path)
# print(full_path)

# print(module_dir)
# # for p in sys.path:
# #     print(p)
# def get_url():
#     server = ServerThread(app)
#     url = f"http://{server.host}:{server.port}/"
#     return url

# script_dir = Path(__file__).parent
# mymodule_path = str( script_dir.joinpath( '..', 'fastapi', 'compute') )

# # Import mymodule
# loader = importlib.machinery.SourceFileLoader( 'compute', mymodule_path )
# spec = importlib.util.spec_from_loader( 'compute', loader )
# mymodule = importlib.util.module_from_spec( spec )
# loader.exec_module( mymodule )

# # Use mymodule
# mymodule.get_url()
subprocess.run([f"{sys.executable}", f"{module_dir}/compute.py"])

st.set_page_config(page_title='Howard County Legislative Record Tracker')
st.markdown("<h1 style='text-align: center; color: #007af9;'>Howard County Executive and County Council Legislative Record</h1>", unsafe_allow_html=True)
st.write('Every month, the Howard County Council takes up several pieces of legislation.\
                This page track the votes of the council members.')

# Initialize connection.
connection = sqlite3.connect('app.db')

# query BILL DETAILS and VOTING RECORD
bill_details = pd.read_sql_query("SELECT * FROM bill_details", connection)
voting_record = pd.read_sql_query("SELECT * FROM voting_record", connection)

calc_bill_details = bill_details.copy()
calc_voting_record = voting_record.copy()
calc_voting_record = calc_voting_record.rename(columns={"ce": "Calvin Ball (CE)", "d1": "Liz Walsh (D1)",\
                                                        "d2": "Opel Jones (D2)", "d3": "Christiana Mercer-Rigby (D3)",\
                                                       "d4": "Deb Jung (D4)", "d5": "David Yungmann (D5)"})

calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']] = calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']].apply(pd.to_numeric)
calc_bill_details = calc_bill_details.fillna(0)
#calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']] = calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']].apply(pd.to_numeric)
calc_bill_details = calc_bill_details.astype({'budget':'int','affordable_housing':'int','school_quality':'int', 'accountability':'int'})

# construct list for unique years
year_introduced = bill_details['year'].unique().tolist()
year_introduced = list(filter(None, year_introduced))

offices = ["Calvin Ball (CE)", "Liz Walsh (D1)", "Opel Jones (D2)", "Christiana Mercer-Rigby (D3)", "Deb Jung (D4)", "David Yungmann (D5)"]

scores = {}
issues = ['accountability','affordable_housing','budget','school_quality']
temp = {}
office_name = {}
temp_score={}
office_holder={}



# this works
# if st.button('get'):
#     r = requests.post('http://host.docker.internal:8000')
#     st.write(r.text)


# def get_scores(year):
#     import re
#     url = f"http://host.docker.internal:8000/table_{str(year)}"
#     score =  requests.get(f"http://host.docker.internal:8000/table_{str(year)}")

#     result = st.markdown(score.text, unsafe_allow_html=True)
#     print(url)
#     return result

year_introduced = ['Pick Year to View'] + year_introduced
select_year = st.selectbox('Year:', year_introduced, 0)
# url = "http://dockhero-contoured-15174.dockhero.io:8000/"
# url = "https://leg-fastapi-procfile.herokuapp.com/"
# url = "http://localhost:8000/"
# url="http://host.docker.internal:8000/"
# url = "https://leg-fastapi-docker-image.herokuapp.com/"
port = os.environ.get('PORT')
# url = "http://host.docker.internal:8080/"

# url = get_url()
url = f"http://fastapi:{port}/"

if st.button("get_url"):
    st.write(url)

if select_year == "2019":
    score_2019 =  requests.get( url +"table_2019")
    st.markdown(score_2019.text, unsafe_allow_html=True)
    with open('static/style1.css') as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
elif select_year == "2020":
    score_2020 =  requests.get(url +"table_2020")
    st.markdown(score_2020.text, unsafe_allow_html=True)
    with open('static/style1.css') as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
elif select_year == "2021":
    score_2021 =  requests.get(url +"table_2021")
    st.markdown(score_2021.text, unsafe_allow_html=True)
    with open('static/style1.css') as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
elif select_year == "2022":
    score_2022 =  requests.get(url +"table_2022")
    st.markdown(score_2022.text, unsafe_allow_html=True)
    with open('static/style1.css') as f:
        st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

