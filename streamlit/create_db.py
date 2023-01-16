import sqlite3

connection = sqlite3.connect('app.db')

cursor = connection.cursor()

cursor.execute("""
    CREATE TABLE IF NOT EXISTS elected_officials (
        district_id TEXT NOT NULL UNIQUE PRIMARY KEY,
        name TEXT NOT NULL UNIQUE,
        role TEXT NOT NULL,
        party_id TEXT NOT NULL,
        council_district TEXT NOT NULL
    )

""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS bill_details (
        item_no INTEGER PRIMARY KEY,
        bill_no TEXT UNIQUE,
        status TEXT,
        description TEXT,
        comments TEXT,
        budget REAL,
        affordable_housing REAL,
        school_quality REAL,
        accountability REAL,
        introduced_date TIMESTAMP,
        council_action TIMESTAMP,
        ce_action TIMESTAMP,
        link_to_bill_text TEXT
    )

""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS voting_record(
        item_no INTEGER PRIMARY KEY,
        bill_no TEXT NOT NULL UNIQUE,
        ce TEXT,
        d1 TEXT,
        d2 TEXT,
        d3 TEXT,
        d4 TEXT,
        d5 TEXT,
        introduced_date TEXT,
        FOREIGN KEY (item_no) REFERENCES bill_details(item_no),
        FOREIGN KEY (bill_no) REFERENCES bill_details(bill_no),
        FOREIGN KEY (introduced_date) REFERENCES bill_details(introduced_date)

    )

""")

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS issues_scores (
#         id INTEGER PRIMARY KEY,
#         issues_scores INTEGER NOT NULL UNIQUE
#     )

# """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS issues (
#         id INTEGER PRIMARY KEY,
#         issues TEXT NOT NULL UNIQUE
#     )

# """)

# cursor.execute("""
#     CREATE TABLE IF NOT EXISTS elected_action (
#         id INTEGER PRIMARY KEY,
#         ce_action TEXT UNIQUE,
#         cc_action TEXT UNIQUE
#     )

# """)

