import sqlite3
import pandas as pd
db = sqlite3.connect('hubway.db')

def run_query(query):
    return pd.read_sql_query(query,db)

query = "select * from trips"
print(run_query(query))