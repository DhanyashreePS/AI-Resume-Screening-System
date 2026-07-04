from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet


from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer
)
from reportlab.lib.styles import getSampleStyleSheet


def generate_pdf(
    filename,
    name,
    email,
    phone,
    skills,
    score,
    similarity_score,
    matched,
    missing,
    questions,
    recommendation,
    reason
):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    # ==========================
    # Title
    # ==========================

    content.append(
        Paragraph(
            "<b>AI Resume Screening Report</b>",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 20))

    # ==========================
    # Candidate Details
    # ==========================

    content.append(
        Paragraph(
            "<b>Candidate Details</b>",
            styles["Heading2"]
        )
    )

    content.append(Paragraph(f"<b>Name:</b> {name}", styles["Normal"]))
    content.append(Paragraph(f"<b>Email:</b> {email}", styles["Normal"]))
    content.append(Paragraph(f"<b>Phone:</b> {phone}", styles["Normal"]))

    content.append(Spacer(1, 15))

    # ==========================
    # Scores
    # ==========================

    content.append(
        Paragraph(
            "<b>Evaluation Scores</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"Match Score : <b>{score}%</b>",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"TF-IDF Similarity : <b>{similarity_score}%</b>",
            styles["Normal"]
        )
    )

    content.append(Spacer(1, 15))

    # ==========================
    # Skills
    # ==========================

    content.append(
        Paragraph(
            "<b>Detected Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in skills:
        content.append(
            Paragraph(f"• {skill}", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    # ==========================
    # Matched Skills
    # ==========================

    content.append(
        Paragraph(
            "<b>Matched Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in matched:
        content.append(
            Paragraph(f"✓ {skill}", styles["Normal"])
        )

    content.append(Spacer(1, 12))

    # ==========================
    # Missing Skills
    # ==========================

    content.append(
        Paragraph(
            "<b>Missing Skills</b>",
            styles["Heading2"]
        )
    )

    for skill in missing:
        content.append(
            Paragraph(f"✗ {skill}", styles["Normal"])
        )

    content.append(Spacer(1, 15))

    # ==========================
    # Interview Questions
    # ==========================

    content.append(
        Paragraph(
            "<b>Interview Questions</b>",
            styles["Heading2"]
        )
    )

    for skill, question_list in questions.items():

        content.append(
            Paragraph(
                f"<b>{skill}</b>",
                styles["Heading3"]
            )
        )

        for question in question_list:

            content.append(
                Paragraph(
                    f"• {question}",
                    styles["Normal"]
                )
            )

        content.append(Spacer(1, 8))
    content.append(Spacer(1, 15))

    content.append(
        Paragraph(
            "<b>Final Recommendation</b>",
            styles["Heading2"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Decision:</b> {recommendation}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"<b>Reason:</b> {reason}",
            styles["Normal"]
        )
    )

    pdf.build(content)