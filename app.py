from flask import Flask, render_template, request
import os

from utils.resume_parser import extract_text_from_pdf
from utils.skill_extractor import extract_skills
from utils.candidate_extractor import (
    extract_name,
    extract_email,
    extract_phone
)
from utils.job_matcher import calculate_match
from utils.interview_generator import generate_questions

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


if __name__ == "__main__":
    app.run(debug=True)