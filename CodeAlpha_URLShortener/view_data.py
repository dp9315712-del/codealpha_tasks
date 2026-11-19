import sqlite3

conn = sqlite3.connect("database.db")

cursor = conn.cursor()

print("\nDATABASE TABLES:")

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table'"
)

print(cursor.fetchall())

print("\nSAVED URL DATA:")

cursor.execute("SELECT * FROM urls")

data = cursor.fetchall()

for row in data:
    print(row)

conn.close()
