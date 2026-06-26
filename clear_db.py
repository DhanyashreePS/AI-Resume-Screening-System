import sqlite3

DB_PATH = "resume_screening.db"   # Use your actual database filename

conn = sqlite3.connect(DB_PATH)

cursor = conn.cursor()

cursor.execute("DELETE FROM candidates")

conn.commit()

conn.close()

print("Database cleared successfully.")