import os
import pandas as pd
import sqlite3
from score.score import issue_score, process_dataframe, color_negative_red
from fastapi import FastAPI, Request, Form, Response
from fastapi.templating import Jinja2Templates
from fastapi.responses import RedirectResponse, JSONResponse, FileResponse
import uvicorn
import json
from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from fastapi.staticfiles import StaticFiles
from jinja2 import Environment, FileSystemLoader
from pathlib import Path
from server_thread import ServerThread

def calc_score():
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
    issues = ["accountability","affordable_housing","budget","school_quality"]
    temp = {}
    office_name = {}
    temp_score={}
    office_holder={}

    for year in year_introduced:
        for office in offices:
            for issue in issues:
                score = issue_score(calc_bill_details, calc_voting_record, year,issue, office)
                temp_score[issue]=str(score)
            office_holder[office]=temp_score
            temp_score = {}
        scores[year] =office_holder
        office_holder = {}

    return scores

all_scores = calc_score()
for year in all_scores:
    for elected in all_scores[year]:
        # print(f'{year} for {elected} {all_scores[year][elected]}')
        # for key in all_scores[year][elected]:
        vals = all_scores[year][elected]

app = FastAPI()

def get_url():
    server = ServerThread(app)
    url = f"http://{server.host}:{server.port}/"
    return url

templates = Jinja2Templates("templates")

# # val = all_scores['2019']['Calvin Ball (CE)']['accountability']

@app.get("/table_2019")
def score_2019(request:Request):
    # Initialize connection.

    return templates.TemplateResponse('table_2019.html',{'request':request,'scores':all_scores})

@app.get("/table_2020")
def score_2020(request:Request):
    # Initialize connection.

    return templates.TemplateResponse('table_2020.html',{'request':request,'scores':all_scores})

@app.get("/table_2021")
def score_2021(request:Request):
    # Initialize connection.

    return templates.TemplateResponse('table_2021.html',{'request':request,'scores':all_scores})

@app.get("/table_2022")
def score_2022(request:Request):
    # Initialize connection.

    return templates.TemplateResponse('table_2022.html',{'request':request,'scores':all_scores})


""""" this works
@app.post("/")
def score():
    # Initialize connection.
    dat = all_scores['2019']
"""