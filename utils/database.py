import sqlite3

DB_PATH = "data/resume_screening.db"


def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        email TEXT,
        phone TEXT,
        skills TEXT,
        score INTEGER
    )
    """)

    conn.commit()
    conn.close()
    
def save_candidate(
        name,
        email,
        phone,
        skills,
        score):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates
    (name,email,phone,skills,score)

    VALUES(?,?,?,?,?)
    """,
    (
        name,
        email,
        phone,
        ",".join(skills),
        score
    ))

    conn.commit()
    conn.close()

def get_all_candidates():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT name, score
    FROM candidates
    ORDER BY score DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows