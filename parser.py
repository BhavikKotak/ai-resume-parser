import pdfplumber
import docx
import os


def extract_text_from_pdf(file_path):
    text = ""

    try:
        with pdfplumber.open(file_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:
        print("PDF Parsing Error:", e)

    return text


def extract_text_from_docx(file_path):
    text = ""

    try:
        document = docx.Document(file_path)

        for para in document.paragraphs:
            text += para.text + "\n"

    except Exception as e:
        print("DOCX Parsing Error:", e)

    return text


def extract_resume_text(file_path):
    extension = os.path.splitext(file_path)[1].lower()

    if extension == ".pdf":
        return extract_text_from_pdf(file_path)

    elif extension == ".docx":
        return extract_text_from_docx(file_path)

    else:
        return ""