import sqlite3

conn = sqlite3.connect("data/resume_screening.db")

cursor = conn.cursor()

cursor.execute("PRAGMA table_info(candidates)")

for row in cursor.fetchall():
    print(row)

conn.close()