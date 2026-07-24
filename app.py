from flask import Flask, render_template, request
from flask import Response
import os
import csv
import json
from utils.database import save_job
from utils.database import get_all_jobs
from flask import session,jsonify
from flask import send_file
from utils.database import get_candidate_email
from utils.pdf_generator import generate_pdf
from flask_mail import Mail, Message
from flask import redirect
from utils.tfidf_matcher import calculate_similarity
from utils.database import clear_db, update_status
from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.database import delete_job
from utils.database import get_recent_jobs
from utils.database import get_job_skills
from utils.database import update_job
from utils.candidate_extractor import (
    extract_name,
    extract_email,
    extract_phone
)
from utils.database import get_job_description
from utils.database import get_job_by_id
from utils.database import get_candidates_by_job
from utils.job_matcher import calculate_match
from utils.interview_generator import generate_questions
from utils.database import save_candidate
from utils.database import (
    get_all_candidates,
    get_candidate_by_id
)
from utils.database import get_user_by_email
from werkzeug.security import generate_password_hash, check_password_hash
from utils.database import create_user
from utils.database import email_exists
from utils.database import get_candidate_count
app = Flask(__name__)

app.secret_key = "resume_screening_secret"
global latest_report
latest_report = {}

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_TLS"] = True
app.config["MAIL_USERNAME"] = "your_email@gmail.com"
app.config["MAIL_PASSWORD"] = "your_app_password"

mail = Mail(app)

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

def send_shortlist_email(email):

    msg = Message(
        "Application Status Update",
        sender=app.config["MAIL_USERNAME"],
        recipients=[email]
    )

    msg.body = """Congratulations!

You have been shortlisted for the next round.

Regards,
HR Team
"""

    try:
        mail.send(msg)
        print("Email sent successfully.")

    except Exception as e:
        print("Email could not be sent:", e)
        
@app.route("/home")
def home():

    if not session.get("logged_in"):
        return redirect("/login")

    jobs = get_all_jobs()

    rows = get_all_candidates()

    print(rows)

    for row in rows:
        print(row)
        print(len(row))

    jobs_posted = len(jobs)

    resumes_screened = len(rows)

    shortlisted = sum(
    1 for row in rows
    if row[11] == "Shortlisted"
    )

    pending = sum(
        1 for row in rows
        if row[11] == "Pending"
    )

    rejected = sum(
        1 for row in rows
        if row[11] == "Rejected"
    )
    recent_jobs = get_recent_jobs()
    jobs = get_all_jobs()
    rows = get_all_candidates()

    print("Jobs:", jobs)
    print("Candidates:", rows)

    jobs_posted = len(jobs)
    resumes_screened = len(rows)
    print("Jobs Posted:", jobs_posted)
    print("Resumes Screened:", resumes_screened)
    print("Rows:", rows)
    hr_name = session.get("hr_name")
    company = session.get("company_name")


    return render_template(
        "home.html",
        jobs_posted=jobs_posted,
        resumes_screened=resumes_screened,
        shortlisted=shortlisted,        
        recent_jobs=recent_jobs,
        hr_name=hr_name,
        company=company

    )
    return redirect("/home")

@app.route("/analyze", methods=["POST"])
def analyze():
    if not session.get("logged_in"):
        return redirect("/login")

    if "resume" not in request.files:
        return "No file uploaded"

    file = request.files["resume"]

    if file.filename == "":
        return "No file selected"

    file_path = os.path.join(
        app.config["UPLOAD_FOLDER"],
        file.filename
    )

    file.save(file_path)

    text = extract_text_from_pdf(file_path)
    job_id = session.get("job_id")   
    job_description = get_job_description(job_id) 
    similarity_score = calculate_similarity(text,job_description)

    print("TF-IDF Similarity:", similarity_score)

    skills = extract_skills(text)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    required_skills = get_job_skills(job_id)
    match_result = calculate_match(
        skills,
        required_skills
    )

    questions = generate_questions(skills)
    print("Saving candidate:", name)
    job_id = session.get("job_id")
    save_candidate(
    job_id,    
    name,
    email,
    phone,
    skills,
    match_result["score"],
    similarity_score,
    match_result["matched_skills"],
    match_result["missing_skills"],
    questions
)
    
    global latest_report

    latest_report = {
    "name": name,
    "email": email,
    "phone": phone,
    "skills": skills,
    "score": match_result["score"],
    "similarity_score": similarity_score,
    "matched": match_result["matched_skills"],
    "missing": match_result["missing_skills"],
    "questions": questions
}
    return redirect("/dashboard")
    #return render_template("results.html", name=name,email=email,phone=phone,skills=skills,score=match_result["score"],matched=match_result["matched_skills"],missing=match_result["missing_skills"], questions=questions,similarity_score=similarity_score)

    print("Similarity:", similarity_score)
    print("Matched:", match_result["matched_skills"])
    print("Missing:", match_result["missing_skills"])
    print("Questions:", questions)


