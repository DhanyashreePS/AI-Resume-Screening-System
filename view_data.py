import sqlite3

conn = sqlite3.connect("data/resume_screening.db")

cursor = conn.cursor()

cursor.execute("SELECT * FROM candidates")

rows = cursor.fetchall()

print("Number of records:", len(rows))

for row in rows:
    print(row)

conn.close()