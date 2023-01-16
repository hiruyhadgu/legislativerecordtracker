import pandas as pd
import sqlite3

# Initialize connection.
connection = sqlite3.connect('app.db')

# query BILL DETAILS and VOTING RECORD
bill_details = pd.read_sql_query("SELECT * FROM bill_details", connection)
voting_record = pd.read_sql_query("SELECT * FROM voting_record", connection)

# assign bill_detials to a new variable for computation purposes
calc_bill_details = bill_details.copy()
calc_voting_record = voting_record.copy()

calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']] = calc_bill_details[['budget', 'affordable_housing','school_quality','accountability']].apply(pd.to_numeric).fillna(0)
calc_bill_details = calc_bill_details.astype({'budget':'int','affordable_housing':'int','school_quality':'int', 'accountability':'int'})

def issue_score(bills, votes, year_list, issue, office):
    year=year_list
    scored = ['Scored']
    bill_issue = bills.loc[(bills[issue] != 0) & (bills['year'] == year) & (bills['status'].isin(scored))]
    bill_issue = bill_issue.join(votes[office])
    # print(bill_issue)
    bill_issue = bill_issue[~bill_issue[issue].isnull()]
    #print(f"{office}, {issue}, {year}, {bill_issue}")

    if office == 'Calvin Ball (CE)':

        negative_score = (bill_issue[issue] < 0) & (bill_issue[office] =='Approve')\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'Veto'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'No Action'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] =='Opposed'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'OverRide +'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'OverRide +'))

        positive_score = (bill_issue[issue] > 0) & (bill_issue[office] =='Approve')\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'No Action'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'Veto'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] =='Opposed'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'OverRide -'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'OverRide -'))

    else:

        negative_score = (bill_issue[issue] < 0) & (bill_issue[office] =='Yes')\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'Not Present Y'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'Not Present N'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'No'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'Abstain'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'OverRide +'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'OverRide +'))        

        positive_score = (bill_issue[issue] > 0) & (bill_issue[office] =='Yes')\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'Not Present Y'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'Not Present N'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'No'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'Abstain'))\
        | ((bill_issue[issue] > 0) & (bill_issue[office] == 'OverRide -'))\
        | ((bill_issue[issue] < 0) & (bill_issue[office] == 'OverRide -'))

    # bill_issue.introduced_date = pd.to_datetime(bill_issue.introduced_date)
    # year = year_list
    # mask = (bill_issue['year'] == year)\
    #     & (bill_issue.status != 'Not Scored')\
    #     & (bill_issue.status != 'Withdrawn')\
    #     & (bill_issue.status != 'Expired')

    vote_negative_score = bill_issue.loc[negative_score]
    vote_negative_score['score'] = vote_negative_score[issue].copy()
    vote_negative_score['score'] = vote_negative_score['score'].apply(lambda x: x*-1 if x > 0 else x)
    # vote_negative_score['score'] = vote_negative_score[issue].apply(lambda x: x*-1 if x > 0 else x)
    # vote_negative_score['score'] = [vote_negative_score[issue] if x < 0 else x*-1 for x in vote_negative_score[issue]]
    #  print(vote_negative_score)
    vote_positive_score = bill_issue.loc[positive_score]
    vote_positive_score['score'] = vote_positive_score[issue].copy()
    vote_positive_score['score'] = vote_positive_score['score'].astype(int).apply(lambda x: x*-1 if x < 0 else x)
    # vote_positive_score['score'] = [vote_positive_score[issue] if x > 0 else x*-1 for x in vote_positive_score[issue]]
    # vote_positive_score['score'] = vote_positive_score[issue].apply(lambda x: x*-1 if x < 0 else x)
    score_sum = vote_negative_score['score'].sum()+vote_positive_score['score'].sum()
    
    return score_sum

def process_dataframe(tables):
    tables = tables.transpose()
    tables = tables.rename(columns={'accountability':'Accountability'\
    ,'affordable_housing':'Affordable Housing', 'budget':'Budget',\
         'school_quality':'School Quality'})
 #   tables = tables.rename(index={'ce':'Calvin Ball (CE)'\
 #   ,'d1':'Liz Walsh (D1)', 'd2':'Opel Jones (D2)',\
 #        'd3':'Christiana Mercer-Rigby (D3)', 'd4':'Deb Jung (D4)',\
  #           'd5':'David Yungmann (D5)'}) 
    return tables 


def color_negative_red(val):
    """
    Takes a scalar and returns a string with
    the css property `'color: red'` for negative
    strings, black otherwise.
    """
    color = 'red' if val < 0 else 'green'
    return 'color: %s' % color



# return  vote_negative_score, vote_positive_score, score_sum
# vote_negative_score, vote_positive_score,
# construct list for unique years
# year_introduced = bill_details['year'].unique().tolist()
# year_introduced = list(filter(None, year_introduced))
# results = issue_score(calc_bill_details, voting_record, '2019', 'affordable_housing', 'ce')

# calc_bill_budget = calc_bill_details.loc[calc_bill_details.budget != 0]
# calc_bill_budget=calc_bill_budget.join(calc_voting_record['ce'])

# ce_negative_score = (calc_bill_budget.budget < 0) & (calc_bill_budget.ce =='Approve')\
#     | ((calc_bill_budget.budget < 0) & (calc_bill_budget.ce == 'No Action'))\
#      | ((calc_bill_details.budget > 0) & (calc_voting_record.ce == 'Veto'))\
#      | ((calc_bill_details.budget > 0) & (calc_voting_record.ce == 'No Action'))\

# calc_bill_budget.introduced_date = pd.to_datetime(calc_bill_budget.introduced_date)

# mask = (calc_bill_budget['year'] == '2019') & (calc_bill_budget.status != 'Not Scored')

# negative_budget_score = calc_bill_budget.loc[mask][ce_negative_score]
# negative_budget_score['score'] = negative_budget_score['budget'].apply(lambda x: x*-1 if x > 0 else x)
# positive_bduget_score = calc_bill_budget.loc[mask][~ ce_negative_score]
# positive_bduget_score['score'] = positive_bduget_score['budget'].apply(lambda x: x*-1 if x < 0 else x)
# print(negative_budget_score)
# print(positive_bduget_score)
# score_sum = negative_budget_score['score'].sum()+positive_bduget_score['score'].sum()
# print(score_sum)
