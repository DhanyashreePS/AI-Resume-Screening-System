import sqlite3
import json
from datetime import datetime

DB_PATH = "data/resume_screening.db"


def save_job(
    title,
    company,
    location,
    experience,
    education,
    required_skills,
    job_description
):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO jobs
    (
        title,
        company,
        location,
        experience,
        education,
        required_skills,
        job_description,
        created_date
    )

    VALUES(?,?,?,?,?,?,?,?)
    """,
    (
        title,
        company,
        location,
        experience,
        education,
        required_skills,
        job_description,
        datetime.now().strftime("%d %b %Y")
    ))

    conn.commit()
    conn.close()


def get_all_jobs():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM jobs
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows


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

    score REAL,
    job_id INTEGER,

    similarity_score REAL,

    matched_skills TEXT,

    missing_skills TEXT,

    interview_questions TEXT,

    status TEXT

)
""")

    conn.commit()
    conn.close()



def create_jobs_table():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS jobs(

        id INTEGER PRIMARY KEY AUTOINCREMENT,

        title TEXT,
        company TEXT,
        location TEXT,
        experience INTEGER,
        education TEXT,
        required_skills TEXT,
        job_description TEXT,
        created_date TEXT
    )
    """)

    conn.commit()
    conn.close()
create_database()
create_jobs_table()   

def save_candidate(
        job_id,
        name,
        email,
        phone,
        skills,
        score,
        similarity_score,
        matched_skills,
        missing_skills,
        interview_questions):
    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO candidates
(
    job_id,
    name,
    email,
    phone,
    skills,
    score,
    similarity_score,
    matched_skills,
    missing_skills,
    interview_questions,
    status
)

    VALUES (?,?,?,?,?,?,?,?,?,?,?)
    """,
    (
    job_id,
    name,
    email,
    phone,
    ",".join(skills),
    score,
    similarity_score,
    ",".join(matched_skills),
    ",".join(missing_skills),
    json.dumps(interview_questions),
    "Pending"
))

    conn.commit()
    conn.close()

def get_candidate_count(job_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM candidates
        WHERE job_id=?
    """, (job_id,))

    count = cursor.fetchone()[0]

    conn.close()

    return count

def delete_job(job_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute(
        "DELETE FROM jobs WHERE id=?",
        (job_id,)
    )

    conn.commit()
    conn.close()
    
def get_candidates_by_job(job_id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM candidates
    WHERE job_id = ?
    ORDER BY score DESC
    """, (job_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows

def get_candidate_email(id):

    conn = sqlite3.connect(DB_PATH)

    cursor = conn.cursor()

    cursor.execute(
        "SELECT email FROM candidates WHERE id=?",
        (id,)
    )

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return None

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
    SELECT *
    FROM candidates
    WHERE id = ?
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

def get_job_by_id(job_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    row = cursor.fetchone()

    conn.close()

    return row
def get_candidates_by_job(job_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM candidates
        WHERE job_id = ?
        ORDER BY score DESC
    """, (job_id,))

    rows = cursor.fetchall()

    conn.close()

    return rows
def get_job_description(job_id):

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT job_description
        FROM jobs
        WHERE id = ?
    """, (job_id,))

    row = cursor.fetchone()

    conn.close()

    if row:
        return row[0]

    return ""

def get_recent_jobs():

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            id,
            title,
            company,
            location,
            created_date
        FROM jobs
        ORDER BY id DESC
    """)

    jobs = cursor.fetchall()

    conn.close()

    return jobs