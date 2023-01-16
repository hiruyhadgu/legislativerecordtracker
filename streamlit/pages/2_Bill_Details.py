import os
import datetime as dt
import pandas as pd
import streamlit as st
import plotly.express as px
import sqlite3
import math
from IPython.display import display, HTML
import streamlit.components.v1 as components

st.set_page_config(page_title='Howard County Legislative Record Tracker')
st.markdown("<h1 style='text-align: center; color: #007af9;'>Howard County Executive and County Council Legislative Record</h1>", unsafe_allow_html=True)
st.write('Every month, the Howard County Council takes up several pieces of legislation.\
                This page tracks the votes of the council members.')

def make_clickable(link):
    # target _blank to open new window
    # extract clickable text to display for your link
    # text = link
    return f'<a href="{link}">{link}</a>'

# Initialize connection.
connection = sqlite3.connect('app.db')

# query BILL DETAILS and VOTING RECORD
bill_details = pd.read_sql_query("SELECT * FROM bill_details", connection)
voting_record = pd.read_sql_query("SELECT * FROM voting_record", connection)

calc_bill_details = bill_details.copy()
calc_voting_record = voting_record.copy()

calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']] = calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']].apply(pd.to_numeric).fillna(0)
calc_bill_details = calc_bill_details.astype({'budget':'int','affordable_housing':'int','school_quality':'int', 'accountability':'int'})

# construct list for unique years
year_introduced = bill_details['year'].unique().tolist()
year_introduced = list(filter(None, year_introduced))

bill_details.columns = ['Item No', 'Bill No', 'Status', 'Description', 'Comments', 'Budget', 'Affordable Housing', 'School Quality', 'Accountability', 'Introduced Date', 'Council Action', 'CE Action', 'Link to Bill Text', 'Year']
bill_details.set_index('Item No', inplace=True)
bill_details['Year'] = bill_details['Year'].astype('string')
bill_details['Introduced Date']=pd.to_datetime(bill_details['Introduced Date']).dt.date

voting_record.columns = ['Item No', 'Bill No', 'Calvin Ball', 'Liz Walsh', 'Opel Jones', 'Christiana Mercer-Rigby', 'Deb Jung', 'David Yungmann', 'Introduced Date', 'Year']
voting_record.set_index('Item No', inplace=True)
voting_record['Introduced Date']=pd.to_datetime(bill_details['Introduced Date']).dt.date

status_list = ['Scored', 'Not Scored']

col_bill_details, col_vote_record = st.columns(2)

with col_bill_details:
   bill_details_checked = st.checkbox('Review Bill Details')
with col_vote_record:
    vote_record_checked = st.checkbox('View Voting Record')

if bill_details_checked:
    col1, col2 = st.columns(2)
    with col1:
        select_year = st.selectbox('Year:', 
        year_introduced)
    with col2:
        mask= bill_details['Year'] == select_year
        bill_id =  bill_details['Bill No'][mask].unique().tolist()
        bill_selection = st.selectbox('Bill Number:',
                                        bill_id)
    if bill_selection:
        bill_to_display = bill_details.loc[bill_details['Bill No']==bill_selection]
        bill_to_display = bill_to_display.reset_index()
        bill_to_display= bill_to_display.drop(['Item No'], axis = 1)
        bill_to_display = bill_to_display.transpose()
        bill_to_display.columns = ['Info']
        scored = (bill_to_display.loc['Status'].astype('string') == 'Scored')
        bill_to_display=bill_to_display.iloc[:-1,:]
        bill_to_display.loc['Link to Bill Text'] = bill_to_display.loc['Link to Bill Text'].apply(make_clickable)
        bill_to_display_html = bill_to_display.to_html(escape=False)
        st.write(bill_to_display_html, unsafe_allow_html=True)
    

        with open('static/style.css') as f:
            st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)
       
    st.markdown('---')

    if vote_record_checked:
        
        if bill_to_display.iloc[1,:].squeeze()in status_list:

                st.markdown(f"<h1 style = 'text-align: center; color: black; font-family: sans-serif'> Voting Record for {bill_selection} </h1>", unsafe_allow_html=True)

                vote_to_display = voting_record.loc[voting_record['Bill No']==bill_selection]
                vote_to_display = vote_to_display.reset_index()
                vote_to_display = vote_to_display.drop(['Item No'], axis=1)
                vote_to_display = vote_to_display.transpose()
                vote_to_display.columns = ['Vote']
                vote_to_display = vote_to_display.iloc[1:-1,:]
                vote_to_display_html = vote_to_display.iloc[1:-1,:]
                st.table(vote_to_display)
                with open('static/style.css') as f:
                    st.markdown(f"<style>{f.read()}</style>",unsafe_allow_html=True)

        else:
            st.write(f"No voting record, yet. Bill status is: {bill_to_display.iloc[1,:].squeeze()}")

