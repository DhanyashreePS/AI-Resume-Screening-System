import sqlite3

conn = sqlite3.connect("data/resume_screening.db")

cursor = conn.cursor()

cursor.execute("""
ALTER TABLE candidates
ADD COLUMN status TEXT DEFAULT 'Pending'
""")

conn.commit()
conn.close()

print("Status column added")