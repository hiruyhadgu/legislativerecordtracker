import sqlite3
import pandas as pd

def change_to_datetime(val):
    converted= pd.to_datetime(val)
    converted = converted.dt.date
    return converted

bill_details_connection = sqlite3.connect('app.db')

cursor = bill_details_connection.cursor()
bill_details = pd.read_excel('Bill_Details.xlsx')
bill_details['bill_no']=bill_details['bill_no'].str.replace(' ','')
bill_details['year']= bill_details['introduced_date'].dt.strftime('%Y')
bill_details ['bill_no']=bill_details['bill_no'].map(str)+'-'+bill_details['year'].map(str)
bill_details.fillna('', inplace=True)
bill_details.drop(columns=['year'])
bill_details = bill_details.astype({'budget':'int'},errors='raise')
# bill_details['budget'] = pd.to_numeric(bill_details['budget'])
# bill_details.fillna('', inplace=True)
# bill_details['budget'] = bill_details['budget'].astype(int, errors='ignore')
# print(bill_details['budget'])
# 
print(bill_details.dtypes)
bill_details['introduced_date'] = change_to_datetime(bill_details['introduced_date'])
bill_details['council_action'] = change_to_datetime(bill_details['council_action'])
bill_details['ce_action'] = change_to_datetime(bill_details['ce_action'])
bill_details.to_sql(name="bill_details", con=bill_details_connection, if_exists="replace", index=False)
bill_details_connection.commit()


voting_record_connection = sqlite3.connect('app.db')

cursor = voting_record_connection.cursor()
voting_record = pd.read_excel('Voting_Records.xlsx')
voting_record['bill_no']=voting_record['bill_no'].str.replace(' ','')
voting_record['year']= voting_record['introduced_date'].dt.strftime('%Y')
voting_record ['bill_no']=voting_record['bill_no'].map(str)+'-'+voting_record['year'].map(str)
voting_record.fillna('', inplace=True)
voting_record['introduced_date'] = change_to_datetime(voting_record['introduced_date'])
voting_record.to_sql(name="voting_record", con=voting_record_connection, if_exists="replace", index=False)
voting_record_connection.commit()
















# for row in bill_details.itertuples():
#     insert_sql = f"INSERT INTO bill_details (item_no, bill_no, status, description, comments, budget, affordable_housing, school_quality, accountability, introduced_date, council_action, ce_action, link_to_bill_text) VALUES ({row[1]},'{row[2]}','{row[3]}','{row[4]}','{row[5]}',{row[6]},{row[7]},{row[8]},{row[9]},'{row[10]}','{row[11]}','{row[12]}','{row[13]}')"
#     print(insert_sql)
#     # insert_sql = f"INSERT INTO bill_details(item_no, bill_no, status, description, \
#     #     comments, budget, affordable_housing, school_quality, accountability, \
#     #         introduced_date, council_action, ce_action, link_to_bill_text) \
#     #     VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)"
#     # sql_value =  (bill_details.Item_Number, bill_details.Bill_Number, bill_details.Status,bill_details.Description, 
#     #         bill_details.Comments,bill_details.Budget, bill_details.Affordable_Housing, 
#     #         bill_details.School_Quality, bill_details.Accountability,bill_details.Introduced_Date, 
#     #         bill_details.Council_Action, bill_details.CE_Action, bill_details.Link_to_Bill_Text,)
#     # print(values)
#     cursor.execute(insert_sql)
# 