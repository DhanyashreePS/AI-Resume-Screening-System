import fitz  # PyMuPDF
from docx import Document


def extract_text_from_pdf(pdf_path):
    text = ""

    pdf_document = fitz.open(pdf_path)

    for page in pdf_document:
        text += page.get_text()

    pdf_document.close()

    return text


def extract_text_from_docx(docx_path):
    doc = Document(docx_path)

    text = ""

    for para in doc.paragraphs:
        text += para.text + "\n"

    return text