@app.route("/jobs")
def jobs():

    if not session.get("logged_in"):
        return redirect("/login")

    rows = get_all_jobs()

    jobs = []

    for row in rows:

        jobs.append({

    "id": row[0],
    "title": row[1],
    "company": row[2],
    "location": row[3],
    "experience": row[4],
    "education": row[5],
    "required_skills": row[6],
    "job_description": row[7],
    "created_date": row[8],
    "candidate_count": get_candidate_count(row[0])

})

    return render_template(
        "jobs.html",
        jobs=jobs
    )
    
print(get_recent_jobs())
@app.route("/create_job", methods=["POST"])


@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        company = request.form["company_name"]
        hr = request.form["hr_name"]
        email = request.form["email"]
        phone = request.form["phone"]

        password = generate_password_hash(
            request.form["password"]
        )

        if email_exists(email):

            return "Email already registered."

        create_user(
            company,
            hr,
            email,
            phone,
            password
        )

        return redirect("/login")

    return render_template("register.html")

def create_job():

    save_job(

        request.form["title"],
        request.form["company"],
        request.form["location"],
        request.form["experience"],
        request.form["education"],
        request.form["required_skills"],
        request.form["job_description"]

    )

    return redirect("/jobs")
 
@app.route("/delete_job/<int:id>")
def delete_job_route(id):

    delete_job(id)

    return redirect("/jobs")


@app.route("/job/<int:id>")
def open_job(id):

    session["job_id"] = id

    return redirect("/dashboard")

@app.route("/get_job/<int:id>")
def get_job_json(id):

    job = get_job_by_id(id)

    return jsonify(job)

@app.route("/candidate/<int:id>")
def candidate_profile(id):

    if not session.get("logged_in"):
        return redirect("/login")

    row = get_candidate_by_id(id)

    if row is None:
        return "Candidate not found"

    print("Database Row:")
    print(row)
    print("Length:", len(row))

    candidate = {
    "id": row[0],
    "name": row[1],
    "email": row[2],
    "phone": row[3],
    "skills": row[4].split(",") if row[4] else [],
    "score": row[5],
    "job_id": row[6],
    "similarity_score": row[7],
    "matched": row[8].split(",") if row[8] else [],
    "missing": row[9].split(",") if row[9] else [],
    "questions": json.loads(row[10]) if row[10] else {},
    "status": row[11]
}
    return render_template(
        "candidate_profile.html",
        candidate=candidate
    )


@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")
    search = request.args.get("search", "").lower()
    status = request.args.get("status", "")

    job_id = session.get("job_id")

    if job_id:
        rows = get_candidates_by_job(job_id)
    else:
        rows = get_all_candidates()

    candidates = []

    for row in rows:
        print("Row:", row)
        candidates.append({
    "id": row[0],
    "name": row[1],
    "email": row[2],
    "phone": row[3],
    "skills": row[4].split(",") if row[4] else [],
    "score": row[5],
    "similarity_score": row[7],   # <-- IMPORTANT
    "status": row[11]
})
    if search:
        candidates = [
            c for c in candidates
            if search in c["name"].lower()
        ]

    # Filter by status
    if status:
        candidates = [
            c for c in candidates
            if c["status"] == status
        ]

    labels = [c["name"] for c in candidates]
    scores = [c["score"] for c in candidates]
    print(candidates)
    
    total_candidates = len(candidates)

    shortlisted = sum(
        1 for c in candidates
        if c["status"] == "Shortlisted"
    )

    pending = sum(
        1 for c in candidates
        if c["status"] == "Pending"
    )

    rejected = sum(
        1 for c in candidates
        if c["status"] == "Rejected"
    )
    
    job = get_job_by_id(job_id) if job_id else None
    
    has_candidates = len(candidates) > 0

    return render_template(
    "dashboard.html",
    candidates=candidates,
    labels=labels,
    scores=scores,
    total_candidates=total_candidates,
    shortlisted=shortlisted,
    pending=pending,
    rejected=rejected,
    latest_report=latest_report,
    job=job,
    has_candidates=has_candidates
) 


