import sqlite3

conn = sqlite3.connect(r"C:\Users\DELL\Stock-screener-2\backend\stock_screener.db")

cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

tables = cursor.fetchall()

print("Tables:")
for table in tables:
    print(table)

conn.close()
