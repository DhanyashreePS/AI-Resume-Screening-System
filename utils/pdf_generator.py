from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
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
    questions
):

    pdf = SimpleDocTemplate(filename)

    styles = getSampleStyleSheet()

    content = []

    content.append(
        Paragraph(
            "Candidate Analysis Report",
            styles["Title"]
        )
    )

    content.append(Spacer(1, 12))

    content.append(
        Paragraph(f"Name: {name}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Email: {email}", styles["Normal"])
    )

    content.append(
        Paragraph(f"Phone: {phone}", styles["Normal"])
    )

    content.append(
        Paragraph(
            f"Skills: {', '.join(skills)}",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"Match Score: {score}%",
            styles["Normal"]
        )
    )

    content.append(
        Paragraph(
            f"TF-IDF Similarity: {similarity_score}%",
            styles["Normal"]
        )
    )
    
    content.append(
        Paragraph(
        f"Matched Skills: {', '.join(matched)}",
        styles["Normal"]
        )
    )

    content.append(
        Paragraph(
        f"Missing Skills: {', '.join(missing)}",
        styles["Normal"]
        )
    )

    pdf.build(content)