@app.route("/update_job/<int:id>", methods=["POST"])
def update_job_route(id):

    update_job(
        id,
        request.form["title"],
        request.form["company"],
        request.form["location"],
        request.form["experience"],
        request.form["education"],
        request.form["required_skills"],
        request.form["job_description"]
    )

    return redirect("/jobs")
   
@app.route("/export")
def export_csv():
    if not session.get("logged_in"):
        return redirect("/login")

    rows = get_all_candidates()
    print("Rows:", rows)

    def generate():
        data = [[
    "Name",
    "Email",
    "Phone",
    "Skills",
    "Score",
    "Status"
]]
        for row in rows:
            data.append([
        row[1],   # Name
        row[2],   # Email
        row[3],   # Phone
        row[4].replace(",", " | "),   # Skills
        row[5],   # Score
        row[6]    # Status
    ])

        for row in data:
            yield ",".join(map(str, row)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={
            "Content-Disposition":
            "attachment; filename=candidates.csv"
        }
    )

@app.route("/shortlist/<int:id>")
def shortlist(id):

    if not session.get("logged_in"):
        return redirect("/login")

    update_status(id, "Shortlisted")

    email = get_candidate_email(id)

    if email:
        send_shortlist_email(email)

    return redirect("/dashboard")

@app.route("/reject/<int:id>")
def reject(id):

    if not session.get("logged_in"):
        return redirect("/login")

    update_status(id, "Rejected")

    return redirect("/dashboard")

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


@app.route("/download_pdf/<int:id>")
def download_pdf(id):

    row = get_candidate_by_id(id)
    print("Database Row:")
    print(row)
    print("Length:", len(row))

    if row is None:
        return "Candidate not found"
    print("===== DOWNLOAD PDF DEBUG =====")
    print("Executing file:", __file__)
    print("Matched line should use row[8]")
    candidate = {
    "id": row[0],
    "name": row[1],
    "email": row[2],
    "phone": row[3],
    "skills": row[4].split(",") if row[4] else [],
    "score": row[5],
    "job_id": row[6],
    "similarity_score": row[7],
    "matched": row[8].split(",") if row[8] else [],
    "missing": row[9].split(",") if row[9] else [],
    "questions": json.loads(row[10]) if row[10] else {},
    "status": row[11]
}
    # Recommendation Logic

    if candidate["score"] >= 80:
        recommendation = "Shortlist Candidate"
        reason = "Excellent skill match with the job requirements."

    elif candidate["score"] >= 60:
        recommendation = "Consider for Interview"
        reason = "Good match but a few important skills are missing."

    else:
        recommendation = "Not Recommended"
        reason = "Candidate does not meet the minimum required skills."

    filename = f"{candidate['name']}_Report.pdf"

    generate_pdf(
    filename,
    candidate["name"],
    candidate["email"],
    candidate["phone"],
    candidate["skills"],
    candidate["score"],
    candidate["similarity_score"],
    candidate["matched"],
    candidate["missing"],
    candidate["questions"],
    recommendation,
    reason
)

    return send_file(
        filename,
        as_attachment=True
    )
@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        email = request.form["email"]
        password = request.form["password"]

        user = get_user_by_email(email)

        if user and check_password_hash(user["password"], password):

            session["logged_in"] = True

            session["user_id"] = user["id"]

            session["company_name"] = user["company_name"]

            session["hr_name"] = user["hr_name"]

            return redirect("/home")

        else:

            return "Invalid Email or Password"

    return render_template("login.html")
@app.route("/clear_db")
def clear_database_route():

    global latest_report

    clear_db()

    latest_report = {}

    return redirect("/dashboard")

@app.route("/")
def index():
    return redirect("/home")

import sqlite3

conn = sqlite3.connect("data/resume_screening.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(candidates)")

for col in cursor.fetchall():
    print(col)

conn.close()

if __name__ == "__main__":
    app.run(debug=True)