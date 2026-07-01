import sqlite3

DB_PATH = "data/resume_screening.db"


def create_database():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS candidates (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    phone TEXT,
    skills TEXT,
    score REAL,
    similarity REAL,
    matched_skills TEXT,
    missing_skills TEXT,
    interview_questions TEXT,
    status TEXT
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
    (name,email,phone,skills,score,status)

    VALUES(?,?,?,?,?,?)
    """,
    (
        name,
        email,
        phone,
        ",".join(skills),
        score,
        "Pending"
    ))

    conn.commit()
    conn.close()

def update_status(candidate_id, status):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "UPDATE candidates SET status=? WHERE id=?",
        (status, candidate_id)
    )

    conn.commit()
    conn.close()

def get_all_candidates():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT
        id,
        name,
        email,
        phone,
        skills,
        score,
        status
    FROM candidates
    ORDER BY score DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_candidate_by_id(id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            name,
            email,
            phone,
            skills,
            score,
            status
        FROM candidates
        WHERE id=?
    """, (id,))

    row = cursor.fetchone()

    conn.close()

    return row

def clear_db():

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("DELETE FROM candidates")

    conn.commit()

    conn.close()