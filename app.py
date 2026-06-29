from flask import Flask, render_template, request
from flask import Response
import os
import csv
from flask import session
from flask import send_file
from utils.pdf_generator import generate_pdf
from flask_mail import Mail, Message
from flask import redirect
from utils.tfidf_matcher import calculate_similarity
from utils.database import clear_db, update_status
from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.candidate_extractor import (
    extract_name,
    extract_email,
    extract_phone
)
from utils.job_matcher import calculate_match
from utils.interview_generator import generate_questions
from utils.database import save_candidate
from utils.database import get_all_candidates

app = Flask(__name__)

app.secret_key = "resume_screening_secret"
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

    mail.send(msg)
    
@app.route("/")
def home():

    if not session.get("logged_in"):
        return redirect("/login")

    return render_template("index.html")


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
    job_description = request.form["job_description"]    
    similarity_score = calculate_similarity(text,job_description)

    print("TF-IDF Similarity:", similarity_score)

    skills = extract_skills(text)

    name = extract_name(text)
    email = extract_email(text)
    phone = extract_phone(text)

    required_skills = [
        "python",
        "sql",
        "django",
        "git",
        "html",
        "css",
        "machine learning"
    ]

    match_result = calculate_match(
        skills,
        required_skills
    )

    questions = generate_questions(skills)
    print("Saving candidate:", name)
    save_candidate(
    name,
    email,
    phone,
    skills,
    match_result["score"]
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
    "missing": match_result["missing_skills"]
}
    return redirect("/dashboard")
    #return render_template("results.html", name=name,email=email,phone=phone,skills=skills,score=match_result["score"],matched=match_result["matched_skills"],missing=match_result["missing_skills"], questions=questions,similarity_score=similarity_score)
@app.route("/dashboard")
def dashboard():
    if not session.get("logged_in"):
        return redirect("/login")
    search = request.args.get("search", "").lower()
    status = request.args.get("status", "")

    rows = get_all_candidates()
    

    candidates = []

    for row in rows:
        candidates.append({
        "id": row[0],
        "name": row[1],
        "score": row[2],
        "status": row[3]
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

    return render_template(
    "dashboard.html",
    candidates=candidates,
    labels=labels,
    scores=scores,
    total_candidates=total_candidates,
    shortlisted=shortlisted,
    pending=pending,
    rejected=rejected,
    latest_report=latest_report

)
    
@app.route("/export")
def export_csv():
    if not session.get("logged_in"):
        return redirect("/login")

    rows = get_all_candidates()
    print("Rows:", rows)

    def generate():
        data = [["Candidate Name", "Score"]]

        for row in rows:
            data.append([row[1], row[2]])

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

@app.route("/download_pdf")
def download_pdf():

    filename = "candidate_report.pdf"

    generate_pdf(
        filename,
        latest_report["name"],
        latest_report["email"],
        latest_report["phone"],
        latest_report["skills"],
        latest_report["score"],
        latest_report["similarity_score"],
        latest_report["matched"],
        latest_report["missing"]
    )

    return send_file(
        filename,
        as_attachment=True
    )

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]
        password = request.form["password"]

        if username == "Dhanya" and password == "2006":

            session["logged_in"] = True

            return redirect("/")

        else:

            return "Invalid Username or Password"

    return render_template("login.html")

@app.route("/clear_db")
def clear_database_route():

    clear_db()

    return redirect("/dashboard")

if __name__ == "__main__":
    app.run(debug=True)