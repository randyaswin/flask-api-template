import pandas as pd

def query(db_connection, *args, **kwargs):
    df = pd.read_sql_query("SELECT 1 as x, 20 as y;", db_connection)
    return df