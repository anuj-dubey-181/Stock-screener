import sqlite3
from sqlalchemy import text
from config import DB_PATH



def execute_query(sql, params):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(sql, params)

    rows = cursor.fetchall()

    columns = [desc[0] for desc in cursor.description]

    # Convert rows to dictionaries
    results = []

    for row in rows:
        record = dict(zip(columns, row))
        results.append(record)

    # Handle empty results
    if len(results) == 0:

        return {
            "meta": {
                "count": 0
            },
            "data": [],
            "message": "No companies satisfy the condition"
        }
    
    conn.close()

    # Success response
    return {
        "meta": {
            "count": len(results)
        },
        "data": results
        }
    


    