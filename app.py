from flask import Flask, render_template, request
from flask import Response
import os
import csv
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

UPLOAD_FOLDER = "resumes"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

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

    return render_template(
        "results.html",
        name=name,
        email=email,
        phone=phone,
        skills=skills,
        score=match_result["score"],
        matched=match_result["matched_skills"],
        missing=match_result["missing_skills"],
        questions=questions
    )
@app.route("/dashboard")
def dashboard():

    rows = get_all_candidates()

    candidates = []

    for row in rows:
        candidates.append({
            "name": row[0],
            "score": row[1]
        })

    labels = [c["name"] for c in candidates]
    scores = [c["score"] for c in candidates]

    return render_template(
        "dashboard.html",
        candidates=candidates,
        labels=labels,
        scores=scores
    )
    
@app.route("/export")
def export_csv():

    rows = get_all_candidates()

    def generate():
        data = [["Candidate Name", "Score"]]

        for row in rows:
            data.append([row[0], row[1]])

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
    
if __name__ == "__main__":
    app.run(debug=True)